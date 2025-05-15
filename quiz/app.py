from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bootstrap import Bootstrap5
from db import db, create_tables  
from models import * #modelle von Kaan
from datetime import date

app = Flask(__name__)


app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    SQLALCHEMY_DATABASE_URI='sqlite:///campusconnect_berlin.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

db.init_app(app)
create_tables(app)




# Information foür jeden ptype
information = {
    "INTJ": {
        "summary": "The Architect: Imaginative and strategic thinkers with a plan for everything.",
        "ei": "Introverted: You recharge alone.",
        "sn": "Intuitive: You focus on patterns and big ideas.",
        "tf": "Thinking: You base decisions on logic and objectivity.",
        "jp": "Judging: You like structure and planning.",
        "sum": "People with the INTJ personality type (Architects) are intellectually curious individuals with a deep-seated thirst for knowledge. They value creative ingenuity, straightforward rationality, and self-improvement. INTJs consistently work toward mastering topics that pique their interest."
    },
    "INTP": {
        "summary": "The Logician: Innovative inventors with an unquenchable thirst for knowledge.",
        "ei": "Introverted: You prefer quiet reflection.",
        "sn": "Intuitive: You explore possibilities and abstract theories.",
        "tf": "Thinking: You analyze situations logically.",
        "jp": "Perceiving: You like flexibility and spontaneity.",
        "sum": "INTPs are deep thinkers known for their intellectual curiosity and innovative problem-solving. They love analyzing complex ideas and exploring abstract concepts."
    },
    "ENTJ": {
        "summary": "The Commander: Bold, imaginative, and strong-willed leaders.",
        "ei": "Extraverted: You gain energy from social interaction.",
        "sn": "Intuitive: You look beyond the surface.",
        "tf": "Thinking: You make decisions based on logic.",
        "jp": "Judging: You value organization and plans.",
        "sum": "ENTJs are strategic and goal-oriented individuals who excel at organizing people and systems to achieve their visions. They're natural-born leaders with confidence and focus."
    },
    "ENTP": {
        "summary": "The Debater: Smart and curious thinkers who love intellectual challenges.",
        "ei": "Extraverted: You draw energy from others.",
        "sn": "Intuitive: You explore big-picture ideas.",
        "tf": "Thinking: You think critically and logically.",
        "jp": "Perceiving: You adapt to change and new ideas.",
        "sum": "ENTPs are energetic and enthusiastic, driven by a desire to understand and challenge existing ideas. They enjoy playful debates and brainstorming new innovations."
    },
    "INFJ": {
        "summary": "The Advocate: Quiet and mystical, yet inspiring and tireless idealists.",
        "ei": "Introverted: You need time alone to recharge.",
        "sn": "Intuitive: You focus on ideas and future possibilities.",
        "tf": "Feeling: You care deeply about people.",
        "jp": "Judging: You prefer structured approaches.",
        "sum": "INFJs are empathetic and visionary, often striving to help others while maintaining strong personal values. They're quiet but passionate about causes they believe in."
    },
    "INFP": {
        "summary": "The Mediator: Poetic, kind, and altruistic people.",
        "ei": "Introverted: You gain energy from solitude.",
        "sn": "Intuitive: You look beneath the surface.",
        "tf": "Feeling: You base decisions on your values.",
        "jp": "Perceiving: You go with the flow.",
        "sum": "INFPs are idealistic and introspective individuals who seek purpose and meaning in life. They often have a strong sense of morality and empathy for others."
    },
    "ENFJ": {
        "summary": "The Protagonist: Charismatic and inspiring leaders.",
        "ei": "Extraverted: You thrive on connection.",
        "sn": "Intuitive: You explore possibilities.",
        "tf": "Feeling: You care about harmony and empathy.",
        "jp": "Judging: You prefer planning and order.",
        "sum": "ENFJs are supportive and inspiring, often working hard to help others grow and reach their potential. They're driven by altruism and leadership."
    },
    "ENFP": {
        "summary": "The Campaigner: Enthusiastic, creative, and sociable free spirits.",
        "ei": "Extraverted: You enjoy group energy.",
        "sn": "Intuitive: You see patterns and possibilities.",
        "tf": "Feeling: You make empathetic decisions.",
        "jp": "Perceiving: You keep options open.",
        "sum": "ENFPs are curious and expressive individuals who love exploring new ideas and connecting deeply with others. They are spontaneous, energetic, and open-hearted."
    },
    "ISTJ": {
        "summary": "The Logistician: Practical and fact-minded individuals.",
        "ei": "Introverted: You recharge by being alone.",
        "sn": "Sensing: You focus on concrete facts.",
        "tf": "Thinking: You trust logic and order.",
        "jp": "Judging: You like predictability.",
        "sum": "ISTJs are responsible and reliable people who value tradition and structure. They are dependable planners who take pride in their work."
    },
    "ISFJ": {
        "summary": "The Defender: Dedicated and warm protectors.",
        "ei": "Introverted: You need alone time to recharge.",
        "sn": "Sensing: You pay attention to details.",
        "tf": "Feeling: You are loyal and compassionate.",
        "jp": "Judging: You like routine and structure.",
        "sum": "ISFJs are caring and nurturing individuals who strive to support others. They work hard behind the scenes and value loyalty and kindness."
    },
    "ESTJ": {
        "summary": "The Executive: Excellent administrators and managers.",
        "ei": "Extraverted: You get energy from leading.",
        "sn": "Sensing: You trust practical experience.",
        "tf": "Thinking: You value structure and logic.",
        "jp": "Judging: You like to be in control.",
        "sum": "ESTJs are organized and assertive individuals who excel at managing tasks and people. They value tradition, stability, and productivity."
    },
    "ESFJ": {
        "summary": "The Consul: Extraordinarily caring and popular people.",
        "ei": "Extraverted: You thrive in social situations.",
        "sn": "Sensing: You are detail-oriented.",
        "tf": "Feeling: You value empathy and harmony.",
        "jp": "Judging: You like clear expectations.",
        "sum": "ESFJs are warm and dependable, often going out of their way to meet others’ needs. They enjoy social harmony and take responsibility seriously."
    },
    "ISTP": {
        "summary": "The Virtuoso: Bold and practical experimenters.",
        "ei": "Introverted: You prefer hands-on alone work.",
        "sn": "Sensing: You are realistic and observant.",
        "tf": "Thinking: You are objective and adaptable.",
        "jp": "Perceiving: You like spontaneity.",
        "sum": "ISTPs are adventurous problem-solvers who enjoy exploring how things work. They are practical, action-oriented, and calm in crisis situations."
    },
    "ISFP": {
        "summary": "The Adventurer: Flexible and charming artists.",
        "ei": "Introverted: You enjoy solo creative work.",
        "sn": "Sensing: You focus on sensory details.",
        "tf": "Feeling: You are sensitive and expressive.",
        "jp": "Perceiving: You embrace freedom.",
        "sum": "ISFPs are gentle and open-minded, often expressing themselves through art or beauty. They live in the moment and value authenticity."
    },
    "ESTP": {
        "summary": "The Entrepreneur: Energetic and perceptive people.",
        "ei": "Extraverted: You thrive in action.",
        "sn": "Sensing: You focus on what's real.",
        "tf": "Thinking: You are confident and tactical.",
        "jp": "Perceiving: You act on impulse.",
        "sum": "ESTPs are dynamic and outgoing, often seeking excitement and challenges. They enjoy taking risks and living on the edge."
    },
    "ESFP": {
        "summary": "The Entertainer: Spontaneous, energetic, and enthusiastic performers.",
        "ei": "Extraverted: You light up in social settings.",
        "sn": "Sensing: You are fun-loving and practical.",
        "tf": "Feeling: You care about people’s experiences.",
        "jp": "Perceiving: You go with the flow.",
        "sum": "ESFPs are cheerful and expressive individuals who live for the moment. They bring joy to others and thrive on new experiences and attention."
    }
}

@app.route('/')
def home():
    return render_template('create_user.html')

#von KI (nur temporär - für die Speicherung von usern und ihre type)
@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    new_user = User(name=username, email=f"{username}@example.com", password="temp123", created_at=date.today())
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.user_id
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/results', methods=['POST'])
def results():
    #zählen
    vector_ei = sum([int(request.form[f'ei_q{i}']) for i in range(1, 4)])
    vector_sn = sum([int(request.form[f'sn_q{i}']) for i in range(1, 4)])
    vector_tf = sum([int(request.form[f'tf_q{i}']) for i in range(1, 4)])
    vector_jp = sum([int(request.form[f'jp_q{i}']) for i in range(1, 4)])

    #MBTI berechnen
    ei = 'E' if vector_ei >= 0 else 'I'
    sn = 'S' if vector_sn >= 0 else 'N'
    tf = 'T' if vector_tf >= 0 else 'F'
    jp = 'J' if vector_jp >= 0 else 'P'
    mbti_type = ei + sn + tf + jp

    personality_info = information.get(mbti_type)
    user_id = session.get('user_id')

    #wenn user existiert
    if user_id:  
        result = PersonalityResult(
            user_id=user_id,
            vec_ei=vector_ei,
            vec_sn=vector_sn,
            vec_tf=vector_tf,
            vec_jp=vector_jp,
            mbti_type=mbti_type,
            completed_at=date.today()
        )
        db.session.add(result)
        db.session.commit()

    return render_template('results.html', mbti_type=mbti_type, information=personality_info)


if __name__ == '__main__':
    app.run(debug=True)
