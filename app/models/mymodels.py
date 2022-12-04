from peewee import (
    SqliteDatabase, MySQLDatabase, CharField, TextField, DateTimeField, Model
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

# Use Peewee ORM to auto create Tables
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

class FellowEntry(Model):
    name = CharField()
    batch = CharField()
    availability = CharField()
    interest = CharField()
    skills = CharField()
    website = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost, FellowEntry])
