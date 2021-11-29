from typing import Optional, Union
from enum import Enum

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.user import UserPublic


class JobType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class JobBase(CoreModel):
    """
    All common characteristics of our Job resource
    """
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    job_type: Optional[JobType] = "spot_clean"


class JobCreate(JobBase):
    name: str
    price: float


class JobUpdate(JobBase):
    job_type: Optional[JobType]


class JobInDB(IDModelMixin, JobBase):
    name: str
    price: float
    job_type: JobType
    owner: str


class JobPublic(IDModelMixin, JobBase):
    owner: Union[str, UserPublic]
