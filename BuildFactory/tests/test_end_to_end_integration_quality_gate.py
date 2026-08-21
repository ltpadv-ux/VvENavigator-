from src.end_to_end_integration_quality_gate import evaluate_production_readiness

def test_all_domains_green_is_ready():
 s={k:{'passed':True,'score_pct':100} for k in ['finance','mjop','risk','governance','audit','digital_twin','scenario','model_controls','excel_master','ci']}; x=evaluate_production_readiness(s); assert x['production_ready'] is True and x['status']=='PRODUCTION READY'
def test_ci_failure_blocks_release():
 s={k:{'passed':True,'score_pct':100} for k in ['finance','mjop','risk','governance','audit','digital_twin','scenario','model_controls','excel_master']}; s['ci']={'passed':False,'score_pct':80}; x=evaluate_production_readiness(s); assert x['production_ready'] is False and any('CI' in b or 'ci' in b for b in x['blockers'])
def test_no_automatic_release():
 x=evaluate_production_readiness({}); assert x['automatic_production_release'] is False
