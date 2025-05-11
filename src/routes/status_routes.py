from flask import Blueprint
from src.controllers.status_controller import get_status, get_status_by_id, create_status

status_bp = Blueprint('status', __name__)

@status_bp.route('/', methods=['GET'])
def all_status():
    return get_status()

@status_bp.route('/<int:id_status>', methods=['GET'])
def status_by_id(id_status):
    return get_status_by_id(id_status)

@status_bp.route('/', methods=['POST'])
def add_status():
    return create_status()
