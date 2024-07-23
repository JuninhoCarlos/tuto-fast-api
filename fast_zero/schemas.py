from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaPublic(BaseModel):
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserSchemaPublic]


class UserDB(UserSchema):
    id: int
