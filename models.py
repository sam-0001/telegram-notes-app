from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
import enum
from .database import Base

# --- Enums for controlled vocabularies ---
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HOD = "hod"
    TEACHER = "teacher"
    VOLUNTEER = "volunteer"
    STUDENT = "student"

class Department(str, enum.Enum):
    COMP = "COMP"
    IT = "IT"
    ENTC = "ENTC"
    MECH = "MECH"
    CIVIL = "CIVIL"
    FE = "FE"

class Year(str, enum.Enum):
    FE = "FE"
    SE = "SE"
    TE = "TE"
    BE = "BE"

class FileType(str, enum.Enum):
    NOTES = "Notes"
    ASSIGNMENT = "Assignments"

# --- SQLAlchemy Models ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    department = Column(SQLEnum(Department))
    year = Column(SQLEnum(Year))
    controlled_by = Column(Integer, ForeignKey("users.id")) # Teacher ID for a volunteer

    supervisor = relationship("User", remote_side=[id])
    uploads = relationship("File", back_populates="uploader")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department = Column(SQLEnum(Department), nullable=False)
    year = Column(SQLEnum(Year), nullable=False)
    type = Column(SQLEnum(FileType), nullable=False)
    drive_file_id = Column(String, unique=True, nullable=False)
    share_link = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=True)

    uploader = relationship("User", back_populates="uploads")

class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(SQLEnum(Department), nullable=False)
    year = Column(SQLEnum(Year), nullable=False)
    subject = Column(String, nullable=False)
    type = Column(SQLEnum(FileType), nullable=False)
    folder_id = Column(String, unique=True, nullable=False)
