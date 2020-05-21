# -*- coding: utf-8 -*-
# Python 3.7.7 required
import os
from random import sample

from flask import Flask, render_template, request

from sources_data import schedule, day_names
from models import db, Teacher, Booking, Order, Goals, Schedule, FreeTime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def render_index():
    teachers_list = db.session.query(Teacher).all()
    random_teachers = sample(teachers_list, 6)
    return render_template(
        'index.html',
        goals=db.session.query(Goals).all(),
        random_teachers=random_teachers
    )


@app.route('/trainers/')
def render_trainers():
    teachers_list = db.session.query(Teacher).order_by(Teacher.rating.desc()).all()
    return render_template(
        'trainers.html',
        goals=db.session.query(Goals).all(),
        teachers=teachers_list
    )


@app.route('/goals/<goal>/')
def render_goals(goal):
    goal = db.session.query(Goals).filter(Goals.id == goal).first()
    goal_teachers = sorted(goal.teachers, key=lambda x: x.rating, reverse=True)
    return render_template(
        'goal.html',
        goal=goal.name.lower(),
        goal_teachers=goal_teachers
    )


@app.route('/profiles/<int:trainer_id>/')
def render_profiles(trainer_id):
    profile = db.session.query(Teacher).get_or_404(trainer_id)
    data = db.session.query(Schedule).filter(Schedule.teacher_id == trainer_id, Schedule.status).order_by(
        Schedule.week_day, Schedule.time).all()
    sked = schedule(data)
    return render_template(
        'profile.html',
        dic=profile,
        sked=sked
    )


@app.route('/request/')
def render_request():
    goals = db.session.query(Goals).all()
    times_for_learning = db.session.query(FreeTime).all()
    return render_template('request.html', goal=goals, time=times_for_learning)


@app.route('/request_done/', methods=['POST'])
def render_request_done():
    radio_goal = request.form.get('goal')
    radio_time = request.form.get('time')
    client_name = request.form.get('clientName')
    phone = request.form.get('clientPhone')
    goal = db.session.query(Goals).get(radio_goal)
    select_time = db.session.query(FreeTime).get(radio_time)
    if client_name and phone:
        order = Order(
            client_name=client_name,
            client_phone=phone,
            goals_id=radio_goal,
            time_id=radio_time
        )
        db.session.add(order)
        db.session.commit()
        return render_template('request_done.html', goal=goal.name, time=select_time.time, name=client_name,
                               phone=phone)
    else:
        return render_request()


@app.route('/booking/<int:trainer_id>/<int:day>/<lesson_time>/')
def render_booking(trainer_id, day, lesson_time):
    profile = db.session.query(Teacher).get_or_404(trainer_id)
    return render_template(
        'booking.html',
        teacher_name=profile.name,
        picture=profile.picture,
        id=trainer_id,
        day=day,
        day_ru=day_names[day - 1],
        lesson_time=lesson_time
    )


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    trainer_id = int(request.form.get('clientTeacher'))
    day = int(request.form.get('clientWeekday'))
    lesson_time = request.form.get('clientTime')
    client_name = request.form.get('clientName')
    phone = request.form.get('clientPhone')
    if client_name and phone:
        sked = db.session.query(Schedule).filter(Schedule.teacher_id == trainer_id, Schedule.week_day == day,
                                                 Schedule.time == lesson_time).first()
        booking = Booking(
            client_name=client_name,
            client_phone=phone,
            schedule_id=sked.id
        )
        db.session.add(booking)
        sked.status = False
        db.session.commit()

        return render_template('booking_done.html', day=day_names[day - 1], time=lesson_time, name=client_name,
                               phone=phone)
    else:
        return render_booking(trainer_id, day, lesson_time)


if __name__ == '__main__':
    app.run()
