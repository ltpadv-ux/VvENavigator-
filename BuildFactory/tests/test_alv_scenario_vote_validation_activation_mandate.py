from src.alv_scenario_vote_validation_activation_mandate import validate_vote_and_issue_activation_mandate

P={'scenario_resolution_pack_id':'R1','status':'CONFIDENCE-GATED BESLUITPAKKET GEREED VOOR BESTUURLIJKE REVIEW','scenario_name':'BASIS','risk_appetite_limits_pct':{'reserve':10,'liquidity':10,'combined':5},'verified_shortfall_pct':{'reserve':5,'liquidity':6,'combined':3},'simulation_confidence_pct':97,'draft_alv_resolution':'De ALV besluit...'}

def test_valid_vote_issues_mandate():
 v={'meeting_id':'M1','total_vote_weight':100,'present_vote_weight':80,'yes_vote_weight':60,'no_vote_weight':15,'abstain_vote_weight':5,'minutes_record_complete':True,'chair_confirmed':True,'execution_owner':'Bestuur','activation_date':'2026-09-01'}; x=validate_vote_and_issue_activation_mandate(P,v); assert x['validated_for_manual_activation'] is True and x['activation_mandate']['requires_manual_activation'] is True

def test_quorum_blocks_mandate():
 v={'total_vote_weight':100,'present_vote_weight':40,'yes_vote_weight':35,'no_vote_weight':5,'minutes_record_complete':True,'chair_confirmed':True,'execution_owner':'Bestuur','activation_date':'2026-09-01'}; x=validate_vote_and_issue_activation_mandate(P,v); assert x['activation_mandate'] is None

def test_no_automatic_activation():
 x=validate_vote_and_issue_activation_mandate(P,{}); assert x['automatic_scenario_activation'] is False and x['automatic_execution'] is False
