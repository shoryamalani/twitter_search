from app import *
import os
if __name__ == "__main__":
    #app.run()
    app = Flask(__name__)#,template_folder="./dist/app/templates"
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
    app.run(host="0.0.0.0",port=5008)