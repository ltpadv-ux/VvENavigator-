"""Enterprise 16.6 Model Drift Root Cause & Recalibration Recommendation Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.6.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVDRC-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def diagnose_model_drift(watchdog:dict[str,Any], evidence:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; causes=[]; recs=[]
 def add(code,label,score,why,action):
  causes.append({'code':code,'cause':label,'score':round(score,1),'evidence':why}); recs.append({'cause_code':code,'recommendation':action,'human_approval_required':True})
 market=abs(_n(evidence.get('market_price_index_change_pct'))); maint=abs(_n(evidence.get('maintenance_pattern_change_pct'))); risk=abs(_n(evidence.get('risk_distribution_shift_pct'))); missing=_n(evidence.get('data_missing_pct')); season=abs(_n(evidence.get('seasonality_residual_pct'))); age=_n(evidence.get('parameter_age_months'))
 if market>=_n(rules.get('market_trigger_pct',5)): add('MARKET_PRICE','Marktprijsregime gewijzigd',min(100,market*8),market,'Herkalibreer prijsindex en kostenelasticiteit; backtest op recente marktperioden.')
 if maint>=_n(rules.get('maintenance_trigger_pct',5)): add('MAINTENANCE_PATTERN','Onderhoudspatroon gewijzigd',min(100,maint*8),maint,'Herijk faalkansen, cycli en bouwdeel-specifieke MJOP-aannames.')
 if risk>=_n(rules.get('risk_shift_trigger_pct',5)): add('RISK_DISTRIBUTION','Risicoverdeling verschoven',min(100,risk*8),risk,'Herkalibreer Monte Carlo-verdelingen, correlaties en contingency.')
 if missing>=_n(rules.get('data_quality_trigger_pct',3)): add('DATA_QUALITY','Datakwaliteit onvoldoende',min(100,missing*10),missing,'Herstel ontbrekende/onjuiste data vóór modelherkalibratie en voer data-quality gate uit.')
 if season>=_n(rules.get('seasonality_trigger_pct',5)): add('SEASONALITY','Seizoenseffect onvoldoende gemodelleerd',min(100,season*8),season,'Voeg seizoen-/periodecorrectie toe en valideer out-of-sample.')
 if age>=_n(rules.get('parameter_age_trigger_months',12)): add('PARAMETER_AGE','Modelparameters verouderd',min(100,age*3),age,'Herijk parameters met recente actuals en vergelijk via Champion/Challenger.')
 causes.sort(key=lambda x:x['score'],reverse=True); primary=causes[0]['code'] if causes else None; drift=bool(watchdog.get('drift_detected',False) or watchdog.get('rollback_review_required',False) or causes); critical=bool(watchdog.get('rollback_review_required',False))
 status='KRITIEKE DRIFT - RECALIBRATIE EN ROLLBACK REVIEW' if critical else ('DRIFT OORZAAK GEVONDEN - RECALIBRATIEVOORSTEL' if drift and causes else ('DRIFT REVIEW - OORZAAK NOG ONVOLDOENDE BEWEZEN' if drift else 'GEEN MODELDRIFT DIAGNOSE NODIG'))
 return {'model_drift_root_cause_recalibration_version':ENGINE_VERSION,'diagnosis_id':_id(watchdog.get('watchdog_id',''),primary,len(causes)),'status':status,'primary_cause':primary,'ranked_root_causes':causes,'recalibration_recommendations':recs,'requires_data_quality_gate':any(c['code']=='DATA_QUALITY' for c in causes),'requires_backtest':bool(causes),'requires_champion_challenger_validation':bool(causes),'requires_monte_carlo_recalibration':any(c['code']=='RISK_DISTRIBUTION' for c in causes),'requires_board_review':critical,'automatic_recalibration':False,'automatic_model_update':False,'automatic_rollback':False,'automatic_baseline_change':False,'next_action':'Voer de gerangschikte recalibratievoorstellen uit als Challenger, backtest en valideer vóór menselijke modelgoedkeuring.' if causes else 'Verzamel aanvullende drift-evidence en behoud de huidige Champion.'}
