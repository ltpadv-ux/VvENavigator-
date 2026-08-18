"""Forecast budget and deadline risks before mandate breaches occur."""
from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Any

ENGINE_VERSION="5.5.0"


def forecast_mandates(mandates: dict[str,Any], today: date|None=None, warning_days:int=30) -> dict[str,Any]:
    today=today or date.today(); forecasts=[]
    for m in mandates.get("mandates",[]) or []:
        item=dict(m); budget=float(item.get("budget",0) or 0); spent=float(item.get("spent_amount",0) or 0); progress=float(item.get("progress_percent",0) or 0); status=str(item.get("status","OPEN")).upper()
        risk="LAAG"; reasons=[]; projected_final=spent
        if progress>0 and spent>0:
            projected_final=round(spent/(progress/100.0),2)
            if budget>0 and projected_final>budget:
                risk="HOOG"; reasons.append(f"Verwachte eindkosten EUR {projected_final:.2f} > budget EUR {budget:.2f}")
            elif budget>0 and projected_final>=budget*0.9:
                risk="MIDDEL"; reasons.append("Verwachte eindkosten naderen 90% van budget")
        deadline=str(item.get("deadline","") or "")
        if deadline and status not in {"GEREED","AFGEROND","CLOSED"}:
            try:
                due=date.fromisoformat(deadline[:10]); days=(due-today).days
                if days<0:
                    risk="HOOG"; reasons.append("Deadline is al verstreken")
                elif days<=warning_days and progress<90:
                    risk="HOOG" if progress<50 else max(risk,"MIDDEL", key=lambda x:{"LAAG":0,"MIDDEL":1,"HOOG":2}[x]); reasons.append(f"Deadline binnen {days} dagen bij {progress:.0f}% voortgang")
            except ValueError:
                reasons.append("Deadline kan niet worden geïnterpreteerd")
                if risk=="LAAG": risk="MIDDEL"
        forecasts.append({"mandate_id":item.get("mandate_id",""),"owner":item.get("owner",""),"risk":risk,"projected_final_cost":projected_final,"budget":budget,"progress_percent":progress,"deadline":deadline,"reasons":reasons,"early_warning":risk in {"MIDDEL","HOOG"}})
    high=sum(1 for x in forecasts if x["risk"]=="HOOG"); medium=sum(1 for x in forecasts if x["risk"]=="MIDDEL")
    return {"mandate_forecast_version":ENGINE_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"status":"VROEGE WAARSCHUWING" if high or medium else "STABIEL","high_risk":high,"medium_risk":medium,"forecasts":forecasts,"next_action":forecasts[0]["reasons"][0] if forecasts and forecasts[0]["reasons"] else "Geen vroegtijdige afwijking voorspeld."}
