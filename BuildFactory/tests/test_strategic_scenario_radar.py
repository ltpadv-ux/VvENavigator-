from src.strategic_scenario_radar import build_strategic_scenario_radar

def test_scenario_radar_returns_preference():
    radar={'outlook':[{'risk_score':4},{'risk_score':6}]}
    tower={'kpis':{'reserve':200000,'total_mandate_budget':100000}}
    result=build_strategic_scenario_radar(radar,tower)
    assert result['scenario_count']==3
    assert result['preferred_scenario'] in {'Basis','Duurzaam','Versneld'}
    assert result['preferred_robustness_score']>=0

def test_high_reserve_pressure_reduces_robustness():
    radar={'outlook':[{'risk_score':2}]}
    tower={'kpis':{'reserve':50000,'total_mandate_budget':100000}}
    result=build_strategic_scenario_radar(radar,tower)
    scores={x['scenario']:x['robustness_score'] for x in result['scenarios']}
    assert scores['Basis']<100
