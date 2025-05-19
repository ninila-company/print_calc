from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from app.models import BusinessCardCalculator, FlyerCalculator

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Полиграфический калькулятор')


@bp.route('/calculator/<product_type>', methods=['GET', 'POST'])
def calculator(product_type):
    """Страница с калькулятором для конкретного типа продукции"""
    if product_type not in ['business_cards', 'flyers', 'booklets', 'posters',
                            'calendars', 'stickers']:
        return redirect(url_for('main.index'))

    return render_template('calculator.html',
                           title=f'Калькулятор - {product_type}',
                           product_type=product_type)


@bp.route('/api/calculate/<product_type>', methods=['POST'])
def api_calculate(product_type):
    """API для расчета стоимости"""
    data = request.json
    result = {'success': False, 'price': 0, 'error': ''}

    try:
        if product_type == 'business_cards':
            calculator = BusinessCardCalculator(
                quantity=int(data.get('quantity', 100)),
                paper_type=data.get('paper_type', 'offset_300'),
                color_scheme=data.get('color_scheme', '4+0'),
                lamination=data.get('lamination', False),
                corners=data.get('corners', None),
                tech_hole=data.get('tech_hole', False),
                mark_mifare=data.get('mark_mifare', False),
                scratch_sticker=data.get('scratch_sticker', ''),
                uf_print=data.get('uf_print', '')
            )
            price = calculator.calculate(data.get('urgency', 'standard'))
            # Получаем стоимость одной визитки (до округления общей)
            if hasattr(calculator, '_get_price_per_card'):
                price_per_card = calculator._get_price_per_card()
                # Применяем все надбавки, как в calculate
                color_factor = calculator.color_factors.get(calculator.color_scheme, 1.0)
                price_per_card = price_per_card * color_factor
                if calculator.lamination:
                    lamination_price = calculator.lamination_prices.get(calculator.lamination, 0)
                    price_per_card += lamination_price
                if calculator.corners:
                    price_per_card += 2
                if calculator.tech_hole:
                    price_per_card += 2
                if calculator.mark_mifare:
                    price_per_card += 14
                if calculator.scratch_sticker and calculator.scratch_sticker in calculator.scratch_sticker_price:
                    sticker_tuple = calculator.scratch_sticker_price[calculator.scratch_sticker]
                    if calculator.quantity < 1000:
                        price_per_card += sticker_tuple[0]
                    else:
                        price_per_card += sticker_tuple[1]
                if calculator.uf_print:
                    uf_print_data = calculator.papers_data.get('UF_Print', {})
                    uf_type = calculator.uf_print if isinstance(calculator.uf_print, str) else 'color_4'
                    uf_prices = uf_print_data.get(uf_type, {})
                    quantities = sorted([int(q) for q in uf_prices.keys()])
                    price_quantity = quantities[0] if quantities else None
                    for i, q in enumerate(quantities):
                        if calculator.quantity < q:
                            if i > 0:
                                price_quantity = quantities[i - 1]
                            break
                        if i == len(quantities) - 1:
                            price_quantity = q
                    if price_quantity is not None:
                        price_per_card += uf_prices[str(price_quantity)]
                price_per_card = calculator.apply_urgency(price_per_card, data.get('urgency', 'standard'))
                # Считаем общую стоимость
                price = price_per_card * calculator.quantity
                # Применяем скидку и наценку к общей цене
                discount = data.get('discount')
                if discount is not None and discount != '' and discount != 0:
                    try:
                        discount = float(discount)
                        if 0 < discount < 100:
                            price = price * (1 - discount / 100)
                    except Exception:
                        pass
                markup = data.get('markup')
                if markup is not None and markup != '' and float(markup) > 0:
                    try:
                        markup = float(markup)
                        price = price * (1 + markup / 100)
                    except Exception:
                        pass
                # Итоговая цена за штуку после скидки/наценки
                price_per_card_final = price / calculator.quantity if calculator.quantity else price
                result = {'success': True, 'price': round(price, 2), 'price_per_card': round(price_per_card_final, 2)}
            else:
                result = {'success': True, 'price': round(price, 2)}

        elif product_type == 'flyers':
            calculator = FlyerCalculator(
                quantity=int(data.get('quantity', 100)),
                size=data.get('size', 'A4'),
                paper_type=data.get('paper_type', 'coated_130'),
                color_scheme=data.get('color_scheme', '4+0'),
                double_sided=data.get('double_sided', True)
            )
            price = calculator.calculate(data.get('urgency', 'standard'))
            discount = data.get('discount')
            if discount is not None and discount != '' and discount != 0:
                try:
                    discount = float(discount)
                    if 0 < discount < 100:
                        price = price * (1 - discount / 100)
                except Exception:
                    pass
            markup = data.get('markup')
            if markup is not None and markup != '' and float(markup) > 0:
                try:
                    markup = float(markup)
                    price = price * (1 + markup / 100)
                except Exception:
                    pass
            result = {'success': True, 'price': round(price, 2)}

        # Здесь будут добавляться другие типы продукции

    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)
