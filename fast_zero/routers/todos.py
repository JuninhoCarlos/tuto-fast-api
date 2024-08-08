from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy import Select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoPublic, TodoSchema, TodoList
from fast_zero.security import get_current_user

SessionDependency = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: SessionDependency):
    todo = Todo(
        title=todo.title, description=todo.description, state=todo.state, user_id=user.id
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo

@router.get('/', response_model=TodoList)
def list_todo(user: CurrentUser, session: SessionDependency):
    todos = session.scalars(Select(Todo).where(Todo.user_id==user.id)).all()
    
    return {'todos': todos}