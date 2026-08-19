"""Convert treasury early warnings into a board/ALV decision agenda and concise board pack."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='8.2.0'
SEVERITY_ORDER={'ROOD':0,'ORANJE':1,'GEEL':2,'GROEN':3}

def _id(month:str,category:str,title:str)->str:
    raw=f'{month}|{category}|{title}'.encode()
    return 'TRAGEN-'+sha256(raw).hexdigest()[:10].upper()

def _draft_decision(action:dict[str,Any])->str:
    category=str(action.get('category','')).upper(); title=str(action.get('title',''))
    templates={
      'LIQUIDITEIT':'Besluit om vóór de risicomaand een liquiditeitsherstelplan vast te stellen, inclusief dekking, eigenaar en rapportagemoment.',
      'KASBUFFER':'Besluit om de minimumkasbuffer te herstellen en niet-kritieke uitgaven zo nodig te faseren.',
      'DSCR':'Besluit om financieringsdekking en schuldendienst te herijken en zo nodig een aangepaste financieringsmix voor te leggen.',
      'HERFINANCIERING':'Besluit om herfinancieringsscenario’s, marktcondities en covenantimpact tijdig uit te werken.',
      'COVENANT':'Besluit om de covenantafwijking te herstellen en benodigde financieringswijzigingen ter goedkeuring voor te leggen.',
      'STRESS':'Besluit om de hoogst gerangschikte treasury-herstelinterventie uit te werken en binnen mandaat uit te voeren na goedkeuring.',
      'MJOP':'Besluit om dekking en timing van de geplande MJOP-kasuitstroom te bevestigen.',
      'MJOP-RISICO':'Besluit om timing, budget en financiering van hoog-risico mandaten te herijken.'}
    return templates.get(category,f'Besluit over treasuryactie: {title}.')

def build_treasury_decision_board_pack(calendar:dict[str,Any], tower:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
    tower=tower or {}; existing=existing or {}; now=datetime.now(timezone.utc).isoformat(); previous={x.get('agenda_id'):x for x in existing.get('agenda_items',[]) or []}
    source=[a for a in calendar.get('actions',[]) or [] if a.get('severity') in {'ROOD','ORANJE'}]
    items=[]
    for a in source:
        aid=_id(str(a.get('month','')),str(a.get('category','')),str(a.get('title',''))); prev=previous.get(aid,{})
        item={'agenda_id':aid,'month':a.get('month',''),'severity':a.get('severity',''),'category':a.get('category',''),'title':a.get('title',''),'detail':a.get('detail',''),'decision_authority':a.get('decision_authority','Bestuur'),'owner':prev.get('owner','Bestuur / beheerder'),'deadline':prev.get('deadline',a.get('month','')),'financial_impact':prev.get('financial_impact','Nader te kwantificeren'),'draft_decision':prev.get('draft_decision',_draft_decision(a)),'decision':prev.get('decision','NOG TE BESLUITEN'),'rationale':prev.get('rationale',''),'approved_by':prev.get('approved_by',''),'approved_at':prev.get('approved_at',''),'status':prev.get('status','OPEN')}
        items.append(item)
    items.sort(key=lambda x:(x['month'],SEVERITY_ORDER.get(x['severity'],9),x['category'],x['title']))
    red=sum(x['severity']=='ROOD' and x['status']!='GESLOTEN' for x in items); orange=sum(x['severity']=='ORANJE' and x['status']!='GESLOTEN' for x in items); open_count=sum(x['status']!='GESLOTEN' for x in items); decided=sum(str(x['decision']).upper() in {'GOEDGEKEURD','AKKOORD','APPROVED','AFGEWEZEN'} for x in items)
    status='GEEN BESLUITPUNTEN' if not items else ('RODE BESLUITEN VEREIST' if red else ('ORANJE BESLUITEN VEREIST' if orange else 'AGENDA BEHEERST'))
    return {'treasury_board_pack_version':ENGINE_VERSION,'generated_at':now,'status':status,'treasury_score':tower.get('treasury_score'),'agenda_count':len(items),'open_count':open_count,'decided_count':decided,'red_open_count':red,'orange_open_count':orange,'agenda_items':items,'executive_summary':{'treasury_status':tower.get('status',calendar.get('status','')),'treasury_score':tower.get('treasury_score'),'next_12m_actions':calendar.get('action_count',0),'red_actions':calendar.get('red_action_count',0),'orange_actions':calendar.get('orange_action_count',0),'top_priority':items[0]['title'] if items else 'Geen urgente besluitpunten.'},'human_decision_required':open_count>0,'automatic_decision':False,'next_action':f"Agendeer {items[0]['title']} voor {items[0]['decision_authority']}." if items else 'Geen treasurybesluit nodig; blijf de kalender maandelijks actualiseren.'}
