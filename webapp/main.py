from flask import Flask, url_for
from flask_restx import Api
from get_marks import api as getmarks_api
from process_marks import api as processmarks_api

class PatchedApi(Api):
    """Patches the swagger.json endpoint when SSL is terminated outside of application
    # https://github.com/python-restx/flask-restx/issues/188
    """

    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"))

app = Flask(__name__)
app.url_map.strict_slashes = False
# Initialize restx
api = PatchedApi(
    app,
    version="0.1.0",
    title="DSCE Marks processor",
    description="A .csv file generating API",
)
api.add_namespace(getmarks_api)
api.add_namespace(processmarks_api)


if __name__ == "__main__":
    bind_address = "0.0.0.0"
    port = 5000
    debug_flask = True
    app.run(host=bind_address, port=port, debug=debug_flask)
