from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import Usuario



