from ..models.mymodels import FellowEntry
from flask import render_template, request, Blueprint
from playhouse.shortcuts import model_to_dict
import os

my_view = Blueprint('my_view', __name__)


@my_view.route('/')
def index():
    return render_template('index.html')


@my_view.route('/fellows', methods=["GET", "POST"])
def fellows():
    if request.form:

        availability = request.form.getlist('availability')
        interest = request.form.getlist('interest')
        skill = request.form.getlist('skills')
        print("get: ", availability, interest, skill)

        query = True

        if "Spring23 Intern" in availability:
            query &= FellowEntry.availability_sp23 == True
        if "Summer23 Intern" in availability:
            query &= FellowEntry.availability_su23 == True 
        if "Fall23 Intern" in availability:
            query &= FellowEntry.availability_fa23 == True
        if "Full Time ASAP" in availability:
            query &= FellowEntry.availability_ft23 == True 
        
        # must match all entered by recruiter (if recruiter enter 2, fellow must have at least both specified)

        if "Front-end" in interest:
            query &= FellowEntry.interest_fe == True 
        if "Back-end" in interest:
            query &= FellowEntry.interest_be == True 
        if "Mobile" in interest:
            query &= FellowEntry.interest_mb == True 
        if "SRE/PE" in interest:
            query &= FellowEntry.interest_pe == True 

        if "Python" in skill:
            query &= FellowEntry.skill_py == True
        if "JavaScript" in skill:
            query &= FellowEntry.skill_js == True
        if "C++" in skill:
            query &= FellowEntry.skill_cp == True
        if "Swift" in skill:
            query &= FellowEntry.skill_sw == True
        
        fellows = list( FellowEntry.select().where(
            query 
        ))


    else:
        fellows = [
            model_to_dict(f)
            for f in FellowEntry.select().order_by(FellowEntry.created_at.desc())
        ]
    return render_template('fellows.html', fellows=fellows)


@my_view.route('/form')
def form():
    return render_template('form.html')


@my_view.route('/fellow/create/', methods=['POST'])
def post_fellow_entries():
    name = request.form['name']
    batch = request.form['batch']
    
    availability = request.form.getlist('availability')
    availability_sp23 = True if "Spring23 Intern" in availability else False
    availability_su23 = True if "Summer23 Intern" in availability else False 
    availability_fa23 = True if "Fall23 Intern" in availability else False 
    availability_ft23 = True if "Full Time ASAP" in availability else False 

    interest = request.form.getlist('interest')
    interest_fe = True if "Front-end" in interest else False 
    interest_be = True if "Back-end" in interest else False 
    interest_mb = True if "Mobile" in interest else False 
    interest_pe = True if "SRE/PE" in interest else False 

    skills = request.form.getlist('skills')
    skill_py = True if "Python" in skills else False 
    skill_js = True if "JavaScript" in skills else False 
    skill_cp = True if "C++" in skills else False 
    skill_sw = True if "Swift" in skills else False         
    
    linkedin = request.form['linkedin']
    github = request.form['github']
    portfolio = request.form['portfolio']

    fellow_entry = FellowEntry.create(
                    name=name, 
                    batch=batch, 
                    availability=availability, 
                    availability_sp23=availability_sp23, 
                    availability_su23=availability_su23,
                    availability_fa23=availability_fa23,
                    availability_ft23=availability_ft23,
                    interest=interest,
                    interest_fe=interest_fe,
                    interest_be=interest_be,
                    interest_mb=interest_mb,
                    interest_pe=interest_pe,
                    skill = skills,
                    skill_py = skill_py,
                    skill_js = skill_js,
                    skill_cp = skill_cp,
                    skill_sw = skill_sw,
                    linkedin=linkedin, 
                    github=github, 
                    portfolio=portfolio )
    return render_template('create_fellow.html', fellow=fellow_entry)