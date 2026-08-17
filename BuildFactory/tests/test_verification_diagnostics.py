from src.verification_diagnostics import diagnose_verification


def test_diagnostics_map_failed_checks_to_modules():
    verification={"checks":{"artifact_pdf":False,"artifact_docx":True,"quality_gate":False}}
    result=diagnose_verification(verification,{"enterprise":{"release":{"quality_gate":{"issues":[]}}}})
    assert result["status"]=="ACTION_REQUIRED"
    assert result["blocker_count"]==2
    modules={d["module"] for d in result["diagnostics"]}
    assert "Production Binary Renderers / PDF" in modules
    assert "Compliance & Quality Engine" in modules


def test_diagnostics_clear_when_all_checks_pass():
    result=diagnose_verification({"checks":{"artifact_pdf":True,"quality_gate":True}})
    assert result["status"]=="CLEAR"
    assert result["blocker_count"]==0
