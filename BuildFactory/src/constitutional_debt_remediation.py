"""Enterprise 12.4 Constitutional Debt Remediation & Policy Normalization."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='12.4.0'

def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_constitutional_debt_remediation(debt:dict[str,Any], constitution:dict[str,Any]|None=None, doctrine:dict[str,Any]|None=None)->dict[str,Any]:
 constitution=constitution or {}; doctrine=doctrine or {}
 level=str(debt.get('constitutional_debt_level','GROEN')).upper(); score=_num(debt.get('constitutional_debt_score'))
 actions=[]
 if level not in {'ORANJE','ROOD'}:
  return {'constitutional_debt_remediation_version':ENGINE_VERSION,'status':'GEEN FORMELE REMEDIATION NODIG','debt_score':score,'debt_level':level,'actions':[],'human_approval_required':True,'automatic_policy_change':False}
 for x in debt.get('stale_waivers',[]) or []:
  actions.append({'priority':'HOOG','type':'WAIVER_TERMINATE_OR_REVIEW','scope':x.get('scope'),'waiver_id':x.get('waiver_id'),'recommended_action':'Beëindig, herbeoordeel of vervang de langdurige waiver door structureel beleid.','financial_impact_eur':_num(x.get('financial_impact_eur'))})
 for x in debt.get('repeated_exception_patterns',[]) or []:
  actions.append({'priority':'HOOG','type':'NORMALIZE_REPEATED_EXCEPTION','scope':x.get('scope'),'recommended_action':'Onderzoek of terugkerende uitzondering moet worden genormaliseerd in doctrine of Constitution.','financial_impact_eur':_num(x.get('financial_impact_eur'))})
 if debt.get('expired_waivers',0):
  actions.append({'priority':'KRITIEK','type':'CLOSE_EXPIRED_WAIVERS','scope':'register','recommended_action':'Sluit verlopen waivers of formaliseer een nieuw besluit vóór verdere toepassing.','financial_impact_eur':0.0})
 if debt.get('review_due_waivers',0):
  actions.append({'priority':'HOOG','type':'COMPLETE_OVERDUE_REVIEWS','scope':'register','recommended_action':'Rond achterstallige waiver-reviews af en leg risicoacceptatie opnieuw vast.','financial_impact_eur':0.0})
 if score>=70:
  actions.append({'priority':'KRITIEK','type':'CONSTITUTION_REBASELINE','scope':'constitution','recommended_action':'Start formele herijking van Governance Constitution, financiële grenzen en beslisregels.','financial_impact_eur':_num(debt.get('total_financial_impact_eur'))})
 elif debt.get('repeated_exception_patterns'):
  actions.append({'priority':'HOOG','type':'DOCTRINE_REVIEW','scope':'doctrine','recommended_action':'Herijk relevante doctrines voordat meer tijdelijke uitzonderingen ontstaan.','financial_impact_eur':0.0})
 rank={'KRITIEK':0,'HOOG':1,'NORMAAL':2}; actions.sort(key=lambda x:(rank.get(x['priority'],9),-x.get('financial_impact_eur',0)))
 return {'constitutional_debt_remediation_version':ENGINE_VERSION,'status':'REMEDIATIONPLAN VEREIST','debt_score':score,'debt_level':level,'current_constitution_id':constitution.get('constitution_id',''),'source_baseline_id':doctrine.get('baseline_id',''),'actions':actions,'action_count':len(actions),'human_approval_required':True,'human_legal_governance_review_required':True,'automatic_waiver_termination':False,'automatic_policy_change':False,'automatic_constitution_change':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV de herstelroute per actie kiezen, besluiten en opvolgen.'}
