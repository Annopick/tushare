import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import Config
from app.services.stock_service import stock_service

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone=Config.SCHEDULER_TIMEZONE)


def sync_job():
    """定时同步任务"""
    logger.info("开始执行股票数据同步任务")
    try:
        count = stock_service.sync_stocks()
        logger.info(f"股票数据同步完成，共同步 {count} 条记录")
    except Exception as e:
        logger.error(f"股票数据同步失败: {e}")


def init_scheduler():
    """初始化调度器"""
    trigger = CronTrigger(
        hour=Config.SYNC_HOUR,
        minute=Config.SYNC_MINUTE,
        timezone=Config.SCHEDULER_TIMEZONE
    )
    scheduler.add_job(
        sync_job,
        trigger=trigger,
        id='sync_stocks',
        name='同步股票数据',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"调度器已启动，同步任务将在每天 {Config.SYNC_HOUR}:{Config.SYNC_MINUTE:02d} 执行")
