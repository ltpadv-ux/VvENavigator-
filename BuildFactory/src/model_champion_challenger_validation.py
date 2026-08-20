"""Enterprise 16.2 Model Champion/Challenger Validation Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.2.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVMCC-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def compare_models(champion:dict[str,Any], challenger:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; min_gain=_n(rules.get('minimum_reliability_gain_points',3)); max_mape=_n(rules.get('maximum_challenger_mape_pct',20)); max_bias=_n(rules.get('maximum_absolute_bias_pct',10)); min_calibration=_n(rules.get('minimum_confidence_calibration_pct',85)); min_stress=_n(rules.get('minimum_stress_resilience_score',70))
 def metrics(x:dict[str,Any])->dict[str,float]:
  return {'mape_pct':_n(x.get('mape_pct')),'bias_pct':_n(x.get('bias_pct')),'confidence_calibration_pct':_n(x.get('confidence_calibration_pct',x.get('coverage_pct'))),'reliability_score':_n(x.get('model_reliability_score',x.get('reliability_score'))),'stress_resilience_score':_n(x.get('stress_resilience_score',100))}
 c=metrics(champion); q=metrics(challenger); blockers=[]; wins=[]
 if q['mape_pct']<c['mape_pct']:wins.append('MAPE')
 if abs(q['bias_pct'])<abs(c['bias_pct']):wins.append('BIAS')
 if q['confidence_calibration_pct']>c['confidence_calibration_pct']:wins.append('CALIBRATION')
 if q['stress_resilience_score']>c['stress_resilience_score']:wins.append('STRESS')
 if q['reliability_score']-c['reliability_score']<min_gain:blockers.append('Reliability gain is kleiner dan de minimale promotiedrempel.')
 if q['mape_pct']>max_mape:blockers.append('Challenger MAPE ligt boven de toegestane grens.')
 if abs(q['bias_pct'])>max_bias:blockers.append('Challenger absolute bias ligt boven de toegestane grens.')
 if q['confidence_calibration_pct']<min_calibration:blockers.append('Confidence calibration van de challenger is onvoldoende.')
 if q['stress_resilience_score']<min_stress:blockers.append('Stressrobustheid van de challenger is onvoldoende.')
 if len(wins)<3:blockers.append('Challenger wint op minder dan drie validatiedimensies.')
 promotable=not blockers
 return {'model_champion_challenger_validation_version':ENGINE_VERSION,'validation_id':_id(champion.get('model_id','CHAMPION'),challenger.get('model_id','CHALLENGER'),q['reliability_score']),'status':'CHALLENGER PROMOTIE GEREED VOOR HUMAN APPROVAL' if promotable else 'CHALLENGER NIET PROMOTIEGEREED','champion_model_id':champion.get('model_id','CHAMPION'),'challenger_model_id':challenger.get('model_id','CHALLENGER'),'champion_metrics':c,'challenger_metrics':q,'reliability_gain_points':round(q['reliability_score']-c['reliability_score'],2),'challenger_wins':wins,'blockers':blockers,'promotion_recommended':promotable,'requires_shadow_run':True,'requires_backtest':True,'requires_monte_carlo_recalibration':True,'requires_model_owner_approval':True,'requires_board_review':True,'automatic_model_promotion':False,'automatic_champion_replacement':False,'automatic_baseline_change':False,'automatic_risk_appetite_change':False,'next_action':'Laat challenger minimaal één volledige shadow-run doorlopen en keur promotie pas goed na model-owner en bestuursreview.' if promotable else 'Verbeter of herkalibreer de challenger en voer de champion/challenger-validatie opnieuw uit.'}
