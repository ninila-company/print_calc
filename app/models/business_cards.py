from app.models.base import BaseCalculator
import json
import os

class BusinessCardCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости визиток"""
    
    def __init__(self, quantity, paper_type, color_scheme, lamination=None, corners=None):
        super().__init__()
        self.quantity = quantity          # Кол-во
        self.paper_type = paper_type      # Тип бумаги
        self.color_scheme = color_scheme  # 4+0, 4+4, etc.
        self.lamination = lamination      # Тип и сторона ламинации
        self.corners = corners            # Скругление углов
        
        # Загружаем данные о ценах из JSON файла
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'papers.json')
        with open(json_path, 'r') as f:
            self.papers_data = json.load(f)
        
        # Коэффициенты для разных цветовых схем
        self.color_factors = {
            '4+0': 1.0,    # Цветная печать с одной стороны
            '4+4': 1.0,    # Цветная печать с двух сторон (множитель уже учтен в JSON)
            '1+0': 0.7,    # Ч/б печать с одной стороны
            '1+1': 0.7,    # Ч/б печать с двух сторон
        }

        # Цены для разных типов ламинации (за 100 шт)
        self.lamination_prices = {
            'gloss_1': 150,      # Глянцевая с одной стороны
            'gloss_2': 250,      # Глянцевая с двух сторон
            'matte_1': 180,      # Матовая с одной стороны
            'matte_2': 300,      # Матовая с двух сторон
            'soft_touch_1': 250, # Софт-тач с одной стороны
            'soft_touch_2': 400, # Софт-тач с двух сторон
        }
        
    def _get_price_per_card(self):
        """Получить базовую цену за одну визитку"""
        paper_prices = self.papers_data['Papers'].get(self.paper_type, {})
        
        # Получаем отсортированный список количеств из прайса
        quantities = sorted([int(q) for q in paper_prices.keys()])
        
        # Находим подходящее количество для расчета цены
        price_quantity = quantities[0]  # Минимальное количество по умолчанию
        
        # Проходим по всем порогам и находим нужный
        for i, q in enumerate(quantities):
            if self.quantity < q:
                # Если количество меньше текущего порога, берем предыдущий порог
                # (кроме случая с первым порогом)
                if i > 0:
                    price_quantity = quantities[i - 1]
                break
            # Если дошли до конца списка, берем последний порог
            if i == len(quantities) - 1:
                price_quantity = q
        
        # Получаем массив цен [цена_одностор, цена_двустор]
        prices = paper_prices.get(str(price_quantity), [0, 0])
        
        # Выбираем цену в зависимости от типа печати (одно- или двусторонняя)
        is_double_sided = self.color_scheme.endswith('4')
        price_per_card = prices[1] if is_double_sided else prices[0]
        
        return price_per_card
        
    def calculate(self, urgency='standard'):
        """Расчет стоимости визиток"""
        # Получаем базовую цену за одну визитку
        price_per_card = self._get_price_per_card()
        
        # Рассчитываем общую стоимость
        price = price_per_card * self.quantity
        
        # Применяем коэффициент для ч/б печати
        color_factor = self.color_factors.get(self.color_scheme, 1.0)
        price = price * color_factor
        
        # Добавляем стоимость постпечатной обработки
        if self.lamination:
            lamination_price = self.lamination_prices.get(self.lamination, 200)
            price += lamination_price * (self.quantity / 100)
            
        if self.corners:
            price += 150 * (self.quantity / 100)  # Скругление углов
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)