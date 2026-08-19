from src.governance_policy_baseline_doctrine import build_policy_baseline_and_doctrine

def history():
 return [
  {'topic':'MJOP','decision':'Versneld onderhoud','same_course':True,'board_rationale_complete':True},
  {'topic':'MJOP','decision':'Versneld onderhoud','same_course':True,'board_rationale_complete':True},
  {'topic':'MJOP','decision':'Versneld onderhoud','same_course':False,'material_divergence':True,'board_rationale_complete':True},
 ]

def test_requires_history():
 x=build_policy_baseline_and_doctrine({},[]); assert x['status']=='ONVOLDOENDE HISTORIE VOOR DOCTRINE'

def test_builds_doctrine():
 x=build_policy_baseline_and_doctrine({'status':'BEWUSTE BELEIDSONTWIKKELING'},history()); assert x['status']=='BELEIDSBASELINE & DOCTRINE GEREED'; assert x['doctrines'][0]['dominant_course']=='Versneld onderhoud'

def test_human_approval_preserved():
 x=build_policy_baseline_and_doctrine({'status':'BELEID CONSISTENT'},history()); assert x['human_policy_approval_required'] is True; assert x['automatic_policy_change'] is False
