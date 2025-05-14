from app.models.base import BaseCalculator

class FlyerCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости листовок/флаеров"""
    
    def __init__(self, quantity, size, paper_type, color_scheme, double_sided=True):
        super().__init__()
        self.quantity = quantity
        self.size = size              # A6, A5, A4, A3
        self.paper_type = paper_type
        self.color_scheme = color_scheme
        self.double_sided = double_sided
        
        # Базовые цены для разных форматов (за 100 шт на офсетной 130 г/м²)
        self.size_prices = {
            'A6': 400,
            'A5': 700,
            'A4': 1300,
            'A3': 2500,
        }
        
        # Коэффициенты для разных типов бумаги
        self.paper_factors = {
            'offset_130': 1.0,     # Офсетная 130 г/м²
            'offset_170': 1.2,     # Офсетная 170 г/м²
            'coated_130': 1.3,     # Мелованная 130 г/м²
            'coated_170': 1.5,     # Мелованная 170 г/м²
            'coated_300': 2.0,     # Мелованная 300 г/м²
        }
        
        # Коэффициенты для разных цветовых схем
        self.color_factors = {
            '4+0': 1.0,    # Цветная печать с одной стороны
            '4+4': 1.8,    # Цветная печать с двух сторон
            '1+0': 0.6,    # Ч/б печать с одной стороны
            '1+1': 1.0,    # Ч/б печать с двух сторон
        }
    
    def calculate(self, urgency='standard'):
        """Расчет стоимости листовок"""
        # Базовая стоимость за 100 шт для выбранного формата
        base_price = self.size_prices.get(self.size, 1000)
        
        # Применяем коэффициент типа бумаги
        paper_factor = self.paper_factors.get(self.paper_type, 1.0)
        price = base_price * paper_factor
        
        # Применяем коэффициент цветности
        color_factor = self.color_factors.get(self.color_scheme, 1.0)
        price = price * color_factor
        
        # Расчет для заданного тиража
        price = price * (self.quantity / 100)
        
        # Применяем скидку по тиражу
        price = self.apply_quantity_discount(price)
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)