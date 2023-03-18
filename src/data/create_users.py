from src import init_app
from src.models.user import User


def insert_dummy_data():
    app = init_app()
    with app.app_context():
        User.create('Owain')
        User.create('Mo')
        User.create('Ryan')
        print('created users!')


if __name__ == "__main__":
    insert_dummy_data()
