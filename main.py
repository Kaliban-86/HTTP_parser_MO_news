import pickle
import re
import sqlite3
import datetime

conn = sqlite3.connect('studies.db')

cursor = conn.cursor()

cursor.execute('SELECT * from lessons')

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.first_lesson = d.id and l.first_lesson_type = ct.id ')

first_lesson_res = cursor.fetchall()

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.second_lesson = d.id and l.second_lesson_type = ct.id')

second_lesson_res = cursor.fetchall()

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.third_lesson = d.id and l.third_lesson_type = ct.id')

third_lesson_res = cursor.fetchall()

sum_lessons_res = []


def concat_lesson(first_lessons, second_lessons, third_lesson):
    res_lessons = []

    for k in range(len(first_lessons)):
        if first_lessons[k][0] == second_lessons[k][0] == third_lesson[k][0]:
            day_lessons = [first_lessons[k][0], str(first_lessons[k][1]) + ' (' + str(first_lessons[k][2]) + ')',
                           str(second_lessons[k][1]) + ' (' + str(second_lessons[k][2]) + ')',
                           str(third_lesson[k][1]) + ' (' + str(third_lesson[k][2]) + ')']
            res_lessons.append(day_lessons)

    return res_lessons


all_lessons = concat_lesson(first_lesson_res, second_lesson_res, third_lesson_res)

if __name__ == '__main__':
    current_date = datetime.date.today()
    for i in all_lessons:
        if str(current_date) == i[0]:
            print(i)
