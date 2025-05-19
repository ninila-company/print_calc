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
                tech_hole=data.get('tech_hole', False)
            )
            price = calculator.calculate(data.get('urgency', 'standard'))
            if data.get('tech_hole', False):
                try:
                    price += int(data.get('quantity', 100)) * 2
                except Exception:
                    price += 2
            discount = data.get('discount')
            if discount is not None and discount != '' and discount != 0:
                try:
                    discount = float(discount)
                    if 0 < discount < 100:
                        price = price * (1 - discount / 100)
                except Exception:
                    pass
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
            result = {'success': True, 'price': round(price, 2)}

        # Здесь будут добавляться другие типы продукции

    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)
