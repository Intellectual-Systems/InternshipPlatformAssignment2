
from .scenario import create_scenario

from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_scenario()
