from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

teachers_goals = db.Table(
    'teachers_goals',
    db.Column("teachers_id", db.Integer, db.ForeignKey("teachers.id")),
    db.Column("goals_id", db.String(12), db.ForeignKey("goals.id")),
)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    about = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.relationship('Goals', secondary=teachers_goals, back_populates='teachers')
    schedule = db.relationship('Schedule', back_populates='teacher')


class Booking(db.Model):
    # render_booking_done
    __tablename__ = 'bookings'  # запись на пробный урок
    id = db.Column(db.Integer, primary_key=True)
    schedule = db.relationship('Schedule', back_populates='bookings')
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    client_name = db.Column(db.String(20), nullable=False)
    client_phone = db.Column(db.String(15), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(20), nullable=False)
    client_phone = db.Column(db.String(15), nullable=False)  # String?
    goals = db.relationship('Goals', back_populates='order')
    goals_id = db.Column(db.String(12), db.ForeignKey('goals.id'))
    time = db.relationship('FreeTime', back_populates='order')
    time_id = db.Column(db.Integer, db.ForeignKey('free_time.id'))


class Goals(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    teachers = db.relationship('Teacher', secondary=teachers_goals, back_populates='goals')
    order = db.relationship('Order', back_populates='goals')


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    teacher = db.relationship('Teacher', back_populates='schedule')
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    bookings = db.relationship('Booking', back_populates='schedule')


class FreeTime(db.Model):
    __tablename__ = 'free_time'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(5), nullable=False)
    order = db.relationship('Order', back_populates='time')