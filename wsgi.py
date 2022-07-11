from app import *
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
if __name__ == "__main__":
    #app.run()
    app = Flask(__name__)#,template_folder="./dist/app/templates"
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    app.run(host="0.0.0.0",port=5008)
    
