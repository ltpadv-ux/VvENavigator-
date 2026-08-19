"""Enterprise 9.5 Strategic Mandate Execution & Predictive Variance Control."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='9.5.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def build_strategic_mandate_variance_control(board_mandate:dict[str,Any], actuals:dict[str,Any]|None=None)->dict[str,Any]:
    actuals=actuals or {}
    mandate=board_mandate.get('mandate',{}) or {}
    if board_mandate.get('status')!='STRATEGISCH MANDAAT ACTIEF' or not mandate:
        return {'strategic_mandate_variance_version':ENGINE_VERSION,'status':'GEEN ACTIEF MANDAAT','variances':{},'alerts':[],'next_action':'Activeer eerst een goedgekeurd strategisch mandaat.'}
    current_month=int(actuals.get('current_month',0) or 0)
    contribution_actual=_num(actuals.get('contribution_delta'))
    mjop_actual=_num(actuals.get('mjop_acceleration'))
    spend_actual=_num(actuals.get('investment_spend'))
    score_actual=_num(actuals.get('governance_score'))
    target_path=mandate.get('contribution_path',[]) or []
    contribution_target=_num(next((x.get('contribution_delta') for x in target_path if int(x.get('month',0))>=max(current_month,1)), target_path[-1].get('contribution_delta',0) if target_path else 0))
    score_targets=mandate.get('kpi_targets',[]) or []
    score_target=_num(next((x.get('target_score') for x in score_targets if int(x.get('month',0))>=max(current_month,1)), score_targets[-1].get('target_score',0) if score_targets else 0))
    budget=_num(mandate.get('investment_budget_36m'))
    variances={
      'contribution_delta_variance':round(contribution_actual-contribution_target,4),
      'mjop_acceleration_variance':round(mjop_actual-_num(mandate.get('mjop_acceleration')),4),
      'budget_variance':round(spend_actual-budget,2),
      'governance_score_variance':round(score_actual-score_target,2),
    }
    alerts=[]
    if variances['contribution_delta_variance'] < -0.02: alerts.append({'severity':'ORANJE','type':'BIJDRAGEPAD','message':'Bijdrageontwikkeling blijft meer dan 2 procentpunt achter op mandaat.'})
    if variances['mjop_acceleration_variance'] < -0.05: alerts.append({'severity':'ORANJE','type':'MJOP','message':'MJOP-tempo blijft materieel achter op mandaat.'})
    if budget>0 and spend_actual>budget: alerts.append({'severity':'ROOD','type':'BUDGET','message':'Investeringsbudget is overschreden.'})
    if score_target>0 and variances['governance_score_variance'] < -5: alerts.append({'severity':'ROOD','type':'KPI','message':'VvE Health & Governance Score loopt meer dan 5 punten achter op target.'})
    if current_month in (12,24,36) and not actuals.get('evidence'): alerts.append({'severity':'ORANJE','type':'BEWIJS','message':'Meetmoment bereikt zonder bewijsset.'})
    status='ROOD' if any(a['severity']=='ROOD' for a in alerts) else ('ORANJE' if alerts else 'GROEN')
    next_action='Escaleren naar Bestuur/ALV en corrigerende maatregel laten besluiten.' if status=='ROOD' else ('Corrigeer uitvoering vóór het volgende meetmoment.' if status=='ORANJE' else 'Mandaat ligt op koers; blijf meten op 12/24/36 maanden.')
    return {'strategic_mandate_variance_version':ENGINE_VERSION,'status':status,'current_month':current_month,'mandate_id':mandate.get('mandate_id',''),'variances':variances,'alerts':alerts,'predictive_variance_control':True,'human_decision_required':True,'automatic_correction':False,'next_action':next_action}
