from ..models.mymodels import FellowEntry
from flask import render_template, request, Blueprint
from playhouse.shortcuts import model_to_dict
import os

my_view = Blueprint('my_view', __name__)

# home
@my_view.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

# page to search for fellows
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

# page for fellows to enter details
@my_view.route('/form')
def form():
    return render_template('form.html', title="Form")

# page to confirm that fellow has been created
@my_view.route('/fellow/create/', methods=['POST'])
def post_fellow_entries():
    try:
        name = request.form['name']
    except Exception as e:
        return "Invalid name", 400
    else:
        if name == '':
            return "Invalid name", 400

    try:
        linkedin = request.form['linkedin']
    except Exception as e:
        return "Invalid linkedin", 400
    else:
        if name == '':
            return "Invalid linkedin", 400

    try:
        github = request.form['github']
    except Exception as e:
        return "Invalid github", 400
    else:
        if name == '':
            return "Invalid github", 400

    try:
        portfolio = request.form['portfolio']
    except Exception as e:
        return "Invalid portfolio", 400
    else:
        if name == '':
            return "Invalid portfolio", 400

    batch = request.form.getlist('batch')
    availability = request.form.getlist('availability')
    interest = request.form.getlist('interest')
    skills = request.form.getlist('skills')

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