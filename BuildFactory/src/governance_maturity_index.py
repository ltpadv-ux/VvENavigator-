"""Continuous Assurance & Governance Maturity Index for VvE Navigator."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='8.8.0'
WEIGHTS={'governance':20,'finance':15,'mjop':15,'treasury':20,'audit':20,'decision_execution':10}

def _clamp(v:Any)->float:
 try:return max(0.0,min(100.0,float(v or 0)))
 except (TypeError,ValueError):return 0.0

def build_governance_maturity_index(report:dict[str,Any])->dict[str,Any]:
 assurance=report.get('treasury_audit_assurance',{}) or {}; remediation=report.get('audit_remediation',{}) or {}; tower=report.get('portfolio_treasury_control_tower',{}) or {}; closed=report.get('closed_loop_management',{}) or {}; accountability=report.get('treasury_accountability_register',{}) or {}; risk=report.get('risk',report.get('risk_engine',{})) or {}; mjop=report.get('mjop',report.get('mjop_engine',{})) or {}; finance=report.get('finance',report.get('financial_cockpit',{})) or {}
 scores={
  'governance':_clamp(closed.get('loop_completeness_score',closed.get('score',0))),
  'finance':_clamp(finance.get('score',finance.get('financial_health_score',75))),
  'mjop':_clamp(mjop.get('score',100-_clamp(risk.get('risk_score',25)))),
  'treasury':_clamp(tower.get('treasury_score',0)),
  'audit':_clamp(assurance.get('overall_assurance_score',0)),
  'decision_execution':_clamp(accountability.get('accountability_score',accountability.get('score',0))),
 }
 index=round(sum(scores[k]*WEIGHTS[k]/100 for k in WEIGHTS),1)
 open_rem=int(remediation.get('open_count',0) or 0); index=max(0,round(index-min(10,open_rem*2),1))
 level='LEIDEND' if index>=90 else ('BEHEERST' if index>=80 else ('ONTWIKKELD' if index>=65 else ('BASIS' if index>=50 else 'KWETSBAAR')))
 weakest=sorted(scores.items(),key=lambda x:x[1])[:3]
 return {'governance_maturity_version':ENGINE_VERSION,'maturity_index':index,'maturity_level':level,'domain_scores':scores,'weights':WEIGHTS,'open_remediation_actions':open_rem,'weakest_domains':[{'domain':k,'score':v} for k,v in weakest],'target_index':90,'continuous_assurance':True,'human_governance_preserved':True,'next_action':'Borg het niveau en blijf continu monitoren.' if index>=90 else 'Verbeter eerst de zwakste domeinen en sluit open audit-remediations.'}
