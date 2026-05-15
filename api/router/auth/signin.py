from fastapi import APIRouter, Request, Response, HTTPException
from shared.factory import db, redis
from shared.env import SESSION_COOKIE_NAME
from .common import UserSigninDto, get_session_token
import bcrypt
import uuid
router = APIRouter()
@router.post('/signin')
async def signin(user: UserSigninDto, request: Request, response: Response):
    if redis.get(get_session_token(request, '')):
        return {'msg': 'success'}
    existing_user = await db.users.find_one({'username': user.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail='incorrect username')
    if bcrypt.checkpw(user.password.encode('utf-8'), existing_user['password']):
        session_token = str(uuid.uuid4())
        redis.set(session_token, str(existing_user.get('_id')))
        response.set_cookie(
            key=SESSION_COOKIE_NAME, value=session_token, httponly=True, max_age=2592000, samesite='none', secure=True
        )
        return {'msg': 'success'}
    raise HTTPException(status_code=400, detail='incorrect password')
