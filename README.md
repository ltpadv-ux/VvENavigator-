# VvE Navigator

Digitale VvE-platform voor Nederland.

## BuildFactory

De map `BuildFactory` bevat de Python-basis voor de VvE Navigator Master Engine.

### Huidige build

**0.2.0 — Core Engine foundation**

In deze build zitten:

- Finance/MJOP-basis voor kostenindexatie en NCW
- risicogestuurde onderhoudsprioriteit
- centrale Navigator-configuratie
- BuildFactory CLI met `init`, `doctor`, `version` en `status`
- eerste geautomatiseerde tests

### Starten

```bash
python BuildFactory/build.py init
python BuildFactory/build.py doctor
python BuildFactory/build.py version
python BuildFactory/build.py status
python -m pytest BuildFactory/tests
```

## Roadmap

1. MJOP Engine
2. Finance Engine: exploitatie, balans, cashflow en reservefonds
3. Risk Engine: NEN 2767 / risico-prioritering
4. Dashboard Engine met KPI's, VNI en MGI
5. Rapportage Engine voor bestuur en ALV
6. Power BI-export
7. Excel Master Workbook-koppeling
