"""CRUD operations for connections."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._base import CRUDBase
from app.models.connection import Connection, IntegrationType
from app.schemas.connection import ConnectionCreate, ConnectionStatus, ConnectionUpdate


class CRUDConnection(CRUDBase[Connection, ConnectionCreate, ConnectionUpdate]):
    """CRUD operations for connections."""

    async def get_by_integration_type(
        self,
        db: AsyncSession,
        integration_type: IntegrationType,
        organization_id: UUID
    ) -> list[Connection]:
        """Get all connections for a specific integration type within an organization."""
        stmt = select(Connection).where(
            Connection.integration_type == integration_type,
            Connection.organization_id == organization_id
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_active_by_integration_type(
        self,
        db: AsyncSession,
        integration_type: IntegrationType,
        organization_id: UUID
    ) -> list[Connection]:
        """Get all active connections for a specific integration type within an organization."""
        stmt = select(Connection).where(
            Connection.integration_type == integration_type,
            Connection.organization_id == organization_id,
            Connection.status == ConnectionStatus.ACTIVE
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())


connection = CRUDConnection(Connection)