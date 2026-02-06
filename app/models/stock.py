from sqlalchemy import create_engine, Column, BigInteger, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from app.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Stock(Base):
    """股票基本信息模型"""
    __tablename__ = 'stocks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), unique=True, nullable=False, index=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    area = Column(String(10))
    industry = Column(String(50))
    market = Column(String(10))
    list_date = Column(Date)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            'ts_code': self.ts_code,
            'symbol': self.symbol,
            'name': self.name,
            'area': self.area,
            'industry': self.industry,
            'market': self.market,
            'list_date': self.list_date.isoformat() if self.list_date else None
        }


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
