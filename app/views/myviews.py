from ..models.mymodels import TimelinePost, FellowEntry, users
from flask import render_template, request, Blueprint
from playhouse.shortcuts import model_to_dict
import os

my_view = Blueprint('my_view', __name__)



# Routes
@my_view.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), users=users)

@my_view.route('/fellows', methods=["GET", "POST"])
def fellows():
    if request.form:
        fellows = list( FellowEntry.select().where(
            (request.form.getlist('availability') in FellowEntry.availability) &
            (request.form.getlist('interest') in FellowEntry.interest) &
            (request.form.getlist('skills') in FellowEntry.skills) 
            ))
    else:
        fellows = [
            model_to_dict(f)
            for f in FellowEntry.select().order_by(FellowEntry.created_at.desc())
        ]
    return render_template('fellows.html', title="Fellows", fellows=fellows)

@my_view.route('/form')
def form():
    return render_template('form.html', title="Form")

@my_view.route('/user/<id>/')
def user(id):
    try:
        user = users[int(id)]
        return render_template('user.html', **user)
    except Exception as e:
        return f"User not found! {id}"

@my_view.route('/timeline')
def timeline():
    posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]
    return render_template('timeline.html', title="Timeline", posts=posts)

# Fellow-entries
@my_view.route('/fellow/create/', methods=['POST'])
def post_fellow_entries():

    name = request.form['name']
    batch = request.form.getlist('batch')
    availability = request.form.getlist('availability')
    interest = request.form.getlist('interest')
    skills = request.form.getlist('skills')
    linkedin = request.form['linkedin']
    github = request.form['github']
    portfolio = request.form['portfolio']

    fellow_entry = FellowEntry.create(name=name, batch=batch, availability=availability, interest=interest, skills=skills, linkedin=linkedin, github=github, portfolio=portfolio )
    return render_template('create_fellow.html', title="New Fellow", fellow=fellow_entry)

@my_view.route('/api/fellow_entry', methods=['GET'])
def get_fellow_entries():
    return {
        'fellow_entry': [
            model_to_dict(p)
            for p in FellowEntry.select().order_by(FellowEntry.created_at.desc())
        ]
    }

# Timeline API
@my_view.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except Exception as e:
        return "Invalid name", 400
    else:
        if name == '':
            return "Invalid name", 400
    
    try:
        email = request.form['email']
    except Exception as e:
        return "Invalid email", 400
    else:
        if email == '':
            return "Invalid email", 400

    try:
        content = request.form['content']
    except Exception as e:
        return "Invalid content", 400
    else:
        if content == '':
            return "Invalid content", 400

    # if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
    #     return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@my_view.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
    
@my_view.route('/api/timeline_post/', methods=['DELETE'])
def delete_time_line_post():
    obj = TimelinePost.get(TimelinePost.name=="test")
    obj.delete_instance()
    return print(f"Deleted test record")
