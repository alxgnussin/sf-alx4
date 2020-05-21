# -*- coding: utf-8 -*-
# Python 3.7.7 required

import json


def get_json_data(file):
    with open(file, 'r', encoding='utf8') as f:
        my_object = json.loads(f.read())
    return my_object


def schedule(data):
    timetable = []
    for i in range(1, 8):
        times = []

        for x in data:
            if x.week_day == i:
                times.append(x.time)

        dic = {'week_day': i,
               'day_name': day_names[i - 1],
               'times': times}

        timetable.append(dic)
    return timetable


week_days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресение'
}

days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресение'
}

day_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']

day_id = {
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6,
    "sun": 7
}

times_for_learning = ('1-2', '3-5', '5-7', '7-10')
