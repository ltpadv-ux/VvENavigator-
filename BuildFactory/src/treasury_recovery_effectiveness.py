"""Validate sustained treasury recovery before closure, including DSCR, covenants and MJOP side-effects."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='7.9.0'
DEFAULT_POLICY={'required_stable_periods':3,'minimum_dscr':1.25,'require_no_covenant_breach':True,'require_no_negative_cash':True,'require_no_buffer_breach':True,'require_no_new_mjop_risk':True}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def evaluate_treasury_recovery_effectiveness(recovery:dict[str,Any], treasury:dict[str,Any], liquidity:dict[str,Any], funding_control:dict[str,Any], mandate_forecast:dict[str,Any]|None=None, existing:dict[str,Any]|None=None, policy:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); rules={**DEFAULT_POLICY,**(policy or {})}; existing=existing or {}; mandate_forecast=mandate_forecast or {}
    if recovery.get('status') in {'GEEN HERSTEL NODIG','BESLUIT VEREIST'}:
        return {'treasury_recovery_effectiveness_version':ENGINE_VERSION,'generated_at':now,'status':'NIET VAN TOEPASSING','closure_status':'OPEN','stable_periods':0,'checks':[],'next_action':recovery.get('next_action','')}
    tracking=recovery.get('tracking',{}) or {}; portfolio=treasury.get('portfolio_timeline',[]) or []; recent=portfolio[-int(rules['required_stable_periods']):] if portfolio else []
    cash_stable=bool(recent) and all(not x.get('negative_cash') and not x.get('below_buffer') for x in recent)
    min_dscr=min((_n(x.get('dscr')) for x in liquidity.get('vves',[]) or [] if x.get('dscr') is not None),default=999.0); dscr_ok=min_dscr>=_n(rules['minimum_dscr'])
    covenant_breaches=int(funding_control.get('breach_count',0) or 0); covenant_ok=(covenant_breaches==0) if rules['require_no_covenant_breach'] else True
    mjop_high=int(mandate_forecast.get('high_risk_count',0) or 0); mjop_ok=(mjop_high==0) if rules['require_no_new_mjop_risk'] else True
    neg_ok=int(treasury.get('negative_cash_count',0) or 0)==0 if rules['require_no_negative_cash'] else True
    buffer_ok=int(treasury.get('buffer_breach_count',0) or 0)==0 if rules['require_no_buffer_breach'] else True
    checks=[{'check':'STABIELE KASBUFFER','ok':cash_stable},{'check':'DSCR','ok':dscr_ok,'actual':None if min_dscr>900 else round(min_dscr,2),'minimum':rules['minimum_dscr']},{'check':'COVENANTEN','ok':covenant_ok,'breaches':covenant_breaches},{'check':'NEGATIEVE KAS','ok':neg_ok},{'check':'BUFFER BREACH','ok':buffer_ok},{'check':'NIEUW MJOP-RISICO','ok':mjop_ok,'high_risk_count':mjop_high}]
    all_ok=all(c['ok'] for c in checks); prev_stable=int(existing.get('stable_periods',0) or 0); stable_periods=prev_stable+1 if all_ok else 0; required=int(rules['required_stable_periods']); closed=all_ok and stable_periods>=required and tracking.get('progress_percent',0)>=100
    status='HERSTEL DUURZAAM BEWEZEN' if closed else ('STABILITEIT OPBOUWEN' if all_ok else 'NADER HERSTEL NODIG')
    return {'treasury_recovery_effectiveness_version':ENGINE_VERSION,'generated_at':now,'status':status,'closure_status':'GESLOTEN' if closed else 'OPEN','stable_periods':stable_periods,'required_stable_periods':required,'checks':checks,'closed_at':existing.get('closed_at',now if closed else ''),'human_closure_required':closed,'automatic_closure':False,'next_action':'Leg duurzame herstelwerking ter bestuurlijke sluiting voor.' if closed else ('Blijf stabiele perioden opbouwen.' if all_ok else 'Herstel resterende DSCR-, covenant-, liquiditeits- of MJOP-afwijkingen.')}
