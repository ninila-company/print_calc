from app.models.base import BaseCalculator

class BusinessCardCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости визиток"""
    
    def __init__(self, quantity, paper_type, color_scheme, lamination=False, corners=None):
        super().__init__()
        self.quantity = quantity
        self.paper_type = paper_type
        self.color_scheme = color_scheme  # 4+0, 4+4, etc.
        self.lamination = lamination      # Ламинация
        self.corners = corners            # Скругление углов
        
        # Базовые цены для разных типов бумаги (за 100 шт)
        self.paper_prices = {
            'offset_300': 500,     # Офсетная 300 г/м²
            'coated_300': 700,     # Мелованная 300 г/м²
            'premium_350': 1000,   # Премиум 350 г/м²
        }
        
        # Коэффициенты для разных цветовых схем
        self.color_factors = {
            '4+0': 1.0,    # Цветная печать с одной стороны
            '4+4': 1.7,    # Цветная печать с двух сторон
            '1+0': 0.7,    # Ч/б печать с одной стороны
            '1+1': 1.2,    # Ч/б печать с двух сторон
        }
        
    def calculate(self, urgency='standard'):
        """Расчет стоимости визиток"""
        # Базовая стоимость за 100 шт
        base_price = self.paper_prices.get(self.paper_type, 600)
        
        # Применяем коэффициент цветности
        color_factor = self.color_factors.get(self.color_scheme, 1.0)
        price = base_price * color_factor
        
        # Расчет для заданного тиража
        price = price * (self.quantity / 100)
        
        # Добавляем стоимость постпечатной обработки
        if self.lamination:
            price += 200 * (self.quantity / 100)  # Ламинация
            
        if self.corners:
            price += 150 * (self.quantity / 100)  # Скругление углов
        
        # Применяем скидку по тиражу
        price = self.apply_quantity_discount(price)
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)