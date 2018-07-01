from twisted.web.resource import Resource

from Logger import Log

logger = Log("WebServer", "\033[36m")
logger_err = Log("WebServer", "\033[36;41m")


class Handler(Resource):
    isLeaf = True

    def render_GET(self, request):
        uri = request.uri

        logger.new_message("Unknown GET: " + uri, 2)

    def render_POST(self, request):
        logger_err.new_message("Unknown POST: " + request.uri, 2)