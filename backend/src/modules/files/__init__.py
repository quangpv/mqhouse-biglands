from src.modules.files.cleanup import cleanup_orphaned_files
from src.modules.files.router import router
from src.platform.container import container
from src.platform.scheduler import AppScheduler


def module():
    scheduler = container.resolve(AppScheduler)
    scheduler.add_job(cleanup_orphaned_files, trigger="interval", hours=24)
    return router
