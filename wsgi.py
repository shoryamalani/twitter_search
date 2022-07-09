from app import *

if __name__ == "__main__":
    #app.run()
    app = Flask(__name__)#,template_folder="./dist/app/templates"
    app.config['SECRET_KEY'] = 'secret!'
    app.run(host="0.0.0.0",port=5008)