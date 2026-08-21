"""Enterprise 17.4 Production Evidence Runner & RC1 Closure Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.4.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')
def _id(*p:Any)->str:return 'GOVEVD-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def build_evidence_pack(evidence:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_evidence',REQUIRED)); rows=[]
 for name in required:
  raw=evidence.get(name,{}) if isinstance(evidence.get(name,{}),dict) else {'present':bool(evidence.get(name))}
  present=bool(raw.get('present',False)); ref=raw.get('evidence_ref'); verified=bool(raw.get('verified',False)); rows.append({'evidence':name,'present':present,'verified':verified,'evidence_ref':ref,'closed':present and verified and bool(ref)})
 closed=sum(1 for r in rows if r['closed']); closure_pct=round(100*closed/len(rows),1) if rows else 0.0; missing=[r['evidence'] for r in rows if not r['closed']]; critical=set(rules.get('critical_evidence',('ci','regression','security','disaster_recovery'))); critical_missing=[x for x in missing if x in critical]
 status='RC1 EVIDENCE PACK CLOSED' if not missing else ('RC1 EVIDENCE PACK BLOCKED' if critical_missing else 'RC1 EVIDENCE PACK INCOMPLETE')
 return {'production_evidence_runner_rc1_closure_pack_version':ENGINE_VERSION,'evidence_pack_id':_id(status,closure_pct,len(missing)),'status':status,'evidence_matrix':rows,'closure_pct':closure_pct,'missing_evidence':missing,'critical_missing_evidence':critical_missing,'rc1_evidence_pack_closed':not missing,'ready_for_final_go_no_go':not missing,'evidence_manifest':{r['evidence']:r['evidence_ref'] for r in rows if r['closed']},'human_evidence_owner_review_required':True,'automatic_evidence_approval':False,'automatic_release':False,'next_action':'Laat evidence owner het gesloten pack reviewen en voer daarna Final Go/No-Go uit.' if not missing else 'Verzamel/valideer ontbrekend bewijs en bouw het RC1 closure pack opnieuw.'}
