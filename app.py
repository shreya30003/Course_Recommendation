from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
from Course_Recommendation import recommend_course

app = Flask(__name__)

df = pd.DataFrame(columns=["UG_Course", "Interests", "Skills", "Certifications", "Certification_Name", "Working", "Job_Title", "Masters", "Factors"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    return redirect(url_for('info'))

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        user_data = {
            "UG_Course": "",  
            "Interests": request.form.get('interests'),
            "Skills": request.form.get('skills'),
            "Certifications": request.form.get('certifications'),
            "Certification_Name": request.form.get('certificate_name'),
            "Working": request.form.get('working'),
            "Job_Title": request.form.get('job_title'),
            "Masters": request.form.get('masters'),
            "Factors": ""  
        }
        # print("User Data : ", user_data)
        recommended_courses = recommend_course(user_data)
        return render_template('result.html', recommended_courses=recommended_courses)
    return render_template('info.html')

if __name__ == '__main__':
    app.run()
