"""Portfolio treasury early-warning engine and 12-month governance action calendar."""
from __future__ import annotations
from datetime import date
from typing import Any

ENGINE_VERSION='8.1.0'
DEFAULT_POLICY={'months':12,'dscr_warning':1.40,'refinancing_warning_months':12,'cash_buffer_warning_months':3,'include_mjop':True}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _month_add(y:int,m:int,offset:int)->str:
    n=y*12+(m-1)+offset
    return f'{n//12:04d}-{n%12+1:02d}'

def build_treasury_early_warning_calendar(report:dict[str,Any], policy:dict[str,Any]|None=None)->dict[str,Any]:
    rules={**DEFAULT_POLICY,**(policy or {})}; months=max(1,int(_n(rules['months']) or 12)); today=date.today(); horizon=[_month_add(today.year,today.month,i) for i in range(months)]
    liquidity=report.get('portfolio_liquidity_debt_control',{}) or {}; funding=report.get('portfolio_funding_covenant_control',{}) or {}; treasury=report.get('treasury_forecast',{}) or {}; stress=report.get('treasury_stress_intervention',{}) or {}; tower=report.get('portfolio_treasury_control_tower',{}) or {}; mandate_forecast=report.get('mandate_forecast',{}) or {}
    actions=[]
    def add(month:str,category:str,severity:str,title:str,detail:str,authority:str='Bestuur'):
        if month in horizon: actions.append({'month':month,'category':category,'severity':severity,'title':title,'detail':detail,'decision_authority':authority})
    for v in treasury.get('vves',[]) or []:
        name=str(v.get('vve','VvE'))
        for row in (v.get('timeline',[]) or [])[:months]:
            if row.get('negative_cash'): add(row['month'],'LIQUIDITEIT','ROOD',f'{name}: negatieve kas verwacht',f"Verwachte kas {row.get('closing_cash',0)} onder nul; herstelplan vóór deze maand vereist.",'Bestuur/ALV')
            elif row.get('below_buffer'): add(row['month'],'KASBUFFER','ORANJE',f'{name}: minimumkasbuffer onder druk',f"Kas {row.get('closing_cash',0)} onder buffer {row.get('minimum_buffer',0)}.",'Bestuur')
            if rules.get('include_mjop') and _n(row.get('mjop_outflow'))>0: add(row['month'],'MJOP','GEEL',f'{name}: MJOP-kasuitstroom',f"Geplande MJOP-uitstroom EUR {_n(row.get('mjop_outflow')):.0f}; bevestig dekking en timing.",'Bestuur')
    for v in liquidity.get('vves',[]) or []:
        name=str(v.get('vve','VvE')); dscr=v.get('dscr'); refi=v.get('refinancing_months')
        if dscr is not None and _n(dscr)<_n(rules['dscr_warning']): add(horizon[0],'DSCR','ROOD' if _n(dscr)<1.25 else 'ORANJE',f'{name}: DSCR aandacht',f'DSCR {_n(dscr):.2f}; financieringsdekking beoordelen.','Bestuur/ALV')
        if refi is not None and 0<=int(_n(refi))<=int(_n(rules['refinancing_warning_months'])):
            idx=min(months-1,max(0,int(_n(refi))-int(_n(rules['refinancing_warning_months'])))); add(horizon[idx],'HERFINANCIERING','ORANJE',f'{name}: herfinanciering voorbereiden',f"Herfinanciering over {int(_n(refi))} maanden; marktcheck, scenario's en besluitvorming starten.",'Bestuur/ALV')
    for d in funding.get('decisions',[]) or []:
        if d.get('covenant_status')=='BREACH': add(horizon[0],'COVENANT','ROOD',f"{d.get('vve','VvE')}: covenant breach",'Herstructureer financieringsmix of voorwaarden en leg opnieuw ter besluitvorming voor.','Bestuur/ALV')
        elif d.get('covenant_status')=='WAARSCHUWING': add(horizon[0],'COVENANT','ORANJE',f"{d.get('vve','VvE')}: covenant waarschuwing",'Beoordeel marge voordat grens wordt overschreden.','Bestuur')
    if int(stress.get('critical_scenario_count',0) or 0)>0: add(horizon[0],'STRESS','ROOD','Kritieke treasury-stressscenario’s',stress.get('next_action','Behandel kritieke stressscenario’s.'),'Bestuur/ALV')
    if int(mandate_forecast.get('high_risk_count',0) or 0)>0: add(horizon[0],'MJOP-RISICO','ORANJE','Hoog-risico mandaten beïnvloeden treasury','Herijk timing en financiering van hoog-risico mandaten.','Bestuur')
    order={'ROOD':0,'ORANJE':1,'GEEL':2}; actions=sorted(actions,key=lambda x:(x['month'],order.get(x['severity'],9),x['category'],x['title']))
    calendar=[]
    for m in horizon:
        rows=[a for a in actions if a['month']==m]; highest=rows[0]['severity'] if rows else 'GROEN'; calendar.append({'month':m,'status':highest,'action_count':len(rows),'actions':rows})
    red=sum(a['severity']=='ROOD' for a in actions); orange=sum(a['severity']=='ORANJE' for a in actions)
    status='ROOD' if red else ('ORANJE' if orange else 'GROEN')
    return {'treasury_early_warning_calendar_version':ENGINE_VERSION,'status':status,'months':months,'treasury_score':tower.get('treasury_score'),'action_count':len(actions),'red_action_count':red,'orange_action_count':orange,'calendar':calendar,'actions':actions,'human_decision_required':bool(red or orange),'automatic_execution':False,'next_action':actions[0]['title'] if actions else 'Geen urgente treasuryactie; actualiseer de kalender maandelijks.'}
