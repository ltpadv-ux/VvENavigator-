"""36-month treasury forecast for VvE portfolio cash planning."""
from __future__ import annotations
from datetime import date
from typing import Any

ENGINE_VERSION='7.6.0'
DEFAULT_POLICY={'months':36,'minimum_cash_buffer_months':3.0,'minimum_cash_balance':0.0,'interest_rate':0.02}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _month_add(y:int,m:int,offset:int)->tuple[int,int]:
    n=(y*12+(m-1))+offset
    return n//12,n%12+1

def build_treasury_forecast(liquidity:dict[str,Any], actuals:dict[str,Any]|None=None, policy:dict[str,Any]|None=None)->dict[str,Any]:
    actuals=actuals or {}; rules={**DEFAULT_POLICY,**(policy or {})}; months=max(1,int(_n(rules['months']) or 36)); today=date.today(); portfolio_months=[]; vves=[]
    for row in liquidity.get('vves',[]) or []:
        name=str(row.get('vve','')); data=actuals.get(name,{}) or {}; opening=_n(data.get('opening_cash',row.get('liquid_reserve',0))); monthly_contrib=_n(data.get('monthly_contributions',0)); monthly_other_income=_n(data.get('monthly_other_income',0)); monthly_operating=_n(data.get('monthly_operating_outflow',0)); monthly_debt=_n(data.get('monthly_debt_service',_n(row.get('annual_debt_service'))/12)); subsidy_schedule=data.get('subsidies',{}) or {}; mjop_schedule=data.get('mjop_outflows',{}) or {}; other_outflows=data.get('other_outflows',{}) or {}; cash=opening; timeline=[]; min_cash=None; breach_months=[]
        buffer_months=_n(rules['minimum_cash_buffer_months']); min_floor=max(_n(rules['minimum_cash_balance']),monthly_operating*buffer_months)
        for i in range(months):
            y,m=_month_add(today.year,today.month,i); key=f'{y:04d}-{m:02d}'; interest=max(0,cash)*_n(rules['interest_rate'])/12; subsidy=_n(subsidy_schedule.get(key)); mjop=_n(mjop_schedule.get(key)); extra=_n(other_outflows.get(key)); inflow=monthly_contrib+monthly_other_income+subsidy+interest; outflow=monthly_operating+monthly_debt+mjop+extra; closing=cash+inflow-outflow; below=closing<min_floor; negative=closing<0
            if below: breach_months.append(key)
            timeline.append({'month':key,'opening_cash':round(cash,2),'contributions':round(monthly_contrib,2),'other_income':round(monthly_other_income,2),'subsidy':round(subsidy,2),'interest_income':round(interest,2),'operating_outflow':round(monthly_operating,2),'debt_service':round(monthly_debt,2),'mjop_outflow':round(mjop,2),'other_outflow':round(extra,2),'closing_cash':round(closing,2),'minimum_buffer':round(min_floor,2),'below_buffer':below,'negative_cash':negative})
            cash=closing; min_cash=closing if min_cash is None else min(min_cash,closing)
        status='NEGATIEVE KAS' if any(x['negative_cash'] for x in timeline) else ('BUFFER BREACH' if breach_months else 'VOLDOENDE LIQUIDITEIT')
        vves.append({'vve':name,'status':status,'opening_cash':round(opening,2),'minimum_cash':round(min_cash or 0,2),'ending_cash':round(cash,2),'minimum_buffer':round(min_floor,2),'breach_months':breach_months,'timeline':timeline})
    for i in range(months):
        y,m=_month_add(today.year,today.month,i); key=f'{y:04d}-{m:02d}'; rows=[v['timeline'][i] for v in vves if len(v['timeline'])>i]; portfolio_months.append({'month':key,'opening_cash':round(sum(r['opening_cash'] for r in rows),2),'total_inflow':round(sum(r['contributions']+r['other_income']+r['subsidy']+r['interest_income'] for r in rows),2),'total_outflow':round(sum(r['operating_outflow']+r['debt_service']+r['mjop_outflow']+r['other_outflow'] for r in rows),2),'closing_cash':round(sum(r['closing_cash'] for r in rows),2),'minimum_buffer':round(sum(r['minimum_buffer'] for r in rows),2),'below_buffer':any(r['below_buffer'] for r in rows),'negative_cash':any(r['negative_cash'] for r in rows)})
    negative=sum(v['status']=='NEGATIEVE KAS' for v in vves); breaches=sum(v['status']=='BUFFER BREACH' for v in vves); overall='NEGATIEVE KAS' if negative else ('BUFFER BREACH' if breaches else 'VOLDOENDE LIQUIDITEIT')
    return {'treasury_forecast_version':ENGINE_VERSION,'status':overall,'forecast_months':months,'policy':rules,'vve_count':len(vves),'negative_cash_count':negative,'buffer_breach_count':breaches,'vves':vves,'portfolio_timeline':portfolio_months,'human_decision_required':overall!='VOLDOENDE LIQUIDITEIT','automatic_cash_transfer':False,'next_action':'Herplan MJOP, bijdragen of financiering voordat negatieve kas ontstaat.' if overall=='NEGATIEVE KAS' else ('Herstel minimumkasbuffer vóór geplande uitgaven.' if overall=='BUFFER BREACH' else 'Liquiditeitsprognose is toereikend; actualiseer maandelijks.')}
