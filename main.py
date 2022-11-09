# from flask import Flask, render_template
#
# app = Flask(__name__)
#
#
# @app.route("/")
# def hello_world():
#     return render_template("index.html")
#
# if __name__=='__main__':
#     app.run(debug=True)
from website._init_ import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)