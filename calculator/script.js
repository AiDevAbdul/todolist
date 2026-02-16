const display = document.getElementById('display');
const historyList = document.getElementById('history-list');
const buttons = document.querySelectorAll('.btn');

let currentExpression = '';
let history = [];

// Add click event listeners to all buttons
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.dataset.value;
        handleInput(value);
    });
});

// Add keyboard support
document.addEventListener('keydown', (e) => {
    const key = e.key;
    
    if (key >= '0' && key <= '9') handleInput(key);
    else if (key === '.') handleInput('.');
    else if (key === '+') handleInput('+');
    else if (key === '-') handleInput('-');
    else if (key === '*') handleInput('*');
    else if (key === '/') handleInput('/');
    else if (key === '%') handleInput('%');
    else if (key === 'Enter' || key === '=') handleInput('=');
    else if (key === 'Backspace') handleInput('backspace');
    else if (key === 'Escape') handleInput('C');
    else if (key === 'c' || key === 'C') handleInput('C');
});

function handleInput(value) {
    switch (value) {
        case 'C':
            clearAll();
            break;
        case 'CE':
            clearEntry();
            break;
        case '=':
            calculate();
            break;
        case 'backspace':
            backspace();
            break;
        default:
            appendValue(value);
    }
}

function appendValue(value) {
    // Prevent multiple operators in a row
    const operators = ['+', '-', '*', '/', '%'];
    if (operators.includes(value)) {
        const lastChar = currentExpression.slice(-1);
        if (operators.includes(lastChar)) {
            currentExpression = currentExpression.slice(0, -1) + value;
        } else {
            currentExpression += value;
        }
    } else {
        currentExpression += value;
    }
    updateDisplay();
}

function clearAll() {
    currentExpression = '';
    updateDisplay();
}

function clearEntry() {
    // Remove the last number entered
    const operators = ['+', '-', '*', '/', '%'];
    let lastOperatorIndex = -1;
    
    for (let i = currentExpression.length - 1; i >= 0; i--) {
        if (operators.includes(currentExpression[i])) {
            lastOperatorIndex = i;
            break;
        }
    }
    
    if (lastOperatorIndex >= 0) {
        currentExpression = currentExpression.slice(0, lastOperatorIndex + 1);
    } else {
        currentExpression = '';
    }
    updateDisplay();
}

function backspace() {
    currentExpression = currentExpression.slice(0, -1);
    updateDisplay();
}

async function calculate() {
    if (!currentExpression) return;
    
    try {
        const response = await fetch('http://localhost:5000/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: currentExpression }),
        });
        
        const data = await response.json();
        
        if (data.error) {
            display.value = 'Error';
        } else {
            // Add to history
            addToHistory(currentExpression, data.result);
            currentExpression = data.result.toString();
            updateDisplay();
        }
    } catch (error) {
        display.value = 'Error';
        console.error('Calculation error:', error);
    }
}

function addToHistory(expression, result) {
    history.unshift({ expression, result });
    if (history.length > 10) history.pop();
    renderHistory();
}

function renderHistory() {
    historyList.innerHTML = history.map(item => `
        <div class="history-item">
            <div class="history-expression">${item.expression}</div>
            <div class="history-result">= ${item.result}</div>
        </div>
    `).join('');
}

function updateDisplay() {
    display.value = currentExpression || '0';
}
