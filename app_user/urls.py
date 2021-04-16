"ICECREAM"
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import pass_data, debug
from bottle_jwt2 import jwt_auth_required

from app_user.controller import get_users, create_user, get_user, activate_user, edit_user, \
    add_person_image, get_rules, set_user_role, change_password, get_current_user, remove_person_image


class USERApp(BaseApp):
    def call_router(self, core):
        core.route('/api/users/<pk>', 'GET', get_user, apply=[debug, jwt_auth_required])
        core.route('/api/users', 'GET', get_users, apply=[])
        core.route('/api/users/current', 'GET', get_current_user, apply=[debug, jwt_auth_required])
        core.route('/api/users/<pk>', 'PATCH', edit_user, apply=[pass_data, jwt_auth_required])
        core.route('/api/users', 'POST', create_user, apply=[pass_data, jwt_auth_required])
        core.route('/api/users/activate/<pk>', 'PATCH', activate_user, apply=[pass_data, jwt_auth_required])
        core.route('/api/users/image', 'POST', add_person_image, apply=[pass_data, jwt_auth_required])
        core.route('/api/users/image/<pk>', 'DELETE', remove_person_image,
                   apply=[jwt_auth_required])
        core.route('/api/users/change-password', 'PATCH', change_password,
                   apply=[pass_data, jwt_auth_required])
        core.route('/api/rules', 'GET', get_rules, apply=[jwt_auth_required])
        core.route('/api/user/role/<pk>', 'PATCH', set_user_role, apply=[pass_data, jwt_auth_required, ])
