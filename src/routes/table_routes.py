from flask import Blueprint
from src.controllers.table_controller import delete_table, get_tables, get_table_by_id, get_tables_by_status, get_available_tables, get_tables_by_waiter, create_table, update_table

table_bp = Blueprint('table', __name__)

@table_bp.route('/', methods=['GET'])
def all_tables():
    return get_tables()

@table_bp.route('/<int:id_table>', methods=['GET'])
def table_by_id(id_table):
    return get_table_by_id(id_table)

@table_bp.route('/status/<int:id_status>', methods=['GET'])
def tables_by_status(id_status):
    return get_tables_by_status(id_status)

@table_bp.route('/available', methods=['GET'])
def available_tables():
    return get_available_tables()

@table_bp.route('/waiter/<int:id_walker>', methods=['GET'])
def tables_by_waiter(id_walker):
    return get_tables_by_waiter(id_walker)

@table_bp.route('/', methods=['POST'])
def add_table():
    return create_table()

@table_bp.route('/<int:id_table>', methods=['PUT'])
def modify_table(id_table):
    return update_table(id_table)

@table_bp.route('/<int:id_table>', methods=['DELETE'])
def remove_table(id_table):
    return delete_table(id_table)
