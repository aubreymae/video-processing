# Reference: https://flask.palletsprojects.com/en/stable/patterns/fileuploads/

from app.api import bp
import os
import sqlite3
from flask import Flask, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from app.queue_store import queue

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

        # Connect to db
        with sqlite3.connect("app/upload-db.db") as connection:
            cursor = connection.cursor()
            status = "Pending"
            raw_size = request.form.get("target_size_mb")
            target_size_mb = float(raw_size) if raw_size else 25.0
            insert_video_query = f"INSERT INTO Videos (filename, status, target_size_mb) VALUES (?, ?, ?);"
            cursor.execute(insert_video_query, (filename, status, target_size_mb))
            connection.commit()
            row_id = cursor.lastrowid

        # Add video_id into queue
        queue.append(row_id)

        return {"message": "Upload successful", "filename": filename, "status": status, "row_id": row_id}, 202
    else:
        return {"error": "File type not allowed"}, 400