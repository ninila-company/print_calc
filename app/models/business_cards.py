from app.models.base import BaseCalculator

class BusinessCardCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости визиток"""
    
    def __init__(self, quantity, paper_type, color_scheme, lamination=None, corners=None):
        super().__init__()
        self.quantity = quantity          # Кол-во
        self.paper_type = paper_type      # Тип бумаги
        self.color_scheme = color_scheme  # 4+0, 4+4, etc.
        self.lamination = lamination      # Тип и сторона ламинации
        self.corners = corners            # Скругление углов
        
        # Базовые цены для разных типов бумаги (за 100 шт)
        self.paper_prices = {
            'offset_270': 6.7,     # Офсетная 250 г/м²
            'offset_300': 5,     # Офсетная 300 г/м²
            'color_copy_300': 7,     # color copy 300 г/м²
            'color_copy_350': 7.5,   # color copy 350 г/м²
        }
        
        # Коэффициенты для разных цветовых схем
        self.color_factors = {
            '4+0': 1.0,    # Цветная печать с одной стороны
            '4+4': 1.28,    # Цветная печать с двух сторон
            '1+0': 0.7,    # Ч/б печать с одной стороны
            '1+1': 1.1,    # Ч/б печать с двух сторон
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
        
    def calculate(self, urgency='standard'):
        """Расчет стоимости визиток"""
        # Базовая стоимость за 100 шт
        base_price = self.paper_prices.get(self.paper_type, 600)
        
        # Применяем коэффициент цветности
        color_factor = self.color_factors.get(self.color_scheme, 1.0)
        price = base_price * color_factor
        
        # Расчет для заданного тиража
        price = price * (self.quantity)
        
        # Добавляем стоимость постпечатной обработки
        if self.lamination:
            lamination_price = self.lamination_prices.get(self.lamination, 200)
            price += lamination_price * (self.quantity / 100)
            
        if self.corners:
            price += 150 * (self.quantity / 100)  # Скругление углов
        
        # Применяем скидку по тиражу
        price = self.apply_quantity_discount(price)
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)