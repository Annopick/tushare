"""集成测试 - 测试API端点和数据库操作"""
import pytest
from datetime import date


class TestHealthEndpoint:
    """测试健康检查端点"""

    def test_health_check(self, client):
        """测试/health端点"""
        response = client.get('/health')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'


class TestStockAPI:
    """测试股票API端点"""

    def test_search_without_keyword(self, client):
        """测试搜索接口 - 无关键词"""
        response = client.get('/api/stocks/search')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_search_with_empty_keyword(self, client):
        """测试搜索接口 - 空关键词"""
        response = client.get('/api/stocks/search?q=')

        assert response.status_code == 400

    def test_search_with_keyword(self, client):
        """测试搜索接口 - 有关键词"""
        response = client.get('/api/stocks/search?q=测试')

        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'count' in data

    def test_search_with_limit(self, client):
        """测试搜索接口 - 限制数量"""
        response = client.get('/api/stocks/search?q=测试&limit=5')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']) <= 5

    def test_get_stock_not_found(self, client):
        """测试查询不存在的股票"""
        response = client.get('/api/stocks/999999.XX')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestDatabaseOperations:
    """测试数据库操作"""

    def test_create_and_query_stock(self, db_session):
        """测试创建和查询股票"""
        from app.models.stock import Stock

        # 创建测试数据
        stock = Stock(
            ts_code='TEST01.SZ',
            symbol='TEST01',
            name='测试股票一号',
            area='测试',
            industry='测试行业',
            market='测试板',
            list_date=date(2024, 1, 1)
        )
        db_session.add(stock)
        db_session.commit()

        # 查询验证
        result = db_session.query(Stock).filter(Stock.ts_code == 'TEST01.SZ').first()
        assert result is not None
        assert result.name == '测试股票一号'

        # 清理
        db_session.delete(result)
        db_session.commit()

    def test_search_by_name_integration(self, db_session):
        """测试名称搜索集成"""
        from app.models.stock import Stock
        from app.services.stock_service import stock_service

        # 创建测试数据
        stock = Stock(
            ts_code='TEST02.SZ',
            symbol='TEST02',
            name='集成测试银行',
            area='测试',
            industry='银行',
            market='主板',
            list_date=date(2024, 1, 1)
        )
        db_session.add(stock)
        db_session.commit()

        # 搜索验证
        results = stock_service.search_by_name('集成测试')
        assert len(results) >= 1
        assert any(s.ts_code == 'TEST02.SZ' for s in results)

        # 清理
        db_session.query(Stock).filter(Stock.ts_code == 'TEST02.SZ').delete()
        db_session.commit()

    def test_get_by_code_integration(self, db_session):
        """测试代码查询集成"""
        from app.models.stock import Stock
        from app.services.stock_service import stock_service

        # 创建测试数据
        stock = Stock(
            ts_code='TEST03.SZ',
            symbol='TEST03',
            name='代码查询测试',
            area='测试',
            industry='测试',
            market='测试',
            list_date=date(2024, 1, 1)
        )
        db_session.add(stock)
        db_session.commit()

        # 查询验证
        result = stock_service.get_by_code('TEST03.SZ')
        assert result is not None
        assert result.name == '代码查询测试'

        # 清理
        db_session.query(Stock).filter(Stock.ts_code == 'TEST03.SZ').delete()
        db_session.commit()
