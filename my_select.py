from connect_db import session
from models import Student, Subject, Teacher, Mark, Group
from sqlalchemy import func, desc


def making_table(
    words, certain_list
):  # this makes our results more beautiful  and readable for eyes
    table = "|{:*^50}|".format(words)
    for mark in certain_list:
        try:
            some_str = "|{:-<25}{:->25}|".format(mark[0], mark[1])
        except IndexError:
            some_str = "|{:-^50}|".format(mark[0])
        table += f"\n{some_str}"
    table += "\n|{:*^50}|".format("The end")
    return table


def select_1():
    result = (
        session.query(
            Student.name, func.round(func.avg(Mark.mark), 2).label("avg_mark")
        )
        .select_from(Mark)
        .group_by(Student.id)
        .order_by(desc("avg_mark"))
        .limit(5)
        .all()
    )

    return result


def select_2():
    subject_name = input("Please, enter subject name: ")
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if subject:
        subject_id = subject.id

        result = (
            session.query(
                Student.name, func.round(func.avg(Mark.mark), 2).label("avg_mark")
            )
            .join(Mark)
            .filter(Mark.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg_mark"))
            .limit(1)
            .first()
        )

        if result:
            return f"Student {result[0]} has the highest average mark {result[1]} from subject {subject_name}"
        else:
            return f"There are no students with marks in this subject {subject_name}"
    return f"There is no subject with such name {subject_name}"


def select_3():
    subject_name = input("Enter subject name: ")
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if subject:
        result = (
            session.query(Group.name, func.round(func.avg(Mark.mark), 2))
            .select_from(Group)
            .join(Student, Student.group_id == Group.id)
            .join(Mark, Mark.student_id == Student.id)
            .join(Subject, Subject.id == Mark.subject_id)
            .filter(Subject.name == subject_name)
            .group_by(Group.name)
            .all()
        )
        return making_table("Groups and marks", result)
    return f"There is no such subject {subject_name}"


def select_4():
    return session.query(func.round(func.avg(Mark.mark), 2)).scalar()


def select_5():
    teacher_name = input("Enter teacher name: ")
    teacher = session.query(Teacher).filter_by(name=teacher_name).first()
    if teacher:
        teacher_id = teacher.id
        courses = (
            session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        )
        return courses
    return f"There is no teacher with such name {teacher_name}"


def select_6():
    group_name = input("Enter group name like this 'Group №': ")
    group = session.query(Group).filter_by(name=group_name).first()
    if group:
        students = session.query(Student.name).filter_by(group_id=group.id).all()
        return making_table(f"Students in {group_name}", students)
    return f"There is no group with such name {group_name}."


def select_7():
    group_name = input("Enter group name like this 'Group №': ")
    subject_name = input("Enter subject name: ")

    group = session.query(Group).filter_by(name=group_name).first()
    subject = session.query(Subject).filter_by(name=subject_name).first()

    if group and subject:
        marks = (
            session.query(Student.name, Mark.mark)
            .join(Mark)
            .join(Subject)
            .join(Group)
            .filter(Group.id == group.id, Subject.id == subject.id)
            .all()
        )
        return making_table(f"Students of {group_name} in {subject_name}", marks)
    return f"There is no such group or subject!"


def select_8():
    teacher_name = input("Enter teacher name: ")
    teacher = session.query(Teacher).filter_by(name=teacher_name).first()
    if teacher:
        teacher_id = teacher.id
        subjects = (
            session.query(Subject.name, func.round(func.avg(Mark.mark), 2))
            .join(Teacher)
            .join(Mark)
            .filter(Teacher.id == teacher_id)
            .group_by(Subject.name)
            .all()
        )

        return making_table(f"Journal of {teacher_name}", subjects)
    return f"There is no teacher with such name {teacher_name}"


def select_9():
    student_name = input("Enter student name: ")
    student = session.query(Student).filter_by(name=student_name).first()
    if student:
        student_id = student.id

        courses = (
            session.query(Subject.name)
            .select_from(Subject)
            .join(Mark)
            .filter(Mark.student_id == student_id)
            .distinct()
            .all()
        )

        if courses:
            return making_table(f"{student_name} visits these subjects", courses)
        else:
            return f"Student {student_name} does not visit any subject."
    return f"There is no student with such name {student_name}"


def select_10():
    student_name = input("Enter student name: ")
    teacher_name = input("Enter teacher name: ")

    student = session.query(Student).filter_by(name=student_name).first()
    teacher = session.query(Teacher).filter_by(name=teacher_name).first()

    if student and teacher:
        student_id = student.id
        teacher_id = teacher.id

        courses = (
            session.query(Subject.name)
            .select_from(Subject)
            .join(Mark)
            .join(Teacher)
            .filter(Mark.student_id == student_id)
            .filter(Subject.teacher_id == teacher_id)
            .distinct()
            .all()
        )

        if courses:
            return making_table(
                f"{student_name} in subjects of {teacher_name}", courses
            )
        else:
            return f"Student {student_name} does not study any subject of the teacher {teacher_name}."

    return "There is no such student or teacher!"


all_functions = (
    [  # I wanted to make searching more universal but later you'll see I couldn't
        select_1,
        select_2,
        select_3,
        select_4,
        select_5,
        select_6,
        select_7,
        select_8,
        select_9,
        select_10,
    ]
)


def numbering():
    """
    if int(number) >= 1 and int(number) <= 10:   #That's how I wanted to do it
        for function in all_functions:
            if str(function).endswith(number):
                return function()
    else:
        return "The number should be >=1 and <=10"
    """
    number = int(
        input("Enter number of a question: ")
    )  # I know it's not good to do like this but I have no time and wanna finish modules to be in the project
    if number == 1:
        return select_1()
    elif number == 2:
        return select_2()
    elif number == 3:
        return select_3()
    elif number == 4:
        return select_4()
    elif number == 5:
        return select_5()
    elif number == 6:
        return select_6()
    elif number == 7:
        return select_7()
    elif number == 8:
        return select_8()
    elif number == 9:
        return select_9()
    elif number == 10:
        return select_10()
    return "The number should be >=1 and <=10"


if __name__ == "__main__":
    print(numbering())
