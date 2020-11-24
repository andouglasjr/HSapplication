from flask import Flask, session
from flask_session import Session

UPLOAD_FOLDER = 'static/saved_holograms'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

from app.controllers import default
from app.controllers import holo_aquisition
from app.controllers import holo_processing
from app.controllers import holo_reconstruction
from app.controllers import holo_segmentation
from app.controllers import holo_classification
