import flask
import os
from markupsafe import escape
import files.valAPI

server = flask.Flask(__name__)
FILE_DIR = os.getcwd() + "/app/" + "/files/"
print(FILE_DIR)


@server.route("/")
def main_page():
    return flask.send_from_directory(FILE_DIR + "/pages/", "main_page.html")


@server.route("/user/<usertag>")
def search(usertag):
    instance = files.valAPI.App(escape(usertag))
    return flask.send_from_directory(FILE_DIR + "/pages/", "user_page.html")


@server.route("/source/main_page.css")
def main_page_css():
    return flask.send_from_directory(FILE_DIR + "/pages/", "main_page.css")


@server.route("/source/user_page.css")
def user_page_css():
    return flask.send_from_directory(FILE_DIR + "/pages/", "user_page.css")


@server.route("/source/favicon.ico")
def favicon():
    return flask.send_from_directory(FILE_DIR, "favicon.ico")


if __name__ == "__main__":
    server.run()
