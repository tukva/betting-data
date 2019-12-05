from sanic import Sanic
from sanic_cors import CORS

from config import BETTING_DATA_API_PORT, BETTING_DATA_API_HOST
from routes import add_routes

app = Sanic(name=__name__)
cors = CORS(app, automatic_options=True)
add_routes(app)

if __name__ == '__main__':
    app.run(host=BETTING_DATA_API_HOST, port=BETTING_DATA_API_PORT)
