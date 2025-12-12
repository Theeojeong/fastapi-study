from fastapi import APIRouter, Depends, HTTPException

from schema.request import SignUpRequest, LogInRequest
from schema.response import UserSchema, JWTResponse
from service.user import UserService
from database.orm import User
from database.repository import UserRepository

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):

    hashed_password = user_service.hash_password(plain_password=request.password)
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    user: User = user_repo.save_user(user=user)

    return UserSchema.model_validate(user)


@router.post("/log-in", status_code=201)
def user_log_in_handler(
    request: LogInRequest,
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends(),
):
    # 1 request body(username, password)
    # 2 db read user
    get_user: User | None = user_repo.get_user_by_username(username=request.username)
    if not get_user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # 3 user.password, request.password -> bcrypt.checkpw
    verify_user_pwd: bool = user_service.verify_password(
        password=request.password,
        hashed_password=get_user.password,
    )

    if not verify_user_pwd:
        raise HTTPException(status_code=401, detail="Unauthorized Password")

    # 4 create jwt
    access_token: str = user_service.create_jwt(username=get_user.username)

    # 5 return jwt
    return JWTResponse(access_token=access_token)
