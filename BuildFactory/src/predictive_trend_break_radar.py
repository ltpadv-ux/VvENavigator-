"""Enterprise 10.3 Predictive Trend Break & Early Intervention Radar."""
from __future__ import annotations
from statistics import mean
from typing import Any
ENGINE_VERSION='10.3.0'
TRACKED=('health_governance_score','financial_health','mjop_health','risk_score','treasury_score','audit_assurance','governance_maturity')

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _signals(values:list[float], reverse:bool=False)->dict[str,Any]:
    if len(values)<4:return {'status':'ONVOLDOENDE DATA','short_slope':0.0,'long_slope':0.0,'trend_break':False,'severity':'GEEN'}
    long_d=[values[i]-values[i-1] for i in range(1,len(values))]
    short_d=long_d[-2:]
    long_s=mean(long_d[:-2]) if len(long_d)>2 else mean(long_d)
    short_s=mean(short_d)
    if reverse:
        long_s=-long_s; short_s=-short_s
    deterioration=short_s < -0.75
    reversal=long_s >= -0.25 and short_s <= -1.0
    acceleration=short_s < long_s-0.75
    break_flag=bool(reversal or acceleration)
    severity='ROOD' if short_s<=-2.0 else ('ORANJE' if break_flag and deterioration else ('GEEL' if deterioration else 'GEEN'))
    return {'status':'TRENDBREUK' if break_flag else ('VERSLECHTERING' if deterioration else 'GEEN TRENDBREUK'),'short_slope':round(short_s,2),'long_slope':round(long_s,2),'trend_break':break_flag,'deterioration':deterioration,'severity':severity,'reversal':reversal,'acceleration':acceleration}

def build_predictive_trend_break_radar(trend_intelligence:dict[str,Any])->dict[str,Any]:
    runs=trend_intelligence.get('runs',[]) or []; results={}; alerts=[]
    for key in TRACKED:
        vals=[_num(r.get('kpis',{}).get(key)) for r in runs if key in (r.get('kpis',{}) or {})]
        sig=_signals(vals,reverse=(key=='risk_score')); results[key]=sig
        if sig.get('severity') in {'GEEL','ORANJE','ROOD'}:
            alerts.append({'domain':key,'severity':sig['severity'],'trend_break':sig['trend_break'],'short_slope':sig['short_slope'],'long_slope':sig['long_slope'],'recommended_action':'Onderzoek oorzaken en bereid preventieve bestuurlijke interventie voor.' if sig['severity']=='GEEL' else 'Agendeer preventieve interventie vóór formele normbreuk.'})
    order={'ROOD':0,'ORANJE':1,'GEEL':2}; alerts.sort(key=lambda x:order.get(x['severity'],9))
    status='VROEG INGREPEN VEREIST' if any(a['severity']=='ROOD' for a in alerts) else ('VROEGE WAARSCHUWING' if alerts else ('TREND OPBOUWEN' if len(runs)<4 else 'GEEN TRENDBREUK'))
    return {'predictive_trend_break_radar_version':ENGINE_VERSION,'status':status,'history_count':len(runs),'domain_signals':results,'early_intervention_alerts':alerts,'alert_count':len(alerts),'human_decision_required':True,'automatic_intervention':False,'automatic_strategy_change':False,'next_action':'Behandel rode/oranje trendbreuken preventief in Bestuur/ALV.' if alerts else 'Blijf trends volgen; geen vroege interventie nodig.'}
