from src.strategy_execution_scorecard import build_strategy_execution_scorecard

def test_waits_for_locked_strategy():
    x=build_strategy_execution_scorecard({},{}); assert x['status']=='WACHT OP STRATEGIE'

def test_green_locked_strategy_scores_on_track():
    strategy={'strategy_lock':{'status':'VERGRENDELD','decision_id':'STR-1','selected_scenario':'Duurzaam','baseline':{'reserve_pressure_percent':50,'adjusted_12m_risk':10}},'deviation':{'score':0}}
    report={'governance_control_tower':{'kpis':{'total_mandate_budget':100,'reserve':200}},'mandate_compliance':{'red_count':0},'mandate_forecast':{'high_risk_count':0},'amendment_effectiveness':{'open_count':0},'executive_risk_radar':{'outlook':[{'risk_score':10}]}}
    x=build_strategy_execution_scorecard(strategy,report); assert x['status']=='OP KOERS'; assert x['score']==100

def test_off_track_strategy_is_flagged():
    strategy={'strategy_lock':{'status':'VERGRENDELD','decision_id':'STR-1','selected_scenario':'Basis','baseline':{'reserve_pressure_percent':40,'adjusted_12m_risk':5}},'deviation':{'score':60}}
    report={'governance_control_tower':{'kpis':{'total_mandate_budget':90,'reserve':100}},'mandate_compliance':{'red_count':2},'mandate_forecast':{'high_risk_count':2},'amendment_effectiveness':{'open_count':1},'executive_risk_radar':{'outlook':[{'risk_score':40}]}}
    x=build_strategy_execution_scorecard(strategy,report); assert x['status']=='BUITEN KOERS'; assert x['off_track_count']>=4
