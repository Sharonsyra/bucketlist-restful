import os
from flask_cors import CORS

from app.bucketlist.views import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
