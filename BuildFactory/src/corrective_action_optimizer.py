"""Optimize corrective actions for mandate budget and deadline risks."""
from __future__ import annotations
from typing import Any

ENGINE_VERSION="5.6.0"


def optimize_corrective_actions(forecast: dict[str,Any]) -> dict[str,Any]:
    recommendations=[]
    for f in forecast.get('forecasts',[]) or []:
        risk=str(f.get('risk','LAAG')).upper()
        if risk not in {'MIDDEL','HOOG'}:
            continue
        budget=float(f.get('budget',0) or 0); projected=float(f.get('projected_final_cost',0) or 0); progress=float(f.get('progress_percent',0) or 0)
        gap=max(0.0,projected-budget)
        options=[]
        if gap>0:
            options.append({'action':'BUDGET_VERHOGEN','description':f'Verhoog budget met minimaal EUR {gap:.2f}.','cost_impact':gap,'schedule_impact_days':0,'risk_score':35})
            options.append({'action':'SCOPE_AANPASSEN','description':'Beperk niet-kritische scope zodat verwachte eindkosten binnen budget vallen.','cost_impact':0.0,'schedule_impact_days':0,'risk_score':25})
            options.append({'action':'FASEREN','description':'Faseer uitvoering en verschuif een deel naar een later moment.','cost_impact':0.0,'schedule_impact_days':30,'risk_score':30})
        if f.get('deadline') and progress<90:
            options.append({'action':'PLANNING_AANPASSEN','description':'Herplan capaciteit en mijlpalen om deadline-risico te verlagen.','cost_impact':0.0,'schedule_impact_days':14,'risk_score':20})
        options=sorted(options,key=lambda x:(x['risk_score'],x['cost_impact'],x['schedule_impact_days']))
        best=options[0] if options else {'action':'MONITOR','description':'Blijf monitoren.','cost_impact':0.0,'schedule_impact_days':0,'risk_score':50}
        recommendations.append({'mandate_id':f.get('mandate_id',''),'risk':risk,'budget':budget,'projected_final_cost':projected,'budget_gap':round(gap,2),'options':options,'recommended_action':best})
    return {'corrective_action_optimizer_version':ENGINE_VERSION,'status':'ACTIEVOORSTEL BESCHIKBAAR' if recommendations else 'GEEN ACTIE NODIG','recommendation_count':len(recommendations),'recommendations':recommendations,'next_action':recommendations[0]['recommended_action']['description'] if recommendations else 'Geen corrigerende maatregel nodig.'}
