from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Part(Base):
    __tablename__ = 'parts'

    part_id = Column('PartID', Integer, primary_key=True, index=True)
    chapter_id = Column('ChapterID', Integer, ForeignKey('chapters.ChapterID'))
    part_name = Column('PartName', String, index=True)
    document = Column('Document', Text)

    chapter = relationship("Chapter", back_populates="parts")