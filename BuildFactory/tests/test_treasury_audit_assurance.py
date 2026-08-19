from src.treasury_audit_assurance import build_treasury_audit_assurance

def base_report():
    return {
      'treasury_audit_lineage':{'chains':[{'lineage_id':'TRLIN-1','agenda_id':'TRAGEN-1','title':'Kasbuffer','complete':True}]},
      'treasury_decision_board_pack':{'agenda_items':[{'agenda_id':'TRAGEN-1','approved_by':'ALV','decision_authority':'Bestuur/ALV','draft_decision':'Herstel buffer','rationale':'Risico te hoog'}]},
      'treasury_accountability_register':{'actions':[{'agenda_id':'TRAGEN-1','action_id':'TRACT-1','owner':'Beheerder','budget':10000,'spent':9000,'status':'AFGEROND','evidence':['factuur.pdf']}]},
      'treasury_decision_effectiveness':{'closures':[{'action_id':'TRACT-1','closure_status':'GESLOTEN','status':'EFFECT BEWEZEN','checks':[{'check':'DSCR','ok':True}],'human_closure_required':True,'automatic_closure':False}]}
    }

def test_strong_assurance():
    x=build_treasury_audit_assurance(base_report()); assert x['overall_assurance_score']==100; assert x['status']=='ASSURANCE STERK'

def test_failed_segregation_lowers_score():
    r=base_report(); r['treasury_accountability_register']['actions'][0]['owner']='ALV'; x=build_treasury_audit_assurance(r); assert x['results'][0]['assurance_score']==85; assert 'FUNCTIESCHEIDING' in x['results'][0]['failed_controls']

def test_over_budget_is_control_failure():
    r=base_report(); r['treasury_accountability_register']['actions'][0]['spent']=12000; x=build_treasury_audit_assurance(r); assert 'BUDGETCONTROLE' in x['results'][0]['failed_controls']
