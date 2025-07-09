# CI/CD Validation Project

Questo è un progetto per testare e validare una toolchain CI/CD completa con Jenkins.

## 📋 Funzionalità

- **Applicazione**: Calcolatrice Python con funzioni matematiche di base
- **Test automatici**: Test unitari completi con unittest e pytest
- **Code coverage**: Analisi della copertura del codice
- **Quality checks**: Controlli di qualità del codice con flake8
- **Artefatti**: Generazione e archiviazione di artefatti della build
- **Deployment**: Simulazione di deploy in ambiente staging

## 🚀 Pipeline CI/CD

La pipeline Jenkins include i seguenti stage:

1. **Checkout** - Clone del repository
2. **Setup Environment** - Installazione dipendenze Python
3. **Code Quality Check** - Controlli di qualità con flake8
4. **Test** - Esecuzione test con coverage
5. **Build Artifact** - Creazione artefatti della build
6. **Deploy to Staging** - Deploy automatico su branch main

## 📊 Reporting e Outcome

La pipeline ora genera i seguenti output e report:

### Test Results
- **JUnit XML**: Report strutturato dei test (`test-results.xml`)
- **Coverage Report**: Report HTML interattivo della copertura del codice
- **Coverage XML**: Report XML per integrazione con altri tools

### Code Quality
- **Flake8 Report**: Analisi della qualità del codice (`flake8-report.txt`)

### Build Artifacts
- **Application Package**: Pacchetto tar.gz dell'applicazione (`app-{BUILD_NUMBER}.tar.gz`)
- **Build Info**: Informazioni dettagliate della build (commit, branch, timestamp)
- **Deployment Log**: Log delle operazioni di deploy

### Dashboard Jenkins
Nella dashboard Jenkins potrai vedere:
- ✅ **Build Status**: Stato di successo/fallimento di ogni build
- 📊 **Test Trends**: Trend dei test nel tempo
- 📈 **Coverage Trends**: Evoluzione della copertura del codice
- 📦 **Artifacts**: Download degli artefatti generati
- 📋 **Console Output**: Log dettagliato di ogni stage

## 🛠️ Requisiti

```bash
# Installa le dipendenze
pip install -r requirements.txt
```

## 🧪 Esecuzione Test Locale

```bash
# Test con unittest
python -m unittest test_app.py

# Test con pytest e coverage
python -m pytest test_app_pytest.py --cov=app --cov-report=html

# Code quality check
python -m flake8 app.py test_app.py
```

## 📁 Struttura Progetto

```
├── app.py                 # Applicazione principale
├── test_app.py           # Test unittest
├── test_app_pytest.py    # Test pytest
├── requirements.txt      # Dipendenze Python
├── setup.cfg            # Configurazione pytest/coverage
├── Jenkinsfile          # Pipeline CI/CD
└── README.md            # Questa documentazione
```

## 🔄 Workflow di Sviluppo

1. **Sviluppo**: Modifica il codice in `app.py`
2. **Test**: Aggiungi/aggiorna test in `test_app.py`
3. **Commit**: Fai commit delle modifiche
4. **Trigger**: Jenkins avvia automaticamente la pipeline
5. **Review**: Controlla i risultati nella dashboard Jenkins
6. **Deploy**: Se i test passano, l'app viene deployata in staging

## 📈 Metriche e KPI

La pipeline ora traccia:
- **Build Success Rate**: Percentuale di build riuscite
- **Test Coverage**: Percentuale di codice coperto dai test
- **Code Quality Score**: Punteggio qualità codice (flake8)
- **Build Duration**: Tempo di esecuzione della pipeline
- **Deployment Frequency**: Frequenza dei deploy
