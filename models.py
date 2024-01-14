from datetime import datetime
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher")


class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, CheckConstraint("mark>=0 AND mark<=100"))
    mark_date = Column(DateTime, default=datetime.now())
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    student = relationship("Student")
    subject = relationship("Subject")
