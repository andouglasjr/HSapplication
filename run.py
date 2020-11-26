from app import app
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from app.controllers.hologram import Hologram
import os

if __name__ == '__main__':
    #socketio.run(app)
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True, use_reloader=False, ssl_context='adhoc')
