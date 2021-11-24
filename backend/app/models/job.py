from typing import Optional
from enum import Enum

from app.models.core import IDModelMixin, CoreModel


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


class JobPublic(IDModelMixin, JobBase):
    pass

