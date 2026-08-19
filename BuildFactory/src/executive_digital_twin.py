"""Enterprise 9.1 Executive Digital Twin & Predictive Governance.

Projects the integrated VvE Health & Governance Score across 12/24/36 months
under configurable operating scenarios. The twin is advisory only: it does not
change approved strategy, budgets, contributions or mandates automatically.
"""
from __future__ import annotations
from copy import deepcopy
from typing import Any

ENGINE_VERSION='9.1.0'
HORIZONS=(12,24,36)
SCENARIOS={
 'BASIS':{'inflation_delta':0.00,'interest_delta':0.00,'contribution_delta':0.00,'mjop_acceleration':0.00,'sustainability_investment':0.00},
 'DRUK':{'inflation_delta':0.03,'interest_delta':0.02,'contribution_delta':0.00,'mjop_acceleration':0.10,'sustainability_investment':0.00},
 'BALANS':{'inflation_delta':0.01,'interest_delta':0.01,'contribution_delta':0.05,'mjop_acceleration':0.05,'sustainability_investment':0.10},
 'VERSNELD DUURZAAM':{'inflation_delta':0.01,'interest_delta':0.01,'contribution_delta':0.08,'mjop_acceleration':0.15,'sustainability_investment':0.25},
}
WEIGHTS={'financial_health':15,'mjop_health':15,'risk_control':10,'treasury_health':15,'governance_maturity':20,'audit_assurance':10,'decision_execution':10,'improvement_progress':5}

def _clamp(v:Any)->float:
 try:return max(0.0,min(100.0,float(v or 0)))
 except (TypeError,ValueError):return 0.0

def _overall(domains:dict[str,float])->float:
 return round(sum(_clamp(domains.get(k))*w/100 for k,w in WEIGHTS.items()),1)

def _status(score:float,domains:dict[str,float])->str:
 critical=any(domains.get(k,100)<50 for k in ('treasury_health','audit_assurance','risk_control','financial_health'))
 if score>=85 and not critical:return 'GROEN'
 if score>=65 and sum(domains.get(k,100)<50 for k in ('treasury_health','audit_assurance','risk_control','financial_health'))<=1:return 'ORANJE'
 return 'ROOD'

def _project_domains(base:dict[str,float], assumptions:dict[str,float], months:int)->dict[str,float]:
    years=months/12
    d=deepcopy(base)
    inflation=assumptions.get('inflation_delta',0); interest=assumptions.get('interest_delta',0); contribution=assumptions.get('contribution_delta',0); accel=assumptions.get('mjop_acceleration',0); sustain=assumptions.get('sustainability_investment',0)
    d['financial_health']=_clamp(d.get('financial_health',0) + years*(contribution*45 - inflation*35 - interest*20))
    d['mjop_health']=_clamp(d.get('mjop_health',0) + years*(accel*35 + sustain*20 - inflation*12))
    d['risk_control']=_clamp(d.get('risk_control',0) + years*(accel*25 + sustain*15 - inflation*10))
    d['treasury_health']=_clamp(d.get('treasury_health',0) + years*(contribution*30 - interest*35 - accel*12 - sustain*8))
    d['governance_maturity']=_clamp(d.get('governance_maturity',0) + years*(2.5 + accel*5))
    d['audit_assurance']=_clamp(d.get('audit_assurance',0) + years*2)
    d['decision_execution']=_clamp(d.get('decision_execution',0) + years*2)
    d['improvement_progress']=_clamp(d.get('improvement_progress',0) + years*(8 + sustain*8))
    return {k:round(v,1) for k,v in d.items()}

def build_executive_digital_twin(governance_os:dict[str,Any], custom_scenarios:dict[str,dict[str,float]]|None=None)->dict[str,Any]:
    base={k:_clamp(v) for k,v in (governance_os.get('domain_scores',{}) or {}).items()}
    for k in WEIGHTS: base.setdefault(k,0.0)
    scenarios=deepcopy(SCENARIOS)
    scenarios.update(custom_scenarios or {})
    projections=[]
    for name,assumptions in scenarios.items():
        horizon_rows=[]
        for months in HORIZONS:
            domains=_project_domains(base,assumptions,months); score=_overall(domains)
            horizon_rows.append({'months':months,'score':score,'status':_status(score,domains),'domain_scores':domains})
        projections.append({'scenario':name,'assumptions':assumptions,'horizons':horizon_rows,'score_36m':horizon_rows[-1]['score'],'status_36m':horizon_rows[-1]['status']})
    projections.sort(key=lambda x:x['score_36m'],reverse=True)
    best=projections[0] if projections else {}
    downside=min(projections,key=lambda x:x['score_36m']) if projections else {}
    return {'executive_digital_twin_version':ENGINE_VERSION,'baseline_score':governance_os.get('overall_vve_health_governance_score',_overall(base)),'baseline_status':governance_os.get('status',_status(_overall(base),base)),'horizons_months':list(HORIZONS),'scenario_count':len(projections),'projections':projections,'best_36m_scenario':best.get('scenario',''),'best_36m_score':best.get('score_36m',0),'downside_36m_scenario':downside.get('scenario',''),'downside_36m_score':downside.get('score_36m',0),'predictive_governance':True,'human_decision_required':True,'automatic_strategy_change':False,'next_action':'Gebruik de scenariovergelijking als bestuurlijke input; laat Bestuur/ALV expliciet besluiten over wijzigingen in bijdrage, MJOP-tempo of verduurzaming.'}
