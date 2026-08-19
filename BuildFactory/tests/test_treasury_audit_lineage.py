from src.treasury_audit_lineage import build_treasury_audit_lineage

def base_report():
    return {
        'treasury_early_warning_calendar':{'actions':[{'month':'2026-09','category':'DSCR','title':'VvE A: DSCR aandacht','severity':'ROOD','detail':'DSCR te laag'}]},
        'treasury_decision_board_pack':{'agenda_items':[{'agenda_id':'TRAGEN-1','month':'2026-09','category':'DSCR','title':'VvE A: DSCR aandacht','decision':'GOEDGEKEURD','rationale':'Herfinancieren'}]},
        'treasury_accountability_register':{'actions':[{'action_id':'TRACT-1','agenda_id':'TRAGEN-1','status':'AFGEROND','evidence':['bankofferte','bestuursbesluit']}]},
        'treasury_decision_effectiveness':{'closures':[{'action_id':'TRACT-1','status':'EFFECT BEWEZEN','closure_status':'GESLOTEN','checks':[{'check':'DSCR','ok':True}]}]},
    }

def test_complete_lineage():
    x=build_treasury_audit_lineage(base_report())
    assert x['status']=='AUDIT TRAIL COMPLEET'
    assert x['complete_chain_count']==1
    assert x['closed_chain_count']==1
    assert x['chains'][0]['lineage_id'].startswith('TRLIN-')

def test_missing_execution_creates_gap():
    r=base_report(); r['treasury_accountability_register']={'actions':[]}
    x=build_treasury_audit_lineage(r)
    assert x['status']=='AUDIT GAP GEVONDEN'
    assert x['incomplete_chain_count']==1

def test_chain_hash_is_deterministic():
    a=build_treasury_audit_lineage(base_report())['chains'][0]['chain_hash']
    b=build_treasury_audit_lineage(base_report())['chains'][0]['chain_hash']
    assert a==b
