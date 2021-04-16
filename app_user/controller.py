"ICECREAM"
import bottle
from ICECREAM import status
from ICECREAM.file_handler import upload
from ICECREAM.http import HTTPError, HTTPResponse
from ICECREAM.models.query import get_or_create, is_object_exist_409, get_object_or_404, set_objects_limit
from ICECREAM.paginator import Paginate
from ICECREAM.rbac import get_rules_json
from ICECREAM.util import str_to_bool
from ICECREAM.validators import validate_data
from sqlalchemy.orm import Session

from app_user.messages import ACTIVATED_MSG, DEACTIVATED_MSG, DELETE_IMG, PASSWORD_CHANGED, OLD_PASSWORD_NOT_VALID
from app_user.models import User, Person, PersonImage
from app_user.schemas import users_serializer, user_serializer, person_image_serializer, user_edit_serializer, \
    set_role_serializer, change_password_serializer


def get_current_user(db_session: Session):
    req_user_json = bottle.request.get_user()
    current_user = db_session.query(User).get(req_user_json['id'])
    result = user_serializer.dump(current_user)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def get_users(db_session: Session):
    users = db_session.query(User).order_by(User.created_date)
    result = Paginate(users, users_serializer)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def get_user(pk, db_session):
    user = get_object_or_404(User, db_session, User.id == pk)
    result = user_serializer.dump(user)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def change_password(db_session, data):
    validate_data(change_password_serializer, data)
    req_user_json = bottle.request.get_user()
    current_user = db_session.query(User).get(req_user_json['id'])
    if current_user.check_password(data['old_password']):
        current_user.set_password(data['password'])
        return HTTPResponse(*PASSWORD_CHANGED)
    raise HTTPError(*OLD_PASSWORD_NOT_VALID)


def activate_user(pk, db_session: Session, data):
    # validate_permission("activate_user", db_session, User)
    activation = data["activation"]
    user = get_object_or_404(User, db_session, User.id == pk)
    user.is_active = str_to_bool(activation)
    db_session.commit()
    if user.is_active:
        return HTTPResponse(*ACTIVATED_MSG)
    return HTTPResponse(*DEACTIVATED_MSG)


def create_user(db_session: Session, data):
    validate_data(user_serializer, data)
    is_object_exist_409(User, db_session, User.phone == data['phone'])
    person = data['person']
    person_obj = get_or_create(Person, db_session, Person.name == person['name'])
    person_obj.name = person['name']
    person_obj.last_name = person['last_name']
    person_obj.email = person['email']
    db_session.add(person_obj)
    user = get_or_create(User, db_session, User.phone == data['phone'])
    user.phone = data['phone']
    user.set_roles(data['roles'])
    user.username = user.phone
    user.set_password(data['password'])
    user.person = person_obj
    db_session.add(user)
    db_session.commit()
    result = user_serializer.dump(db_session.query(User).get(user.id))
    return HTTPResponse(status=status.HTTP_201_CREATED, body=result)


def edit_user(pk, db_session: Session, data):
    validate_data(user_edit_serializer, data)
    user = get_object_or_404(User, db_session, User.id == pk)
    person = data['person']
    user.person.name = person['name']
    user.person.last_name = person['last_name']
    user.person.email = person['email']
    user.phone = data['phone']
    user.username = data['phone']
    db_session.commit()
    result = user_serializer.dump(db_session.query(User).get(user.id))
    return HTTPResponse(status=status.HTTP_201_CREATED, body=result)


def add_person_image(db_session: Session, data):
    validate_data(person_image_serializer, data)
    person_image = PersonImage()
    person = get_object_or_404(Person, db_session, Person.id == data['person_id'])
    set_objects_limit(person.person_images, limit=1, session=db_session)
    person_image.name = upload(data=data)
    person_image.person_id = data['person_id']
    db_session.add(person_image)
    db_session.commit()
    result = db_session.query(PersonImage).get(person_image.id)
    result = person_image_serializer.dump(result)
    return HTTPResponse(status=status.HTTP_200_OK, body=result)


def remove_person_image(pk, db_session: Session):
    person_image = get_object_or_404(Person, db_session, Person.id == pk)
    db_session.delete(person_image)
    db_session.commit()
    return HTTPResponse(*DELETE_IMG)


def set_user_role(pk, db_session: Session, data):
    validate_data(set_role_serializer, data)
    # validate_permission("edit_roles", db_session, User)
    user = get_object_or_404(User, db_session, User.id == pk)
    user.set_roles(data['roles'])
    db_session.commit()
    result = user_serializer.dump(db_session.query(User).get(user.id))
    return HTTPResponse(status=status.HTTP_201_CREATED, body=result)


def get_rules(db_session: Session):
    req_user_json = bottle.request.get_user()
    current_user = db_session.query(User).get(req_user_json['id'])
    return HTTPResponse(status=status.HTTP_200_OK, body=get_rules_json(current_user), message="rules")
