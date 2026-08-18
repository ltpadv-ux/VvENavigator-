"""Stress 36-month treasury forecasts and rank human-governed liquidity interventions."""
from __future__ import annotations
from copy import deepcopy
from typing import Any

ENGINE_VERSION='7.7.0'
DEFAULT_STRESSES={
    'RENTE +2%':{'interest_rate_add':0.02},
    'RENTE +4%':{'interest_rate_add':0.04},
    'KOSTENINFLATIE +10%':{'operating_factor':1.10},
    'SUBSIDIE 12M VERTRAAGD':{'subsidy_delay_months':12},
    'BIJDRAGE-Achterstand 8%':{'contribution_factor':0.92},
    'MJOP 6M VERVROEGD':{'mjop_shift_months':-6},
}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _shift_key(key:str, months:int)->str:
    y,m=(int(x) for x in key.split('-')); n=y*12+(m-1)+months; return f'{n//12:04d}-{n%12+1:02d}'

def _stress_vve(vve:dict[str,Any], spec:dict[str,Any])->dict[str,Any]:
    timeline=deepcopy(vve.get('timeline',[]) or []); cash=_n(vve.get('opening_cash')); min_cash=None; breach=[]
    subsidy_map={r['month']:_n(r.get('subsidy')) for r in timeline}; mjop_map={r['month']:_n(r.get('mjop_outflow')) for r in timeline}
    if spec.get('subsidy_delay_months'):
        subsidy_map={_shift_key(k,int(spec['subsidy_delay_months'])):v for k,v in subsidy_map.items() if v}
    if spec.get('mjop_shift_months'):
        mjop_map={_shift_key(k,int(spec['mjop_shift_months'])):v for k,v in mjop_map.items() if v}
    stressed=[]
    for r in timeline:
        month=r['month']; contrib=_n(r.get('contributions'))*_n(spec.get('contribution_factor',1)); other_income=_n(r.get('other_income')); operating=_n(r.get('operating_outflow'))*_n(spec.get('operating_factor',1)); debt=_n(r.get('debt_service')); mjop=_n(mjop_map.get(month)); subsidy=_n(subsidy_map.get(month)); base_interest=_n(r.get('interest_income')); opening=max(0,cash); extra_interest=opening*_n(spec.get('interest_rate_add'))/12; interest=max(0,base_interest-extra_interest); outflow=operating+debt+mjop+_n(r.get('other_outflow')); inflow=contrib+other_income+subsidy+interest; closing=cash+inflow-outflow; floor=_n(r.get('minimum_buffer')); below=closing<floor; negative=closing<0
        if below:breach.append(month)
        stressed.append({'month':month,'closing_cash':round(closing,2),'minimum_buffer':round(floor,2),'below_buffer':below,'negative_cash':negative,'stress_delta':round(closing-_n(r.get('closing_cash')),2)})
        cash=closing; min_cash=closing if min_cash is None else min(min_cash,closing)
    status='NEGATIEVE KAS' if any(x['negative_cash'] for x in stressed) else ('BUFFER BREACH' if breach else 'VOLDOENDE LIQUIDITEIT')
    return {'vve':vve.get('vve',''),'status':status,'minimum_cash':round(min_cash or 0,2),'ending_cash':round(cash,2),'breach_months':breach,'timeline':stressed}

def _interventions(stress_rows:list[dict[str,Any]])->list[dict[str,Any]]:
    severe=sum(r['status']=='NEGATIEVE KAS' for r in stress_rows); warning=sum(r['status']=='BUFFER BREACH' for r in stress_rows)
    options=[
      {'action':'MJOP FASEREN','effect':'Verschuif niet-kritieke MJOP-uitgaven naar latere maanden.','score':90 if severe or warning else 40,'decision_authority':'Bestuur/ALV'},
      {'action':'TIJDELIJKE EXTRA BIJDRAGE','effect':'Verhoog maandelijkse instroom tijdelijk totdat minimumkasbuffer is hersteld.','score':85 if severe else 65,'decision_authority':'ALV'},
      {'action':'WERKKAPITAALLIJN / HERFINANCIERING','effect':'Creëer tijdelijke liquiditeitsruimte met expliciete covenantcontrole.','score':80 if severe else 50,'decision_authority':'Bestuur/ALV'},
      {'action':'SUBSIDIE- EN INCASSOVERSNELLING','effect':'Versnel subsidieclaims en achterstallige bijdragen.','score':75 if warning or severe else 45,'decision_authority':'Bestuur'},
      {'action':'UITGAVENSTOP NIET-KRITIEK','effect':'Bevries niet-kritieke uitgaven tot kasbuffer is hersteld.','score':88 if severe else 55,'decision_authority':'Bestuur'},
    ]
    return sorted(options,key=lambda x:(-x['score'],x['action']))

def build_treasury_stress_interventions(treasury:dict[str,Any], stresses:dict[str,dict[str,Any]]|None=None)->dict[str,Any]:
    stresses=stresses or DEFAULT_STRESSES; scenarios=[]
    for name,spec in stresses.items():
        rows=[_stress_vve(v,spec) for v in treasury.get('vves',[]) or []]; neg=sum(r['status']=='NEGATIEVE KAS' for r in rows); buf=sum(r['status']=='BUFFER BREACH' for r in rows); worst=min((_n(r['minimum_cash']) for r in rows),default=0.0); status='CRITIEK' if neg else ('AANDACHT' if buf else 'ROBUUST'); scenarios.append({'scenario':name,'status':status,'negative_cash_count':neg,'buffer_breach_count':buf,'worst_minimum_cash':round(worst,2),'vves':rows})
    critical=sum(s['status']=='CRITIEK' for s in scenarios); attention=sum(s['status']=='AANDACHT' for s in scenarios); combined=[r for s in scenarios for r in s['vves']]; interventions=_interventions(combined)
    overall='CRITIEK' if critical else ('AANDACHT' if attention else 'ROBUUST')
    return {'treasury_stress_intervention_version':ENGINE_VERSION,'status':overall,'scenario_count':len(scenarios),'critical_scenario_count':critical,'attention_scenario_count':attention,'scenarios':scenarios,'interventions':interventions,'preferred_intervention':interventions[0] if interventions else {},'human_decision_required':overall!='ROBUUST','automatic_execution':False,'next_action':'Leg de voorkeursinterventie en alternatieven ter besluitvorming voor aan Bestuur/ALV.' if overall!='ROBUUST' else 'Treasury blijft robuust onder de geteste schokken; blijf actualiseren.'}
