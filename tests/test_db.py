from sqlalchemy import select

from fast_zero.models import Todo, User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='alice@example.com')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_todo(session, user):
    new_todo = Todo(
        description='desc test', title='title test', state='draft', user_id=user.id
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert new_todo in user.todos
