from flask import Flask, render_template, url_for, request, flash, redirect,jsonify, send_file
from extensions import db 
from models import Question, Testimony, Contact
from commands import create_tables
from chat import get_response
from error_handlers import errors
import time

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)
    # login_manager.init_app(app)

    # login_manager.login_view = ''
    # @login_manager.user_loader
    # def load_user(user_id):
    #    return User.query.get(user_id) 


    @app.route('/home')
    def index():
        return render_template('index.html')

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/blog')
    def blog():
        return render_template('blog.html')
    
    @app.route('/download')
    def download_file():
        file_path = "download/Murtaza_CV.pdf"
        return send_file(file_path, as_attachment=True)
    
    @app.post("/predict")
    def predict():
        text = request.get_json().get("message")
        response = get_response(text)
        
        message = {"answer": response}
        return jsonify(message)

    @app.route('/about')
    def about():
        return render_template('about.html') 

    @app.route('/projects')
    def projects():
        return render_template('projects.html')

    @app.route('/contact', methods=["POST", "GET"])
    def contact():
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']       

            new_subject = Contact(name=name, email=email, subject=subject)
            try:
                db.session.add(new_subject)
                db.session.commit()
                flash('Awesome😎. Thank you for the valuable message.')
                return redirect('/contact')
            except:
                return "There was an error posting your question"
            
        else:
            return render_template('contact.html')
        

    @app.route('/services')
    def services():
        return render_template('services.html')

    @app.route('/bot', methods=['POST', 'GET'])
    def bot():
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['emailid']
            question = request.form['question']
            summary = request.form['message']
            
            new_question = Question(first_name=first_name, last_name=last_name, email=email, subject=question, text = summary)
            try:
                db.session.add(new_question)
                db.session.commit()
                flash('Awesome😎. Thank you for the valuable question. We will get back to you shortly')
                return redirect('/bot')
            except:
                return "There was an error posting your question"
            
        else:
            return render_template('bot.html')
    
    @app.route('/write_testimony', methods=['POST', 'GET'])
    def write_testimony():
        if request.method == "POST":
            first_name = request.form['name']
            company = request.form['company_name']
            testimony = request.form['testimony']
            
            new_testimony = Testimony(name=first_name, company_name=company, testimony=testimony)
            try:
                db.session.add(new_testimony)
                db.session.commit()
                flash('Gratitude🙏. I appriciate your testimony')
                return redirect('/write_testimony')
            except:
                return "There was an error posting your testimony"
            
        else:
            testimonies = Testimony.query.order_by(Testimony.id)
            return render_template('write_testimony.html')


    @app.route('/questions_asked')
    def questions_asked():
        questions = Question.query.order_by(Question.first_name)
        subjects = Contact.query.order_by(Contact.date_created)
        return render_template('questions_asked.html', questions=questions, subjects=subjects)
        
    app.register_blueprint(errors)
    app.cli.add_command(create_tables)

    if __name__ == '__main__':
        app.run(debug=True)
    
    return app