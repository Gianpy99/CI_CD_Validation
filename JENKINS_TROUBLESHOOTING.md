# 🚨 JENKINS PIPELINE TROUBLESHOOTING GUIDE

## PROBLEMA IDENTIFICATO
Jenkins esegue solo il Git checkout ma NON esegue le fasi del pipeline.
Risultato: Sempre "SUCCESS" anche quando dovrebbe fallire.

## ⚠️ RISCHIO SICUREZZA
Senza test execution, codice buggy può andare in produzione!

## 🔍 CHECKLIST CONFIGURAZIONE JENKINS

### 1. VERIFICA TIPO DI JOB
- [ ] Accedi alla dashboard Jenkins
- [ ] Vai al job "Python-Test-Pipeline" 
- [ ] Clicca "Configure"
- [ ] Verifica che sia un "Pipeline" job, NON:
  - ❌ Freestyle project
  - ❌ Multi-configuration project
  - ❌ Altri tipi

### 2. VERIFICA PIPELINE CONFIGURATION
- [ ] Nella sezione "Pipeline":
  - Definition: dovrebbe essere "Pipeline script from SCM"
  - SCM: dovrebbe essere "Git"
  - Repository URL: https://github.com/Gianpy99/CI_CD_Validation.git
  - Script Path: "Jenkinsfile" (default)

### 3. VERIFICA PLUGIN JENKINS
Vai in "Manage Jenkins" > "Manage Plugins" e verifica che siano installati:
- [ ] Pipeline plugin
- [ ] Pipeline: Stage View Plugin
- [ ] Git plugin
- [ ] GitHub plugin
- [ ] Pipeline: Groovy Plugin

### 4. VERIFICA LOG COMPLETO
- [ ] Vai al build che ha fallito
- [ ] Clicca "Console Output"
- [ ] Controlla se ci sono errori come:
  - "No such file: Jenkinsfile"
  - "Pipeline script not found"
  - "Plugin not found"
  - Errori di parsing Groovy

### 5. VERIFICA PERMESSI RASPBERRY PI
- [ ] SSH al Raspberry Pi
- [ ] Controlla spazio disco: `df -h`
- [ ] Controlla memoria: `free -h`
- [ ] Controlla log Jenkins: `sudo journalctl -u jenkins`

## 🛠️ SOLUZIONI RAPIDE

### Se Jenkins non esegue il pipeline:
1. **Ricrea il job come Pipeline**:
   - New Item > Pipeline
   - Nome: Python-Test-Pipeline-New
   - Pipeline from SCM > Git
   - Repo: https://github.com/Gianpy99/CI_CD_Validation.git

2. **Installa plugin mancanti**:
   ```bash
   # Nel container Jenkins o Raspberry Pi
   sudo systemctl restart jenkins
   ```

3. **Verifica Jenkinsfile syntax**:
   - Usa "Pipeline Syntax" helper nella dashboard

### Se tutto sembra configurato correttamente:
**Il problema potrebbe essere risorse Raspberry Pi**:
- Memoria insufficiente
- Storage pieno
- Jenkins in crash silenzioso

## 📞 PROSSIMI PASSI
1. Controlla la configurazione del job Jenkins
2. Verifica i plugin installati
3. Guarda il console output completo
4. Se necessario, ricrea il job come Pipeline

## 🎯 OBIETTIVO
Dobbiamo vedere questo nel log Jenkins:
```
[Pipeline] Start of Pipeline
[Pipeline] stage
[Pipeline] { (Test Basic Execution)
[Pipeline] echo
🚀 Testing if Jenkins can execute pipeline stages...
[Pipeline] sh
+ echo Current working directory: /var/jenkins_home/workspace/Python-Test-Pipeline
...
[Pipeline] stage
[Pipeline] { (Force Failure Test)
[Pipeline] echo  
🧪 Testing if Jenkins can detect failures...
[Pipeline] sh
+ exit 1
[Pipeline] End of Pipeline
ERROR: script returned exit code 1
Finished: FAILURE
```

NON questo (che è quello che vediamo ora):
```
Checking out Revision...
Finished: SUCCESS
```
