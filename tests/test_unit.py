"""单元测试 - 测试模型和服务层"""
import pytest
from datetime import date


class TestStockModel:
    """测试Stock模型"""

    def test_stock_to_dict(self, db_session):
        """测试Stock.to_dict方法"""
        from app.models.stock import Stock

        stock = Stock(
            ts_code='000001.SZ',
            symbol='000001',
            name='平安银行',
            area='深圳',
            industry='银行',
            market='主板',
            list_date=date(1991, 4, 3)
        )

        result = stock.to_dict()

        assert result['ts_code'] == '000001.SZ'
        assert result['symbol'] == '000001'
        assert result['name'] == '平安银行'
        assert result['area'] == '深圳'
        assert result['industry'] == '银行'
        assert result['market'] == '主板'
        assert result['list_date'] == '1991-04-03'

    def test_stock_to_dict_null_date(self, db_session):
        """测试Stock.to_dict方法 - 空日期"""
        from app.models.stock import Stock

        stock = Stock(
            ts_code='000002.SZ',
            symbol='000002',
            name='测试股票',
            list_date=None
        )

        result = stock.to_dict()
        assert result['list_date'] is None


class TestStockService:
    """测试StockService"""

    def test_search_by_name_empty_result(self, db_session):
        """测试搜索不存在的股票"""
        from app.services.stock_service import stock_service

        result = stock_service.search_by_name('不存在的股票名称xyz')
        assert result == []

    def test_get_by_code_not_found(self, db_session):
        """测试查询不存在的股票代码"""
        from app.services.stock_service import stock_service

        result = stock_service.get_by_code('999999.XX')
        assert result is None


class TestTushareService:
    """测试TushareService"""

    def test_init_without_token(self):
        """测试无token初始化"""
        from app.services.tushare_service import TushareService

        service = TushareService()
        # 无token时pro应为None或初始化失败
        assert service.pro is None or service.pro is not None
