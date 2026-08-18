"""Explain off-track strategy KPIs and prepare human-governed intervention proposals."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='6.5.0'

def _proposal(kpi:dict[str,Any])->dict[str,Any]:
    domain=kpi.get('domain','ONBEKEND'); name=kpi.get('kpi',''); actual=kpi.get('actual',0); target=kpi.get('target',0)
    catalog={
      'FINANCIEEL':('Reservedruk boven strategische bandbreedte',['Faseer niet-kritieke uitgaven','Herijk bijdrage/reserve-opbouw','Onderzoek alternatieve financiering'],'Bestuur/ALV'),
      'RISICO':('12-maands risicodruk boven strategische baseline',['Versnel kritieke MJOP-maatregelen','Mitigeer hoogste risico eerst','Herbereken scenario na interventie'],'Bestuur'),
      'COMPLIANCE':('Een of meer mandaten zijn rood',['Blokkeer niet-conforme uitvoering','Herstel budget/termijn/voorwaarden','Leg noodzakelijke mandaatwijziging ter goedkeuring voor'],'Bestuur/ALV'),
      'UITVOERING':('Mandaten hebben hoog uitvoeringsrisico',['Versnel besluitvorming','Herplan deadline of capaciteit','Activeer correctief actieplan'],'Bestuur'),
      'GOVERNANCE':('Effect van wijziging is nog niet aantoonbaar gesloten',['Verzamel effectbewijs','Verleng gecontroleerde observatie','Escaleren bij uitblijvend effect'],'Bestuur'),
      'STRATEGIE':('Werkelijkheid wijkt materieel af van vergrendelde strategie',['Analyseer oorzaak van afwijking','Bereken impact van bijsturen versus herijken','Bereid nieuw strategisch besluit voor indien nodig'],'Bestuur/ALV')}
    cause,options,authority=catalog.get(domain,('KPI buiten koers',['Voer oorzaakanalyse uit'],'Bestuur'))
    return {'domain':domain,'kpi':name,'cause':cause,'target':target,'actual':actual,'options':options,'decision_authority':authority,'automatic_execution':False,'approval_required':True}

def build_strategy_interventions(scorecard:dict[str,Any], report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); kpis=scorecard.get('kpis',[]) or []; off=[x for x in kpis if not x.get('on_track',False)]
    proposals=[_proposal(x) for x in off]
    reserve=float(((report.get('governance_control_tower',{}) or {}).get('kpis',{}) or {}).get('reserve',0) or 0)
    budget=float(((report.get('governance_control_tower',{}) or {}).get('kpis',{}) or {}).get('total_mandate_budget',0) or 0)
    for p in proposals:
        if p['domain']=='FINANCIEEL': p['estimated_financial_exposure']=max(0,round(budget-reserve,2))
        elif p['domain']=='RISICO': p['estimated_financial_exposure']='Te bepalen via MJOP/scenario-herberekening'
        else: p['estimated_financial_exposure']='Nader te kwantificeren'
    status='GEEN INTERVENTIE' if not proposals else 'VOORSTEL VEREIST' if scorecard.get('status')=='AANDACHT' else 'BESTUURLIJKE INTERVENTIE VEREIST'
    return {'strategy_intervention_version':ENGINE_VERSION,'generated_at':now,'decision_id':scorecard.get('decision_id',''),'selected_scenario':scorecard.get('selected_scenario',''),'scorecard_status':scorecard.get('status',''),'status':status,'proposal_count':len(proposals),'proposals':proposals,'human_decision_required':bool(proposals),'automatic_strategy_change':False,'next_action':'Geen interventie nodig; blijf maandelijks monitoren.' if not proposals else f"Beoordeel {len(proposals)} interventievoorstel(len) en leg vereiste besluiten voor aan Bestuur/ALV."}
