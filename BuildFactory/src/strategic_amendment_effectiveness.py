"""Enterprise 9.8 Strategic Amendment Effectiveness & Re-baselining."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='9.8.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(*parts:Any)->str:
    return 'PSRB-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def evaluate_amendment_effectiveness(amendment_result:dict[str,Any], variance_control:dict[str,Any], actuals:dict[str,Any], existing:dict[str,Any]|None=None, stable_periods_required:int=2)->dict[str,Any]:
    existing=existing or {}; amended=amendment_result.get('amended_mandate',{}) or {}; amendment=amendment_result.get('amendment',{}) or {}
    if amendment_result.get('status')!='MANDAATWIJZIGING GOEDGEKEURD' or not amended:
        return {'strategic_amendment_effectiveness_version':ENGINE_VERSION,'status':'GEEN ACTIEVE WIJZIGING','rebaseline':{},'automatic_rebaseline':False}
    status=str(variance_control.get('status','')).upper(); variances=variance_control.get('variances',{}) or {}
    score_ok=_num(variances.get('governance_score_variance'))>=-2
    contribution_ok=_num(variances.get('contribution_delta_variance'))>=-0.01
    mjop_ok=_num(variances.get('mjop_acceleration_variance'))>=-0.02
    budget_ok=_num(variances.get('budget_variance'))<=0
    treasury_ok=str(actuals.get('treasury_status','GROEN')).upper() not in {'ROOD','CRITIEK'}
    audit_ok=_num(actuals.get('audit_assurance_score',100))>=85
    period_ok=status=='GROEN' and all([score_ok,contribution_ok,mjop_ok,budget_ok,treasury_ok,audit_ok])
    prior=int(existing.get('stable_periods',0) or 0); stable=prior+1 if period_ok else 0
    effective=stable>=max(1,stable_periods_required)
    checks={'governance_score':score_ok,'contribution_path':contribution_ok,'mjop_path':mjop_ok,'budget':budget_ok,'treasury':treasury_ok,'audit_assurance':audit_ok}
    if not effective:
        return {'strategic_amendment_effectiveness_version':ENGINE_VERSION,'status':'EFFECTMETING ACTIEF' if period_ok else 'NADER HERSTEL NODIG','stable_periods':stable,'stable_periods_required':stable_periods_required,'checks':checks,'rebaseline':{},'human_rebaseline_required':True,'automatic_rebaseline':False,'next_action':'Bouw stabiele groene meetperioden op.' if period_ok else 'Herstel de resterende afwijkingen voordat een nieuwe baseline wordt vastgesteld.'}
    baseline_id=(existing.get('rebaseline',{}) or {}).get('baseline_id') or _id(amendment.get('amendment_id',''),amended.get('mandate_id',''))
    baseline={'baseline_id':baseline_id,'amendment_id':amendment.get('amendment_id',''),'mandate_id':amended.get('mandate_id',''),'finance':actuals.get('finance',{}),'mjop':actuals.get('mjop',{}),'treasury':actuals.get('treasury',{}),'governance':actuals.get('governance',{}),'governance_score':_num(actuals.get('governance_score')),'audit_assurance_score':_num(actuals.get('audit_assurance_score')),'kpi_targets':amended.get('kpi_targets',[]),'status':'CONCEPT RE-BASELINE','evidence':actuals.get('evidence',[])}
    return {'strategic_amendment_effectiveness_version':ENGINE_VERSION,'status':'WIJZIGING EFFECTIEF - RE-BASELINE GEREED','stable_periods':stable,'stable_periods_required':stable_periods_required,'checks':checks,'rebaseline':baseline,'human_rebaseline_required':True,'automatic_rebaseline':False,'automatic_strategy_change':False,'next_action':'Laat Bestuur/ALV de nieuwe Finance/MJOP/Treasury/Governance-baseline formeel vaststellen.'}
