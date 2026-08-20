"""Enterprise 15.9 Baseline Breach Diagnosis & Corrective Action Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.9.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVBRC-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def diagnose_baseline_breach(monitoring:dict[str,Any], actuals:dict[str,Any], baseline:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; material=_n(rules.get('material_variance_pct',5)); causes=[]; actions=[]
 def add(code,label,severity,evidence,action): causes.append({'code':code,'cause':label,'severity':severity,'evidence':evidence}); actions.append({'cause_code':code,'recommended_action':action,'human_approval_required':True})
 reserve_a=_n(actuals.get('reserve_eur')); reserve_b=_n(baseline.get('reserve_eur')); cash_a=_n(actuals.get('cash_eur')); cash_b=_n(baseline.get('cash_eur')); contrib_a=_n(actuals.get('annual_contribution_eur')); contrib_b=_n(baseline.get('annual_contribution_eur')); mjop_a=_n(actuals.get('mjop_spend_eur')); mjop_b=_n(baseline.get('mjop_spend_eur'))
 price=_n(actuals.get('price_variance_eur')); timing=_n(actuals.get('timing_variance_eur')); scope=_n(actuals.get('scope_variance_eur')); risk=_n(actuals.get('unexpected_risk_cost_eur'))
 if price>0:add('PRICE','Prijs/kosten hoger dan baseline','HOOG' if price>max(1,mjop_b)*material/100 else 'MATIG',price,'Herijk prijsindex, aanbesteding en resterende contractramingen.')
 if timing!=0:add('TIMING','Timing van uitgaven wijkt af', 'MATIG',timing,'Herfaseer cashflow en MJOP-planning zonder technische of wettelijke verplichtingen uit te stellen.')
 if scope>0:add('SCOPE','Scope/meerwerk boven goedgekeurde baseline','HOOG',scope,'Bevries niet-goedgekeurd meerwerk en leg scopewijziging bestuurlijk voor.')
 if risk>0:add('RISK','Onvoorziene risico- of schadekosten','HOOG',risk,'Actualiseer risico-register, contingency en Monte Carlo-aannames.')
 if contrib_b and contrib_a<contrib_b*(1-material/100):add('CONTRIBUTION','Bijdrage-inkomsten onder baseline','HOOG',round(contrib_b-contrib_a,2),'Analyseer achterstanden/inning en herijk bijdrage- en liquiditeitsforecast.')
 if cash_a<cash_b*(1-material/100):add('CASHFLOW','Liquiditeit onder baseline','HOOG',round(cash_b-cash_a,2),'Maak 12-maands liquiditeitsherforecast en toets financierings-/bijdragepad.')
 if reserve_a<reserve_b*(1-material/100):add('RESERVE','Reserve onder baseline','HOOG',round(reserve_b-reserve_a,2),'Herijk reserve-opbouw en toets opnieuw aan risk appetite en MJOP-buffer.')
 if mjop_b and mjop_a>mjop_b*(1+material/100):add('MJOP','MJOP-uitgaven boven baseline','HOOG',round(mjop_a-mjop_b,2),'Voer technische oorzaak- en kostenanalyse uit en actualiseer MJOP-forecast.')
 breach=bool(monitoring.get('baseline_breach',False) or causes); critical=any(c['severity']=='HOOG' for c in causes); status='BREACH DIAGNOSE - CORRECTIEF BESTUURSBESLUIT VEREIST' if critical else ('BREACH DIAGNOSE - HERFORECAST VEREIST' if breach else 'GEEN MATERIELE BASELINE BREACH')
 return {'baseline_breach_diagnosis_corrective_action_version':ENGINE_VERSION,'diagnosis_id':_id(monitoring.get('monitoring_id',''),baseline.get('baseline_id',''),len(causes)),'status':status,'baseline_breach_confirmed':breach,'root_causes':causes,'corrective_actions':actions,'cause_codes':[c['code'] for c in causes],'requires_reforecast':breach,'requires_board_review':critical,'requires_new_formal_resolution':any(c['code']=='SCOPE' for c in causes),'rerun_monte_carlo_after_approved_correction':breach,'human_financial_review_required':breach,'human_board_approval_required':critical,'automatic_corrective_action':False,'automatic_baseline_change':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'next_action':'Beoordeel oorzaken en correctieve acties, herforecast de Digital Twin en voer daarna opnieuw Monte Carlo/Risk Appetite-controle uit.' if breach else 'Blijf actuals monitoren tegen de bevroren baseline.'}
