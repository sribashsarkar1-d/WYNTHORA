from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """
    Base generic repository enforcing DDD by abstracting database access.
    Services should use repositories, never SQLAlchemy directly.
    """
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: Any) -> Optional[T]:
        query = select(self.model).where(getattr(self.model, "id") == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[T]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def bulk_add(self, entities: List[T]) -> None:
        self.session.add_all(entities)
        await self.session.flush()

    async def update(self, entity: T) -> T:
        # Assuming the session tracks modifications
        await self.session.flush()
        return entity
        
    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()
