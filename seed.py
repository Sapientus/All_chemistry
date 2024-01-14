from connect_db import session
from models import Student, Subject, Teacher, Mark, Group
from random import randint
import faker
from datetime import datetime

STUDENTS_AMOUNT = (30, 50)
TEACHERS_AMOUNT = (3, 5)
GROUPS_AMOUNT = (3, 5)
SUBJECTS_AMOUNT = (6, 9)
fake_data = faker.Faker()


def fake_names(certain_constant):
    fake_names = []
    for _ in range(randint(certain_constant[0], certain_constant[1])):
        fake_names.append(fake_data.name())
    return fake_names


def fake_words(certain_constant):
    fake_words = []
    for _ in range(randint(certain_constant[0], certain_constant[1])):
        fake_words.append(fake_data.word())
    return fake_words


def fake_numbers(certain_constant, limit):
    fake_numbers = []
    for _ in range(randint(certain_constant[0], certain_constant[1])):
        fake_numbers.append(randint(*limit))
    return fake_numbers


def main():
    teachers = []
    groups = []
    subjects = []
    students = []
    marks = []
    numbers = fake_numbers(GROUPS_AMOUNT, (0, 20))
    for n in numbers:
        group = Group(name=f"Group {n}")
        groups.append(group)
    for names in fake_names(STUDENTS_AMOUNT):
        obj = Student(name=names, group_id=randint(1, len(groups)))
        students.append(obj)
    for teacher_name in fake_names(TEACHERS_AMOUNT):
        teacher_obj = Teacher(
            name=teacher_name,
        )
        teachers.append(teacher_obj)
    for words in fake_words(SUBJECTS_AMOUNT):
        subject_obj = Subject(name=words, teacher_id=randint(1, len(teachers)))
        subjects.append(subject_obj)
    for month in range(1, 13):
        mark_d = datetime(2023, month, randint(10, 20)).date()
        for st_id in range(1, len(students) + 1):
            mark_obj = Mark(
                mark=randint(1, 100),
                mark_date=mark_d,
                student_id=st_id,
                subject_id=randint(1, len(subjects)),
            )
            marks.append(mark_obj)
    ready_objects = [*teachers, *students, *subjects, *groups, *marks]
    return ready_objects


if __name__ == "__main__":
    for smth in main():
        session.add(smth)
    session.commit()
