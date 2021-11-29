from typing import Optional, Union
from enum import Enum

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.user import UserPublic


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class cleaningBase(CoreModel):
    """
    All common characteristics of our cleaning resource
    """
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    cleaning_type: Optional[CleaningType] = "spot_clean"


class CleaningCreate(cleaningBase):
    name: str
    price: float


class CleaningUpdate(cleaningBase):
    cleaning_type: Optional[CleaningType]


class CleaningInDB(IDModelMixin, cleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType
    owner: str


class CleaningPublic(IDModelMixin, cleaningBase):
    owner: Union[str, UserPublic]
