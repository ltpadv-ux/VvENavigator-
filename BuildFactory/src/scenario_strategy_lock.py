"""Persist a human-approved strategic scenario and measure future deviation from its locked baseline."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import hashlib

ENGINE_VERSION="6.3.0"
APPROVED={"GOEDGEKEURD","AKKOORD","APPROVED"}

def _decision_id(scenario:str, created_at:str)->str:
    raw=f"{scenario}|{created_at}".encode()
    return "STR-"+hashlib.sha256(raw).hexdigest()[:10].upper()

def build_strategy_lock(scenario_radar:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); existing=existing or {}
    locked=existing.get('strategy_lock') or {}
    if locked.get('status')=='VERGRENDELD':
        return evaluate_strategy_deviation(scenario_radar, existing)
    preferred=str(scenario_radar.get('preferred_scenario',''))
    candidates={str(x.get('scenario','')):x for x in scenario_radar.get('scenarios',[]) or []}
    selected=str(existing.get('selected_scenario') or preferred)
    decision=str(existing.get('decision','NOG TE BESLUITEN')).upper()
    approved_by=str(existing.get('approved_by','')); rationale=str(existing.get('rationale',''))
    baseline=candidates.get(selected,{})
    ready=bool(selected and baseline)
    if decision in APPROVED and ready and approved_by:
        created=str(existing.get('approved_at') or now)
        lock={"decision_id":existing.get('decision_id') or _decision_id(selected,created),"status":"VERGRENDELD","selected_scenario":selected,"approved_by":approved_by,"approved_at":created,"rationale":rationale,"baseline":{"robustness_score":float(baseline.get('robustness_score',0) or 0),"adjusted_12m_risk":float(baseline.get('adjusted_12m_risk',0) or 0),"adjusted_mandate_budget":float(baseline.get('adjusted_mandate_budget',0) or 0),"reserve_pressure_percent":float(baseline.get('reserve_pressure_percent',0) or 0),"schedule_factor":float(baseline.get('schedule_factor',1) or 1),"assumptions":baseline.get('assumptions',{})},"locked_at":now}
        return {"strategy_lock_version":ENGINE_VERSION,"generated_at":now,"status":"STRATEGIE VERGRENDELD","selected_scenario":selected,"decision":decision,"strategy_lock":lock,"deviation":{"status":"BASISLIJN VASTGELEGD","score":0,"signals":[]},"next_action":"Monitor toekomstige afwijkingen ten opzichte van de vergrendelde strategie."}
    return {"strategy_lock_version":ENGINE_VERSION,"generated_at":now,"status":"BESLUIT VEREIST","selected_scenario":selected,"decision":decision,"approved_by":approved_by,"rationale":rationale,"available_scenarios":list(candidates),"preferred_scenario":preferred,"strategy_lock":{},"deviation":{"status":"NIET BESCHIKBAAR","score":0,"signals":[]},"next_action":"Bestuur/ALV moet het strategische scenario formeel goedkeuren en goedkeurder vastleggen."}

def evaluate_strategy_deviation(scenario_radar:dict[str,Any], state:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); lock=(state.get('strategy_lock') or {}); selected=str(lock.get('selected_scenario','')); baseline=lock.get('baseline',{}) or {}; current=next((x for x in scenario_radar.get('scenarios',[]) or [] if str(x.get('scenario',''))==selected),{})
    signals=[]; score=0
    if current:
        risk_delta=float(current.get('adjusted_12m_risk',0) or 0)-float(baseline.get('adjusted_12m_risk',0) or 0)
        budget_delta=float(current.get('adjusted_mandate_budget',0) or 0)-float(baseline.get('adjusted_mandate_budget',0) or 0)
        pressure_delta=float(current.get('reserve_pressure_percent',0) or 0)-float(baseline.get('reserve_pressure_percent',0) or 0)
        robustness_delta=float(current.get('robustness_score',0) or 0)-float(baseline.get('robustness_score',0) or 0)
        if risk_delta>0: signals.append(f"12m-risico +{risk_delta:.1f}"); score+=min(40,int(risk_delta))
        if budget_delta>0: signals.append(f"mandaatbudget +EUR {budget_delta:.0f}"); score+=10
        if pressure_delta>5: signals.append(f"reservedruk +{pressure_delta:.1f}%-punt"); score+=20
        if robustness_delta<-5: signals.append(f"robuustheid {robustness_delta:.1f} punt"); score+=20
    else:
        signals.append('Gekozen scenario ontbreekt in actuele scenarioanalyse.'); score=100
    score=min(100,score); status='BINNEN STRATEGIE' if score<20 else 'AANDACHT' if score<50 else 'AFWIJKING'
    return {"strategy_lock_version":ENGINE_VERSION,"generated_at":now,"status":"STRATEGIE VERGRENDELD","selected_scenario":selected,"decision":state.get('decision','GOEDGEKEURD'),"strategy_lock":lock,"deviation":{"status":status,"score":score,"signals":signals,"current":current},"next_action":"Reguliere strategische monitoring voortzetten." if status=='BINNEN STRATEGIE' else "Bespreek afwijkingen en bepaal of herijking of nieuw ALV-besluit nodig is."}
