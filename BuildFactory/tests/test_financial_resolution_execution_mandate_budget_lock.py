from src.financial_resolution_execution_mandate_budget_lock import create_execution_mandate, validate_commitment
V={'validation_id':'V1','validated_for_formal_registration':True}
P={'resolution_pack_id':'R1','preferred_path':{'scenario_name':'GEBALANCEERD','term_months':36,'maximum_monthly_extra_eur':25,'reserve_draw_eur':5000,'cost_eur':20000}}
def test_mandate_ready():
 e={'approved_budget_eur':20000,'responsible_owner':'Bestuur','formal_resolution_reference':'ALV-2026-14','term_months':36}; x=create_execution_mandate(V,P,e); assert x['budget_lock_active'] is True and x['maximum_commitment_eur']==20000
def test_unvalidated_blocks():
 x=create_execution_mandate({'validated_for_formal_registration':False},P,{'approved_budget_eur':20000,'responsible_owner':'Bestuur','formal_resolution_reference':'ALV-X','term_months':36}); assert x['budget_lock_active'] is False
def test_commitment_outside_lock_is_blocked():
 m=create_execution_mandate(V,P,{'approved_budget_eur':10000,'budget_tolerance_pct':5,'responsible_owner':'Bestuur','formal_resolution_reference':'ALV-X','term_months':36}); x=validate_commitment(m,6000,5000); assert x['allowed_within_budget_lock'] is False and x['status']=='GEBLOKKEERD BUITEN MANDAAT'
