"""Score treasury audit chains on governance, control evidence and closure quality."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='8.6.0'

def _score_bool(ok:bool, weight:int)->int:
    return weight if ok else 0

def build_treasury_audit_assurance(report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat()
    lineage=report.get('treasury_audit_lineage',{}) or {}
    board=report.get('treasury_decision_board_pack',{}) or {}
    accountability=report.get('treasury_accountability_register',{}) or {}
    effectiveness=report.get('treasury_decision_effectiveness',{}) or {}
    agenda_by_id={x.get('agenda_id'):x for x in board.get('agenda_items',[]) or []}
    action_by_agenda={x.get('agenda_id'):x for x in accountability.get('actions',[]) or []}
    closure_by_action={x.get('action_id'):x for x in effectiveness.get('closures',[]) or []}
    results=[]
    for chain in lineage.get('chains',[]) or []:
        agenda=agenda_by_id.get(chain.get('agenda_id'),{})
        action=action_by_agenda.get(chain.get('agenda_id'),{})
        closure=closure_by_action.get(action.get('action_id'),{}) if action else {}
        approved_by=str(agenda.get('approved_by','')).strip(); owner=str(action.get('owner','')).strip()
        segregation=bool(approved_by and owner and approved_by.lower()!=owner.lower())
        decision_quality=bool(agenda.get('draft_decision')) and bool(agenda.get('decision_authority')) and bool(agenda.get('rationale'))
        budget_control=(not action) or (float(action.get('budget',0) or 0)<=0 or float(action.get('spent',0) or 0)<=float(action.get('budget',0) or 0))
        execution_evidence=(not action) or (action.get('status')!='AFGEROND' or bool(action.get('evidence')))
        effect_testing=(not action) or (action.get('status')!='AFGEROND' or bool(closure.get('checks')))
        closure_control=(not closure) or closure.get('closure_status')!='GESLOTEN' or (closure.get('status')=='EFFECT BEWEZEN' and closure.get('human_closure_required') is True and closure.get('automatic_closure') is False)
        lineage_complete=bool(chain.get('complete'))
        tests=[
            {'control':'FUNCTIESCHEIDING','ok':segregation,'weight':15},
            {'control':'BESLUITKWALITEIT','ok':decision_quality,'weight':15},
            {'control':'BUDGETCONTROLE','ok':budget_control,'weight':15},
            {'control':'UITVOERINGSBEWIJS','ok':execution_evidence,'weight':15},
            {'control':'EFFECTMETING','ok':effect_testing,'weight':15},
            {'control':'SLUITINGSCONTROLE','ok':closure_control,'weight':15},
            {'control':'LINEAGE COMPLEET','ok':lineage_complete,'weight':10},
        ]
        score=sum(_score_bool(t['ok'],t['weight']) for t in tests)
        assurance='HOOG' if score>=85 else ('REDELIJK' if score>=70 else ('MATIG' if score>=50 else 'LAAG'))
        failed=[t['control'] for t in tests if not t['ok']]
        results.append({'lineage_id':chain.get('lineage_id',''),'agenda_id':chain.get('agenda_id',''),'title':chain.get('title',''),'assurance_score':score,'assurance_level':assurance,'tests':tests,'failed_controls':failed,'audit_ready':score>=85 and not failed})
    overall=round(sum(x['assurance_score'] for x in results)/len(results),1) if results else 0.0
    low=sum(x['assurance_level'] in {'LAAG','MATIG'} for x in results)
    status='GEEN CONTROLES' if not results else ('ASSURANCE STERK' if overall>=85 and low==0 else ('ASSURANCE AANDACHT' if overall>=70 else 'ASSURANCE ONVOLDOENDE'))
    return {'treasury_audit_assurance_version':ENGINE_VERSION,'generated_at':now,'status':status,'overall_assurance_score':overall,'chain_count':len(results),'weak_chain_count':low,'results':results,'human_assurance_required':True,'automatic_audit_opinion':False,'next_action':'Controleomgeving is sterk; laat accountant/ALV de assurance-uitkomst beoordelen.' if status=='ASSURANCE STERK' else ('Herstel zwakke controls vóór formele assurance of accountantsbeoordeling.' if results else 'Geen auditketens beschikbaar voor control testing.')}
