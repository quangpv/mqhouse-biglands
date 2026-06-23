import time
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.file_repo import FileRepo
from src.platform.config import settings
from src.platform.database import async_session_factory
from src.platform.logger import AppLogger

ORPHAN_GRACE_SECONDS = 24 * 60 * 60
logger = AppLogger("files.cleanup")


async def cleanup_orphaned_files(session: AsyncSession | None = None, upload_dir: str | None = None) -> None:
    upload_dir = Path(upload_dir or settings.upload_dir)
    if not upload_dir.exists():
        return

    if session is None:
        async with async_session_factory() as s:
            await _run_cleanup(upload_dir, s)
            await s.commit()
    else:
        await _run_cleanup(upload_dir, session)
        await session.flush()


async def _run_cleanup(upload_dir: Path, session: AsyncSession) -> None:
    repo = FileRepo(db=session)
    db_records = await repo.get_all_paths()
    db_paths = set(rec.path for rec in db_records)

    disk_files = {p for p in upload_dir.iterdir() if p.is_file()}
    now = time.time()

    for disk_file in disk_files:
        if str(disk_file) not in db_paths:
            age = now - disk_file.stat().st_mtime
            if age >= ORPHAN_GRACE_SECONDS:
                disk_file.unlink()
                logger.info("Deleted orphaned disk file: %s", disk_file)
            else:
                logger.debug("Skipped recent orphan (age=%.1fh): %s", age / 3600, disk_file)

    disk_paths_str = {str(p) for p in disk_files}
    all_entities = await repo.get_all_ids()
    for entity_id in all_entities:
        entity = await repo.get(entity_id)
        if entity and entity.path not in disk_paths_str:
            await repo.delete(entity)
            logger.info("Deleted orphaned DB record: %s (path: %s)", entity_id, entity.path)
