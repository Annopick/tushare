import logging
from flask import Flask, jsonify

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)

    # 加载配置
    from app.config import Config
    app.config.from_object(Config)

    # 初始化数据库
    from app.models.stock import init_db
    init_db()

    # 注册路由
    from app.routes.stock_routes import bp as stocks_bp
    app.register_blueprint(stocks_bp)

    # 健康检查
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})

    # 初始化调度器
    from app.scheduler.jobs import init_scheduler
    init_scheduler()

    return app
