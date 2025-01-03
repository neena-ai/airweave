"""Module for sync context."""


from typing import Optional

from app import schemas
from app.platform.destinations._base import BaseDestination
from app.platform.embedding_models._base import BaseEmbeddingModel
from app.platform.sources._base import BaseSource


class SyncContext:
    """Context container for a sync."""

    source: BaseSource
    destination: BaseDestination
    embedding_model: BaseEmbeddingModel
    sync: schemas.Sync
    white_label: Optional[schemas.WhiteLabel] = None
