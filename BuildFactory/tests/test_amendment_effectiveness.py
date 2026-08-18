from src.amendment_effectiveness import evaluate_amendment_effectiveness

def test_effective_amendment_closes_when_risk_is_low_and_within_budget():
    amendment={'applied':[{'corrective_id':'COR-1','mandate_id':'MAN-1'}]}
    before_c={'mandates':[{'mandate_id':'MAN-1','compliance_status':'ORANJE'}]}
    before_f={'forecasts':[{'mandate_id':'MAN-1','risk':'HOOG','projected_final_cost':120000}]}
    after_c={'mandates':[{'mandate_id':'MAN-1','compliance_status':'GROEN','budget':120000,'spent_amount':60000}]}
    after_f={'forecasts':[{'mandate_id':'MAN-1','risk':'LAAG','projected_final_cost':110000}]}
    result=evaluate_amendment_effectiveness(amendment,before_c,before_f,after_c,after_f)
    assert result['closed_count']==1
    assert result['status']=='EFFECT BEWEZEN'

def test_amendment_stays_open_when_risk_remains_high():
    amendment={'applied':[{'corrective_id':'COR-1','mandate_id':'MAN-1'}]}
    before_c={'mandates':[]}; before_f={'forecasts':[{'mandate_id':'MAN-1','risk':'HOOG'}]}
    after_c={'mandates':[{'mandate_id':'MAN-1','compliance_status':'GROEN','budget':100000,'spent_amount':50000}]}
    after_f={'forecasts':[{'mandate_id':'MAN-1','risk':'HOOG'}]}
    result=evaluate_amendment_effectiveness(amendment,before_c,before_f,after_c,after_f)
    assert result['open_count']==1
    assert result['status']=='NADER BEWIJS NODIG'
