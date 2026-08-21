from src.final_enterprise_production_baseline_handover import build_handover_pack,REQUIRED_DOCS

def _docs(): return {k:{'present':True,'verified':True,'reference':'ref-'+k} for k in REQUIRED_DOCS}
def _base(): return {'version':'19.0.0','commit_sha':'abc','tag':'v19.0.0','ga_release_record_ref':'ga-1','continuous_assurance_ref':'assurance-1','baseline_frozen':True,'release_freeze_enabled':True}
def _approvals(): return {'product_owner_approved':True,'operations_owner_approved':True,'security_owner_approved':True,'business_owner_approved':True}
def test_complete_handover_is_accepted():
 x=build_handover_pack(_base(),_docs(),_approvals()); assert x['decision']=='HANDOVER ACCEPTED' and x['steady_state_operations_authorized'] is True
def test_missing_document_holds():
 d=_docs(); d['operations_runbook']['reference']=None; x=build_handover_pack(_base(),d,_approvals()); assert x['decision']=='HANDOVER HOLD' and 'operations_runbook' in x['open_documents']
def test_release_freeze_required():
 b=_base(); b['release_freeze_enabled']=False; x=build_handover_pack(b,_docs(),_approvals()); assert x['handover_complete'] is False and x['automatic_release_unfreeze'] is False
