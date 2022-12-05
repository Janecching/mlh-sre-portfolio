from peewee import (
    SqliteDatabase, MySQLDatabase, CharField, BooleanField, DateTimeField, Model
)
import datetime
import os

# Set up MySQL database
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

# Use Peewee ORM to auto create tables
class FellowEntry(Model):
    name = CharField()
    batch = CharField()
    availability = CharField()
    availability_sp23 = BooleanField()
    availability_su23 = BooleanField()
    availability_fa23 = BooleanField()
    availability_ft23 = BooleanField()
    interest = CharField()
    interest_fe = BooleanField()
    interest_be = BooleanField()
    interest_mb = BooleanField()
    interest_pe = BooleanField()
    skill = CharField()
    skill_py = BooleanField()
    skill_js = BooleanField()
    skill_cp = BooleanField()
    skill_sw = BooleanField()
    linkedin = CharField()
    github = CharField()
    portfolio = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([FellowEntry])
