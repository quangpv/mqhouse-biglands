import os
import time
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.file import EntityType, FileEntity
from src.data.repositories.file_repo import FileRepo
from src.modules.files.cleanup import ORPHAN_GRACE_SECONDS, cleanup_orphaned_files
from tests.conftest import ADMIN_UUID


@pytest.mark.asyncio
async def test_orphaned_disk_file_older_than_grace_is_deleted(
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    orphan_file = upload_dir / "orphan.txt"
    orphan_file.write_text("orphan")
    old_mtime = time.time() - (ORPHAN_GRACE_SECONDS + 3600)
    os.utime(str(orphan_file), (old_mtime, old_mtime))

    await cleanup_orphaned_files(session=db_session, upload_dir=str(upload_dir))

    assert not orphan_file.exists()


@pytest.mark.asyncio
async def test_recent_orphan_disk_file_is_not_deleted(
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    orphan_file = upload_dir / "recent_orphan.txt"
    orphan_file.write_text("recent")

    await cleanup_orphaned_files(session=db_session, upload_dir=str(upload_dir))

    assert orphan_file.exists()


@pytest.mark.asyncio
async def test_orphaned_db_record_without_disk_file_is_deleted(
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    fake_path = str(upload_dir / "missing.txt")

    repo = FileRepo(db=db_session)
    entity = FileEntity(
        origin_name="missing.txt",
        path=fake_path,
        mimetype="text/plain",
        size=0,
        entity_type=EntityType.AVATAR,
        created_by_id=ADMIN_UUID,
    )
    entity = await repo.save(entity)
    db_session.add(entity)
    await db_session.flush()

    await cleanup_orphaned_files(session=db_session, upload_dir=str(upload_dir))

    remaining = await repo.get(entity.id)
    assert remaining is None


@pytest.mark.asyncio
async def test_valid_file_is_not_touched_by_cleanup(
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True)
    valid_file = upload_dir / "valid.txt"
    valid_file.write_text("valid content")

    repo = FileRepo(db=db_session)
    entity = FileEntity(
        origin_name="valid.txt",
        path=str(valid_file),
        mimetype="text/plain",
        size=len("valid content"),
        entity_type=EntityType.AVATAR,
        created_by_id=ADMIN_UUID,
    )
    entity = await repo.save(entity)
    db_session.add(entity)
    await db_session.flush()

    await cleanup_orphaned_files(session=db_session, upload_dir=str(upload_dir))

    assert valid_file.exists()
    remaining = await repo.get(entity.id)
    assert remaining is not None
