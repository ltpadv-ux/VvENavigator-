"""Enterprise 17.2 Final Production Validation & Release Candidate RC1."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.2.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','release_candidate')
def _id(*p:Any)->str:return 'GOVRC1-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def evaluate_rc1(checks:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_checks',REQUIRED)); minimum=float(rules.get('minimum_rc1_readiness_pct',98)); rows=[]
 for name in required:
  x=checks.get(name,{}) if isinstance(checks.get(name,{}),dict) else {'passed':bool(checks.get(name))}
  rows.append({'check':name,'passed':bool(x.get('passed',False)),'score_pct':float(x.get('score_pct',100 if x.get('passed') else 0) or 0),'evidence_ref':x.get('evidence_ref')})
 passed=sum(1 for r in rows if r['passed']); readiness=round(100*passed/len(rows),1) if rows else 0.0; evidence_complete=all(r['evidence_ref'] for r in rows if r['passed']); blockers=[r['check'] for r in rows if not r['passed']]
 rc1_ready=(readiness>=minimum and not blockers and evidence_complete)
 return {'final_production_validation_rc1_version':ENGINE_VERSION,'rc1_id':_id(readiness,len(blockers),evidence_complete),'status':'RC1 VALIDATED' if rc1_ready else 'RC1 NOT READY','rc1_readiness_pct':readiness,'minimum_rc1_readiness_pct':minimum,'validation_matrix':rows,'blockers':blockers,'evidence_complete':evidence_complete,'release_candidate_rc1_ready':rc1_ready,'requires_go_no_go_board':rc1_ready,'requires_manual_release_tag':rc1_ready,'automatic_release':False,'automatic_tagging':False,'next_action':'Leg RC1 voor aan de Go/No-Go Board en maak pas na GO handmatig de release-tag.' if rc1_ready else 'Los RC1-blockers op, completeer bewijs en voer de finale productievalidatie opnieuw uit.'}
