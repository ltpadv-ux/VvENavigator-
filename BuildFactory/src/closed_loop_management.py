"""Enterprise 7.0 closed-loop management: connect strategy, decisions, mandates, execution and realized benefits."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='7.0.0'

def build_closed_loop_management(report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat()
    strategy=report.get('scenario_strategy_lock',{}) or {}; score=report.get('strategy_execution_scorecard',{}) or {}; intervention=report.get('strategy_intervention_engine',{}) or {}; matrix=report.get('intervention_decision_matrix',{}) or {}; mandate=report.get('intervention_execution_mandate',{}) or {}; benefits=report.get('execution_benefits_tracking',{}) or {}; tower=report.get('governance_control_tower',{}) or {}
    stages=[
      {'stage':'STRATEGIE','ready':strategy.get('status')=='VERGRENDELD','status':strategy.get('status','ONBEKEND')},
      {'stage':'STURING','ready':score.get('status') in {'OP KOERS','AANDACHT','BUITEN KOERS'},'status':score.get('status','ONBEKEND')},
      {'stage':'INTERVENTIE','ready':intervention.get('status') in {'GEEN INTERVENTIE','VOORSTEL VEREIST','BESTUURLIJKE INTERVENTIE VEREIST'},'status':intervention.get('status','ONBEKEND')},
      {'stage':'BESLUIT','ready':matrix.get('status') in {'GEEN INTERVENTIES','VOORKEURSVARIANT BESCHIKBAAR'},'status':matrix.get('status','ONBEKEND')},
      {'stage':'MANDAAT','ready':mandate.get('status') in {'GEEN BESLUIT NODIG','MANDAAT ACTIEF'},'status':mandate.get('status','ONBEKEND')},
      {'stage':'REALISATIE','ready':benefits.get('status') in {'GEEN ACTIEF MANDAAT','IN UITVOERING','EFFECTCONTROLE','EFFECT BEWEZEN'},'status':benefits.get('status','ONBEKEND')},
    ]
    ready=sum(1 for s in stages if s['ready']); loop_score=round(ready/len(stages)*100,1)
    closure=(benefits.get('closure',{}) or {}).get('status',''); strategy_status=score.get('status','')
    if closure=='GESLOTEN' and strategy_status=='OP KOERS': state='GESLOTEN STUURKRING'
    elif strategy_status=='BUITEN KOERS': state='BIJSTURING VEREIST'
    elif mandate.get('status')=='BESLUIT VEREIST': state='BESTUURLIJK BESLUIT VEREIST'
    elif benefits.get('status') in {'IN UITVOERING','EFFECTCONTROLE'}: state='REALISATIE LOPEND'
    elif strategy.get('status')!='VERGRENDELD': state='STRATEGIEBESLUIT VEREIST'
    else: state='STUURKRING ACTIEF'
    governance_ok=tower.get('overall_status','')!='ROOD'
    return {'closed_loop_version':ENGINE_VERSION,'generated_at':now,'status':state,'loop_completeness_score':loop_score,'governance_safe':governance_ok,'stages':stages,'strategy_decision_id':(strategy.get('decision',{}) or {}).get('decision_id',''),'intervention_decision_id':(mandate.get('decision',{}) or {}).get('decision_id',''),'execution_mandate_id':(mandate.get('mandate',{}) or {}).get('mandate_id',''),'benefits_realization_score':(benefits.get('benefits',{}) or {}).get('realization_score',0),'human_governance_preserved':True,'automatic_strategy_change':False,'next_action':'Nieuwe cyclus starten vanuit actuele KPI-baseline.' if state=='GESLOTEN STUURKRING' else ('Bestuur/ALV moet eerst besluiten.' if 'BESLUIT VEREIST' in state else 'Volg de open stap in de stuurkring en actualiseer de onderliggende KPI’s.')}
