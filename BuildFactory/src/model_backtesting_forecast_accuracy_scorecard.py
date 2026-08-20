"""Enterprise 16.1 Model Backtesting & Forecast Accuracy Scorecard."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.1.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVBTS-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def build_backtest_scorecard(records:list[dict[str,Any]], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; min_obs=max(1,int(rules.get('minimum_observations',3))); good_mape=_n(rules.get('good_mape_pct',10)); warn_mape=_n(rules.get('warning_mape_pct',20)); rows=[]
 for r in records:
  actual=_n(r.get('actual_eur')); forecast=_n(r.get('forecast_eur')); err=actual-forecast; ape=abs(err)/abs(actual)*100 if actual else (0 if forecast==0 else 100); bias=err/abs(actual)*100 if actual else 0
  low=r.get('p05_eur'); high=r.get('p95_eur'); covered=True if low is None or high is None else _n(low)<=actual<=_n(high)
  rows.append({'year':r.get('year'),'component':r.get('component','TOTAL'),'forecast_eur':round(forecast,2),'actual_eur':round(actual,2),'error_eur':round(err,2),'absolute_percentage_error_pct':round(ape,2),'bias_pct':round(bias,2),'confidence_interval_covered':covered})
 n=len(rows); mape=round(sum(x['absolute_percentage_error_pct'] for x in rows)/n,2) if n else 0; bias=round(sum(x['bias_pct'] for x in rows)/n,2) if n else 0; coverage=round(sum(1 for x in rows if x['confidence_interval_covered'])/n*100,2) if n else 0
 confidence_target=_n(rules.get('confidence_coverage_target_pct',90)); coverage_gap=abs(confidence_target-coverage); reliability=max(0,min(100,100-mape*2-abs(bias)-coverage_gap*0.5)); reliability=round(reliability,1)
 status='BETROUWBAAR MODEL' if n>=min_obs and mape<=good_mape and reliability>=80 else ('MODEL AANDACHT' if n>=min_obs and mape<=warn_mape and reliability>=60 else ('ONVOLDOENDE BACKTESTDATA' if n<min_obs else 'MODEL HERKALIBRATIE VEREIST'))
 by_component={}
 for x in rows:
  by_component.setdefault(x['component'],[]).append(x)
 component_scores=[]
 for comp,vals in by_component.items():
  cmape=round(sum(v['absolute_percentage_error_pct'] for v in vals)/len(vals),2); cbias=round(sum(v['bias_pct'] for v in vals)/len(vals),2); ccoverage=round(sum(1 for v in vals if v['confidence_interval_covered'])/len(vals)*100,2)
  component_scores.append({'component':comp,'observations':len(vals),'mape_pct':cmape,'bias_pct':cbias,'confidence_coverage_pct':ccoverage})
 component_scores.sort(key=lambda x:x['mape_pct'],reverse=True)
 return {'model_backtesting_forecast_accuracy_scorecard_version':ENGINE_VERSION,'backtest_id':_id(n,mape,bias,coverage),'status':status,'observations':n,'mape_pct':mape,'bias_pct':bias,'confidence_coverage_pct':coverage,'confidence_coverage_target_pct':confidence_target,'model_reliability_score':reliability,'rows':rows,'component_scorecard':component_scores,'requires_recalibration':status=='MODEL HERKALIBRATIE VEREIST','requires_learning_loop_review':bool(n>=min_obs and (mape>good_mape or abs(bias)>good_mape or coverage_gap>10)),'human_model_owner_review_required':True,'automatic_model_update':False,'automatic_baseline_change':False,'automatic_risk_appetite_change':False,'next_action':'Gebruik MAPE, bias en confidence calibration als input voor 16.0 learning proposals; herkalibreer en backtest opnieuw vóór modelwijziging.'}
