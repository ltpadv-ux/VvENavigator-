from src.release_control_center import build_release_control_center


def test_control_center_green():
    report={"release":{"status":"VRIJGEGEVEN VOOR ALV"},"verification":{"verified":True,"status":"VERIFIED"},"diagnostics":{"diagnostics":[]},"self_healing":{"status":"NOT_NEEDED","repairs":[],"human_actions":[]}}
    result=build_release_control_center(report)
    assert result["status"]=="GROEN"
    assert result["human_action_count"]==0


def test_control_center_repaired():
    report={"release":{"status":"VRIJGEGEVEN VOOR ALV"},"verification":{"verified":False,"status":"FAILED"},"diagnostics":{"diagnostics":[]},"self_healing":{"status":"HEALED","after":{"verified":True},"repairs":[{"status":"REPAIRED"}],"human_actions":[]}}
    result=build_release_control_center(report)
    assert result["status"]=="HERSTELD"


def test_control_center_blocked():
    action={"remediation":"Herstel brondata"}
    report={"release":{"status":"BLOCKED"},"verification":{"verified":False,"status":"FAILED"},"diagnostics":{"diagnostics":[action]},"self_healing":{"status":"ESCALATE","repairs":[],"human_actions":[action]}}
    result=build_release_control_center(report)
    assert result["status"]=="GEBLOKKEERD"
    assert result["next_action"]=="Herstel brondata"
