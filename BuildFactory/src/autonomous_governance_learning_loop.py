"""Enterprise 16.0 Autonomous Governance Learning Loop with human-approved model updates."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.0.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVLRN-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def build_learning_proposal(history:list[dict[str,Any]], current:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; min_obs=int(rules.get('minimum_observations',3)); max_step=_n(rules.get('max_parameter_step_pct',10)); proposals=[]; evidence=[]
 categories=('price_variance_pct','timing_variance_pct','risk_cost_variance_pct','contribution_variance_pct','mjop_variance_pct')
 for key in categories:
  vals=[_n(x.get(key)) for x in history if x.get(key) is not None]
  if len(vals)>=min_obs:
   avg=sum(vals)/len(vals); bounded=max(-max_step,min(max_step,avg)); evidence.append({'metric':key,'observations':len(vals),'average_variance_pct':round(avg,2)})
   if abs(avg)>=_n(rules.get('learning_trigger_pct',3)):
    target={'price_variance_pct':'cost_index_adjustment_pct','timing_variance_pct':'timing_buffer_adjustment_pct','risk_cost_variance_pct':'risk_contingency_adjustment_pct','contribution_variance_pct':'collection_assumption_adjustment_pct','mjop_variance_pct':'mjop_cost_adjustment_pct'}[key]
    proposals.append({'parameter':target,'current_value':_n(current.get(target)),'proposed_delta_pct':round(bounded,2),'reason':f'Historisch gemiddelde {key} = {avg:.2f}%','requires_human_approval':True})
 confidence=min(99.0,round(50+5*len(history),1)); status='LEARNING PROPOSAL READY FOR HUMAN REVIEW' if proposals else ('INSUFFICIENT LEARNING EVIDENCE' if len(history)<min_obs else 'NO MATERIAL MODEL LEARNING REQUIRED')
 return {'autonomous_governance_learning_loop_version':ENGINE_VERSION,'learning_id':_id(len(history),len(proposals),confidence),'status':status,'observations':len(history),'learning_confidence_pct':confidence,'evidence':evidence,'parameter_proposals':proposals,'proposal_count':len(proposals),'update_targets':['Cost assumptions','Timing buffers','Risk contingency','Contribution collection assumptions','MJOP cost assumptions'],'requires_model_validation':bool(proposals),'requires_monte_carlo_recalibration':bool(proposals),'requires_backtest':bool(proposals),'human_model_owner_approval_required':bool(proposals),'human_board_review_required':bool(proposals),'automatic_model_update':False,'automatic_baseline_change':False,'automatic_risk_appetite_change':False,'automatic_contribution_change':False,'automatic_mjop_change':False,'next_action':'Backtest de voorgestelde parameters, herkalibreer Monte Carlo en laat model owner/bestuur wijzigingen expliciet goedkeuren.' if proposals else 'Blijf historische afwijkingen verzamelen voor toekomstige leercycli.'}
