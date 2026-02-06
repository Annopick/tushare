from flask import Blueprint, jsonify, request

from app.services.stock_service import stock_service

bp = Blueprint('stocks', __name__, url_prefix='/api/stocks')


@bp.route('/search', methods=['GET'])
def search_stocks():
    """模糊搜索股票"""
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify({'error': '请提供搜索关键词', 'data': []}), 400

    limit = request.args.get('limit', 20, type=int)
    limit = min(max(limit, 1), 100)

    stocks = stock_service.search_by_name(keyword, limit)
    return jsonify({
        'data': [stock.to_dict() for stock in stocks],
        'count': len(stocks)
    })


@bp.route('/<ts_code>', methods=['GET'])
def get_stock(ts_code: str):
    """根据代码查询股票"""
    stock = stock_service.get_by_code(ts_code)
    if not stock:
        return jsonify({'error': '股票不存在'}), 404
    return jsonify({'data': stock.to_dict()})
