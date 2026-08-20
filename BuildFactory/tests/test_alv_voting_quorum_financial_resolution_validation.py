from src.alv_voting_quorum_financial_resolution_validation import validate_financial_resolution
P={'resolution_pack_id':'R1','recommendation':'VOORLEGGEN MET POSITIEF ADVIES','draft_alv_resolution':'De ALV besluit...'}
def test_valid_vote():
 v={'meeting_id':'M1','total_vote_weight':100,'present_vote_weight':80,'yes_vote_weight':55,'no_vote_weight':20,'abstain_vote_weight':5,'financial_mandate_confirmed':True,'minutes_record_complete':True}; x=validate_financial_resolution(P,v,{'quorum_pct':50,'majority_pct':50}); assert x['validated_for_formal_registration'] is True
def test_quorum_blocks():
 v={'total_vote_weight':100,'present_vote_weight':40,'yes_vote_weight':35,'no_vote_weight':5,'financial_mandate_confirmed':True,'minutes_record_complete':True}; assert validate_financial_resolution(P,v)['validated_for_formal_registration'] is False
def test_no_automatic_adoption():
 x=validate_financial_resolution(P,{}); assert x['automatic_adoption'] is False and x['automatic_execution'] is False
