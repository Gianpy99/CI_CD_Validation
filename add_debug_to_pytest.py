#!/usr/bin/env python3
"""
Script per aggiungere debug JavaScript al report pytest
"""

import re
import sys

def add_debug_to_pytest_report(input_file, output_file):
    """Aggiunge codice di debug JavaScript al report pytest"""
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Debug JavaScript da inserire
        debug_js = '''
// =========================
// DEBUG CODE INJECTION
// =========================
console.log('[DEBUG] Starting pytest report debug injection...');

// Override console methods to show all messages
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;

console.log = function(...args) {
    const message = args.join(' ');
    originalLog.apply(console, args);
    if (window.debugDisplay) {
        debugDisplay.innerHTML += `<div style="color: blue;">[LOG] ${message}</div>`;
    }
};

console.error = function(...args) {
    const message = args.join(' ');
    originalError.apply(console, args);
    if (window.debugDisplay) {
        debugDisplay.innerHTML += `<div style="color: red;">[ERROR] ${message}</div>`;
    }
};

console.warn = function(...args) {
    const message = args.join(' ');
    originalWarn.apply(console, args);
    if (window.debugDisplay) {
        debugDisplay.innerHTML += `<div style="color: orange;">[WARN] ${message}</div>`;
    }
};

// Catch all errors
window.addEventListener('error', function(event) {
    const message = `Global Error: ${event.message} at ${event.filename}:${event.lineno}:${event.colno}`;
    console.error(message);
});

// Create debug display
window.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] DOM Content Loaded');
    
    // Create debug panel
    const debugPanel = document.createElement('div');
    debugPanel.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        width: 300px;
        max-height: 400px;
        background: white;
        border: 2px solid #007cba;
        padding: 10px;
        overflow-y: auto;
        z-index: 10000;
        font-family: monospace;
        font-size: 12px;
    `;
    debugPanel.innerHTML = '<h4>Debug Console</h4><button onclick="this.parentElement.style.display=\\'none\\'">Hide</button><div id="debug-messages"></div>';
    document.body.appendChild(debugPanel);
    
    window.debugDisplay = document.getElementById('debug-messages');
    
    console.log('[DEBUG] Debug panel created');
    
    // Test buttons immediately
    setTimeout(function() {
        console.log('[DEBUG] Testing buttons...');
        
        const showBtn = document.getElementById('show_all_details');
        const hideBtn = document.getElementById('hide_all_details');
        
        console.log(`[DEBUG] Show button: ${showBtn ? 'EXISTS' : 'NOT FOUND'}`);
        console.log(`[DEBUG] Hide button: ${hideBtn ? 'EXISTS' : 'NOT FOUND'}`);
        
        if (showBtn) {
            console.log(`[DEBUG] Show button innerHTML: "${showBtn.innerHTML}"`);
            console.log(`[DEBUG] Show button onclick: ${typeof showBtn.onclick}`);
            console.log(`[DEBUG] Show button listeners: checking...`);
            
            // Override the click method to add debug
            const originalClick = showBtn.click;
            showBtn.click = function() {
                console.log('[DEBUG] Show button click() called');
                return originalClick.call(this);
            };
            
            // Add debug click listener
            showBtn.addEventListener('click', function() {
                console.log('[DEBUG] Show button event listener triggered');
            }, true);
        }
        
        if (hideBtn) {
            console.log(`[DEBUG] Hide button innerHTML: "${hideBtn.innerHTML}"`);
            console.log(`[DEBUG] Hide button onclick: ${typeof hideBtn.onclick}`);
            
            const originalClick = hideBtn.click;
            hideBtn.click = function() {
                console.log('[DEBUG] Hide button click() called');
                return originalClick.call(this);
            };
            
            hideBtn.addEventListener('click', function() {
                console.log('[DEBUG] Hide button event listener triggered');
            }, true);
        }
        
        // Check for manager object
        if (typeof manager !== 'undefined') {
            console.log('[DEBUG] Manager object exists');
            console.log(`[DEBUG] Manager type: ${typeof manager}`);
            
            // Override manager.allCollapsed setter
            if (manager && typeof manager === 'object') {
                console.log('[DEBUG] Adding debug to manager');
                
                const originalDescriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(manager), 'allCollapsed');
                if (originalDescriptor && originalDescriptor.set) {
                    Object.defineProperty(manager, 'allCollapsed', {
                        set: function(value) {
                            console.log(`[DEBUG] manager.allCollapsed set to: ${value}`);
                            return originalDescriptor.set.call(this, value);
                        },
                        get: originalDescriptor.get,
                        configurable: true
                    });
                }
            }
        } else {
            console.log('[DEBUG] Manager object NOT found');
        }
        
        // Check collapsible elements
        const collapsibles = document.querySelectorAll('.collapsible');
        console.log(`[DEBUG] Found ${collapsibles.length} collapsible elements`);
        
        collapsibles.forEach((el, index) => {
            console.log(`[DEBUG] Collapsible ${index}: display=${el.style.display}, classes=${el.className}`);
        });
        
    }, 1000);
});

// =========================
// END DEBUG CODE INJECTION
// =========================
'''
        
        # Find the end of the existing script tag and insert debug code before it
        script_end = content.rfind('</script>')
        if script_end != -1:
            new_content = content[:script_end] + debug_js + content[script_end:]
        else:
            # If no script tag found, add it before </body>
            body_end = content.rfind('</body>')
            if body_end != -1:
                new_content = content[:body_end] + f'<script>{debug_js}</script>' + content[body_end:]
            else:
                new_content = content + f'<script>{debug_js}</script>'
        
        # Write the modified content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Debug code added successfully!")
        print(f"Input: {input_file}")
        print(f"Output: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    input_file = "pytest-report-debug.html"
    output_file = "pytest-report-with-debug.html"
    
    success = add_debug_to_pytest_report(input_file, output_file)
    if success:
        print("\\nTo test the debug version:")
        print(f"1. Open {output_file} in your browser")
        print("2. Check the debug panel on the top-right")
        print("3. Try clicking the 'Show all details' and 'Hide all details' buttons")
        print("4. Watch the debug messages to see what happens")
    else:
        print("Failed to add debug code")
