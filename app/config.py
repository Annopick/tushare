import os


class Config:
    """应用配置"""
    # Tushare配置
    TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN', '')

    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_NAME = os.environ.get('DB_NAME', 'tushare')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 调度器配置
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    SYNC_HOUR = int(os.environ.get('SYNC_HOUR', 1))
    SYNC_MINUTE = int(os.environ.get('SYNC_MINUTE', 0))
