function addRule() {
    const container = document.getElementById('rulesContainer');
    const ruleDiv = document.createElement('div');
    ruleDiv.className = 'rule-input mb-2';
    ruleDiv.innerHTML = `
        <div class="row">
            <div class="col-5">
                <input type="text" class="form-control premise" placeholder="Premise">
            </div>
            <div class="col-2 text-center">→</div>
            <div class="col-5">
                <input type="text" class="form-control conclusion" placeholder="Conclusion">
            </div>
        </div>
    `;
    container.appendChild(ruleDiv);
}

function loadExample() {
    document.getElementById('axioms').value = 'human(socrates)\\nmortal(X)';
    document.getElementById('facts').value = 'human(socrates)';
    document.getElementById('theorem').value = 'mortal(socrates)';
    
    // Clear existing rules and add example rule
    document.getElementById('rulesContainer').innerHTML = `
        <div class="rule-input mb-2">
            <div class="row">
                <div class="col-5">
                    <input type="text" class="form-control premise" placeholder="Premise" value="human(X)">
                </div>
                <div class="col-2 text-center">→</div>
                <div class="col-5">
                    <input type="text" class="form-control conclusion" placeholder="Conclusion" value="mortal(X)">
                </div>
            </div>
        </div>
    `;
}

document.getElementById('theoremForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const axioms = document.getElementById('axioms').value.split(/\r?\n/).filter(a => a.trim());
    const facts = document.getElementById('facts').value.split(/\r?\n/).filter(f => f.trim());

    const theorem = document.getElementById('theorem').value.trim();
    
    // Collect rules
    const rules = [];
    document.querySelectorAll('.rule-input').forEach(ruleDiv => {
        const premise = ruleDiv.querySelector('.premise').value.trim();
        const conclusion = ruleDiv.querySelector('.conclusion').value.trim();
        if (premise && conclusion) {
            rules.push({premise, conclusion});
        }
    });
    
    const requestData = {
        axioms: axioms,
        rules: rules,
        facts: facts,
        theorem: theorem
    };
    
    try {
        const response = await fetch('/prove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        displayResult(result);
    } catch (error) {
        displayResult({
            success: false,
            message: 'Error connecting to server: ' + error.message
        });
    }
});

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    
    if (result.success) {
        let html = `<div class="success-message">
            <strong>✅ ${result.message}</strong>
        </div>`;
        
        if (result.proof_trace && result.proof_trace.length > 0) {
            html += '<h6 class="mt-3">Proof Steps:</h6>';
            result.proof_trace.forEach((step, index) => {
                html += `<div class="proof-step">
                    <strong>Step ${index + 1}:</strong> ${step.goal}<br>
                    <small><em>Method: ${step.method}</em></small>
                    ${step.details ? `<br><small>Details: ${step.details}</small>` : ''}
                </div>`;
            });
        }
        
        resultDiv.innerHTML = html;
    } else {
        resultDiv.innerHTML = `<div class="error-message">
            <strong>❌ ${result.message}</strong>
            ${result.error ? `<br><small>Error: ${result.error}</small>` : ''}
        </div>`;
    }
}