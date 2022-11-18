from ..models.mymodels import TimelinePost, FellowEntry, users
from flask import render_template, request, Blueprint
from playhouse.shortcuts import model_to_dict
import os

my_view = Blueprint('my_view', __name__)

# Routing 
@my_view.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), users=users)

@my_view.route('/timeline')
def timeline():
    posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]
    return render_template('timeline.html', title="Timeline", posts=posts)

@my_view.route('/fellows')
def fellows():
    posts = [
        model_to_dict(p)
        for p in FellowEntry.select().order_by(FellowEntry.created_at.desc())
    ]
    return render_template('fellows.html', title="Fellows", posts=posts)

@my_view.route('/form')
def form():
    posts = [
        model_to_dict(p)
        for p in FellowEntry.select().order_by(FellowEntry.created_at.desc())
    ]
    return render_template('form.html', title="Form", posts=posts)

@my_view.route('/user/<id>/')
def user(id):
    try:
        user = users[int(id)]
        return render_template('user.html', **user)
    except Exception as e:
        return f"User not found! {id}"


# Fellow entries API
@my_view.route('/api/fellow_entry', methods=['POST'])
def post_time_line_post():

    name = request.form['name']
    batch = request.form['batch']
    availability = request.form['availability']
    interest = request.form['interest']
    skills = request.form['skills']
    website = request.form['website']

    fellow_entry = FellowEntry.create(name=name, batch=batch, availability=availability, interest=interest, skills=skills, website=website )
    return model_to_dict(fellow_entry)

@my_view.route('/api/fellow_entry', methods=['GET'])
def get_time_line_post():
    return {
        'fellow_entry': [
            model_to_dict(p)
            for p in FellowEntry.select().order_by(FellowEntry.created_at.desc())
        ]
    }