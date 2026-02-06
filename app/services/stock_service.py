import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from app.models.stock import Stock, SessionLocal
from app.services.tushare_service import tushare_service

logger = logging.getLogger(__name__)


class StockService:
    """股票业务服务"""

    def sync_stocks(self) -> int:
        """同步股票数据到数据库"""
        df = tushare_service.get_stock_basic()
        if df.empty:
            logger.warning("没有获取到股票数据")
            return 0

        db = SessionLocal()
        try:
            count = 0
            for _, row in df.iterrows():
                list_date = None
                if row['list_date']:
                    try:
                        list_date = datetime.strptime(str(row['list_date']), '%Y%m%d').date()
                    except (ValueError, TypeError):
                        pass

                stmt = insert(Stock).values(
                    ts_code=row['ts_code'],
                    symbol=row['symbol'],
                    name=row['name'],
                    area=row.get('area'),
                    industry=row.get('industry'),
                    market=row.get('market'),
                    list_date=list_date
                ).on_duplicate_key_update(
                    symbol=row['symbol'],
                    name=row['name'],
                    area=row.get('area'),
                    industry=row.get('industry'),
                    market=row.get('market'),
                    list_date=list_date
                )
                db.execute(stmt)
                count += 1

            db.commit()
            logger.info(f"成功同步 {count} 条股票数据")
            return count
        except Exception as e:
            db.rollback()
            logger.error(f"同步股票数据失败: {e}")
            raise
        finally:
            db.close()

    def search_by_name(self, keyword: str, limit: int = 20) -> List[Stock]:
        """根据名称模糊搜索股票"""
        db = SessionLocal()
        try:
            stocks = db.query(Stock).filter(
                Stock.name.like(f'%{keyword}%')
            ).limit(limit).all()
            return stocks
        finally:
            db.close()

    def get_by_code(self, ts_code: str) -> Optional[Stock]:
        """根据代码查询股票"""
        db = SessionLocal()
        try:
            stock = db.query(Stock).filter(Stock.ts_code == ts_code).first()
            return stock
        finally:
            db.close()


stock_service = StockService()
