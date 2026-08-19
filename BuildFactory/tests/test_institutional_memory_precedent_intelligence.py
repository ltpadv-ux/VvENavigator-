from src.institutional_memory_precedent_intelligence import retrieve_precedents

def test_precedent_found():
    archive={'entries':[{'memory_id':'GOVMEM-1','title':'Dakonderhoud','decision_text':'Versnel dakonderhoud','financial_result':{'planned_budget':10000,'actual_spend':9500},'final_result':'dak hersteld','lessons_learned':['vroeg inspecteren'],'evidence_count':4}]}
    result=retrieve_precedents(archive,{'question':'dakonderhoud','domain':'dak'})
    assert result['status']=='PRECEDENT INTELLIGENCE BESCHIKBAAR'
    assert result['best_precedent']['memory_id']=='GOVMEM-1'

def test_empty_archive():
    result=retrieve_precedents({'entries':[]},'dak')
    assert result['status']=='ONVOLDOENDE GEHEUGEN OF VRAAGCONTEXT'

def test_advisory_only():
    archive={'entries':[{'memory_id':'GOVMEM-1','title':'Dak','decision_text':'Dak herstel','financial_result':{},'evidence_count':1}]}
    result=retrieve_precedents(archive,'dak')
    assert result['automatic_decision'] is False
    assert result['human_judgment_required'] is True
