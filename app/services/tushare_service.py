import logging
from datetime import datetime

import tushare as ts
import pandas as pd

from app.config import Config

logger = logging.getLogger(__name__)


class TushareService:
    """Tushare API服务"""

    def __init__(self):
        self.pro = None
        self._init_api()

    def _init_api(self):
        """初始化Tushare API"""
        token = Config.TUSHARE_TOKEN
        if not token:
            logger.warning("TUSHARE_TOKEN未设置")
            return
        ts.set_token(token)
        self.pro = ts.pro_api()

    def get_stock_basic(self) -> pd.DataFrame:
        """获取股票基本信息列表"""
        if not self.pro:
            logger.error("Tushare API未初始化")
            return pd.DataFrame()

        try:
            df = self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,symbol,name,area,industry,market,list_date'
            )
            logger.info(f"获取到 {len(df)} 条股票数据")
            return df
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return pd.DataFrame()


tushare_service = TushareService()
