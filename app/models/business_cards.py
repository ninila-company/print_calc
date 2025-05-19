from app.models.base import BaseCalculator
import json
import os

class BusinessCardCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости визиток"""
    
    def __init__(self, quantity, paper_type, color_scheme, lamination=None, corners=None, tech_hole=False):
        super().__init__()
        self.quantity = quantity          # Кол-во
        self.paper_type = paper_type      # Тип бумаги
        self.color_scheme = color_scheme  # 4+0, 4+4, etc.
        self.lamination = lamination      # Тип и сторона ламинации
        self.corners = corners            # Скругление углов
        self.tech_hole = tech_hole        # Технологическое отверстие
        
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

        # Цены для разных типов ламинации (за 1 шт)
        self.lamination_prices = {
            'gloss_32': 1.1,
            'matte_32': 1.25,
            'matte_32_anti': 2.3,
            'gloss_75': 1.85,
            'matte_75': 2.45,
            'gloss_150': 3.65,
            'gloss_250': 4.6,
            'matte_250': 6.75,
            'soft_touch_1': 2.3,
            'soft_touch_2': 2.8,
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
        prices = paper_prices.get(str(price_quantity), [1.1, 0])
        
        # Выбираем цену в зависимости от типа печати (одно- или двусторонняя)
        is_double_sided = self.color_scheme.endswith('4')
        price_per_card = prices[1] if is_double_sided else prices[0]
        
        return price_per_card
        
    def calculate(self, urgency='standard'):
        """Расчет стоимости визиток"""
        # Получаем базовую цену за одну визитку
        price_per_card = self._get_price_per_card()
        
        # Применяем коэффициент для ч/б печати
        color_factor = self.color_factors.get(self.color_scheme, 1.0)
        price_per_card = price_per_card * color_factor
        
        # Добавляем стоимость ламинации к цене одной визитки
        if self.lamination:
            lamination_price = self.lamination_prices.get(self.lamination, 0)
            price_per_card += lamination_price
        
        # Добавляем стоимость скругления углов к цене одной визитки
        if self.corners:
            price_per_card += 2  # Добавляем 2 рубля за скругление углов
        
        # Добавляем стоимость технологического отверстия к цене одной визитки
        if self.tech_hole:
            price_per_card += 2  # Добавляем 2 рубля за технологическое отверстие
        
        # Рассчитываем общую стоимость
        price = price_per_card * self.quantity
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)