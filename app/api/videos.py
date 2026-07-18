# Reference: https://flask.palletsprojects.com/en/stable/patterns/fileuploads/

from app.api import bp
import os
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"mp4", "mov"}

def allowed_file(filename):
    return "." in filename and \
    filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/videos/<int:id>", methods=["GET"])
def get_video(id):
    pass

@bp.route("/videos", methods=["POST"])
def create_video():
    # check if post request has file part
    if "file" not in request.files:
        return {"error": "No file provided"}, 400
    file = request.files["file"]
    # if user does not select a file, browser submits an empty file
    if file.filename == "":
        return {"error": "No selected file provided"}, 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        return {"message": "Upload successful", "filename": filename}, 202
    else:
        return {"error": "File type not allowed"}, 400