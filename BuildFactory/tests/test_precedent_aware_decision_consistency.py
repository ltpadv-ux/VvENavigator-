from src.precedent_aware_decision_consistency import evaluate_precedent_consistency

def test_consistent_course():
    cur={'best_recommendation':{'intervention':'dakisolatie'}}
    prev={'precedents':[{'memory_id':'1','title':'Dak','precedent_score':90,'similarity_score':85,'decision_text':'dakisolatie uitvoeren','final_result':'goed','lessons_learned':[]}]}
    x=evaluate_precedent_consistency(cur,prev); assert x['status']=='CONSISTENT MET PRECEDENT'; assert x['consistency_control_passed']

def test_material_divergence_requires_rationale():
    cur={'best_recommendation':{'intervention':'warmtepomp'}}
    prev={'precedents':[{'memory_id':'1','title':'Dak','precedent_score':90,'similarity_score':80,'decision_text':'dakisolatie uitvoeren','final_result':'goed','lessons_learned':[]}]}
    x=evaluate_precedent_consistency(cur,prev); assert x['status']=='MATERIELE AFWIJKING - MOTIVERING VEREIST'; assert not x['consistency_control_passed']

def test_rationale_closes_control():
    cur={'best_recommendation':{'intervention':'warmtepomp'}}
    prev={'precedents':[{'memory_id':'1','title':'Dak','precedent_score':90,'similarity_score':80,'decision_text':'dakisolatie uitvoeren','final_result':'goed','lessons_learned':[]}]}
    x=evaluate_precedent_consistency(cur,prev,{'board_rationale':'Nieuwe energieprijzen en installatieconditie rechtvaardigen afwijking.'}); assert x['status']=='BEWUSTE AFWIJKING - MOTIVERING VASTGELEGD'; assert x['consistency_control_passed']
