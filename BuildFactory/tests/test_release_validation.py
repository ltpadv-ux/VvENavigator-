from pathlib import Path
from hashlib import sha256
from src.release_validation import validate_release


def _item(name, path):
    p=Path(path); return {"name":name,"path":str(p),"sha256":sha256(p.read_bytes()).hexdigest()}


def test_release_validation_go(tmp_path):
    files=[]
    for name in ("pdf","docx","xlsx"):
        p=tmp_path/f"test.{name}"; p.write_bytes(name.encode()); files.append(_item(name,p))
    result=validate_release({"release_version":"3.9.0","vve_name":"Test","files":files},{"status":"GOEDGEKEURD","can_publish":True})
    assert result["approved"] is True
    assert result["status"]=="VRIJGEGEVEN VOOR ALV"


def test_release_validation_no_go_when_missing(tmp_path):
    p=tmp_path/"test.pdf"; p.write_bytes(b"pdf")
    result=validate_release({"files":[_item("pdf",p)]},{"status":"GOEDGEKEURD","can_publish":True})
    assert result["approved"] is False
    assert result["sign_off"]["decision"]=="NO-GO"
