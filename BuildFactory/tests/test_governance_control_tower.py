from src.governance_control_tower import build_control_tower

def test_green_control_tower():
    r={'autonomous_governance':{'cycle_status':'AUTONOOM GROEN'},'reliability_sla':{'compliant':True},'governance_decision_register':{'dashboard':{'open_decisions':0}},'mandate_compliance':{'red_count':0},'mandate_forecast':{'high_risk_count':0},'corrective_decision_workflow':{'pending_count':0},'amendment_effectiveness':{'open_count':0}}
    x=build_control_tower(r); assert x['overall_status']=='GROEN'; assert x['governance_score']==100

def test_red_control_tower_prioritizes_blocked_mandates():
    r={'reliability_sla':{'compliant':False},'governance_decision_register':{'dashboard':{'open_decisions':1}},'mandate_compliance':{'red_count':1},'mandate_forecast':{'high_risk_count':1},'corrective_decision_workflow':{'pending_count':1},'amendment_effectiveness':{'open_count':1}}
    x=build_control_tower(r); assert x['overall_status']=='ROOD'; assert x['priority_actions'][0].startswith('Los geblokkeerde')
