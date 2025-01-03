"""CRUD operations for chunks."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base_organization import CRUDBaseOrganization
from app.models.chunk import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate


class CRUDChunk(CRUDBaseOrganization[Chunk, ChunkCreate, ChunkUpdate]):
    """CRUD operations for chunks."""

    async def get_by_entity_id(
        self,
        db: AsyncSession,
        entity_id: str,
        sync_id: UUID,
    ) -> Optional[Chunk]:
        """Get a chunk by entity id and sync id."""
        stmt = select(Chunk).where(Chunk.entity_id == entity_id, Chunk.sync_id == sync_id)
        result = await db.execute(stmt)
        return result.unique().scalars().one_or_none()

    async def update_job_id(
        self,
        db: AsyncSession,
        db_obj: Chunk,
        sync_job_id: UUID,
    ) -> Chunk:
        """Update a chunk with a sync job id."""
        db_obj.sync_job_id = sync_job_id
        return await self.update(db, db_obj=db_obj)

    async def get_all_outdated(
        self,
        db: AsyncSession,
        sync_job_id: UUID,
    ) -> list[Chunk]:
        """Get all chunks that are outdated."""
        stmt = select(Chunk).where(Chunk.sync_job_id != sync_job_id)
        result = await db.execute(stmt)
        return list(result.unique().scalars().all())

    async def get_by_sync_job(
        self,
        db: AsyncSession,
        sync_job_id: UUID,
    ) -> list[Chunk]:
        """Get all chunks for a specific sync job."""
        stmt = select(Chunk).where(Chunk.sync_job_id == sync_job_id)
        result = await db.execute(stmt)
        return list(result.unique().scalars().all())

    async def anti_get_by_sync_job(
        self,
        db: AsyncSession,
        sync_job_id: UUID,
    ) -> list[Chunk]:
        """Get all chunks for that are not from a specific sync job."""
        stmt = select(Chunk).where(Chunk.sync_job_id != sync_job_id)
        result = await db.execute(stmt)
        return list(result.unique().scalars().all())


chunk = CRUDChunk(Chunk)