from src.native_export_engine import build_native_export_contract

def test_native_export_contract_declares_binary_renderers():
    model={"meta":{"vve_name":"VvE Test","version":"3.6.0"},"page_plan":{"page_size":"A4"},"sections":[]}
    result=build_native_export_contract(model)
    assert result["native_export_version"]=="3.6.0"
    assert result["renderers"]["pdf"]["library"]=="reportlab"
    assert result["renderers"]["docx"]["library"]=="python-docx"
    assert result["renderers"]["xlsx"]["library"]=="openpyxl"
    assert result["distribution_zip"].endswith("-distribution.zip")
