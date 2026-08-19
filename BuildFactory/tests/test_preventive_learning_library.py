from src.preventive_learning_library import update_preventive_learning_library

def sample():
 e={'status':'PREVENTIEF EFFECT BEWEZEN','effectiveness_score':100,'verification':{'actual_spend':9000,'verified_avoided_recovery_cost':25000,'health_uplift_vs_baseline':4,'risk_reduction_vs_baseline':6}}
 m={'mandate':{'mandate_id':'PEAM-1','scenario':'VROEG INGRIJPEN','evidence':['bewijs']}}
 return e,m

def test_adds_learning_case():
 e,m=sample(); x=update_preventive_learning_library(e,m,{'vve_profile':'34-app','risk_type':'treasury'}); assert x['entry_count']==1; assert x['best_known_intervention']['risk_type']=='treasury'

def test_duplicate_case_not_added_twice():
 e,m=sample(); first=update_preventive_learning_library(e,m,{'vve_profile':'34-app','risk_type':'treasury'}); second=update_preventive_learning_library(e,m,{'vve_profile':'34-app','risk_type':'treasury'},first); assert second['entry_count']==1

def test_more_cases_strengthen_evidence():
 e,m=sample(); lib={}
 for i in range(3):
  m2={'mandate':{**m['mandate'],'mandate_id':f'PEAM-{i}','evidence':['bewijs']}}
  lib=update_preventive_learning_library(e,m2,{'vve_profile':'34-app','risk_type':'treasury'},lib)
 assert lib['best_known_intervention']['evidence_strength']=='REDELIJK'
