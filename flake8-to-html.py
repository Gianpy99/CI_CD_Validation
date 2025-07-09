#!/usr/bin/env python3
"""
Script per convertire i report flake8 in HTML formattato
Dimostra come i report possono essere utilizzati e personalizzati
"""

import sys
import re
from datetime import datetime

def convert_flake8_to_html(input_file, output_file):
    """Converte un report flake8 testuale in HTML formattato"""
    
    html_header = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flake8 Code Quality Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .error {{ background: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 5px 0; }}
        .warning {{ background: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 5px 0; }}
        .filename {{ font-weight: bold; color: #1976d2; }}
        .code {{ font-family: monospace; background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #1976d2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Flake8 Code Quality Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Purpose:</strong> Analisi automatica della qualità del codice Python</p>
    </div>
"""

    html_footer = """
    <div class="summary">
        <h3>📊 Utilizzi di questo Report:</h3>
        <ul>
            <li><strong>CI/CD Pipeline:</strong> Quality gate automatici</li>
            <li><strong>Code Review:</strong> Identificazione problemi prima del merge</li>
            <li><strong>Monitoring:</strong> Tracking della qualità del codice nel tempo</li>
            <li><strong>Training:</strong> Educazione del team su standard di codice</li>
            <li><strong>Compliance:</strong> Dimostrazione aderenza a standard aziendali</li>
        </ul>
    </div>
    
    <div class="summary">
        <h3>🔧 Come Migliorare:</h3>
        <ul>
            <li><strong>E302:</strong> Aggiungi 2 righe vuote tra funzioni</li>
            <li><strong>W293:</strong> Rimuovi spazi da righe vuote</li>
            <li><strong>E501:</strong> Spezza righe lunghe (&gt;79 caratteri)</li>
            <li><strong>E305:</strong> Aggiungi 2 righe vuote dopo classi/funzioni</li>
        </ul>
    </div>
    
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>🚀 Questo report è generato automaticamente dalla pipeline Jenkins per garantire la qualità del codice.</p>
    </footer>
</body>
</html>"""

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ File {input_file} non trovato!")
        return False

    # Analizza gli errori
    errors = []
    warnings = []
    files = set()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse formato: filename:line:col: code message
        match = re.match(r'(.+?):(\d+):(\d+):\s+([EW]\d+)\s+(.+)', line)
        if match:
            filename, line_num, col_num, code, message = match.groups()
            files.add(filename)
            
            entry = {
                'file': filename,
                'line': line_num,
                'col': col_num,
                'code': code,
                'message': message
            }
            
            if code.startswith('E'):
                errors.append(entry)
            else:
                warnings.append(entry)

    # Genera statistiche
    total_issues = len(errors) + len(warnings)
    stats_html = f"""
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{len(files)}</div>
            <div>File Analizzati</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(errors)}</div>
            <div>Errori</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(warnings)}</div>
            <div>Warning</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_issues}</div>
            <div>Problemi Totali</div>
        </div>
    </div>
    """

    # Genera HTML per errori e warning
    issues_html = ""
    
    if errors:
        issues_html += "<h3>🚨 Errori (E-codes)</h3>\n"
        for error in errors:
            issues_html += f"""
            <div class="error">
                <span class="filename">{error['file']}</span> 
                linea {error['line']}, colonna {error['col']}: 
                <span class="code">{error['code']}</span> - {error['message']}
            </div>
            """
    
    if warnings:
        issues_html += "<h3>⚠️ Warning (W-codes)</h3>\n"
        for warning in warnings:
            issues_html += f"""
            <div class="warning">
                <span class="filename">{warning['file']}</span> 
                linea {warning['line']}, colonna {warning['col']}: 
                <span class="code">{warning['code']}</span> - {warning['message']}
            </div>
            """

    if total_issues == 0:
        issues_html = """
        <div class="summary">
            <h3>✅ Ottimo Lavoro!</h3>
            <p>Nessun problema di stile trovato. Il codice rispetta tutti gli standard flake8!</p>
        </div>
        """

    # Scrivi il file HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_header)
        f.write(stats_html)
        f.write(issues_html)
        f.write(html_footer)
    
    print(f"✅ Report HTML generato: {output_file}")
    print(f"📊 Statistiche: {len(errors)} errori, {len(warnings)} warning, {len(files)} file")
    return True

if __name__ == "__main__":
    input_file = "flake8-report.txt"
    output_file = "flake8-report-enhanced.html"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"🔄 Convertendo {input_file} -> {output_file}")
    success = convert_flake8_to_html(input_file, output_file)
    
    if success:
        print(f"🌐 Apri il file nel browser: file://{output_file}")
        print("\n📋 Questo dimostra come i report flake8 possono essere:")
        print("  • Convertiti in formati visuali accattivanti")
        print("  • Integrati in dashboard di monitoraggio")
        print("  • Utilizzati per training e documentazione")
        print("  • Archiviati come artifact in Jenkins/CI")
    else:
        sys.exit(1)
