from pathlib import Path
from src.production_verification import verify_production_result


def test_production_verification_detects_complete_release(tmp_path):
    files={}
    for ext in ("pdf","docx","xlsx"):
        p=tmp_path/f"test.{ext}"; p.write_bytes(b"ok"); files[ext]=str(p)
    z=tmp_path/"release.zip"; z.write_bytes(b"zip")
    result={
        "status":"VRIJGEGEVEN VOOR ALV",
        "native_export":{"files":files},
        "package":{"distribution_zip":str(z)},
        "validation":{"sign_off":{"decision":"GO"}},
        "enterprise":{"release":{"quality_gate":{"can_publish":True}}},
    }
    verification=verify_production_result(result)
    assert verification["verified"] is True
    assert verification["status"]=="VERIFIED"


def test_production_verification_fails_on_missing_artifacts():
    verification=verify_production_result({"status":"NIET VRIJGEGEVEN"})
    assert verification["verified"] is False
    assert verification["issues"]
