"""Enterprise 9.0 Integrated VvE Governance Operating System."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='9.0.0'
WEIGHTS={'financial_health':15,'mjop_health':15,'risk_control':10,'treasury_health':15,'governance_maturity':20,'audit_assurance':10,'decision_execution':10,'improvement_progress':5}

def _score(v:Any,default:float=0)->float:
 try:return max(0.0,min(100.0,float(v if v is not None else default)))
 except (TypeError,ValueError):return default

def build_vve_governance_os(report:dict[str,Any])->dict[str,Any]:
 fin=report.get('financial_cockpit',report.get('finance',{})) or {}; mjop=report.get('mjop_engine',report.get('mjop',{})) or {}; risk=report.get('risk_engine',report.get('risk',{})) or {}; treasury=report.get('portfolio_treasury_control_tower',{}) or {}; maturity=report.get('governance_maturity_index',{}) or {}; assurance=report.get('treasury_audit_assurance',{}) or {}; accountability=report.get('treasury_accountability_register',{}) or {}; roadmap=report.get('governance_improvement_roadmap',{}) or {}
 domains={
 'financial_health':_score(fin.get('financial_health_score',fin.get('score',75)),75),
 'mjop_health':_score(mjop.get('score',75),75),
 'risk_control':100-_score(risk.get('risk_score',25),25),
 'treasury_health':_score(treasury.get('treasury_score',0)),
 'governance_maturity':_score(maturity.get('maturity_index',0)),
 'audit_assurance':_score(assurance.get('overall_assurance_score',0)),
 'decision_execution':_score(accountability.get('accountability_score',accountability.get('score',0))),
 'improvement_progress':_score(roadmap.get('overall_progress',0)),
 }
 overall=round(sum(domains[k]*WEIGHTS[k]/100 for k in WEIGHTS),1)
 critical=[]
 if domains['treasury_health']<50: critical.append('TREASURY')
 if domains['audit_assurance']<50: critical.append('AUDIT')
 if domains['risk_control']<50: critical.append('RISICO')
 if domains['financial_health']<50: critical.append('FINANCE')
 status='GROEN' if overall>=85 and not critical else ('ORANJE' if overall>=65 and len(critical)<=1 else 'ROOD')
 weakest=sorted(domains.items(),key=lambda x:x[1])[:3]
 return {'vve_governance_os_version':ENGINE_VERSION,'overall_vve_health_governance_score':overall,'status':status,'domain_scores':domains,'weights':WEIGHTS,'critical_domains':critical,'top_improvement_priorities':[{'domain':k,'score':v} for k,v in weakest],'maturity_level':maturity.get('maturity_level','ONBEKEND'),'treasury_status':treasury.get('status','ONBEKEND'),'human_governance_preserved':True,'automatic_decision_execution':False,'next_action':'Borg prestaties en blijf continu monitoren.' if status=='GROEN' else 'Behandel eerst de laagst scorende en kritieke domeinen in Bestuur/ALV.'}
