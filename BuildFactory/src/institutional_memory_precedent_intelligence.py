"""Enterprise 11.6 Institutional Memory Retrieval & Precedent Intelligence.

Finds relevant historical governance dossiers and summarizes precedent, costs,
outcomes and lessons for a new board question. Advisory only; precedents do not
replace current legal/governance review.
"""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='11.6.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _tokens(v:Any)->set[str]:
    if isinstance(v,list): v=' '.join(str(x) for x in v)
    text=''.join(ch.lower() if ch.isalnum() else ' ' for ch in str(v or ''))
    return {x for x in text.split() if len(x)>2}

def retrieve_precedents(archive:dict[str,Any], question:dict[str,Any]|str, top_n:int=5)->dict[str,Any]:
    entries=archive.get('entries',[]) or []
    if isinstance(question,str): context={'question':question}
    else: context=question or {}
    query_text=' '.join(str(context.get(k,'')) for k in ('question','topic','domain','risk_type','intervention','keywords'))
    qtokens=_tokens(query_text)
    if not entries or not qtokens:
        return {'institutional_memory_precedent_intelligence_version':ENGINE_VERSION,'status':'ONVOLDOENDE GEHEUGEN OF VRAAGCONTEXT','precedents':[],'human_judgment_required':True,'automatic_decision':False}
    ranked=[]
    for e in entries:
        fields=' '.join(str(e.get(k,'')) for k in ('title','decision_text','decision_rationale','delivery_note','final_result','future_recommendation'))
        etokens=_tokens(fields)|_tokens(e.get('lessons_learned',[]))|_tokens(e.get('what_worked',[]))|_tokens(e.get('what_to_improve',[]))
        overlap=len(qtokens & etokens); union=max(1,len(qtokens | etokens)); lexical=overlap/union
        domain_bonus=0.0
        if context.get('domain') and str(context.get('domain')).lower() in fields.lower(): domain_bonus+=0.15
        if context.get('risk_type') and str(context.get('risk_type')).lower() in fields.lower(): domain_bonus+=0.15
        if context.get('intervention') and str(context.get('intervention')).lower() in fields.lower(): domain_bonus+=0.10
        similarity=min(1.0,lexical*2.2+domain_bonus)
        if similarity<=0: continue
        fin=e.get('financial_result',{}) or {}; planned=_num(fin.get('planned_budget')); actual=_num(fin.get('actual_spend'))
        outcome_quality=100.0
        if planned>0 and actual>planned: outcome_quality=max(0,100-(actual-planned)/planned*100)
        score=round((similarity*0.75+outcome_quality/100*0.15+min(1.0,_num(e.get('evidence_count'))/5.0)*0.10)*100,1)
        ranked.append({'memory_id':e.get('memory_id'),'title':e.get('title'),'meeting_date':e.get('meeting_date'),'similarity_score':round(similarity*100,1),'precedent_score':score,'decision_text':e.get('decision_text'),'decision_rationale':e.get('decision_rationale'),'planned_budget':planned,'actual_spend':actual,'financial_variance':_num(fin.get('variance')),'final_result':e.get('final_result'),'lessons_learned':e.get('lessons_learned',[]),'what_worked':e.get('what_worked',[]),'what_to_improve':e.get('what_to_improve',[]),'future_recommendation':e.get('future_recommendation',''),'evidence_count':int(e.get('evidence_count',0) or 0),'minutes_reference':e.get('minutes_reference','')})
    ranked.sort(key=lambda x:(x['precedent_score'],x['similarity_score'],x['evidence_count']),reverse=True)
    selected=ranked[:max(1,top_n)]
    if not selected:
        status='GEEN VERGELIJKBAAR PRECEDENT'
    else: status='PRECEDENT INTELLIGENCE BESCHIKBAAR'
    best=selected[0] if selected else {}
    summary={
      'question':context.get('question',''),
      'best_precedent':best.get('title',''),
      'what_was_decided':best.get('decision_text',''),
      'what_it_cost':best.get('actual_spend',0),
      'what_it_delivered':best.get('final_result',''),
      'key_lessons':best.get('lessons_learned',[]),
      'board_guidance':best.get('future_recommendation','')
    } if best else {}
    return {'institutional_memory_precedent_intelligence_version':ENGINE_VERSION,'status':status,'query_context':context,'precedent_count':len(selected),'precedents':selected,'best_precedent':best,'precedent_summary':summary,'human_judgment_required':True,'human_legal_governance_review_required':True,'automatic_decision':False,'automatic_policy_change':False,'next_action':'Gebruik precedenten als context, maar toets opnieuw aan actuele feiten, bevoegdheden en VvE-regels.' if selected else 'Behandel het vraagstuk zonder precedent en voeg de uitkomst later toe aan het institutionele geheugen.'}
