#financial
from pyrogram import Client
import time

api_id = ----- # from telegram PI
api_hash = ""
import jdatetime
import psycopg2
from pyrogram import Client
from pyrogram.handlers import MessageHandler
import os
import matplotlib.pyplot as plt


class db_process:
    def insert_(count_, thing, price, ioe, year, month, day, time_):
        try:
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()
        except:
            os.system('service postgresql restart')
            time.sleep(3)
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()

        query = f"""INSERT INTO public."finance_IaE"(
        	count_, thing, price, ioe, year, month, day, time_)
        	VALUES ({int(count_)},'{thing}', {price},{ioe},{year},'{month}',{day},'{time_}');
            """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def select_(query):
        try:
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()
        except:
            os.system('service postgresql restart')
            time.sleep(3)
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()
        cursor.execute(query)
        rec = cursor.fetchall()
        print(rec)
        cursor.close()
        connection.close()
        return rec

    def monthly(month):
        try:
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()
        except:
            os.system('service postgresql restart')
            time.sleep(3)
            connection = psycopg2.connect(host="127.0.0.1", port="5432", user="", password="",
                                          database="", options="-c search_path=dbo,public")
            cursor = connection.cursor()
        query = f"""select thing,sum(price) from "finance_IaE" where month = '{month}' and ioe = False group by thing """
        print("query", query)
        cursor.execute(query)
        rec = cursor.fetchall()
        thing = []
        price = []

        for i in rec:
            thing.append(i[0])
            price.append(i[1])
        print("thing", thing)
        print("price", price)
        fig, ax = plt.subplots()
        ax.bar(thing, price)
        fig.savefig("/root/month.png")
        app.send_message(username, str(rec))
        app.send_photo(username, "/root/month.png")
        # app.send_message(username, f"month : {month}")
        cursor.close()
        connection.close()


firs_message = 0


def my_function(client, message):
    # try:
    global m1
    global firs_message
    if firs_message == 0:
        app.send_message(username, "SERVER IS UP")
        firs_message = firs_message + 1

    m = app.get_history(username, limit=1)[0]['text']
    if m1 != m:
        print(m)
        m1 = m
        if m[0] == '#' and len(m.split(' ')) == 2:
            thing = m[1:].split(' ')[0]
            price = m[1:].split(' ')[1]
            time_ = str(jdatetime.datetime.now().time())
            ioe = False
            year = str(jdatetime.datetime.now().date()).split('-')[0]
            month = month_[int(str(jdatetime.datetime.now().date()).split('-')[1]) - 1]
            day = int(str(jdatetime.datetime.now().date()).split('-')[2])
            print(year, month)
            try:
                count_ = db_process.select_(f"""select max(count_) from "finance_IaE" where thing = '{thing}' """)[0][
                             0] + 1

            except:
                count_ = 1
            db_process.insert_(count_, thing, price, ioe, year, month, day, time_)
            app.send_message(username, "insert to database")
            time.sleep(.5)
            amount = db_process.select_(
                f""" select (SELECT amount FROM category where element_ = '{thing}') - (select sum(price) from "finance_IaE" where thing = '{thing}') """)[
                0][0]
            # format(int(count_ls_2[2]), "8,d")
            app.send_message(username, thing + " amount : " + format(int(amount), "8,d") + " Toman")

        if m[0] == '.' and len(m.split(' ')) == 2:
            thing = m[1:].split(' ')[0]
            price = m[1:].split(' ')[1]
            time_ = str(jdatetime.datetime.now().time())
            ioe = True
            year = str(jdatetime.datetime.now().date()).split('-')[0]
            month = month_[int(str(jdatetime.datetime.now().date()).split('-')[1]) - 1]
            day = int(str(jdatetime.datetime.now().date()).split('-')[2])
            print(year, month)
            try:
                count_ = db_process.select_(f"""select max(count_) from "finance_IaE" where thing = '{thing}' """)[0][
                             0] + 1
            except:
                count_ = 1
            db_process.insert_(count_, thing, price, ioe, year, month, day, time_)
            app.send_message(username, "insert to database")

        if m[0] == '!':
            try:
                app.send_message(username, "please wait")
                os.system(m[1:] + " > /root/log.txt")
                with open('/root/log.txt', 'r') as os_log:
                    log = os_log.read()
                    app.send_message(username, log)
            except:
                pass
        if m[0] == '?':
            app.send_message(username, "*********Start*********")
            try:
                print("?????????")
                p1 = m[1:].split(' ')[0]
                if p1 == 'rm':
                    "report month"
                    month = m[1:].split(' ')[1]
                    print("month", month)
                    db_process.monthly(month)
                    t_amount = db_process.select_(
                        f"""select (select amount from category where element_ = 'asset') - (select sum(price) from "finance_IaE" where month = '{month}' and ioe = False)""")[
                        0][0]

                    app.send_message(username, f"amount asset of {month}: " + format(int(t_amount), "8,d"))

                    all_thing = db_process.select_(
                        """SELECT  distinct(thing)	FROM public."finance_IaE" where ioe = False ;""")
                    for i in all_thing:
                        print("==========", i[0])
                        amount = db_process.select_(
                            f""" select (SELECT amount FROM category where element_ = '{i[0]}') - (select sum(price) from "finance_IaE" where thing = '{i[0]}') """)[
                            0][0]
                        app.send_message(username, f"inventory of {str(i[0])} : " + format(int(amount), "8,d"))

                if p1 == 'inventory':
                    thing_ = m[1:].split(' ')[1]
                    amount = db_process.select_(
                        f""" select (SELECT amount FROM category where element_ = '{thing_}') - (select sum(price) from "finance_IaE" where thing = '{thing_}') """)[
                        0][0]
                    app.send_message(username, format(int(amount), "8,d"))
            except Exception as e:
                app.send_message(username, f"err in '?' part : {str(e)}")
                os.system('service postgresql restart')
                time.sleep(3)
            app.send_message(username, "*********END*********")




    else:
        global handshake
        print('NOTHING but Server is UP')
        handshake = handshake + 1
        m1 = m
        if (handshake % 1000 == 0):
            app.send_message(username, "NOTHING but Server is UP")


# except Exception as e :
# print("ERR",str(e))
# app.send_message(username, "ERR: "+ str(e))
month_ = ['farvardin', 'ordibehesht', 'khordad', 'tir', 'mordad', 'shahrivar', 'mehr', 'aban', 'azar', 'dey', 'bahman',
          'esfand']
m1 = ''
handshake = 0
username = "" #TODO user to send and recieve message 

app = Client("", api_id, api_hash)  #TODO username --  api

my_handler = MessageHandler(my_function)
app.add_handler(my_handler)

app.run()


"""
-- Table: public.finance_IaE

-- DROP TABLE public."finance_IaE";

CREATE TABLE IF NOT EXISTS public."finance_IaE"
(
    count_ integer NOT NULL DEFAULT 1,
    thing text COLLATE pg_catalog."default" NOT NULL,
    price integer,
    ioe boolean,
    year integer,
    month text COLLATE pg_catalog."default" NOT NULL,
    day integer NOT NULL,
    time_ text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "finance_IaE_pkey" PRIMARY KEY (count_, thing, time_, month, day)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."finance_IaE"
    OWNER to admin;
"""

"""
-- Table: public.category

-- DROP TABLE public.category;

CREATE TABLE IF NOT EXISTS public.category
(
    category text COLLATE pg_catalog."default" NOT NULL,
    amount integer,
    CONSTRAINT category_pkey PRIMARY KEY (category)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.category
    OWNER to admin;
"""





















