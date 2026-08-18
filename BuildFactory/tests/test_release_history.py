from src.release_history import build_trend_monitor


def test_release_history_reliability_and_trend():
    history=[
        {"control_status":"GEBLOKKEERD","repair_count":0,"quality_issue_count":2},
        {"control_status":"HERSTELD","repair_count":1,"quality_issue_count":0},
        {"control_status":"GROEN","repair_count":0,"quality_issue_count":0},
    ]
    result=build_trend_monitor(history)
    assert result["runs"]==3
    assert result["blocked_runs"]==1
    assert result["healed_runs"]==1
    assert result["green_runs"]==1
    assert result["release_reliability_score"]==58.3
    assert result["trend"] in {"STABIEL","VERBETEREND","VERSLECHTEREND"}
