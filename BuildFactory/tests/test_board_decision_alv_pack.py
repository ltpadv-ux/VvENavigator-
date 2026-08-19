from src.board_decision_alv_pack import build_board_decision_alv_pack

def explainable():
 return {'status':'UITLEG BESCHIKBAAR','decision_readiness':'BESLUITRIJP','best_explanation':{'intervention':'VROEG INGRIJPEN','confidence_score':86,'decision_readiness':'BESLUITRIJP','trigger_context':{'domain':'treasury','severity':'ORANJE'},'why_recommended':'Sterke match en bewijsbasis.','alternatives_considered':[{'intervention':'NIETS DOEN'}],'uncertainties':['Scenario-onzekerheid blijft aanwezig.'],'board_tradeoffs':['Effect versus kosten']},'traceability':{'recommendation_engine_version':'10.8.0'}}

def confidence():
 return {'decision_readiness':'BESLUITRIJP','best_recommendation':{'avg_health_uplift':4.5,'avg_risk_reduction':6.0,'avg_value_per_euro':2.2,'evidence_strength':'STERK'}}

def test_no_explanation_no_pack():
 x=build_board_decision_alv_pack({'status':'GEEN UITLEG BESCHIKBAAR'},{}); assert x['status']=='GEEN BESLUITSTUK BESCHIKBAAR'

def test_pack_contains_decision_points_and_audit_trail():
 x=build_board_decision_alv_pack(explainable(),confidence(),{'executive_command_center_version':'10.0.0','board_status':'ACTIE VEREIST'}); assert x['status']=='BESLUITSTUK GEREED'; assert len(x['pack']['decision_points'])>=5; assert x['pack']['audit_trail']['source_board_status']=='ACTIE VEREIST'

def test_human_approval_preserved():
 x=build_board_decision_alv_pack(explainable(),confidence()); assert x['human_approval_required'] is True; assert x['automatic_decision'] is False
