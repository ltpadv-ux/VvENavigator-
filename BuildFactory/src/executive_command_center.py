"""Enterprise 10.0 VvE Navigator Executive Command Center."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='10.0.0'

def _n(v:Any,default:float=0)->float:
    try:return float(v if v is not None else default)
    except (TypeError,ValueError):return default

def build_executive_command_center(report:dict[str,Any])->dict[str,Any]:
    os=report.get('vve_governance_operating_system',{}) or {}; rec=report.get('autonomous_governance_recommendation',{}) or {}; twin=report.get('executive_digital_twin',{}) or {}; fin=report.get('financial_cockpit',report.get('finance',{})) or {}; mjop=report.get('mjop_engine',report.get('mjop',{})) or {}; risk=report.get('risk_engine',report.get('risk',{})) or {}; treasury=report.get('portfolio_treasury_control_tower',{}) or {}; assurance=report.get('treasury_audit_assurance',{}) or {}; maturity=report.get('governance_maturity_index',{}) or {}
    health=_n(os.get('overall_vve_health_governance_score'))
    status=os.get('status','ONBEKEND')
    top_actions=(rec.get('recommendations',[]) or [])[:5]
    summary={'health_governance_score':health,'health_status':status,'financial_health':_n(fin.get('financial_health_score',fin.get('score',0))),'mjop_health':_n(mjop.get('score',0)),'risk_score':_n(risk.get('risk_score',0)),'treasury_score':_n(treasury.get('treasury_score',0)),'audit_assurance':_n(assurance.get('overall_assurance_score',0)),'governance_maturity':_n(maturity.get('maturity_index',0)),'best_36m_scenario':twin.get('best_36m_scenario',''),'best_36m_score':_n(twin.get('best_36m_score',0)),'downside_36m_scenario':twin.get('downside_36m_scenario',''),'downside_36m_score':_n(twin.get('downside_36m_score',0))}
    critical=sum(1 for a in top_actions if str(a.get('priority','')).upper() in {'KRITIEK','ROOD'})
    board_status='DIRECT BESLUIT VEREIST' if critical else ('ACTIE VEREIST' if top_actions else 'OP KOERS')
    return {'executive_command_center_version':ENGINE_VERSION,'board_status':board_status,'executive_summary':summary,'top_board_actions':top_actions,'critical_action_count':critical,'command_center_sections':['VvE Health & Governance','Finance','MJOP','Risk','Treasury','Audit & Assurance','Digital Twin','Board Recommendations'],'single_source_of_truth':True,'human_decision_required':True,'automatic_decision':False,'automatic_execution':False,'next_action':'Behandel kritieke acties eerst en gebruik de cockpit als vaste bestuurlijke startpagina.' if top_actions else 'Blijf monitoren; er zijn geen directe bestuurlijke acties.'}
