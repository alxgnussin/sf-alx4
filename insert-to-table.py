import json
import os

import psycopg2

from sources_data import get_json_data, day_id, days, times_for_learning

conn_str = os.environ.get("DATABASE_URL")

teachers = get_json_data('teachers.json')
goals = get_json_data('goals.json')


def insert_teachers():
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "teachers" ("name", "about", "rating", "picture", "price", "goals", "free") VALUES '
    for x in teachers:
        query = prefix + '(%s, %s, %s, %s, %s, %s, %s)'
        curs.execute(query, [x['name'], x['about'], x['rating'], x['picture'], x['price'],
                             json.dumps(x['goals'], ensure_ascii=False), json.dumps(x['free'], ensure_ascii=False)])
        conn.commit()
    conn.close()


def insert_goals():
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "goals" ("id", "name") VALUES '
    for key, name in goals.items():
        query = prefix + '(%s, %s)'
        curs.execute(query, [key, name])
        conn.commit()
    conn.close()


def insert_association():
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "teachers_goals" ("teachers_id", "goals_id") VALUES '
    for teacher in teachers:
        select_id_query = 'SELECT "id" FROM "teachers" WHERE "name" = %s'
        curs.execute(select_id_query, [teacher['name']])
        teacher_id = curs.fetchone()[0]

        for goal in teacher['goals']:
            query = prefix + '(%s, %s)'
            curs.execute(query, [teacher_id, goal])
            conn.commit()
    conn.close()


def insert_to_schedule():
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "schedule" ("teacher_id", "week_day", "day_name", "time", "status") VALUES '
    for teacher in teachers:
        select_id_query = 'SELECT "id" FROM "teachers" WHERE "name" = %s'
        curs.execute(select_id_query, [teacher['name']])
        teacher_id = curs.fetchone()[0]
        for key, values in teacher['free'].items():
            for time, status in values.items():
                if len(time) == 4:
                    time = '0' + time
                query = prefix + '(%s, %s, %s, %s, %s)'
                curs.execute(query, [teacher_id, day_id[key], days[key], time, status])
                conn.commit()
    conn.close()


def insert_to_free_time():
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "free_time" ("time") VALUES '
    for x in times_for_learning:
        query = prefix + '(%s)'
        curs.execute(query, [x])
        conn.commit()
    conn.close()


insert_to_free_time()
