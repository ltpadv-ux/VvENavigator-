"""Integrated portfolio treasury control tower across funding, covenants, liquidity, forecast, stress and recovery."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='8.0.0'

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def build_portfolio_treasury_control_tower(report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat()
    funding=report.get('portfolio_funding_covenant_control',{}) or {}
    liquidity=report.get('portfolio_liquidity_debt_control',{}) or {}
    treasury=report.get('treasury_forecast',{}) or {}
    stress=report.get('treasury_stress_intervention',{}) or {}
    recovery=report.get('treasury_recovery_mandate',{}) or {}
    effectiveness=report.get('treasury_recovery_effectiveness',{}) or {}
    portfolio=report.get('portfolio_intelligence',{}) or {}
    breaches=int(funding.get('breach_count',0) or 0)+int(liquidity.get('breach_count',0) or 0)
    warnings=int(funding.get('warning_count',0) or 0)+int(liquidity.get('warning_count',0) or 0)
    negative=int(treasury.get('negative_cash_count',0) or 0)
    buffer_breach=int(treasury.get('buffer_breach_count',0) or 0)
    critical_stress=int(stress.get('critical_scenario_count',0) or 0)
    recovery_open=1 if recovery.get('status') in {'HERSTELMANDAAT ACTIEF','EFFECTCONTROLE','BESLUIT VEREIST'} else 0
    recovery_not_proven=1 if effectiveness.get('closure_status')=='OPEN' and effectiveness.get('status') not in {'NIET VAN TOEPASSING',''} else 0
    score=100-(breaches*20+warnings*8+negative*25+buffer_breach*12+critical_stress*10+recovery_open*8+recovery_not_proven*8)
    score=max(0,min(100,score)); status='GROEN' if score>=80 else ('ORANJE' if score>=50 else 'ROOD')
    priorities=[]
    if negative: priorities.append('Herstel negatieve kasposities vóór nieuwe niet-kritieke uitgaven.')
    if breaches: priorities.append('Los covenant- of DSCR-breaches op en leg noodzakelijke financieringsbesluiten voor.')
    if buffer_breach: priorities.append('Herstel minimumkasbuffers in de 36-maands treasuryprognose.')
    if critical_stress: priorities.append('Behandel kritieke treasury-stressscenario’s en activeer herstelinterventies.')
    if recovery_open: priorities.append('Rond open treasury-herstelmandaten af en actualiseer eigenaar/deadline.')
    if recovery_not_proven: priorities.append('Bouw stabiele herstelperioden op en verzamel effectbewijs voor sluiting.')
    if not priorities: priorities.append('Treasury is beheerst; blijf maandelijks forecast, DSCR en convenanten actualiseren.')
    return {
      'portfolio_treasury_control_tower_version':ENGINE_VERSION,
      'generated_at':now,
      'status':status,
      'treasury_score':score,
      'portfolio_count':int(portfolio.get('portfolio_count',0) or 0),
      'kpis':{
        'total_debt':round(_n(liquidity.get('total_debt')),2),
        'annual_debt_service':round(_n(liquidity.get('annual_debt_service')),2),
        'portfolio_dscr':liquidity.get('portfolio_dscr'),
        'funding_covenant_breaches':int(funding.get('breach_count',0) or 0),
        'funding_covenant_warnings':int(funding.get('warning_count',0) or 0),
        'liquidity_breaches':int(liquidity.get('breach_count',0) or 0),
        'liquidity_warnings':int(liquidity.get('warning_count',0) or 0),
        'negative_cash_vves':negative,
        'buffer_breach_vves':buffer_breach,
        'critical_stress_scenarios':critical_stress,
        'attention_stress_scenarios':int(stress.get('attention_scenario_count',0) or 0),
        'recovery_status':recovery.get('status',''),
        'recovery_effectiveness_status':effectiveness.get('status',''),
        'stable_recovery_periods':int(effectiveness.get('stable_periods',0) or 0),
      },
      'priority_actions':priorities,
      'human_governance_preserved':True,
      'automatic_financing_commitment':False,
      'automatic_cash_transfer':False,
      'next_action':priorities[0]
    }
