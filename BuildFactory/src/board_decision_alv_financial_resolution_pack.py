"""Enterprise 14.1 Board Decision Recommendation & ALV Financial Resolution Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.1.0'

def _id(*parts:Any)->str:return 'GOVRPK-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def build_financial_resolution_pack(cockpit:dict[str,Any], context:dict[str,Any]|None=None)->dict[str,Any]:
 context=context or {}; best=cockpit.get('integrated_preferred_path') or {}; rows=cockpit.get('ranked_integrated_paths',[]) or []
 if not best:return {'board_decision_alv_financial_resolution_pack_version':ENGINE_VERSION,'status':'ONVOLDOENDE INPUT VOOR BESLUITPAKKET','automatic_decision':False}
 alternatives=[{'scenario_name':x.get('scenario_name'),'term_months':x.get('term_months'),'reserve_share_pct':x.get('reserve_share_pct'),'integrated_decision_score':x.get('integrated_decision_score'),'decision_status':x.get('decision_status')} for x in rows[1:4]]
 blockers=[]
 if best.get('blocker'):blockers.append('Voorkeurspad bevat een harde financiële/governance blocker.')
 if not best.get('reserve_floor_ok',False):blockers.append('Reservevloer is onvoldoende beschermd.')
 if not best.get('mjop_buffer_ok',False):blockers.append('MJOP-buffer is onvoldoende beschermd.')
 recommendation='VOORLEGGEN MET POSITIEF ADVIES' if not blockers and float(best.get('integrated_decision_score',0) or 0)>=80 else ('VOORLEGGEN MET NADERE VOORWAARDEN' if not blockers else 'NIET VOORLEGGEN ZONDER HERIJKING')
 decision_points=['Instemmen met het geselecteerde financierings- en bijdragepad.','Instemmen met de voorgestelde looptijd en reserve-inzet.','Bevestigen dat reservevloer en MJOP-buffer na besluit bewaakt blijven.','Bestuur mandateren om uitvoering binnen het vastgestelde besluit en budget voor te bereiden.']
 resolution_text=(f"De ALV besluit, onder voorbehoud van de toepasselijke statutaire en wettelijke vereisten, in te stemmen met scenario {best.get('scenario_name','')}, met een looptijd van {best.get('term_months','')} maanden en een reserve-inzet van {best.get('reserve_share_pct','')}%, waarbij de extra maandlast, reservepositie, MJOP-buffer en stressbestendigheid conform het besluitpakket worden bewaakt.")
 return {'board_decision_alv_financial_resolution_pack_version':ENGINE_VERSION,'resolution_pack_id':_id(cockpit.get('cockpit_id',''),best.get('decision_path_id','')),'status':'BESLUITPAKKET GEREED VOOR BESTUURLIJKE REVIEW','recommendation':recommendation,'preferred_path':best,'alternatives':alternatives,'blockers':blockers,'decision_points':decision_points,'board_narrative':{'subject':context.get('subject','Preventief financieel governancebesluit'),'rationale':'Integraal voorkeursbeeld op basis van effect, uitvoerbaarheid, financiële weerbaarheid, fairness, smoothing, stress resilience en governance.','integrated_decision_score':best.get('integrated_decision_score'),'maximum_monthly_extra_eur':best.get('maximum_monthly_extra_eur'),'stressed_max_monthly_extra_eur':best.get('stressed_max_monthly_extra_eur'),'reserve_after_eur':best.get('reserve_after_eur'),'stressed_reserve_after_eur':best.get('stressed_reserve_after_eur'),'mjop_space_after_eur':best.get('mjop_space_after_eur')},'draft_alv_resolution':resolution_text,'human_board_review_required':True,'human_alv_approval_required':True,'human_legal_governance_review_required':True,'automatic_resolution_adoption':False,'automatic_contribution_change':False,'automatic_reserve_draw':False,'automatic_financing':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Laat Bestuur het besluitpakket controleren en leg daarna de definitieve besluittekst en financiële onderbouwing voor aan de ALV.'}
