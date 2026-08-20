"""Enterprise 14.9 Financial Close Variance Intelligence & Forecast Feedback."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.9.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVFBK-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def build_forecast_feedback(close:dict[str,Any], baseline:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; material_pct=_n(rules.get('material_variance_pct',5)); actual=_n(close.get('spent_ledger_eur')); budget=_n(baseline.get('period_budget_eur')); cash=_n(baseline.get('cash_balance_eur')); reserve=_n(baseline.get('reserve_balance_eur')); mjop=_n(baseline.get('mjop_remaining_eur')); contribution=_n(baseline.get('monthly_contribution_total_eur')); variance=actual-budget; pct=round(variance/budget*100,2) if budget else 0.0; accrual=_n(close.get('accrual_eur')); payable=_n(close.get('accounts_payable_eur')); cash_delta=-(variance+accrual+payable); projected_cash=round(cash+cash_delta,2); projected_reserve=round(reserve+min(0,cash_delta),2); projected_mjop=round(mjop-variance,2); material=abs(pct)>=material_pct; contribution_pressure=max(0.0,-projected_cash); suggested_monthly_uplift=round(contribution_pressure/12,2) if contribution_pressure else 0.0
 signals=[]
 if material:signals.append('Materiële budgetafwijking terugvoeren naar forecast.')
 if accrual>0:signals.append('Open commitments/accruals opnemen in liquiditeitsforecast.')
 if payable>0:signals.append('Crediteurenpositie opnemen in korte-termijn cash forecast.')
 if projected_cash<0:signals.append('Liquiditeitsdruk vereist herijking bijdrage- of financieringspad.')
 status='FORECAST HERIJKING VEREIST' if material or projected_cash<0 else ('FORECAST UPDATE AANBEVOLEN' if signals else 'FORECAST OP KOERS')
 return {'financial_close_variance_forecast_feedback_version':ENGINE_VERSION,'feedback_id':_id(close.get('close_id',''),baseline.get('forecast_id',''),actual,budget),'status':status,'actual_spend_eur':round(actual,2),'baseline_budget_eur':round(budget,2),'variance_eur':round(variance,2),'variance_pct':pct,'material_variance':material,'forecast_feedback':{'projected_cash_balance_eur':projected_cash,'projected_reserve_balance_eur':projected_reserve,'projected_mjop_remaining_eur':projected_mjop,'monthly_contribution_total_eur':round(contribution,2),'suggested_monthly_contribution_uplift_total_eur':suggested_monthly_uplift,'accrual_eur':round(accrual,2),'accounts_payable_eur':round(payable,2)},'signals':signals,'update_targets':['MJOP forecast','Liquidity forecast','Reserve forecast','Contribution planning'],'human_forecast_approval_required':True,'automatic_budget_change':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_forecast_writeback':False,'next_action':'Laat financieel verantwoordelijke de forecast-feedback beoordelen en geaccordeerde wijzigingen verwerken.'}
