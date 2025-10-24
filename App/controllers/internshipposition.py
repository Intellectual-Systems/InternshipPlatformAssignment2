from App.models.internshipposition import InternshipPosition
from App.database import db


def get_position_by_id(positionID):
    pos = InternshipPosition.query.filter_by(id=positionID).first()
    if not pos:
        return None
    return pos

def get_all_positions():
    posits = InternshipPosition.query.all()
    if not posits:
        return None
    return posits
