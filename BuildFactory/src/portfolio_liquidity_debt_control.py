"""Portfolio liquidity, debt-service, interest sensitivity and refinancing control."""
from __future__ import annotations
from typing import Any

ENGINE_VERSION='7.5.0'
DEFAULT_POLICY={'minimum_dscr':1.25,'warning_dscr':1.40,'minimum_liquidity_months':6.0,'refinancing_warning_months':24,'interest_stress_addition':0.02,'loan_years':15}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _annuity(principal:float, annual_rate:float, years:int)->float:
    if principal<=0:return 0.0
    n=max(1,int(years)*12); r=max(0.0,annual_rate)/12
    if r==0:return principal/n
    return principal*r/(1-(1+r)**(-n))

def build_portfolio_liquidity_control(funding_control:dict[str,Any], actuals:dict[str,Any]|None=None, policy:dict[str,Any]|None=None)->dict[str,Any]:
    actuals=actuals or {}; rules={**DEFAULT_POLICY,**(policy or {})}; rows=[]
    for d in funding_control.get('decisions',[]) or []:
        if not d.get('approved'): continue
        name=str(d.get('vve','')); mix=d.get('funding_mix',{}) or {}; data=actuals.get(name,{}) or {}
        loan=max(0,_n(mix.get('loan_amount'))); rate=next((_n(c.get('actual')) for c in d.get('covenants',[]) or [] if c.get('covenant')=='RENTE'),0.0); years=max(1,int(_n(data.get('loan_years',rules['loan_years'])) or rules['loan_years']))
        annual_debt_service=round(_annuity(loan,rate,years)*12,2); stressed_rate=rate+_n(rules['interest_stress_addition']); stressed_debt_service=round(_annuity(loan,stressed_rate,years)*12,2)
        inflow=_n(data.get('annual_cash_inflow')); operating=_n(data.get('annual_operating_outflow')); cash_for_debt=_n(data.get('cash_available_for_debt_service',max(0,inflow-operating))); liquid_reserve=_n(data.get('liquid_reserve')); monthly_operating=operating/12 if operating>0 else 0; liquidity_months=liquid_reserve/monthly_operating if monthly_operating>0 else (999.0 if liquid_reserve>0 else 0.0)
        dscr=(cash_for_debt/annual_debt_service) if annual_debt_service>0 else 999.0; stressed_dscr=(cash_for_debt/stressed_debt_service) if stressed_debt_service>0 else 999.0; refi_months=int(_n(data.get('refinancing_months',999)) or 999)
        data_complete=bool(inflow or operating or data.get('cash_available_for_debt_service') is not None)
        breaches=[]; warnings=[]
        if data_complete and dscr<_n(rules['minimum_dscr']): breaches.append('DSCR')
        elif data_complete and dscr<_n(rules['warning_dscr']): warnings.append('DSCR')
        if data_complete and liquidity_months<_n(rules['minimum_liquidity_months']): breaches.append('LIQUIDITEITSBUFFER')
        if loan>0 and refi_months<=int(_n(rules['refinancing_warning_months'])): warnings.append('HERFINANCIERING')
        if data_complete and stressed_dscr<_n(rules['minimum_dscr']): warnings.append('RENTESTRESS')
        status='DATA AANVULLEN' if not data_complete and loan>0 else ('BREACH' if breaches else ('WAARSCHUWING' if warnings else 'GEZOND'))
        rows.append({'vve':name,'funding_decision_id':d.get('decision_id',''),'loan_amount':round(loan,2),'interest_rate':rate,'annual_debt_service':annual_debt_service,'stressed_interest_rate':round(stressed_rate,4),'stressed_annual_debt_service':stressed_debt_service,'cash_available_for_debt_service':round(cash_for_debt,2),'dscr':round(dscr,2) if dscr<900 else None,'stressed_dscr':round(stressed_dscr,2) if stressed_dscr<900 else None,'liquid_reserve':round(liquid_reserve,2),'liquidity_months':round(liquidity_months,1) if liquidity_months<900 else None,'refinancing_months':refi_months if refi_months<900 else None,'breaches':breaches,'warnings':sorted(set(warnings)),'status':status})
    counts={s:sum(r['status']==s for r in rows) for s in ['GEZOND','WAARSCHUWING','BREACH','DATA AANVULLEN']}; total_debt=sum(r['loan_amount'] for r in rows); total_service=sum(r['annual_debt_service'] for r in rows); total_cash=sum(r['cash_available_for_debt_service'] for r in rows); portfolio_dscr=(total_cash/total_service) if total_service>0 else None
    overall='BREACH' if counts['BREACH'] else ('WAARSCHUWING' if counts['WAARSCHUWING'] else ('DATA AANVULLEN' if counts['DATA AANVULLEN'] else 'GEZOND'))
    return {'portfolio_liquidity_debt_version':ENGINE_VERSION,'status':overall,'policy':rules,'vve_count':len(rows),'healthy_count':counts['GEZOND'],'warning_count':counts['WAARSCHUWING'],'breach_count':counts['BREACH'],'data_required_count':counts['DATA AANVULLEN'],'total_debt':round(total_debt,2),'annual_debt_service':round(total_service,2),'portfolio_dscr':round(portfolio_dscr,2) if portfolio_dscr is not None else None,'vves':rows,'human_decision_required':overall in {'BREACH','WAARSCHUWING'},'automatic_refinancing':False,'next_action':'Herstel liquiditeit/dekking of herstructureer financiering en leg benodigde besluiten voor.' if overall=='BREACH' else ('Beoordeel waarschuwingen en herfinancieringsmomenten.' if overall=='WAARSCHUWING' else ('Vul kasstroom- en liquiditeitsactuals aan.' if overall=='DATA AANVULLEN' else 'Financiering is binnen liquiditeits- en schuldservicenormen; blijf periodiek monitoren.'))}
