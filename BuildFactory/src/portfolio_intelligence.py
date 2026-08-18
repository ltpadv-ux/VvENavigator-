"""Portfolio Intelligence & Benchmarking for multiple VvE closed-loop results."""
from __future__ import annotations
from statistics import median
from typing import Any, Iterable

ENGINE_VERSION='7.1.0'

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _pct_rank(value:float, values:list[float], higher_better:bool=True)->float:
    if not values:return 0.0
    wins=sum(1 for x in values if (value>=x if higher_better else value<=x))
    return round(100*wins/len(values),1)

def build_portfolio_intelligence(results:Iterable[tuple[str,dict[str,Any]]])->dict[str,Any]:
    rows=[]
    for name,r in results:
        release=r.get('release',{}) or {}; dash=release.get('dashboard',{}) or {}; cockpit=release.get('executive_cockpit',{}) or {}; km=cockpit.get('key_metrics',{}) or {}; tower=r.get('governance_control_tower',{}) or {}; tk=tower.get('kpis',{}) or {}; closed=r.get('closed_loop_management',{}) or {}; benefits=r.get('execution_benefits_tracking',{}) or {}; apartments=int(_n(km.get('apartments',dash.get('apartments',34))) or 34); reserve=_n(tk.get('reserve',km.get('reserve',dash.get('reserve_fund',dash.get('reserve',0))))); risk=_n(dash.get('risk_score',tk.get('risk_score',0))); lcc30=_n(km.get('lcc_30_year',km.get('lcc',0))); monthly=_n(tk.get('monthly_per_apartment',km.get('monthly_per_apartment',0))); sustainability=_n(dash.get('vni',dash.get('VNI',0))); loop=_n(closed.get('loop_completeness_score',0)); benefit=_n((benefits.get('benefits',{}) or {}).get('realization_score',0)); governance=100.0 if closed.get('governance_safe',tower.get('overall_status','')!='ROOD') else 0.0
        rows.append({'name':name,'apartments':apartments,'reserve':round(reserve,2),'reserve_per_apartment':round(reserve/apartments,2),'monthly_per_apartment':round(monthly,2),'risk_score':round(risk,2),'sustainability_score':round(sustainability,2),'governance_score':governance,'closed_loop_score':round(loop,1),'benefits_score':round(benefit,1),'lcc_30_year':round(lcc30,2),'lcc_per_apartment':round(lcc30/apartments,2)})
    if not rows:return {'portfolio_intelligence_version':ENGINE_VERSION,'status':'GEEN PORTFOLIO DATA','portfolio_count':0,'benchmarks':{},'ranking':[]}
    metrics={'reserve_per_apartment':True,'monthly_per_apartment':False,'risk_score':False,'sustainability_score':True,'governance_score':True,'closed_loop_score':True,'benefits_score':True,'lcc_per_apartment':False}
    benchmarks={k:{'median':round(median([_n(r[k]) for r in rows]),2),'best':round((max if hb else min)([_n(r[k]) for r in rows]),2)} for k,hb in metrics.items()}
    for r in rows:
        ranks={k:_pct_rank(_n(r[k]),[_n(x[k]) for x in rows],hb) for k,hb in metrics.items()}; r['percentiles']=ranks; r['portfolio_score']=round(sum(ranks.values())/len(ranks),1)
    ranking=sorted(rows,key=lambda x:(-x['portfolio_score'],x['name']))
    for i,r in enumerate(ranking,1):r['rank']=i
    return {'portfolio_intelligence_version':ENGINE_VERSION,'status':'PORTFOLIO BENCHMARK BESCHIKBAAR','portfolio_count':len(rows),'benchmarks':benchmarks,'ranking':ranking,'priority_vves':[r['name'] for r in sorted(rows,key=lambda x:(-x['risk_score'],x['reserve_per_apartment']))[:5]],'next_action':'Gebruik benchmarkafwijkingen om portefeuilleprioriteiten en VvE-specifieke verbeteracties te bepalen.'}
