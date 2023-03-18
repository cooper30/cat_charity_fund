from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.base_mixin import ModelMixin


class Donation(ModelMixin, Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
