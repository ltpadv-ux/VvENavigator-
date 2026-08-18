from src.executive_risk_radar import build_risk_radar

def test_radar_flags_financial_and_mandate_risk():
    report={'governance_control_tower':{'overall_status':'ORANJE'},'mandate_forecast':{'forecasts':[{'mandate_id':'MAN-1','risk':'HOOG','reasons':['Budgetrisico']}]},'mandate_compliance':{'findings':[]},'governance_decision_register':{'dashboard':{'open_decisions':0}},'alv_decision_workflow':{'ready_for_alv':0},'alv_execution_mandates':{'total_budget':120000},'release':{'executive_cockpit':{'key_metrics':{'reserve':100000}}}}
    result=build_risk_radar(report,months=12)
    assert result['high_risk_count']>=2
    assert result['outlook'][-1]['risk_count']>=2

def test_radar_green_without_elevated_risks():
    report={'governance_control_tower':{'overall_status':'GROEN'},'mandate_forecast':{'forecasts':[]},'mandate_compliance':{'findings':[]},'governance_decision_register':{'dashboard':{'open_decisions':0}},'alv_decision_workflow':{'ready_for_alv':0},'alv_execution_mandates':{'total_budget':50000},'release':{'executive_cockpit':{'key_metrics':{'reserve':100000}}}}
    result=build_risk_radar(report)
    assert result['risk_count']==0
    assert result['outlook'][-1]['status']=='GROEN'
