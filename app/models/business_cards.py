from app.models.base import BaseCalculator
import json
import os

class BusinessCardCalculator(BaseCalculator):
    """Калькулятор для расчета стоимости визиток"""
    
    def __init__(self, quantity, paper_type, color_scheme, lamination=None, corners=None, tech_hole=False, mark_mifare=False, scratch_sticker=False, uf_print=False):
        super().__init__()
        self.quantity = quantity          # Кол-во
        self.paper_type = paper_type      # Тип бумаги
        self.color_scheme = color_scheme  # 4+0, 4+4, etc.
        self.lamination = lamination      # Тип и сторона ламинации
        self.corners = corners            # Скругление углов
        self.tech_hole = tech_hole        # Технологическое отверстие
        self.mark_mifare = mark_mifare    # Метка mifare
        self.scratch_sticker = scratch_sticker  # Скретч-наклейка
        self.uf_print = uf_print          # Уф печать
        
        # Загружаем данные о ценах из JSON файла
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'papers.json')
        with open(json_path, 'r') as f:
            self.papers_data = json.load(f)
        
        # Коэффициенты для разных цветовых схем
        self.color_factors = {
            '4+0': 1.0,    # Цветная печать с одной стороны
            '4+4': 1.0,    # Цветная печать с двух сторон (множитель уже учтен в JSON)
            '4+1': 1.05,   # Цветная печать с одной стороны, ч/б с другой
            '1+0': 0.7,    # Ч/б печать с одной стороны
            '1+1': 0.8,    # Ч/б печать с двух сторон
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

        self.scratch_sticker_price = {
            'standart': (2.8, 2.5),
            '13x42': (3.1, 2.9),
            '18x40': (3.1, 2.9),
            '30x30': (3.5, 3.3)
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

        # Добавляем стоимость метки Mifare к цене одной визитки
        if self.mark_mifare:
            price_per_card += 14  # Добавляем 14 рублей за метку Mifare

        # Добавляем стоимость скретч-наклейки к цене одной визитки
        if self.scratch_sticker and self.scratch_sticker in self.scratch_sticker_price:
            sticker_tuple = self.scratch_sticker_price[self.scratch_sticker]
            if self.quantity < 1000:
                price_per_card += sticker_tuple[0]
            else:
                price_per_card += sticker_tuple[1]
        
        # Добавляем стоимость уф-печати к цене одной визитки
        if self.uf_print:
            uf_print_data = self.papers_data.get('UF_Print', {})
            uf_type = self.uf_print if isinstance(self.uf_print, str) else 'color_4'
            uf_prices = uf_print_data.get(uf_type, {})
            # Получаем отсортированный список порогов тиража (ключи словаря)
            quantities = sorted([int(q) for q in uf_prices.keys()])
            price_quantity = quantities[0] if quantities else None
            # Логика выбора ближайшего меньшего или равного порога тиража:
            # Например, если тираж 1200, а пороги: 1000, 2000, то выберется 1000
            for i, q in enumerate(quantities):
                if self.quantity < q:
                    if i > 0:
                        price_quantity = quantities[i - 1]
                    break
                if i == len(quantities) - 1:
                    price_quantity = q
            # Если найден подходящий порог, добавляем соответствующую цену к стоимости одной визитки
            if price_quantity is not None:
                price_per_card += uf_prices[str(price_quantity)]
        
        # Рассчитываем общую стоимость
        price = price_per_card * self.quantity
        
        # Применяем коэффициент срочности
        price = self.apply_urgency(price, urgency)
        
        return round(price, 2)