"""Enterprise 11.0 Explainable Governance AI & Board Decision Intelligence."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='11.0.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def explain_governance_recommendations(confidence_result:dict[str,Any], recommendation_result:dict[str,Any], trend_radar:dict[str,Any]|None=None, context:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; trend_radar=trend_radar or {}; recs=confidence_result.get('recommendations',[]) or []
    if not recs:
        return {'explainable_governance_ai_version':ENGINE_VERSION,'status':'GEEN UITLEG BESCHIKBAAR','explanations':[],'human_decision_required':True,'automatic_decision':False}
    alerts=trend_radar.get('early_intervention_alerts',[]) or []
    dominant=alerts[0] if alerts else {}
    explanations=[]
    for i,rec in enumerate(recs):
        comps=rec.get('confidence_components',{}) or {}
        drivers=[
            {'driver':'Vergelijkbaarheid','value':_num(rec.get('similarity_score')),'why':'Mate waarin historische cases overeenkomen met VvE-profiel en risicotype.'},
            {'driver':'Effectiviteit','value':_num(rec.get('avg_effectiveness_score')),'why':'Gemiddeld bewezen effect van deze interventie in eerdere cases.'},
            {'driver':'Bewijssterkte','value':str(rec.get('evidence_strength','BEPERKT')),'why':'Sterkte van de historische bewijsbasis.'},
            {'driver':'Datakwaliteit','value':_num(comps.get('data_quality')),'why':'Betrouwbaarheid en volledigheid van de actuele VvE-data.'},
            {'driver':'Modelconsistentie','value':_num(comps.get('model_consistency')),'why':'Consistentie tussen modeluitkomst en de actuele casus.'},
            {'driver':'Scenariozekerheid','value':_num(comps.get('scenario_uncertainty')),'why':'Resterende zekerheid nadat scenario-onzekerheid is verwerkt.'},
        ]
        uncertainties=[]
        if _num(rec.get('case_count'))<3: uncertainties.append('Beperkt aantal vergelijkbare historische cases.')
        if str(rec.get('evidence_strength','')).upper()=='BEPERKT': uncertainties.append('Historische bewijssterkte is beperkt.')
        if _num(rec.get('similarity_score'))<70: uncertainties.append('Casusvergelijkbaarheid is lager dan de besluitrijpheidsgrens.')
        if _num(comps.get('data_quality'))<80: uncertainties.append('Actuele datakwaliteit vraagt aanvullende validatie.')
        if _num(comps.get('scenario_uncertainty'))<70: uncertainties.append('Scenario-onzekerheid is relatief hoog.')
        alternatives=[]
        for alt in recs:
            if alt is rec: continue
            reasons=[]
            if _num(alt.get('confidence_score'))<_num(rec.get('confidence_score')): reasons.append('lagere confidence score')
            if _num(alt.get('ranking_score'))<_num(rec.get('ranking_score')): reasons.append('lagere evidence ranking')
            if _num(alt.get('similarity_score'))<_num(rec.get('similarity_score')): reasons.append('minder vergelijkbaar met huidige VvE')
            alternatives.append({'intervention':alt.get('intervention'),'confidence_score':_num(alt.get('confidence_score')),'ranking_score':_num(alt.get('ranking_score')),'why_not_preferred':', '.join(reasons) or 'Geen doorslaggevend nadeel; bestuurlijke afweging blijft mogelijk.'})
        explanation={
            'rank':i+1,
            'intervention':rec.get('intervention'),
            'confidence_score':_num(rec.get('confidence_score')),
            'decision_readiness':rec.get('decision_readiness'),
            'why_recommended':f"Deze interventie combineert een evidence-ranking van {_num(rec.get('ranking_score')):.1f}, confidence van {_num(rec.get('confidence_score')):.1f} en vergelijkbaarheid van {_num(rec.get('similarity_score')):.1f}.",
            'trigger_context':{'domain':dominant.get('domain',context.get('risk_type','algemeen')),'severity':dominant.get('severity','ONBEKEND'),'trend_break':dominant.get('trend_break',False)},
            'decisive_drivers':drivers,
            'uncertainties':uncertainties,
            'alternatives_considered':alternatives[:4],
            'board_tradeoffs':['Effect versus kosten','Snelheid van ingrijpen versus aanvullend onderzoek','Bewijssterkte versus lokale VvE-context','Risicoreductie versus budgetimpact'],
            'required_board_checks':['Controleer of data actueel en volledig zijn.','Beoordeel of budget en bevoegdheid beschikbaar zijn.','Weeg alternatieven en resterende onzekerheden expliciet.','Leg motivering, besluit en eventuele afwijking van het advies vast.'],
            'human_judgment_required':True,
        }
        explanations.append(explanation)
    return {'explainable_governance_ai_version':ENGINE_VERSION,'status':'UITLEG BESCHIKBAAR','decision_readiness':confidence_result.get('decision_readiness','ONBEKEND'),'explanation_count':len(explanations),'explanations':explanations,'best_explanation':explanations[0] if explanations else {},'traceability':{'recommendation_engine_version':recommendation_result.get('evidence_based_intervention_recommendation_version',''),'confidence_engine_version':confidence_result.get('intervention_confidence_readiness_version',''),'trend_radar_version':trend_radar.get('predictive_trend_break_radar_version','')},'human_decision_required':True,'automatic_decision':False,'automatic_execution':False,'next_action':'Gebruik uitleg, alternatieven en onzekerheden als vaste bijlage bij het Bestuur/ALV-besluit.'}
