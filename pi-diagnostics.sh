#!/bin/bash
# Jenkins Raspberry Pi Diagnostic Script

echo "===================================="
echo "🔍 JENKINS RASPBERRY PI DIAGNOSTICS"
echo "===================================="
echo "Date: $(date)"
echo ""

echo "📊 SYSTEM RESOURCES:"
echo "Memory usage:"
free -h
echo ""
echo "Disk usage:"
df -h
echo ""
echo "CPU load:"
uptime
echo ""

echo "🐳 JENKINS SERVICE STATUS:"
sudo systemctl status jenkins --no-pager || echo "Jenkins service not found"
echo ""

echo "📂 JENKINS HOME:"
echo "Jenkins home: ${JENKINS_HOME:-/var/jenkins_home}"
ls -la ${JENKINS_HOME:-/var/jenkins_home}/ 2>/dev/null || echo "Cannot access Jenkins home"
echo ""

echo "🔌 JENKINS PLUGINS:"
if [ -d "${JENKINS_HOME:-/var/jenkins_home}/plugins" ]; then
    echo "Checking key plugins..."
    ls ${JENKINS_HOME:-/var/jenkins_home}/plugins/ | grep -E "(pipeline|git|github)" || echo "Pipeline plugins not found"
else
    echo "Plugins directory not accessible"
fi
echo ""

echo "📝 JENKINS LOGS (last 20 lines):"
sudo journalctl -u jenkins --no-pager -n 20 || tail -20 /var/log/jenkins/jenkins.log 2>/dev/null || echo "Cannot access Jenkins logs"
echo ""

echo "🐍 PYTHON ENVIRONMENT:"
echo "Python3: $(which python3 2>/dev/null || echo 'Not found')"
echo "Python: $(which python 2>/dev/null || echo 'Not found')"
if command -v python3 &> /dev/null; then
    echo "Python3 version: $(python3 --version)"
    echo "Pip3: $(which pip3 2>/dev/null || echo 'Not found')"
fi
echo ""

echo "🌐 NETWORK & GIT:"
echo "Git version: $(git --version 2>/dev/null || echo 'Git not found')"
echo "Can reach GitHub:"
curl -s -I https://github.com | head -1 || echo "Cannot reach GitHub"
echo ""

echo "🔧 WORKSPACE CHECK:"
WORKSPACE="/var/jenkins_home/workspace/Python-Test-Pipeline"
if [ -d "$WORKSPACE" ]; then
    echo "Workspace exists: $WORKSPACE"
    echo "Files in workspace:"
    ls -la "$WORKSPACE"
    if [ -f "$WORKSPACE/Jenkinsfile" ]; then
        echo "Jenkinsfile found! First 10 lines:"
        head -10 "$WORKSPACE/Jenkinsfile"
    else
        echo "❌ Jenkinsfile NOT found in workspace"
    fi
else
    echo "❌ Workspace directory does not exist: $WORKSPACE"
fi
echo ""

echo "====================================="
echo "✅ DIAGNOSTIC COMPLETE"
echo "====================================="
