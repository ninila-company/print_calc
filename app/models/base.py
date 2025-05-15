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
        if self.quantity >= 1008:
            return price * 0.36
        elif self.quantity >= 888:
            return price * 0.43
        elif self.quantity >= 816:
            return price * 0.45
        elif self.quantity >= 720:
            return price * 0.47
        elif self.quantity >= 600:
            return price * 0.5
        elif self.quantity >= 480:
            return price * 0.52
        elif self.quantity >= 408:
            return price * 0.58
        elif self.quantity >= 312:
            return price * 0.66
        elif self.quantity >= 216:
            return price * 0.7
        elif self.quantity >= 120:
            return price * 0.8  # TODO Скидка 5% для небольших тиражей, пока поставил 1
        return price