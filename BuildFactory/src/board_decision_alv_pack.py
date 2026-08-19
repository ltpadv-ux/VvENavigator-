"""Enterprise 11.1 Board Decision Narrative & ALV Decision Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='11.1.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(*parts:Any)->str:
    return 'ALVPK-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_board_decision_alv_pack(explainable:dict[str,Any], confidence:dict[str,Any], command_center:dict[str,Any]|None=None, simulator:dict[str,Any]|None=None, context:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; command_center=command_center or {}; simulator=simulator or {}
    best=explainable.get('best_explanation',{}) or {}
    if explainable.get('status')!='UITLEG BESCHIKBAAR' or not best:
        return {'board_decision_alv_pack_version':ENGINE_VERSION,'status':'GEEN BESLUITSTUK BESCHIKBAAR','pack':{},'automatic_decision':False}
    pack_id=_id(best.get('intervention',''),best.get('confidence_score',0),context.get('meeting_date',''))
    selected=(confidence.get('best_recommendation',{}) or {})
    scenarios=simulator.get('scenarios',[]) or []
    financial_impact=selected.get('estimated_cost',simulator.get('recommended_scenario',{}).get('estimated_cost'))
    decision_points=[
        'Stem in met de voorgestelde interventie of motiveer een afwijkende keuze.',
        'Stel het maximale budget en de financieringsbron vast.',
        'Benoem eigenaar, deadline en verantwoordingsmoment.',
        'Bevestig KPI-doelen voor Health, Risk en eventuele vermeden herstelkosten.',
        'Leg vast welke onzekerheden expliciet zijn meegewogen.'
    ]
    pack={
      'pack_id':pack_id,
      'title':context.get('title','Bestuurs-/ALV-besluitstuk preventieve interventie'),
      'meeting_type':context.get('meeting_type','Bestuur/ALV'),
      'meeting_date':context.get('meeting_date',''),
      'decision_readiness':explainable.get('decision_readiness',confidence.get('decision_readiness','ONBEKEND')),
      'proposal':f"Voorgesteld wordt om '{best.get('intervention','interventie')}' bestuurlijk te beoordelen en, bij akkoord, als preventieve maatregel te mandateren.",
      'why_now':best.get('trigger_context',{}),
      'why_this_option':best.get('why_recommended',''),
      'financial_impact':financial_impact,
      'expected_effect':{'health_uplift':_num(selected.get('avg_health_uplift')),'risk_reduction':_num(selected.get('avg_risk_reduction')),'value_per_euro':_num(selected.get('avg_value_per_euro'))},
      'confidence':{'score':_num(best.get('confidence_score')),'readiness':best.get('decision_readiness'),'evidence_strength':selected.get('evidence_strength','')},
      'alternatives':best.get('alternatives_considered',[]),
      'uncertainties':best.get('uncertainties',[]),
      'board_tradeoffs':best.get('board_tradeoffs',[]),
      'decision_points':decision_points,
      'scenarios':scenarios,
      'audit_trail':{'traceability':explainable.get('traceability',{}),'command_center_version':command_center.get('executive_command_center_version',''),'source_board_status':command_center.get('board_status','ONBEKEND')},
      'human_decision_required':True,
      'decision_status':'BESLUIT VEREIST'
    }
    narrative=[
      f"Aanleiding: {pack['why_now']}",
      f"Voorgestelde interventie: {best.get('intervention','')}",
      f"Onderbouwing: {best.get('why_recommended','')}",
      f"Confidence: {pack['confidence']['score']:.1f} ({pack['confidence']['readiness']}).",
      f"Financiële impact: {financial_impact if financial_impact is not None else 'nader vast te stellen'}.",
      'Besluitvorming blijft voorbehouden aan Bestuur/ALV.'
    ]
    return {'board_decision_alv_pack_version':ENGINE_VERSION,'status':'BESLUITSTUK GEREED','pack':pack,'narrative':'\n'.join(narrative),'human_approval_required':True,'automatic_decision':False,'automatic_execution':False,'next_action':'Agendeer het besluitstuk en leg besluit, motivering, budget en eigenaar formeel vast.'}
