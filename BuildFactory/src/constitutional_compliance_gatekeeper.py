"""Enterprise 12.1 Constitutional Compliance & Decision Gatekeeper."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.1.0'

def _id(*parts:Any)->str:return 'GOVGATE-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def evaluate_decision_gate(proposal:dict[str,Any], constitution:dict[str,Any])->dict[str,Any]:
 checks=[]; blockers=[]; reviews=[]
 approved=bool(constitution.get('approved',False) or str(constitution.get('status','')).upper() in {'VASTGESTELD','GOEDGEKEURD','APPROVED'})
 if not approved: blockers.append('Governance Constitution is nog niet formeel vastgesteld.')
 authority=constitution.get('authority_matrix',{}); organ=str(proposal.get('decision_authority',''))
 if not organ or organ not in authority: blockers.append('Beslissingsbevoegdheid past niet aantoonbaar binnen de Authority Matrix.')
 amount=_num(proposal.get('financial_commitment_eur')); approved_budget=_num(proposal.get('approved_budget_eur'))
 if amount>approved_budget and amount>0: blockers.append('Financiële verplichting overschrijdt het goedgekeurde budget.')
 risk=str(proposal.get('risk_level','')).upper()
 if risk in {'ROOD','KRITIEK'} and not proposal.get('explicit_risk_decision',False): reviews.append('Expliciet risicobesluit vereist voor ROOD/KRITIEK.')
 if proposal.get('mjop_deviation',False) and not str(proposal.get('mjop_deviation_rationale','')).strip(): reviews.append('MJOP-afwijking vereist expliciete motivering.')
 if not proposal.get('audit_trail_complete',False): reviews.append('Audittrail is nog niet compleet.')
 if not proposal.get('explainability_complete',False): reviews.append('Explainability is nog niet compleet.')
 doctrine_conflict=bool(proposal.get('doctrine_conflict',False))
 if doctrine_conflict and not str(proposal.get('doctrine_deviation_rationale','')).strip(): blockers.append('Afwijking van vastgestelde doctrine is niet gemotiveerd.')
 gate='BLOCK' if blockers else ('REVIEW' if reviews else 'GO')
 checks=[{'control':'Constitution Approved','pass':approved},{'control':'Authority','pass':not any('Authority Matrix' in x for x in blockers)},{'control':'Financial Limit','pass':not any('budget' in x for x in blockers)},{'control':'Risk Rule','pass':not any('risicobesluit' in x for x in reviews)},{'control':'MJOP Rule','pass':not any('MJOP' in x for x in reviews)},{'control':'Decision Traceability','pass':proposal.get('audit_trail_complete',False) and proposal.get('explainability_complete',False)},{'control':'Doctrine Consistency','pass':not doctrine_conflict or bool(str(proposal.get('doctrine_deviation_rationale','')).strip())}]
 score=round(sum(1 for x in checks if x['pass'])/len(checks)*100,1)
 return {'constitutional_compliance_gatekeeper_version':ENGINE_VERSION,'gate_id':_id(proposal.get('proposal_id',''),constitution.get('constitution_id','')),'gate':gate,'compliance_score':score,'checks':checks,'blockers':blockers,'review_items':reviews,'human_decision_required':True,'human_legal_governance_review_required':gate!='GO','automatic_approval':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Voorstel kan bestuurlijk worden behandeld.' if gate=='GO' else ('Los blokkerende constitutionele afwijkingen op.' if gate=='BLOCK' else 'Laat reviewpunten expliciet beoordelen vóór besluitvorming.')}
