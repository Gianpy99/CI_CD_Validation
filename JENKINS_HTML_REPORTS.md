# 📊 Jenkins HTML Reports Guide

## 🎯 Report HTML Disponibili

Il nostro pipeline Jenkins genera diversi report HTML interattivi che vengono archiviati come **Build Artifacts** e sono disponibili per il download:

### 1. 🧪 Report dei Test (pytest-report.html)
- **Percorso**: `test-reports/pytest-report.html`
- **Contenuto**: 
  - Risultati dettagliati di tutti i test pytest
  - Tempi di esecuzione per ogni test
  - Stack trace completi per i test falliti
  - Statistiche riassuntive dei test
- **Formato**: Self-contained HTML (include CSS/JS inline)

### 2. 📈 Report di Coverage (htmlcov/index.html)
- **Percorso**: `test-reports/htmlcov/index.html`
- **Contenuto**:
  - Percentuale di copertura del codice per file
  - Visualizzazione delle righe coperte/non coperte
  - Report navigabile per ogni file sorgente
  - Metriche dettagliate di coverage
- **Formato**: HTML multipagina con navigazione

### 3. 🔍 Report di Code Quality (flake8-report.html)
- **Percorso**: `flake8-report.html`
- **Contenuto**:
  - Violazioni di stile del codice
  - Warning e errori di linting
  - Posizione esatta dei problemi nel codice
- **Formato**: HTML semplice

## 🚀 Come Accedere ai Report

### Metodo 1: Download dai Build Artifacts
1. Vai alla pagina del build Jenkins
2. Clicca su **"Build Artifacts"** nella barra laterale
3. Naviga nella cartella `test-reports/`
4. Scarica i file HTML che ti interessano:
   - `pytest-report.html` 
   - `htmlcov/index.html` (e tutti i file nella cartella htmlcov/)
   - `flake8-report.html`
5. Apri i file scaricati nel tuo browser

### Metodo 2: Link Diretto (se plugin HTML Publisher disponibile)
Se il plugin HTML Publisher è installato in Jenkins, vedrai anche link diretti:
- **"Pytest HTML Report"** - per i risultati dei test
- **"Coverage HTML Report"** - per il coverage del codice

## 📋 Contenuti dei Report

### Pytest Report Features:
- ✅ Lista di tutti i test eseguiti
- ⏱️ Tempo di esecuzione per ogni test
- 📊 Statistiche riassuntive (passed/failed/skipped)
- 🔍 Dettagli completi degli errori
- 🎨 Interfaccia web moderna e interattiva

### Coverage Report Features:
- 📈 Percentuale di copertura globale
- 📂 Coverage per ogni file del progetto
- 🔍 Visualizzazione line-by-line del codice
- 🎯 Identificazione di righe non testate
- 📊 Grafici e metriche dettagliate

### Flake8 Report Features:
- 🔍 Violazioni di PEP8 e standard Python
- ⚠️ Warning e errori di sintassi
- 📍 Posizione esatta dei problemi
- 🔧 Suggerimenti per la risoluzione

## 🛠️ Automatizzazione

Questi report vengono generati automaticamente ad ogni build e sono sempre disponibili tramite:
- **Build Artifacts** ✅ (sempre disponibile)
- **HTML Publisher** ⚠️ (se plugin installato)

## 💡 Best Practices

1. **Controlla sempre** i report HTML dopo ogni build
2. **Scarica e conserva** i report per build importanti
3. **Condividi** i report con il team per review
4. **Usa i report** per identificare aree di miglioramento nel codice
5. **Monitora** le tendenze di coverage nel tempo

## 🔧 Risoluzione Problemi

### Se i report HTML non vengono generati:
1. Verifica che `pytest-html` sia installato: `pip install pytest-html`
2. Controlla che `coverage` sia installato: `pip install coverage`
3. Verifica i log del build Jenkins per errori di generazione report

### Se i report non sono scaricabili:
1. Verifica che il stage "Test" sia completato con successo
2. Controlla che la cartella `test-reports/` sia stata creata
3. Verifica i permessi sui file nel workspace Jenkins

---

**📌 Nota**: Questo sistema garantisce che i report siano sempre disponibili come artifact, indipendentemente dalla disponibilità di plugin aggiuntivi in Jenkins.
