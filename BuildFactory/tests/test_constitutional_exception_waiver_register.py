from datetime import date
from src.constitutional_exception_waiver_register import register_constitutional_waiver

G={'gate':'BLOCK','gate_id':'G1','blockers':['budget']}
P={'proposal_id':'P1','financial_commitment_eur':25000}
def test_incomplete_waiver():
 x=register_constitutional_waiver(G,P,{}); assert x['status']=='WAIVER ONVOLLEDIG OF NIET GOEDGEKEURD'
def test_active_approved_waiver():
 w={'reason':'Urgent herstel','decision_authority':'ALV','approval_status':'GOEDGEKEURD','valid_from':'2026-08-19','valid_until':'2026-12-31','review_date':'2026-10-01','risk_acceptance':'Risico expliciet geaccepteerd','scope':'P1'}
 x=register_constitutional_waiver(G,P,w,today=date(2026,8,19)); assert x['status']=='WAIVER ACTIEF'; assert x['waiver']['waiver_id'].startswith('GOVWVR-')
def test_expired_waiver():
 w={'reason':'Tijdelijk','decision_authority':'ALV','approval_status':'GOEDGEKEURD','valid_from':'2026-01-01','valid_until':'2026-02-01','review_date':'2026-01-15','risk_acceptance':'Geaccepteerd','scope':'P1'}
 x=register_constitutional_waiver(G,P,w,today=date(2026,8,19)); assert x['status']=='WAIVER VERLOPEN'
