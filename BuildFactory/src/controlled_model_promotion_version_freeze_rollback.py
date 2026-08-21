"""Enterprise 16.4 Controlled Model Promotion, Version Freeze & Rollback Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.4.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVPRM-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def promote_model(champion:dict[str,Any], challenger:dict[str,Any], shadow:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; blockers=[]
 if not shadow.get('promotion_review_ready',False): blockers.append('Shadow run is niet promotiegereed.')
 if not approvals.get('model_owner_approved',False): blockers.append('Model-owner approval ontbreekt.')
 if not approvals.get('board_approved',False): blockers.append('Bestuursgoedkeuring ontbreekt.')
 if not approvals.get('final_monte_carlo_passed',False): blockers.append('Finale Monte Carlo-validatie is niet geslaagd.')
 champion_id=str(champion.get('model_id','CHAMPION')); challenger_id=str(challenger.get('model_id','CHALLENGER')); promotion_date=str(approvals.get('promotion_date','')).strip()
 if not promotion_date: blockers.append('Promotiedatum ontbreekt.')
 rollback_threshold=_n(rules.get('rollback_reliability_drop_points',5)); max_live_mape=_n(rules.get('rollback_max_live_mape_pct',25)); promoted=not blockers
 archive={'model_id':champion_id,'version':champion.get('version'),'frozen':True,'immutable':True,'role':'FORMER_CHAMPION','rollback_eligible':True} if promoted else None
 new_champion={'model_id':challenger_id,'version':challenger.get('version'),'role':'CHAMPION','active':False,'requires_manual_activation':True,'promotion_date':promotion_date,'source_shadow_run_id':shadow.get('shadow_run_id')} if promoted else None
 rollback={'enabled':promoted,'rollback_model_id':champion_id if promoted else None,'trigger_reliability_drop_points':rollback_threshold,'trigger_live_mape_pct':max_live_mape,'requires_human_confirmation':True,'automatic_rollback':False}
 return {'controlled_model_promotion_version_freeze_rollback_version':ENGINE_VERSION,'promotion_id':_id(champion_id,challenger_id,promotion_date),'status':'MODEL PROMOTIE GEREED VOOR HANDMATIGE ACTIVATIE' if promoted else 'MODEL PROMOTIE GEBLOKKEERD','blockers':blockers,'former_champion_archive':archive,'new_champion':new_champion,'rollback_policy':rollback,'promotion_authorized':promoted,'human_manual_activation_required':True,'human_model_owner_approval_required':True,'human_board_approval_required':True,'automatic_model_promotion':False,'automatic_champion_activation':False,'automatic_rollback':False,'automatic_baseline_change':False,'automatic_risk_appetite_change':False,'next_action':'Activeer de nieuwe Champion handmatig en monitor live reliability/MAPE tegen rollbackdrempels.' if promoted else 'Los promotieblokkades op en herhaal de promotievalidatie.'}
def evaluate_rollback(promotion:dict[str,Any], live_metrics:dict[str,Any])->dict[str,Any]:
 policy=promotion.get('rollback_policy') or {}; new=promotion.get('new_champion') or {}; former=promotion.get('former_champion_archive') or {}
 drop=_n(live_metrics.get('reliability_drop_points')); mape=_n(live_metrics.get('live_mape_pct')); rel_trigger=_n(policy.get('trigger_reliability_drop_points',5)); mape_trigger=_n(policy.get('trigger_live_mape_pct',25)); reasons=[]
 if drop>=rel_trigger: reasons.append('Reliability is boven de rollbackdrempel verslechterd.')
 if mape>=mape_trigger: reasons.append('Live MAPE ligt boven de rollbackdrempel.')
 triggered=bool(reasons) and bool(policy.get('enabled',False))
 return {'status':'ROLLBACK REVIEW VEREIST' if triggered else 'GEEN ROLLBACKTRIGGER','current_champion_model_id':new.get('model_id'),'rollback_model_id':former.get('model_id'),'reasons':reasons,'rollback_recommended':triggered,'human_rollback_confirmation_required':True,'automatic_rollback':False}
