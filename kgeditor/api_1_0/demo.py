from . import api

@api.route("/index")
def index():
    return "index"