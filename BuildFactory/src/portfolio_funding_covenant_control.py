"""Human-approved portfolio funding decisions with covenant monitoring and early warning."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='7.4.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}
DEFAULT_COVENANTS={'max_monthly_cost_per_apartment':75.0,'max_loan_share':0.80,'max_interest_rate':0.06,'min_reserve_share':0.05,'warning_margin':0.10}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(name:str,scenario:str)->str:
    return 'FUND-'+sha256(f'{name}|{scenario}'.encode()).hexdigest()[:10].upper()

def build_funding_decision_and_covenants(strategy:dict[str,Any], existing:dict[str,Any]|None=None, covenants:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}; rules={**DEFAULT_COVENANTS,**(covenants or {})}; now=datetime.now(timezone.utc).isoformat(); old={x.get('decision_id'):x for x in existing.get('decisions',[]) or []}; decisions=[]
    for item in strategy.get('strategies',[]) or []:
        name=str(item.get('name','')); preferred=str(item.get('preferred_scenario','')); scenarios=item.get('scenarios',[]) or []
        selected=preferred; probe_id=_id(name,selected); prev=old.get(probe_id,{})
        if prev.get('selected_scenario'): selected=str(prev['selected_scenario'])
        row=next((x for x in scenarios if str(x.get('scenario',''))==selected),scenarios[0] if scenarios else {})
        did=_id(name,selected); prev=old.get(did,prev); decision=str(prev.get('decision','NOG TE BESLUITEN')).upper(); approved=decision in APPROVED
        gap=max(0,_n(item.get('funding_gap'))); loan=_n(row.get('loan_amount')); reserve=_n(row.get('reserve_use')); monthly=_n(row.get('monthly_cost_per_apartment')); rate=_n((strategy.get('assumptions',{}) or {}).get('loan_rate'))
        loan_share=loan/gap if gap>0 else 0; reserve_share=reserve/gap if gap>0 else 0
        checks=[
          {'covenant':'MAANDLAST','actual':monthly,'limit':_n(rules['max_monthly_cost_per_apartment']),'compliant':monthly<=_n(rules['max_monthly_cost_per_apartment'])},
          {'covenant':'LENINGAANDEEL','actual':round(loan_share,4),'limit':_n(rules['max_loan_share']),'compliant':loan_share<=_n(rules['max_loan_share'])},
          {'covenant':'RENTE','actual':rate,'limit':_n(rules['max_interest_rate']),'compliant':rate<=_n(rules['max_interest_rate'])},
          {'covenant':'RESERVE-INZET','actual':round(reserve_share,4),'minimum':_n(rules['min_reserve_share']),'compliant':reserve_share>=_n(rules['min_reserve_share'])},
        ]
        breaches=sum(not c['compliant'] for c in checks); warning=False; margin=max(0,_n(rules['warning_margin']))
        for c in checks:
            if c['covenant']=='RESERVE-INZET': warning=warning or (c['actual']<_n(c.get('minimum'))*(1+margin) and c['compliant'])
            else: warning=warning or (c['actual']>_n(c.get('limit'))*(1-margin) and c['compliant'])
        covenant_status='BREACH' if breaches else ('WAARSCHUWING' if warning else 'BINNEN CONVENANT')
        decisions.append({'decision_id':did,'vve':name,'selected_scenario':selected,'decision':decision,'approved_by':prev.get('approved_by',''),'approved_at':prev.get('approved_at',''),'rationale':prev.get('rationale',''),'decision_authority':prev.get('decision_authority','Bestuur/ALV'),'approved':approved,'funding_gap':round(gap,2),'funding_mix':row,'covenants':checks,'covenant_status':covenant_status,'breach_count':breaches,'updated_at':now})
    approved_count=sum(d['approved'] for d in decisions); breaches=sum(d['breach_count'] for d in decisions); warnings=sum(d['covenant_status']=='WAARSCHUWING' for d in decisions); pending=sum(not d['approved'] for d in decisions)
    status='COVENANT BREACH' if breaches else ('BESLUIT VEREIST' if pending else ('COVENANT WAARSCHUWING' if warnings else 'FINANCIERING GEBORGD'))
    return {'portfolio_funding_covenant_version':ENGINE_VERSION,'generated_at':now,'status':status,'decision_count':len(decisions),'approved_count':approved_count,'pending_count':pending,'breach_count':breaches,'warning_count':warnings,'covenant_policy':rules,'decisions':decisions,'human_decision_required':bool(decisions),'automatic_financing_commitment':False,'next_action':'Herstructureer financieringsmix of convenanten en leg opnieuw ter besluitvorming voor.' if breaches else ('Laat Bestuur/ALV de gekozen financieringsmix(en) formeel goedkeuren.' if pending else ('Beoordeel convenantwaarschuwingen voordat grenzen worden overschreden.' if warnings else 'Financieringsbesluiten zijn goedgekeurd en binnen convenanten; monitor periodiek.'))}
