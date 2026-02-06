import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3307'
os.environ['DB_NAME'] = 'tushare'
os.environ['DB_USER'] = 'tushare'
os.environ['DB_PASSWORD'] = 'tusharepassword'
os.environ['TUSHARE_TOKEN'] = ''


@pytest.fixture(scope='session')
def app():
    """创建测试应用"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope='session')
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture(scope='session')
def db_session():
    """创建数据库会话"""
    from app.models.stock import SessionLocal, init_db
    init_db()
    session = SessionLocal()
    yield session
    session.close()
