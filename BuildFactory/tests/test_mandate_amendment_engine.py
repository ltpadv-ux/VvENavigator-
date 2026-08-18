from src.mandate_amendment_engine import apply_mandate_amendments

def test_budget_and_deadline_amendment_are_applied_once():
    mandates={'mandates':[{'mandate_id':'MAN-1','budget':100000,'deadline':'2026-12-01','amendment_version':0}]}
    amendments=[{'corrective_id':'COR-1','mandate_id':'MAN-1','action':'BUDGET_VERHOGEN','budget_change':20000,'schedule_change_days':14,'approved_by':'ALV'}]
    first=apply_mandate_amendments(mandates,amendments)
    item=first['mandates']['mandates'][0]
    assert item['budget']==120000
    assert item['deadline']=='2026-12-15'
    assert item['amendment_version']==1
    second=apply_mandate_amendments(first['mandates'],amendments,first)
    assert second['applied_count']==0

def test_scope_adjustment_records_before_after_history():
    mandates={'mandates':[{'mandate_id':'MAN-2','budget':50000,'deadline':''}]}
    amendments=[{'corrective_id':'COR-2','mandate_id':'MAN-2','action':'SCOPE_AANPASSEN','rationale':'Niet-kritische scope vervalt'}]
    result=apply_mandate_amendments(mandates,amendments)
    assert result['mandates']['mandates'][0]['scope_status']=='AANGEPAST'
    assert result['history'][0]['before']['mandate_id']=='MAN-2'
