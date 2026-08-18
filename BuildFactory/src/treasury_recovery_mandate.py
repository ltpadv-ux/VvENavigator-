"""Human-approved treasury recovery decision, liquidity mandate, and recovery tracking."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='7.8.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    raw='|'.join(str(x) for x in parts); return f"{prefix}-{sha256(raw.encode()).hexdigest()[:10].upper()}"

def build_treasury_recovery_mandate(stress:dict[str,Any], treasury:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}; now=datetime.now(timezone.utc).isoformat(); preferred=stress.get('preferred_intervention',{}) or {}
    if stress.get('status')=='ROBUUST' or not preferred:
        return {'treasury_recovery_version':ENGINE_VERSION,'generated_at':now,'status':'GEEN HERSTEL NODIG','decision':{},'mandate':{},'tracking':{},'next_action':'Treasury is robuust; reguliere monitoring voortzetten.'}
    prev_dec=existing.get('decision',{}) or {}; action=str(prev_dec.get('selected_action') or preferred.get('action','')); decision=str(prev_dec.get('decision','NOG TE BESLUITEN')).upper(); approved=decision in APPROVED
    decision_id=prev_dec.get('decision_id') or _id('TRDEC',action,stress.get('status',''))
    decision_rec={'decision_id':decision_id,'selected_action':action,'decision':decision,'approved_by':prev_dec.get('approved_by',''),'approved_at':prev_dec.get('approved_at',''),'rationale':prev_dec.get('rationale',''),'decision_authority':prev_dec.get('decision_authority',preferred.get('decision_authority','Bestuur/ALV')),'stress_status':stress.get('status','')}
    if not approved:
        return {'treasury_recovery_version':ENGINE_VERSION,'generated_at':now,'status':'BESLUIT VEREIST','decision':decision_rec,'mandate':{},'tracking':{},'human_approval_required':True,'automatic_execution':False,'next_action':f"Laat {decision_rec['decision_authority']} de treasury-herstelactie formeel goedkeuren."}
    prev_man=existing.get('mandate',{}) or {}; mandate_id=prev_man.get('mandate_id') or _id('TRMAN',decision_id,action)
    portfolio=treasury.get('portfolio_timeline',[]) or []; first_shortfall=next((x for x in portfolio if x.get('below_buffer') or x.get('negative_cash')),{})
    target_buffer=max((float(x.get('minimum_buffer',0) or 0) for x in portfolio),default=0.0)
    mandate={'mandate_id':mandate_id,'decision_id':decision_id,'status':prev_man.get('status','ACTIEF'),'owner':prev_man.get('owner','Bestuur / beheerder'),'action':action,'deadline':prev_man.get('deadline',''),'target_minimum_cash_buffer':round(target_buffer,2),'target_negative_cash_months':0,'target_buffer_breach_months':0,'first_risk_month':first_shortfall.get('month',''),'budget_ceiling':float(prev_man.get('budget_ceiling',0) or 0),'created_at':prev_man.get('created_at',now)}
    prev_track=existing.get('tracking',{}) or {}; actual_min=float(prev_track.get('actual_minimum_cash',0) or 0); neg=int(prev_track.get('negative_cash_months',treasury.get('negative_cash_count',0)) or 0); breaches=int(prev_track.get('buffer_breach_months',treasury.get('buffer_breach_count',0)) or 0); progress=float(prev_track.get('progress_percent',0) or 0)
    recovered=(neg==0 and breaches==0 and actual_min>=mandate['target_minimum_cash_buffer'] and progress>=100)
    tracking={'progress_percent':progress,'actual_minimum_cash':actual_min,'negative_cash_months':neg,'buffer_breach_months':breaches,'recovery_proven':recovered,'updated_at':now,'closed_at':prev_track.get('closed_at',now if recovered else '')}
    status='HERSTEL BEWEZEN' if recovered else ('EFFECTCONTROLE' if progress>=100 else 'HERSTELMANDAAT ACTIEF')
    return {'treasury_recovery_version':ENGINE_VERSION,'generated_at':now,'status':status,'decision':decision_rec,'mandate':mandate,'tracking':tracking,'human_approval_required':True,'automatic_execution':False,'next_action':'Herstel is bewezen; sluit mandaat bestuurlijk af.' if recovered else ('Meet actuele kasbuffer en breaches om effect te bewijzen.' if progress>=100 else 'Voer herstelmandaat uit en actualiseer voortgang en liquiditeits-KPI’s.')}
