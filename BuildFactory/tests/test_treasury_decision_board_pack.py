from src.treasury_decision_board_pack import build_treasury_decision_board_pack

def test_no_items_when_calendar_green():
    x=build_treasury_decision_board_pack({'status':'GROEN','actions':[]},{'treasury_score':95,'status':'GROEN'})
    assert x['status']=='GEEN BESLUITPUNTEN'
    assert x['agenda_count']==0

def test_red_and_orange_become_agenda_items():
    cal={'status':'ROOD','action_count':2,'red_action_count':1,'orange_action_count':1,'actions':[
      {'month':'2026-11','category':'LIQUIDITEIT','severity':'ROOD','title':'VvE A: negatieve kas verwacht','detail':'Kas onder nul','decision_authority':'Bestuur/ALV'},
      {'month':'2026-12','category':'HERFINANCIERING','severity':'ORANJE','title':'VvE B: herfinanciering voorbereiden','detail':'Marktcheck starten','decision_authority':'Bestuur/ALV'}]}
    x=build_treasury_decision_board_pack(cal,{'treasury_score':62,'status':'ORANJE'})
    assert x['status']=='RODE BESLUITEN VEREIST'
    assert x['agenda_count']==2
    assert x['agenda_items'][0]['agenda_id'].startswith('TRAGEN-')
    assert x['agenda_items'][0]['draft_decision']

def test_existing_decision_state_is_preserved():
    cal={'actions':[{'month':'2026-11','category':'DSCR','severity':'ROOD','title':'VvE A: DSCR aandacht','detail':'DSCR 1.1','decision_authority':'Bestuur/ALV'}]}
    first=build_treasury_decision_board_pack(cal)
    first['agenda_items'][0].update(decision='GOEDGEKEURD',owner='Penningmeester',status='GESLOTEN')
    second=build_treasury_decision_board_pack(cal,existing=first)
    assert second['agenda_items'][0]['decision']=='GOEDGEKEURD'
    assert second['agenda_items'][0]['owner']=='Penningmeester'
    assert second['open_count']==0
