from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy import MetaData


# creating tables


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    field: Mapped[str]
    semester_no: Mapped[int]
    selected_course: Mapped[list["SelectedCourse"]] = relationship(back_populates="student")


class Teacher(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    profession: Mapped[str] = mapped_column(String(255))
    course: Mapped[list["Course"]] = relationship(back_populates="teacher")


class Lesson(Base):
    __tablename__ = "lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    pre_rel: Mapped[list["Lesson"]] = relationship(back_populates="prerequisite")
    course: Mapped[list["Course"]] = relationship(back_populates="lesson")


class LessonLesson(Base):
    __tablename__ = "lesson_lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"))
    prerequisite_id = Mapped[int] = mapped_column(ForeignKey("lesson.id"))

    lesson: Mapped["Lesson"] = relationship(back_populates="pre_rel")
    prerequisite: Mapped["Lesson"] = relationship(back_populates="pre_rel")


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("Lesson.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("Teacher.id"))
    time: Mapped[str]
    lesson: Mapped["Lesson"] = relationship(back_populates="course")
    teacher: Mapped["Teacher"] = relationship(back_populates="course")
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="course")
    selected_course: Mapped[list["SelectedCourse"]] = relationship(back_populates="course")


class Class(Base):
    __tablename__ = "class"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="class_")


class Schedule(Base):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("Course.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("Class.id"))
    time: Mapped[str]
    course: Mapped["Course"] = relationship(back_populates="schedule")
    class_: Mapped["Class"] = relationship(back_populates="schedule")


class SelectedCourse(Base):
    __tablename__ = "selected_course"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("Student.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("Course.id"))
    student: Mapped["Student"] = relationship(back_populates="selected_course")
    course: Mapped["Course"] = relationship(back_populates="selected_course")


engine = create_engine("postgresql+psycopg2://postgres:88775566@localhost:5432/postgres", echo=True)


# Base.metadata.create_all(bind=engine)

class StudentSession:
    def add(self):
        id_ = int(input("enter student id: "))
        name = input("enter student name: ")
        field = input("enter filed of student: ")
        semester_no = int(input("enter semester number of student: "))
        new_student = Student(id=id_, name=name, field=field, semester_no=semester_no)
        with Session(engine) as session:
            session.add_all([new_student])
            session.commit()

    def update(self):
        id_ = int(input("enter student id: "))
        with Session(engine) as session:
            stmt = select(Student).where(Student.id.in_([id_]))
            student = session.scalars(stmt).one()
            student.id = int(input("enter new id of student: "))
            student.name = input("enter new name of student: ")
            student.field = input("enter new field of student: ")
            student.semester_no = int(input("enter new semester number of student: "))
            session.commit()

    def delete(self):
        id_ = int(input("enter student id: "))
        with Session(engine) as session:
            student = session.get(Student, id_)
            session.delete(student)
            session.commit()


class TeacherSession:
    def add(self):
        id_ = int(input("enter teacher id: "))
        name = input("enter teacher name: ")
        profession = input("enter profession of teacher: ")
        new_teacher = Teacher(id=id_, name=name, profession=profession)
        with Session(engine) as session:
            session.add_all([new_teacher])
            session.commit()

    def update(self):
        id_ = int(input("enter teacher id: "))
        with Session(engine) as session:
            stmt = select(Teacher).where(Teacher.id.in_([id_]))
            techer = session.scalars(stmt).one()
            techer.id = int(input("enter new id of student: "))
            techer.name = input("enter new name of student: ")
            techer.profession = input("enter new profession of teacher: ")
            session.commit()

    def delete(self):
        id_ = int(input("enter student id: "))
        with Session(engine) as session:
            teacher = session.get(Teacher, id_)
            session.delete(teacher)
            session.commit()


class LessonSession:
    def add(self):
        id_ = int(input("enter lesson id: "))
        name = input("enter lesson name: ")
        new_lesson = Lesson(id=id_, name=name)
        with Session(engine) as session:
            session.add_all([new_lesson])
            session.commit()

    def update(self):
        id_ = int(input("enter lesson id: "))
        with Session(engine) as session:
            stmt = select(Lesson).where(Lesson.id.in_([id_]))
            lesson = session.scalars(stmt).one()
            lesson.id = int(input("enter new id of lesson: "))
            lesson.name = input("enter new name of lesson: ")
            session.commit()

    def delete(self):
        id_ = int(input("enter lesson id: "))
        with Session(engine) as session:
            lesson = session.get(Lesson, id_)
            session.delete(lesson)
            session.commit()


class CourseSession:
    def add(self):
        id_ = int(input("enter course id: "))
        lesson_id = int(input("enter lesson id: "))
        teacher_id = int(input("enter teacher id: "))
        time = input("enter presentation time: ")
        new_course = Course(id=id_, lesson_id=lesson_id, teacher_id=teacher_id, time=time)
        with Session(engine) as session:
            session.add_all([new_course])
            session.commit()

    def update(self):
        id_ = int(input("enter course id: "))
        with Session(engine) as session:
            stmt = select(Course).where(Course.id.in_([id_]))
            course = session.scalars(stmt).one()
            course.id = int(input("enter new id of student: "))
            course.lesson_id = int(input("enter new lesson id: "))
            course.teacher_id = int(input("enter new teacher id: "))
            course.time = input("enter new presentation time: ")
            session.commit()

    def delete(self):
        id_ = int(input("enter course id: "))
        with Session(engine) as session:
            course = session.get(Course, id_)
            session.delete(course)
            session.commit()


class ClassSession:
    def add(self):
        id_ = int(input("enter class id: "))
        name = input("enter class name: ")
        new_class = Class(id=id_, name=name)
        with Session(engine) as session:
            session.add_all([new_class])
            session.commit()

    def update(self):
        id_ = int(input("enter class id: "))
        with Session(engine) as session:
            stmt = select(Class).where(Class.id.in_([id_]))
            class_ = session.scalars(stmt).one()
            class_.id = int(input("enter new id of class: "))
            class_.name = input("enter new name of class: ")
            session.commit()

    def delete(self):
        id_ = int(input("enter class id: "))
        with Session(engine) as session:
            class_ = session.get(Class, id_)
            session.delete(class_)
            session.commit()


class ScheduleSession:
    def add(self):
        id_ = int(input("enter schedule id: "))
        course_id = int(input("enter course id: "))
        class_id = int(input("enter class id: "))
        time = input("enter presentation time: ")
        new_schedule = Schedule(id=id_, course_id=course_id, class_id=class_id, time=time)
        with Session(engine) as session:
            session.add_all([new_schedule])
            session.commit()

    def update(self):
        id_ = int(input("enter schedule id: "))
        with Session(engine) as session:
            stmt = select(Schedule).where(Schedule.id.in_([id_]))
            schedule = session.scalars(stmt).one()
            schedule.id = int(input("enter new id of schedule: "))
            schedule.course_id = int(input("enter new course id: "))
            schedule.class_id = int(input("enter new class id: "))
            schedule.time = input("enter new presentation time: ")
            session.commit()

    def delete(self):
        id_ = int(input("enter schedule id: "))
        with Session(engine) as session:
            schedule = session.get(Schedule, id_)
            session.delete(schedule)
            session.commit()


class SelectedCourseSession:
    def add(self):
        id_ = int(input("enter selected course id: "))
        student_id = int(input("enter student id: "))
        course_id = id(input("enter course id: "))
        new_selected_course = SelectedCourse(id=id_, student_id=student_id, course_id=course_id)
        with Session(engine) as session:
            session.add_all([new_selected_course])
            session.commit()

    def update(self):
        id_ = int(input("enter selected course id: "))
        with Session(engine) as session:
            stmt = select(SelectedCourse).where(SelectedCourse.id.in_([id_]))
            selected_course = session.scalars(stmt).one()
            selected_course.id = int(input("enter new id of selected course: "))
            selected_course.student_id = int(input("enter new student id of selected course : "))
            selected_course.course_id = int(input("enter new course id of selected course: "))
            session.commit()

    def delete(self):
        id_ = int(input("enter selected course id: "))
        with Session(engine) as session:
            selected_course = session.get(SelectedCourse, id_)
            session.delete(selected_course)
            session.commit()
