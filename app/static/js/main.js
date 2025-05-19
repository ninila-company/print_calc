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
    
    // Добавляем кнопку сброса
    let resetButton = document.getElementById('reset-button');
    if (!resetButton) {
        resetButton = document.createElement('button');
        resetButton.id = 'reset-button';
        resetButton.className = 'btn';
        resetButton.type = 'button';
        resetButton.textContent = 'Сбросить';
        resetButton.style.marginLeft = '10px';
        calculateButton.parentNode.insertBefore(resetButton, calculateButton.nextSibling);
    }
    resetButton.addEventListener('click', function() {
        generateForm(productType);
        document.getElementById('price').textContent = '0';
        let perCard = document.getElementById('price_per_card');
        if (perCard) perCard.remove();
    });
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
                    <input type="number" id="quantity" name="quantity" value="48" min="48" step="12">
                </div>
                <div class="form-group">
                    <label for="paper_type">Тип бумаги</label>
                    <select id="paper_type" name="paper_type">
                        <option value="offset_300">Мелованная 300 г/м²</option>
                        <option value="color_copy_300">Color Copy 300 г/м²</option>
                        <option value="color_copy_350">Color Copy 350 г/м²</option>
                        <option value="color_copy_400">Color Copy 400 г/м²</option>
                        <option value="carton_270">Картон 270 г/м²</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="color_scheme">Цветность</label>
                    <select id="color_scheme" name="color_scheme">
                        <option value="4+0">4+0 (цвет с одной стороны)</option>
                        <option value="4+4">4+4 (цвет с двух сторон)</option>
                        <option value="4+1">4+1 (цвет с одной стороны, ч/б с другой)</option>
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
                            <option value="gloss_32">Глянцевая 32 мкр</option>
                            <option value="matte_32">Матовая 32 мкр</option>
                            <option value="matte_32_anti">Матовая 32 мкр антивандальная</option>
                            <option value="gloss_75">Глянцевая 75 мкр</option>
                            <option value="matte_75">Матовая 75 мкр</option>
                            <option value="gloss_150">Глянцевая 150 мкр</option>
                            <option value="gloss_250">Глянцевая 250 мкр</option>
                            <option value="matte_250">Матовая 250 мкр</option>
                            <option value="soft_touch_1">Soft Touch</option>
                            <option value="soft_touch_2">Soft Touch цифра</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="scratch_sticker">Скретч-наклейка</label>
                        <select id="scratch_sticker" name="scratch_sticker">
                            <option value="">Без скретч-наклейки</option>
                            <option value="standart">Стандартная</option>
                            <option value="13x42">13 на 42</option>
                            <option value="18x40">18 на 40</option>
                            <option value="30x30">30 на 30</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="uf_print">УФ-печать</label>
                        <select id="uf_print" name="uf_print">
                            <option value="">Без уф-печати</option>
                            <option value="color_4">УФ 4 цвета</option>
                            <option value="uf_belila_from_50">УФ белила от 50%</option>
                            <option value="uf_belila_to_50">УФ белила до 50%</option>
                            <option value="uf_lak_from_50">УФ лак от 50%</option>
                            <option value="uf_lak_to_50">УФ лак до 50%</option>
                        </select>
                    </div>
                     <div>
                        <input type="checkbox" id="corners" name="corners">
                        <label for="corners" class="checkbox-label">Скругление углов</label>
                    </div>
                    <div>
                        <input type="checkbox" id="tech_hole" name="tech_hole">
                        <label for="tech_hole" class="checkbox-label">Технологическое отверстие</label>
                    </div>
                    <div>
                        <input type="checkbox" id="mark_mifare" name="mark_mifare">
                        <label for="mark_mifare" class="checkbox-label">Метка Mifare 1K</label>
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
                <div class="form-group">
                    <label for="discount">Скидка (%)</label>
                    <input type="number" id="discount" name="discount" min="0" max="100" step="1" placeholder="0">
                </div>
                <div class="form-group">
                    <label for="markup">Наценка (%)</label>
                    <input type="number" id="markup" name="markup" min="0" max="100" step="1" placeholder="0">
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
                <div class="form-group">
                    <label for="discount">Скидка (%)</label>
                    <input type="number" id="discount" name="discount" min="0" max="100" step="1" placeholder="0">
                </div>
                <div class="form-group">
                    <label for="markup">Наценка (%)</label>
                    <input type="number" id="markup" name="markup" min="0" max="100" step="1" placeholder="0">
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
            if (input.value === '' || isNaN(input.value)) {
                formData[input.name] = null;
            } else {
                formData[input.name] = parseInt(input.value);
            }
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
            if (data.price_per_card !== undefined) {
                let perCard = document.getElementById('price_per_card');
                if (!perCard) {
                    perCard = document.createElement('p');
                    perCard.id = 'price_per_card';
                    document.getElementById('calculation-result').appendChild(perCard);
                }
                perCard.textContent = `Стоимость одной визитки: ${data.price_per_card.toLocaleString('ru-RU')} руб.`;
            }
        } else {
            alert('Ошибка при расчете: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при отправке запроса');
    });
}