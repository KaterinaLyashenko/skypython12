from flask import Blueprint, render_template, request
import logging
from werkzeug.exceptions import abort
from main import utils
from loader.utils import *
from config import POST_PATH

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder="templates")
logging.basicConfig(filename='../logger.log', level=logging.INFO)


@loader_blueprint.route("/post", method=["GET"])
def create_new_post_page():
    return render_template("post_form.html")


@loader_blueprint.route("/post", method=["POST"])
def create_new_post_by_user():
    picture = request.files.get("picture")
    content = request.form.get("content")
    if not picture or not content:
        logging.info("Данные не загруженны, отсутствует часть данных")
        return "отсутствует часть данных"

    posts = utils.load_json_data(POST_PATH)

    try:
        new_post = {"pic": save_picrture(picture), "content": content}
    except WrongImgType:
        abort(400)

    add_post(posts, new_post)
    return render_template("post_uploaded.html", new_post=new_post)