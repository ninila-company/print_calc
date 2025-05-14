class BaseCalculator:
    """Базовый класс для всех калькуляторов"""
    
    def __init__(self):
        self.base_price = 0
        self.quantity = 0
        self.urgency_factors = {
            'standard': 1.0,  # Стандартный срок
            'urgent': 1.3,    # Срочный заказ (+30%)
            'express': 1.6    # Экспресс-заказ (+60%)
        }
        
    def calculate(self):
        """Базовый метод расчета, должен быть переопределен"""
        raise NotImplementedError("Subclasses must implement calculate()")
    
    def apply_urgency(self, price, urgency_type='standard'):
        """Применяет множитель срочности к цене"""
        factor = self.urgency_factors.get(urgency_type, 1.0)
        return price * factor
    
    def apply_quantity_discount(self, price):
        """Применяет скидку в зависимости от тиража"""
        if self.quantity >= 1000:
            return price * 0.85  # Скидка 15% для больших тиражей
        elif self.quantity >= 500:
            return price * 0.9   # Скидка 10% для средних тиражей
        elif self.quantity >= 100:
            return price * 0.95  # Скидка 5% для небольших тиражей
        return price