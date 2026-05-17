from app.api import bp

@bp.route("/videos/<int:id>", methods=["GET"])
def get_video(id):
    pass

@bp.route("/videos", methods=["POST"])
def create_video():
    pass