import bcrypt
from jose import jwt 
from datetime import datetime, timedelta

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "0df0e5b856442a4ec42f11756bfdbb9af74aaabf23c03d366120b55d57c101ee"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str):
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(self.encoding),
            hashed_password=hashed_password.encode(self.encoding),
        )

    def create_jwt(self, username: str):
        return jwt.encode(
            claims={
                "sub": username,
                "exp": datetime.now() + timedelta(days=1),
                "iat": datetime.now()
            }, 
            key=self.secret_key, 
            algorithm=self.jwt_algorithm,
        )
