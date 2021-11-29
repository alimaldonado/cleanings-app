from typing import Optional, Union
from enum import Enum

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.user import UserPublic


class cleaningType(str, Enum):
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
    cleaning_type: Optional[cleaningType] = "spot_clean"


class cleaningCreate(cleaningBase):
    name: str
    price: float


class cleaningUpdate(cleaningBase):
    cleaning_type: Optional[cleaningType]


class cleaningInDB(IDModelMixin, cleaningBase):
    name: str
    price: float
    cleaning_type: cleaningType
    owner: str


class cleaningPublic(IDModelMixin, cleaningBase):
    owner: Union[str, UserPublic]
