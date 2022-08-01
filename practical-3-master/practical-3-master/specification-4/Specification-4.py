from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///Spec4.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Adds the class Student, creating the student object
class Student(Base):
    __tablename__ = 'students'
    studentid = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    surname = Column(String(50))


    def __repr__(self):
        return "<User(firstname='%s', surname'%s')>" % (self.firstname, self.surname)


# Adds the class Course, creating the course object
class Course(Base):
    __tablename__ = 'courses'
    courseid = Column(Integer, primary_key=True)
    coursename = Column(String(50))

    def __repr__(self):
        return "<User(coursename='%s')>" % (self.coursename)


# Adds the class Grade, creating the Grade object
class Grade(Base):
    __tablename__ = 'grades'
    studentid = Column(Integer, ForeignKey('students.studentid'), primary_key=True)
    coursename = Column(String, ForeignKey('courses.coursename'), primary_key=True)
    mark = Column(Integer)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")


Base.metadata.create_all(bind=engine)

# Creates relationship between student and grade, and course and grade.
Student.grades = relationship("Grade", back_populates="student")
Course.grades = relationship("Grade", back_populates="course")

session = Session()


# Allows user to add a student
def add_student():
    fname=input("Please input a first name for your new student.")
    sname=input("Please input a surname for your new student.")
    new_student = Student(firstname=fname, surname=sname)
    session.add(new_student)
    session.commit()
    menu()


# Allows user to have a list of all students, which is ordered by studentid
def list_student():
    for instance in session.query(Student).order_by(Student.studentid):
        print("Student ID : ",instance.studentid, " Student's First Name : ", instance.firstname, " Student's Surname : ",
        instance.surname)
    menu()


# Allows user to add a course
def add_course():
    cname=input("Please input the name of the new course")
    new_course = Course(coursename=cname)
    session.add(new_course)
    session.commit()
    menu()


# Allows user to have a list of all courses, which is ordered by courseid
def list_course():
    for instance in session.query(Course).order_by(Course.courseid):
        print("Course ID : ", instance.courseid, " Course Name : ", instance.coursename)
    menu()


# Allows user to add a grade for a student in a certain course
def add_grade():
    valid = "False"
    valid2 = "False"
    # Validation for student id via query
    while valid == "False":
        sid=int(input("Please input the student ID for the student you wish to give a mark."))
        for instance in session.query(Student).order_by(Student.studentid):
            if instance.studentid == sid:
                valid = "True"
            else:
                valid == "False"
    # Validation for course name via query
    while valid2 == "False":
        cname = input("Please input the course name you wish to give the student a mark for.")
        for instance in session.query(Course).order_by(Course.courseid):
            if instance.coursename == cname:
                valid2 = "True"
            else:
                valid2 == "False"
    mrk = int(input("Please input the mark you want to give the student in that specific course"))
    new_mark = Grade(studentid=sid, coursename=cname, mark=mrk)
    session.add(new_mark)
    session.commit()
    menu()


# Allows user to have a list of all the grades, which is ordered by studentid.
def list_grade():
    for instance in session.query(Grade).order_by(Grade.studentid):
        print("Student ID : ",instance.studentid, " Course Name : ",instance.coursename, " Course Mark : ", instance.mark)
    menu()


# Menu for user to interact with, also has recursive function validation.
def menu():
    inp = "0"
    print('''
Add a new student-------------------1
See list of students----------------2
Add a new course--------------------3
See list of courses-----------------4
Add a grade to a student------------5
See list of student grades----------6
Quit--------------------------------7
''')
    inp=input("Please choose an option")
    if inp == "1":
        add_student()
    elif inp == "2":
        list_student()
    elif inp == "3":
        add_course()
    elif inp == "4":
        list_course()
    elif inp == "5":
        add_grade()
    elif inp == "6":
        list_grade()
    elif inp == "7":
        quit()
    else:
        print("Not a valid option, please try again")
        menu()


menu()
