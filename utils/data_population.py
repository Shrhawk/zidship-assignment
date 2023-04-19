from db import get_db
from models import CourierModel


def populate_courier():
    db = next(get_db())
    if not db.query(CourierModel).all():
        db.add(CourierModel(name='EasyPost'))
        db.commit()
        db.close()
    return
