"""Enterprise 16.5 Post-Promotion Stability & Model Drift Watchdog."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.5.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVDRF-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def monitor_post_promotion_stability(promotion:dict[str,Any], live_periods:list[dict[str,Any]], baseline_metrics:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; min_periods=max(1,int(_n(rules.get('minimum_monitoring_periods',3)) or 3)); warn_rel=_n(rules.get('warning_reliability_drop_points',3)); critical_rel=_n(rules.get('critical_reliability_drop_points',5)); warn_mape=_n(rules.get('warning_mape_deterioration_pct_points',5)); critical_mape=_n(rules.get('critical_live_mape_pct',25)); min_cal=_n(rules.get('minimum_confidence_calibration_pct',85)); max_risk_drift=_n(rules.get('maximum_combined_shortfall_drift_pct_points',3))
 n=len(live_periods); avg=lambda k: round(sum(_n(x.get(k)) for x in live_periods)/n,2) if n else 0.0
 live_mape=avg('mape_pct'); live_bias=avg('bias_pct'); live_rel=avg('reliability_score'); live_cal=avg('confidence_calibration_pct'); live_short=avg('combined_shortfall_pct')
 base_mape=_n(baseline_metrics.get('mape_pct')); base_rel=_n(baseline_metrics.get('reliability_score')); base_cal=_n(baseline_metrics.get('confidence_calibration_pct')); base_short=_n(baseline_metrics.get('combined_shortfall_pct'))
 rel_drop=round(base_rel-live_rel,2); mape_drift=round(live_mape-base_mape,2); cal_drift=round(live_cal-base_cal,2); risk_drift=round(live_short-base_short,2)
 warnings=[]; critical=[]
 if n<min_periods:warnings.append('Onvoldoende post-promotion perioden voor stabiele driftbeoordeling.')
 if rel_drop>=critical_rel:critical.append('Reliability drop bereikt kritieke rollback-zone.')
 elif rel_drop>=warn_rel:warnings.append('Reliability vertoont materiële verslechtering.')
 if live_mape>=critical_mape:critical.append('Live MAPE bereikt kritieke rollback-zone.')
 elif mape_drift>=warn_mape:warnings.append('MAPE verslechtert materieel ten opzichte van promotiebaseline.')
 if live_cal<min_cal:warnings.append('Confidence calibration ligt onder de minimale grens.')
 if risk_drift>max_risk_drift:warnings.append('Monte Carlo combined-shortfall risico drift materieel omhoog.')
 if abs(live_bias)>abs(_n(rules.get('maximum_absolute_bias_pct',10))):warnings.append('Absolute live bias ligt boven de toegestane grens.')
 status='KRITIEKE MODELDRIFT - ROLLBACK REVIEW VEREIST' if critical else ('MODELDRIFT WAARSCHUWING - MODEL REVIEW VEREIST' if warnings else 'NIEUWE CHAMPION STABIEL')
 return {'post_promotion_stability_model_drift_watchdog_version':ENGINE_VERSION,'watchdog_id':_id((promotion.get('new_champion') or {}).get('model_id',''),n,live_rel,live_mape),'status':status,'monitoring_periods':n,'minimum_monitoring_periods':min_periods,'baseline_metrics':{'mape_pct':base_mape,'reliability_score':base_rel,'confidence_calibration_pct':base_cal,'combined_shortfall_pct':base_short},'live_metrics':{'average_mape_pct':live_mape,'average_bias_pct':live_bias,'average_reliability_score':live_rel,'average_confidence_calibration_pct':live_cal,'average_combined_shortfall_pct':live_short},'drift':{'reliability_drop_points':rel_drop,'mape_deterioration_pct_points':mape_drift,'confidence_calibration_drift_points':cal_drift,'combined_shortfall_drift_pct_points':risk_drift},'warnings':warnings,'critical_signals':critical,'early_warning':bool(warnings),'rollback_review_required':bool(critical),'requires_model_owner_review':bool(warnings or critical),'requires_board_review':bool(critical),'requires_monte_carlo_recheck':bool(warnings or critical),'automatic_rollback':False,'automatic_model_change':False,'automatic_baseline_change':False,'next_action':'Start rollback review volgens 16.4 en bevestig handmatig of terugval naar de vorige Champion nodig is.' if critical else ('Voer model-owner review en Monte Carlo-hercheck uit voordat drift verder oploopt.' if warnings else 'Blijf de nieuwe Champion monitoren tegen de promotiebaseline.')}
