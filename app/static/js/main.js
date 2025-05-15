document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, находимся ли мы на странице калькулятора
    const calculatorForm = document.getElementById('calculator-form');
    if (!calculatorForm) return;
    
    // Генерируем форму в зависимости от типа продукции
    generateForm(productType);
    
    // Добавляем обработчик для кнопки расчета
    const calculateButton = document.getElementById('calculate-button');
    if (calculateButton) {
        calculateButton.addEventListener('click', calculatePrice);
    }
});

function generateForm(productType) {
    const formContainer = document.getElementById('calculator-form');
    if (!formContainer) return;
    
    let formHTML = '';
    
    switch (productType) {
        case 'business_cards':
            formHTML = `
                <div class="form-group">
                    <label for="quantity">Тираж (шт)</label>
                    <input type="number" id="quantity" name="quantity" value="100" min="10" step="10">
                </div>
                <div class="form-group">
                    <label for="paper_type">Тип бумаги</label>
                    <select id="paper_type" name="paper_type">
                        <option value="offset_250">Офсетная 250 г/м²</option>
                        <option value="offset_300">Офсетная 300 г/м²</option>
                        <option value="coated_300">Мелованная 300 г/м²</option>
                        <option value="premium_350">Премиум 350 г/м²</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="color_scheme">Цветность</label>
                    <select id="color_scheme" name="color_scheme">
                        <option value="4+0">4+0 (цвет с одной стороны)</option>
                        <option value="4+4">4+4 (цвет с двух сторон)</option>
                        <option value="1+0">1+0 (ч/б с одной стороны)</option>
                        <option value="1+1">1+1 (ч/б с двух сторон)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Дополнительная обработка</label>
                    <div class="form-group">
                        <label for="lamination">Ламинация</label>
                        <select id="lamination" name="lamination">
                            <option value="">Без ламинации</option>
                            <option value="gloss_1">Глянцевая с одной стороны</option>
                            <option value="gloss_2">Глянцевая с двух сторон</option>
                            <option value="matte_1">Матовая с одной стороны</option>
                            <option value="matte_2">Матовая с двух сторон</option>
                            <option value="soft_touch_1">Софт-тач с одной стороны</option>
                            <option value="soft_touch_2">Софт-тач с двух сторон</option>
                        </select>
                    </div>
                    <div>
                        <input type="checkbox" id="corners" name="corners">
                        <label for="corners">Скругление углов</label>
                    </div>
                </div>
                <div class="form-group">
                    <label for="urgency">Срочность</label>
                    <select id="urgency" name="urgency">
                        <option value="standard">Стандартная (3-5 дней)</option>
                        <option value="urgent">Срочная (1-2 дня, +30%)</option>
                        <option value="express">Экспресс (в тот же день, +60%)</option>
                    </select>
                </div>
            `;
            break;
            
        case 'flyers':
            formHTML = `
                <div class="form-group">
                    <label for="quantity">Тираж (шт)</label>
                    <input type="number" id="quantity" name="quantity" value="100" min="10" step="10">
                </div>
                <div class="form-group">
                    <label for="size">Формат</label>
                    <select id="size" name="size">
                        <option value="A6">A6 (105×148 мм)</option>
                        <option value="A5">A5 (148×210 мм)</option>
                        <option value="A4" selected>A4 (210×297 мм)</option>
                        <option value="A3">A3 (297×420 мм)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="paper_type">Тип бумаги</label>
                    <select id="paper_type" name="paper_type">
                        <option value="offset_130">Офсетная 130 г/м²</option>
                        <option value="offset_170">Офсетная 170 г/м²</option>
                        <option value="coated_130" selected>Мелованная 130 г/м²</option>
                        <option value="coated_170">Мелованная 170 г/м²</option>
                        <option value="coated_300">Мелованная 300 г/м²</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="color_scheme">Цветность</label>
                    <select id="color_scheme" name="color_scheme">
                        <option value="4+0">4+0 (цвет с одной стороны)</option>
                        <option value="4+4" selected>4+4 (цвет с двух сторон)</option>
                        <option value="1+0">1+0 (ч/б с одной стороны)</option>
                        <option value="1+1">1+1 (ч/б с двух сторон)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="urgency">Срочность</label>
                    <select id="urgency" name="urgency">
                        <option value="standard">Стандартная (3-5 дней)</option>
                        <option value="urgent">Срочная (1-2 дня, +30%)</option>
                        <option value="express">Экспресс (в тот же день, +60%)</option>
                    </select>
                </div>
            `;
            break;
            
        // Здесь будут добавлены формы для других типов продукции
            
        default:
            formHTML = '<p>Выберите тип продукции для расчета</p>';
    }
    
    formContainer.innerHTML = formHTML;
}

function calculatePrice() {
    // Собираем данные формы
    const formData = {};
    
    // Получаем значения всех полей ввода
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            formData[input.name] = input.checked;
        } else if (input.type === 'number') {
            formData[input.name] = parseInt(input.value);
        } else {
            formData[input.name] = input.value;
        }
    });
    
    // Отправляем запрос на API для расчета
    fetch(`/api/calculate/${productType}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('price').textContent = data.price.toLocaleString('ru-RU');
        } else {
            alert('Ошибка при расчете: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при отправке запроса');
    });
}