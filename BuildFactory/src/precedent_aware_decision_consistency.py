"""Enterprise 11.7 Precedent-Aware Board Recommendation & Decision Consistency Control."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='11.7.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def evaluate_precedent_consistency(current:dict[str,Any], precedents:dict[str,Any], context:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; rec=current.get('best_recommendation',current.get('recommendation',{})) or {}; hist=precedents.get('precedents',[]) or []
    if not rec or not hist:
        return {'precedent_aware_decision_consistency_version':ENGINE_VERSION,'status':'ONVOLDOENDE ADVIES OF PRECEDENT','comparisons':[],'human_decision_required':True,'automatic_decision':False}
    intervention=str(rec.get('intervention',rec.get('recommended_action',''))).strip().lower()
    comparisons=[]
    for p in hist:
        ptext=' '.join(str(p.get(k,'')) for k in ('decision_text','decision_rationale','future_recommendation')).lower()
        same=bool(intervention and intervention in ptext)
        similarity=_num(p.get('similarity_score'))
        divergence=max(0.0,100.0-similarity)
        if same: divergence=max(0.0,divergence-25)
        comparisons.append({'memory_id':p.get('memory_id'),'title':p.get('title'),'precedent_score':_num(p.get('precedent_score')),'similarity_score':similarity,'same_course':same,'divergence_score':round(divergence,1),'prior_decision':p.get('decision_text'),'prior_result':p.get('final_result'),'prior_lessons':p.get('lessons_learned',[])})
    comparisons.sort(key=lambda x:(x['precedent_score'],x['similarity_score']),reverse=True)
    best=comparisons[0]
    threshold=_num(context.get('material_divergence_threshold',45),45)
    material=best['divergence_score']>=threshold or (not best['same_course'] and best['similarity_score']>=70)
    rationale=str(context.get('board_rationale','')).strip()
    rationale_required=material
    rationale_complete=bool(rationale) if rationale_required else True
    status='CONSISTENT MET PRECEDENT' if best['same_course'] and not material else ('BEWUSTE AFWIJKING - MOTIVERING VASTGELEGD' if material and rationale_complete else ('MATERIELE AFWIJKING - MOTIVERING VEREIST' if material else 'AFWIJKING BINNEN BANDWIDTH'))
    return {'precedent_aware_decision_consistency_version':ENGINE_VERSION,'status':status,'current_intervention':rec.get('intervention',rec.get('recommended_action','')),'best_precedent':best,'comparisons':comparisons[:5],'material_divergence':material,'divergence_threshold':threshold,'board_rationale_required':rationale_required,'board_rationale':rationale,'board_rationale_complete':rationale_complete,'consistency_control_passed':not material or rationale_complete,'human_decision_required':True,'human_legal_governance_review_required':True,'automatic_decision':False,'automatic_policy_change':False,'next_action':'Leg expliciet vast waarom het bestuur van vergelijkbaar precedent afwijkt.' if material and not rationale_complete else 'Neem precedentvergelijking en motivering op in het bestuurs-/ALV-dossier.'}
