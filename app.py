#Dependencies
from flask import Flask,render_template,session,redirect,url_for,jsonify,send_from_directory,request
from random import randint,choice
# from dbs_scripts.get_question import *
# from misc_scripts.parse_answer import *
# App stuff
app = Flask(__name__)

#Routers
# @app.route("/",methods=["GET"])
# def home():
#     return render_template("index.html")

# @app.route("/echo/<text>")
# def repeat(text):
#     return render_template("text.html",txt=text)


@app.route("/get_question")
def return_template_question():
    # questions = [{"question":"Who was the first president of the United States? This moron had white hair.","questionId":0,"answer":"George Washington"},{"question":"When was the constitution written","questionId":1,"answer":"1776"},{"question":"How tall is the Statue of Liberty","questionId":2,"answer":"305 feet"},{"question":"Who is the most epic of the four Malani cousins","questionId":3,"answer":"Arnav"},{"question":"Who wrote the Great Gatsby","questionId":4,"answer":"Francis Scott Fitzgerald"},{"question":"Who is the best Mom","questionId":5,"answer":"Shailaja Malani"}]
    # question_to_answer = questions[randint(0,5)]
    # question_to_answer["question"] = question_to_answer["question"].split()
    question = get_random_question()
    question_to_answer = {"question":question[2].replace("&apos;","'").split(),"questionId":question[0],"answer":question[4]}

    return jsonify(question_to_answer)
@app.route("/get_round_questions_with_difficulty",methods=["POST"])
def return_template_question_with_difficulty():
    request_data = request.get_json()
    print(request_data)
    questions = get_question_with_specific_difficulty(request_data["difficulty"])
    final_questions = []
    for question in questions:
        print(question)
        # question = question[0]
        print(question)
        final_questions.append({"question":question[2].replace("&apos;","'").split(),"questionId":question[0],"answer":question[4]})
    return jsonify(final_questions)
@app.route("/get_round_questions")
# get many questions in one round
def return_template_questions():
    questions = get_many_questions()
    final_questions = []
    for question in questions:
        question = question[0]
        final_questions.append({"question":question[2].replace("&apos;","'").split(),"questionId":question[0],"answer":question[4]})
    return jsonify(final_questions)
@app.route("/check_answer",methods=["POST"])
#parse answers sent from the app
def check_answer():
    data = request.get_json()
    print(data)
    answer = data["answer"]
    correct_answer = data["serverAnswer"]
    questionId = data["questionId"]

    # if we are getting data from web form
    # correct_answer = request.form['serverAnswer']
    # answer = request.form['answer']
    # questionId = request.form['questionId']
    
    print(answer)
    print(questionId)
    #check if answer is correct
    correct_or_not = check_answer_from_user(answer,correct_answer)
    return jsonify({"correctOrNot":correct_or_not[0],"correctAnswer":correct_or_not[1]})
@app.route("/get_questions_with_diff_topic_and_ques",methods=["POST"])
def get_questions_with_diff_topic_and_ques():
    data = request.get_json()
    print(data)
    data = data["data"]
    topics = data["topics"]
    topics_to_get = []
    for key,value in topics.items():
        if value:
            topics_to_get.append(key)
    topics_to_get = make_topics_to_get(topics_to_get,int(data["numOfQuestions"]))
    final_questions = []
    if data["difficulty"] == 11:
        for item,value in topics_to_get.items():
            for x in range(value):
                question = get_question_with_specific_difficulty_and_topic(difficulty=random.randint(1,9),topic=item)

                final_questions.append({"question":parse_question(question[1]),"questionId":question[0],"answer":question[2]})
    else:
        for item,value in topics_to_get.items():
            for x in range(value):
                question = get_question_with_specific_difficulty_and_topic(difficulty=data["difficulty"],topic=item)
                final_questions.append({"question":parse_question(question[1]),"questionId":question[0],"answer":question[2]})
    print(final_questions)
    print("responded")
    return jsonify(final_questions)


def make_topics_to_get(topics_to_get,questions):
    final_topics_to_get = {}
    for _ in range(int(questions/len(topics_to_get))):
        for x in topics_to_get:
            if x not in final_topics_to_get:
                final_topics_to_get[x] = 1
            else:
                final_topics_to_get[x] += 1
    questions_left = questions % len(topics_to_get)
    for _ in range(questions_left):
        final_topics_to_get[choice(topics_to_get)] += 1 
    return final_topics_to_get



#Run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)