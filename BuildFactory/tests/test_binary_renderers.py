from pathlib import Path
from src.binary_renderers import render_pdf, render_docx, render_xlsx


def _model():
    return {"document_title":"VvE Test","meta":{"vve_name":"VvE Test"},"sections":[
        {"title":"Voorblad","type":"cover","content":{"vve_name":"VvE Test","version":"3.7.0"}},
        {"title":"KPI","type":"table","content":[{"kpi":"VNI","value":80}]},
        {"title":"Acties","type":"list","content":["Actie 1","Actie 2"]}
    ]}


def test_binary_renderers_write_files(tmp_path):
    pdf=Path(render_pdf(_model(),tmp_path/"report.pdf")); docx=Path(render_docx(_model(),tmp_path/"report.docx")); xlsx=Path(render_xlsx(_model(),tmp_path/"report.xlsx"))
    assert pdf.exists() and pdf.stat().st_size>0
    assert docx.exists() and docx.stat().st_size>0
    assert xlsx.exists() and xlsx.stat().st_size>0
