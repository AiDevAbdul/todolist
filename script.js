function display(val) {
    document.getElementById('result').value += val;
}

function calculate() {
    let x = document.getElementById('result').value;
    let y = eval(x);
    document.getElementById('result').value = y;
}

function clearScreen() {
    document.getElementById('result').value = '';
}

function deleteChar() {
    let x = document.getElementById('result').value;
    document.getElementById('result').value = x.substring(0, x.length - 1);
}