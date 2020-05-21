-- DROP TABLE public.teachers;

CREATE TABLE public.teachers (
	id serial NOT NULL,
	"name" varchar(20) NOT NULL,
	about text NOT NULL,
	picture varchar(128) NOT NULL,
	rating numeric(2,1) NOT NULL,
	price int4 NOT NULL,
	"free" text NOT NULL,
	CONSTRAINT teachers_pk PRIMARY KEY (id)
);


-- DROP TABLE public.goals;

CREATE TABLE public.goals (
	id varchar(12) NOT NULL,
	"name" varchar(24) NOT NULL,
	CONSTRAINT goals_pk PRIMARY KEY (id)
);


-- DROP TABLE public.free_time;

CREATE TABLE public.free_time (
	id serial NOT NULL,
	"time" varchar(5) NOT NULL,
	CONSTRAINT free_time_pk PRIMARY KEY (id)
);


-- DROP TABLE public.schedule;

CREATE TABLE public.schedule (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	week_day int4 NOT NULL,
	"time" varchar(5) NOT NULL,
	status bool NOT NULL,
	teacher_id int4 NOT NULL,
	CONSTRAINT schedule_pk PRIMARY KEY (id)
);


-- public.schedule foreign keys

ALTER TABLE public.schedule ADD CONSTRAINT schedule_fk FOREIGN KEY (teacher_id) REFERENCES teachers(id);


-- DROP TABLE public.bookings;

CREATE TABLE public.bookings (
	id serial NOT NULL,
	schedule_id int4 NOT NULL,
	client_name varchar(20) NOT NULL,
	client_phone varchar(15) NOT NULL,
	CONSTRAINT bookings_pk PRIMARY KEY (id)
);


-- public.bookings foreign keys

ALTER TABLE public.bookings ADD CONSTRAINT bookings_fk FOREIGN KEY (schedule_id) REFERENCES schedule(id);


-- DROP TABLE public.teachers_goals;

CREATE TABLE public.teachers_goals (
	teachers_id int4 NOT NULL,
	goals_id varchar(12) NOT NULL,
	CONSTRAINT teachers_goals_pk PRIMARY KEY (teachers_id, goals_id)
);


-- public.teachers_goals foreign keys

ALTER TABLE public.teachers_goals ADD CONSTRAINT teachers_goals_fk FOREIGN KEY (teachers_id) REFERENCES teachers(id);
ALTER TABLE public.teachers_goals ADD CONSTRAINT teachers_goals_fk_1 FOREIGN KEY (goals_id) REFERENCES goals(id);


-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	id serial NOT NULL,
	client_name varchar(20) NOT NULL,
	client_phone varchar(15) NOT NULL,
	goals_id varchar(12) NOT NULL,
	time_id int4 NOT NULL,
	CONSTRAINT orders_pk PRIMARY KEY (id)
);


-- public.orders foreign keys

ALTER TABLE public.orders ADD CONSTRAINT orders_fk FOREIGN KEY (goals_id) REFERENCES goals(id);
ALTER TABLE public.orders ADD CONSTRAINT orders_fk_1 FOREIGN KEY (time_id) REFERENCES free_time(id);