from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app

landing_bp = Blueprint('landing', __name__)

#
# Home page
#
@landing_bp.route('/')
def home():
    return render_template('landing/index.html')