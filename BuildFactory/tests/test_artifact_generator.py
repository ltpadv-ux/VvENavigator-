from src.artifact_generator import artifact_contract, build_artifact_plan


def test_artifact_plan_has_all_physical_outputs():
    model={"meta":{"vve_name":"VvE Test","version":"3.5.0"},"page_plan":{"page_size":"A4"},"sections":[{},{}]}
    plan=build_artifact_plan(model)
    assert plan["artifact_engine_version"]=="3.5.0"
    assert all(key in plan["files"] for key in ("html","pdf","docx","xlsx","manifest"))
    contract=artifact_contract(model)
    assert contract["adapters"]["pdf"]["page_size"]=="A4"
    assert contract["adapters"]["docx"]["sections"]==2
