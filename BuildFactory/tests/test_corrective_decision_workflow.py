from src.corrective_decision_workflow import build_corrective_decisions, approved_mandate_amendments

def test_corrective_recommendation_becomes_approval_record():
    optimizer={'recommendations':[{'mandate_id':'MAN-1','risk':'HOOG','recommended_action':{'action':'BUDGET_VERHOGEN','description':'Verhoog budget','cost_impact':20000,'schedule_impact_days':0}}]}
    result=build_corrective_decisions(optimizer)
    assert result['pending_count']==1
    assert result['decisions'][0]['approval_level']=='ALV'

def test_approved_decision_yields_mandate_amendment():
    optimizer={'recommendations':[{'mandate_id':'MAN-1','risk':'HOOG','recommended_action':{'action':'PLANNING_AANPASSEN','description':'Herplan','cost_impact':0,'schedule_impact_days':14}}]}
    first=build_corrective_decisions(optimizer); first['decisions'][0].update(decision='GOEDGEKEURD',status='BESLOTEN',approved_by='Bestuur',rationale='Continuiteit')
    second=build_corrective_decisions(optimizer,first); amendments=approved_mandate_amendments(second)
    assert second['decisions'][0]['decision']=='GOEDGEKEURD'
    assert amendments[0]['schedule_change_days']==14
