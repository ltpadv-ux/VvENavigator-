from src.formal_resolution_voting_register import build_formal_resolution_voting_register

def pack():
    return {'status':'BESLUITSTUK GEREED','pack':{'pack_id':'ALVPK-1','meeting_type':'ALV','meeting_date':'2026-09-01','proposal':'Stem in met maatregel X','financial_impact':25000,'expected_effect':{'health_uplift':4}}}

def test_adopted_resolution_creates_execution_mandate():
    voting={'eligible_votes':100,'present_votes':80,'quorum_required_pct':50,'votes_for':60,'votes_against':20,'abstentions':0,'majority_required_pct':50,'minutes_reference':'ALV-2026-09-01-3','decision_authority':'ALV'}
    x=build_formal_resolution_voting_register(pack(),voting)
    assert x['status']=='BESLUIT AANGENOMEN - MANDAAT GEREED'
    assert x['resolution']['adopted'] is True
    assert x['execution_mandate']['mandate_id'].startswith('ALVMND-')

def test_missing_minutes_blocks_adoption():
    voting={'eligible_votes':100,'present_votes':80,'votes_for':70,'votes_against':10}
    x=build_formal_resolution_voting_register(pack(),voting)
    assert x['resolution']['adopted'] is False
    assert x['status']=='FORMELE REGISTRATIE ONVOLLEDIG'

def test_quorum_failure_blocks_resolution():
    voting={'eligible_votes':100,'present_votes':40,'quorum_required_pct':50,'votes_for':35,'votes_against':5,'minutes_reference':'ALV-1','decision_authority':'ALV'}
    x=build_formal_resolution_voting_register(pack(),voting)
    assert x['resolution']['quorum_met'] is False
    assert x['status']=='QUORUM NIET GEHAALD'
