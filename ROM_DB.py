from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///timetable.db', echo=True)
engine.connect()

Base = declarative_base()


class DayTimetable(Base):
    __tablename__ = 'Day timetable'
    date = Column(Date, primary_key=True)
    first_lesson = Column(String)
    first_lesson_type = Column(String)
    second_lesson = Column(String)
    second_lesson_type = Column(String)
    third_lesson = Column(String)
    third_lesson_type = Column(String)

    def __init__(self, date, first_lesson, first_lesson_type, second_lesson, second_lesson_type, third_lesson,
                 third_lesson_type):
        self.date = date
        self.first_lesson = first_lesson
        self.first_lesson_type = first_lesson_type
        self.second_lesson = second_lesson
        self.second_lesson_type = second_lesson_type
        self.third_lesson = third_lesson
        self.third_lesson_type = third_lesson_type

    def __str__(self):
        return f'{self.date}:{self.first_lesson}({self.first_lesson_type})-{self.second_lesson}({self.second_lesson_type})-{self.third_lesson}({self.third_lesson_type})'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
current_date = datetime.date.today()


# mon_26_09 = DayTimetable(current_date, '04', 'L', '04', 'L', '10', 'L')
#
# session.add(mon_26_09)
#
# session.commit()

def save_data_to_db(session_to, date_y, date_m, date_d, first_lesson, first_lesson_type, second_lesson, second_lesson_type,
                    third_lesson,
                    third_lesson_type):

    lesson_date = datetime.datetime(date_y, date_m, date_d)

    day_to = DayTimetable(lesson_date, first_lesson, first_lesson_type, second_lesson, second_lesson_type,
                          third_lesson,
                          third_lesson_type)
    session_to.add(day_to)
    session_to.commit()


my_date = datetime.datetime(2022, 9, 30)


save_data_to_db(session, 2022, 10, 1, '10', 'L', 'T', 'GY', 'T', 'GY')
days = session.query(DayTimetable).filter(DayTimetable.first_lesson == 'T').all()

for day in days:
    print(day)
