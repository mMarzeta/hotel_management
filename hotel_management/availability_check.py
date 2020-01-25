from . import schemas
from sqlalchemy.orm import Session


def check_availability(availability: schemas.AvailabilityRequest, db: Session):
    return None
