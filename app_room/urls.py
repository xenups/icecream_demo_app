"ICECREAM"
from bottle_jwt2 import jwt_auth_required
from ICECREAM.baseapp import BaseApp
from ICECREAM.wrappers import debug, pass_data

from app_room.controller import (
    get_rooms,
    new_room,
    add_room_image,
    filter_rooms,
    get_room,
)


class RoomApp(BaseApp):
    def call_router(self, core):
        core.route("/api/rooms", "GET", get_rooms, apply=[debug])
        core.route("/api/rooms/<pk:int>", "GET", get_room, apply=[debug])
        core.route("/api/rooms", "POST", new_room, apply=[pass_data, debug])
        core.route("/api/room_image", "POST", add_room_image, apply=[pass_data, debug])
        core.route("/api/rooms/filter", "GET", filter_rooms, apply=[debug])
