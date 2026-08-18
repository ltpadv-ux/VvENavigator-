from src.closed_loop_management import build_closed_loop_management

def test_empty_report_requires_strategy():
    result = build_closed_loop_management({})
    assert result['status'] == 'STRATEGIEBESLUIT VEREIST'
    assert result['human_governance_preserved'] is True

def test_off_course_requires_adjustment():
    report = {'scenario_strategy_lock': {'status': 'VERGRENDELD'}, 'strategy_execution_scorecard': {'status': 'BUITEN KOERS'}}
    result = build_closed_loop_management(report)
    assert result['status'] == 'BIJSTURING VEREIST'

def test_completed_cycle():
    report = {
        'scenario_strategy_lock': {'status': 'VERGRENDELD'},
        'strategy_execution_scorecard': {'status': 'OP KOERS'},
        'strategy_intervention_engine': {'status': 'GEEN INTERVENTIE'},
        'intervention_decision_matrix': {'status': 'GEEN INTERVENTIES'},
        'intervention_execution_mandate': {'status': 'GEEN BESLUIT NODIG'},
        'execution_benefits_tracking': {'status': 'EFFECT BEWEZEN', 'closure': {'status': 'GESLOTEN'}, 'benefits': {'realization_score': 100}},
        'governance_control_tower': {'overall_status': 'GROEN'}
    }
    result = build_closed_loop_management(report)
    assert result['status'] == 'GESLOTEN STUURKRING'
    assert result['loop_completeness_score'] == 100
