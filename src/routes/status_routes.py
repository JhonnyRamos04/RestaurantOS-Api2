from flask import Blueprint
from src.controllers.status_controller import delete_status, get_status, get_status_by_id, create_status, update_status

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

@status_bp.route('/<int:id_status>', methods=['PUT'])
def modify_status(id_status):
    return update_status(id_status)

@status_bp.route('/<int:id_status>', methods=['DELETE'])
def remove_status(id_status):
    return delete_status(id_status)
