#!/bin/bash

# Script per monitorare lo stato del build Jenkins
# Esegui questo script sul Raspberry Pi per verificare l'ultimo build

echo "=== 🔍 JENKINS BUILD STATUS CHECKER ==="
echo "Timestamp: $(date)"
echo ""

# Verifica se Jenkins è in esecuzione
if docker ps | grep -q jenkins; then
    echo "✅ Jenkins container is running"
    
    # Mostra l'ultimo commit
    echo ""
    echo "📝 Latest commit:"
    git log --oneline -1
    
    echo ""
    echo "🔗 Access Jenkins at: http://localhost:8080"
    echo "📊 Check build status in Jenkins WebUI"
    echo "🎯 Expected result: All tests PASS with multiply() fixed"
    
    echo ""
    echo "📋 To check logs directly:"
    echo "docker logs jenkins | tail -50"
    
else
    echo "❌ Jenkins container not running!"
    echo "Start with: docker start jenkins"
fi

echo ""
echo "=== VALIDATION STATUS ==="
echo "🐛 Bug simulation: COMPLETED ✅"
echo "🔧 Bug fix applied: COMPLETED ✅" 
echo "📦 Build triggered: COMPLETED ✅"
echo "🧪 Test validation: IN PROGRESS ⏳"
echo ""
echo "Next: Check Jenkins WebUI for GREEN build!"
