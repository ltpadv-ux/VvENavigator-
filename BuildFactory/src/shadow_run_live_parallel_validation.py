"""Enterprise 16.3 Shadow Run & Live Parallel Validation Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.3.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVSHD-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def validate_shadow_run(champion_periods:list[dict[str,Any]], challenger_periods:list[dict[str,Any]], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; min_periods=max(1,int(_n(rules.get('minimum_shadow_periods',3)) or 3)); min_win_rate=_n(rules.get('minimum_challenger_win_rate_pct',60)); min_live_gain=_n(rules.get('minimum_live_reliability_gain_points',2)); max_mape=_n(rules.get('maximum_live_mape_pct',20)); paired=min(len(champion_periods),len(challenger_periods)); rows=[]; wins=0
 for i in range(paired):
  c=champion_periods[i]; q=challenger_periods[i]; cm=_n(c.get('mape_pct')); qm=_n(q.get('mape_pct')); cb=abs(_n(c.get('bias_pct'))); qb=abs(_n(q.get('bias_pct'))); cr=_n(c.get('reliability_score',c.get('model_reliability_score'))); qr=_n(q.get('reliability_score',q.get('model_reliability_score'))); better=(qm<cm and qb<=cb and qr>=cr); wins+=int(better); rows.append({'period':q.get('period',c.get('period',i+1)),'champion_mape_pct':cm,'challenger_mape_pct':qm,'champion_abs_bias_pct':cb,'challenger_abs_bias_pct':qb,'champion_reliability_score':cr,'challenger_reliability_score':qr,'challenger_wins_period':better})
 win_rate=round(wins/paired*100,2) if paired else 0.0; avg_c_rel=round(sum(_n(x.get('reliability_score',x.get('model_reliability_score'))) for x in champion_periods[:paired])/paired,2) if paired else 0.0; avg_q_rel=round(sum(_n(x.get('reliability_score',x.get('model_reliability_score'))) for x in challenger_periods[:paired])/paired,2) if paired else 0.0; avg_q_mape=round(sum(_n(x.get('mape_pct')) for x in challenger_periods[:paired])/paired,2) if paired else 0.0; blockers=[]
 if paired<min_periods:blockers.append('Onvoldoende volledige shadow-run perioden.')
 if win_rate<min_win_rate:blockers.append('Challenger wint onvoldoende live perioden.')
 if avg_q_rel-avg_c_rel<min_live_gain:blockers.append('Live reliability gain ligt onder de promotiedrempel.')
 if avg_q_mape>max_mape:blockers.append('Gemiddelde live MAPE van challenger ligt boven de grens.')
 ready=not blockers
 return {'shadow_run_live_parallel_validation_version':ENGINE_VERSION,'shadow_run_id':_id(paired,wins,avg_q_rel),'status':'SHADOW RUN GESLAAGD - PROMOTIE REVIEW GEREED' if ready else 'SHADOW RUN NIET PROMOTIEGEREED','paired_periods':paired,'minimum_shadow_periods':min_periods,'challenger_period_wins':wins,'challenger_win_rate_pct':win_rate,'minimum_challenger_win_rate_pct':min_win_rate,'champion_average_reliability_score':avg_c_rel,'challenger_average_reliability_score':avg_q_rel,'live_reliability_gain_points':round(avg_q_rel-avg_c_rel,2),'challenger_average_mape_pct':avg_q_mape,'period_results':rows,'blockers':blockers,'promotion_review_ready':ready,'requires_model_owner_approval':True,'requires_board_review':True,'requires_final_monte_carlo_validation':True,'automatic_model_promotion':False,'automatic_champion_replacement':False,'automatic_baseline_change':False,'next_action':'Voer finale Monte Carlo-validatie uit en laat model-owner/bestuur promotie expliciet goedkeuren.' if ready else 'Laat de challenger langer parallel draaien of herkalibreer hem vóór een nieuwe promotiebeoordeling.'}
