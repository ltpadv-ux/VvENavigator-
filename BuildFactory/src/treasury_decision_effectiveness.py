"""Close treasury accountability actions only when the original issue is resolved without creating new financial risks."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='8.4.0'

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def evaluate_treasury_decision_effectiveness(accountability:dict[str,Any], report:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); existing=existing or {}; prev={x.get('action_id'):x for x in existing.get('closures',[]) or []}
    treasury=report.get('treasury_forecast',{}) or {}; liquidity=report.get('portfolio_liquidity_debt_control',{}) or {}; funding=report.get('portfolio_funding_covenant_control',{}) or {}; mandate_forecast=report.get('mandate_forecast',{}) or {}; stress=report.get('treasury_stress_intervention',{}) or {}
    dscr_ok=all((v.get('dscr') is None or _n(v.get('dscr'))>=1.25) for v in liquidity.get('vves',[]) or [])
    covenant_ok=int(funding.get('breach_count',0) or 0)==0
    cash_ok=int(treasury.get('negative_cash_count',0) or 0)==0
    buffer_ok=int(treasury.get('buffer_breach_count',0) or 0)==0
    mjop_ok=int(mandate_forecast.get('high_risk_count',0) or 0)==0
    stress_ok=int(stress.get('critical_scenario_count',0) or 0)==0
    closures=[]
    for a in accountability.get('actions',[]) or []:
        old=prev.get(a.get('action_id'),{})
        executed=a.get('status')=='AFGEROND' and bool(a.get('evidence'))
        checks=[
          {'check':'UITVOERING BEWEZEN','ok':executed},
          {'check':'DSCR','ok':dscr_ok},
          {'check':'COVENANTEN','ok':covenant_ok},
          {'check':'NEGATIEVE KAS','ok':cash_ok},
          {'check':'KASBUFFER','ok':buffer_ok},
          {'check':'MJOP-RISICO','ok':mjop_ok},
          {'check':'TREASURY STRESS','ok':stress_ok},
        ]
        all_ok=all(x['ok'] for x in checks)
        stable=int(old.get('stable_periods',0) or 0)+1 if all_ok else 0
        closed=all_ok and stable>=2
        closures.append({'action_id':a.get('action_id',''),'agenda_id':a.get('agenda_id',''),'title':a.get('title',''),'status':'EFFECT BEWEZEN' if closed else ('STABILITEIT OPBOUWEN' if all_ok else 'NADER HERSTEL NODIG'),'closure_status':'GESLOTEN' if closed else 'OPEN','stable_periods':stable,'required_stable_periods':2,'checks':checks,'closed_at':old.get('closed_at',now if closed else ''),'human_closure_required':closed,'automatic_closure':False})
    open_count=sum(x['closure_status']=='OPEN' for x in closures); closed_count=sum(x['closure_status']=='GESLOTEN' for x in closures)
    status='GEEN ACTIES' if not closures else ('VOLLEDIG EFFECTIEF' if open_count==0 else ('EFFECTCONTROLE LOPEND' if closed_count else 'NADER HERSTEL NODIG'))
    return {'treasury_decision_effectiveness_version':ENGINE_VERSION,'generated_at':now,'status':status,'closure_count':len(closures),'open_count':open_count,'closed_count':closed_count,'closures':closures,'automatic_closure':False,'human_closure_required':closed_count>0,'next_action':'Geen treasuryacties om te sluiten.' if not closures else ('Leg bewezen effectieve acties ter bestuurlijke sluiting voor.' if closed_count else 'Herstel resterende treasury-, DSCR-, covenant- of MJOP-afwijkingen en bouw stabiele perioden op.')}
