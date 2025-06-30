// mathFunctions.js
function calculateFormula() {
    const a = parseFloat(document.getElementById('inputA').value);
    const b = parseFloat(document.getElementById('inputB').value);
    const outputDiv = document.getElementById('outputFormula');
    
    try {
        const result = customMathFunction(a, b);
        outputDiv.innerHTML = `<p>Результат вычисления: ${result}</p>`;
    } catch (error) {
        outputDiv.innerHTML = '';
        alert(error.message);
    }
}

function customMathFunction(a, b) {
    // Первый случай: a > 5, b > 0
    if (a > 5 && b > 0) {
        if (a === 0) {
            throw new Error('Ошибка: деление на ноль (a = 0)');
        }
        return 3*(a*a);
    }
    // Второй случай: 0 < a ≤ 5, b ≠ 0
    else if (a > 0 && a <= 5 && b !== 0) {
        if (b === 0) {
            throw new Error('Ошибка: деление на ноль (b = 0)');
        }
        return a/b;
    }
    // Третий случай: другие варианты
    else {
        if (b === 0) {
            throw new Error('Ошибка: деление на ноль (b = 0)');
        }
        return b+a-1;
    }
}

// scripts.js
function stringOperations() {
    // 1. Создание строковых переменных
    const S1 = "Уланович"; // Ваша фамилия
    const S2 = "АДРЕС";
    
    // Обновляем отображение строк
    document.getElementById('s1Value').textContent = `S1: ${S1}`;
    document.getElementById('s2Value').textContent = `S2: ${S2}`;
    
    // 2. Выполнение операций
    const results = [];
    
    // 1. Определить длину строки S2
    const lengthS2 = S2.length;
    results.push(`1. Длина S2: ${lengthS2}`);
    
    // 2. Выполнить сцепление строк S1 и S2
    const concatenated = S1 + S2;
    results.push(`2. Сцепление: "${concatenated}"`);
    
    // 3. Преобразовать строку S2 в нижний регистр
    const lowerS2 = S2.toLowerCase();
    results.push(`3. S2 в нижнем регистре: "${lowerS2}"`);
    
    // Вывод результатов
    document.getElementById('stringResults').innerHTML = results.join('<br>');
}