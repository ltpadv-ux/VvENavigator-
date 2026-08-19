"""Enterprise 9.9 advisory layer: What should the Board do now? No autonomous decisions."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='9.9.0'

def _id(source:str,topic:str)->str:
 return 'GRA-'+sha256(f'{source}|{topic}'.encode()).hexdigest()[:10].upper()

def _add(out:list, source:str, topic:str, priority:str, action:str, authority:str='Bestuur', impact:Any=None, deadline:str='Zo spoedig mogelijk', rationale:str=''):
 out.append({'recommendation_id':_id(source,topic),'source':source,'topic':topic,'priority':priority,'recommended_action':action,'decision_authority':authority,'financial_impact':impact,'deadline':deadline,'rationale':rationale})

def build_governance_recommendations(report:dict[str,Any], max_actions:int=10)->dict[str,Any]:
 out=[]; os=report.get('vve_governance_operating_system',{}) or {}; variance=report.get('strategic_mandate_variance_control',{}) or {}; corrective=report.get('predictive_corrective_action_optimizer',{}) or {}; remediation=report.get('audit_remediation',{}) or {}; treasury=report.get('portfolio_treasury_control_tower',{}) or {}; calendar=report.get('treasury_early_warning_calendar',{}) or {}; rebase=report.get('strategic_amendment_effectiveness',{}) or {}; roadmap=report.get('governance_improvement_roadmap',{}) or {}
 if str(os.get('status','')).upper()=='ROOD': _add(out,'governance_os','overall_health','KRITIEK','Agendeer de drie laagst scorende domeinen en besluit over herstelmaatregelen.','Bestuur/ALV',rationale='Overall VvE Health & Governance staat ROOD.')
 if str(treasury.get('status','')).upper() in {'ROOD','CRITIEK'} or float(treasury.get('treasury_score',100) or 100)<50: _add(out,'treasury_control_tower','liquidity','KRITIEK','Beoordeel liquiditeit, DSCR en convenanten en activeer zo nodig een treasury-herstelmandaat.','Bestuur/ALV',rationale='Treasury is kritisch of scoort onder 50.')
 if str(variance.get('status','')).upper() in {'ORANJE','ROOD'}:
  top=(corrective.get('ranking',[]) or [{}])[0]; _add(out,'variance_control','strategic_variance','HOOG' if str(variance.get('status','')).upper()=='ORANJE' else 'KRITIEK','Beoordeel het hoogst gerangschikte correctieve herstelpad.','Bestuur/ALV',top.get('estimated_corrective_cost'),rationale='Strategisch mandaat wijkt af van target.')
 if int(remediation.get('open_count',0) or 0)>0: _add(out,'audit_remediation','failed_controls','HOOG','Sluit open audit-remediations met eigenaar, bewijs en menselijke her-test.','Bestuur',rationale=f"{remediation.get('open_count')} control-herstelacties staan open.")
 for item in (calendar.get('actions',calendar.get('calendar',[])) or []):
  if str(item.get('status',item.get('priority',''))).upper() in {'ROOD','ORANJE'}: _add(out,'treasury_calendar',str(item.get('topic','treasury_action')),str(item.get('status',item.get('priority'))).upper(),str(item.get('action',item.get('description','Behandel treasury-actie.'))),str(item.get('decision_authority','Bestuur')),item.get('financial_impact'),str(item.get('deadline',item.get('month','Binnen 12 maanden'))),str(item.get('rationale','Treasury early-warning.')))
 if str(rebase.get('status','')).startswith('WIJZIGING EFFECTIEF'): _add(out,'rebaseline','new_baseline','NORMAAL','Stel de nieuwe Finance/MJOP/Treasury/Governance-baseline formeel vast.','Bestuur/ALV',deadline='Volgend bestuurs-/ALV-moment',rationale='Mandaatwijziging is aantoonbaar effectief.')
 if float(roadmap.get('overall_progress',100) or 100)<50: _add(out,'improvement_roadmap','roadmap_progress','NORMAAL','Versnel de governance improvement roadmap op de zwakste domeinen.','Bestuur',rationale='Verbeterprogramma loopt achter.')
 rank={'KRITIEK':0,'ROOD':0,'HOOG':1,'ORANJE':1,'NORMAAL':2,'GEEL':2}; out.sort(key=lambda x:(rank.get(x['priority'],3),x['recommendation_id']))
 out=out[:max_actions]
 return {'autonomous_governance_recommendation_version':ENGINE_VERSION,'question':'Wat moet het Bestuur nu doen?','status':'ACTIE VEREIST' if out else 'GEEN DIRECTE ACTIE','recommendation_count':len(out),'recommendations':out,'human_decision_required':True,'advisory_only':True,'automatic_decision':False,'automatic_execution':False,'next_action':'Behandel aanbevelingen op prioriteit en leg menselijke besluiten vast.' if out else 'Blijf monitoren en herbereken bij nieuwe data.'}
