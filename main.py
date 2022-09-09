import pickle
import re
import sqlite3

conn = sqlite3.connect('studies.db')

# Создаем курсор
cursor = conn.cursor()

cursor.execute('SELECT * from lessons')

# cursor.execute('SELECT * from lessons where date=?', ('2022-09-08',))

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


# for i in second_lesson_res:
#     print(i)


def concat_lesson(first_lessons, second_lessons, third_lesson):
    res_lessons = []

    for k in range(len(first_lessons)):
        if first_lessons[k][0] == second_lessons[k][0] == third_lesson[k][0]:
            day_lessons = [first_lessons[k][0], str(first_lessons[k][1]) + '(' + str(first_lessons[k][2]) + ')',
                           str(second_lessons[k][1]) + '(' + str(second_lessons[k][2]) + ')',
                           str(third_lesson[k][1]) + '(' + str(third_lesson[k][2]) + ')']
            res_lessons.append(day_lessons)

    return res_lessons


all_lessons = concat_lesson(first_lesson_res, second_lesson_res, third_lesson_res)

for i in all_lessons:
    print(i)
