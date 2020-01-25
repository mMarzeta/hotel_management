import peewee
import datetime
from playhouse.shortcuts import model_to_dict

db = peewee.SqliteDatabase('users.db')


class UserModel(peewee.Model):
    id = peewee.UUIDField()
    username = peewee.CharField(primary_key=True, max_length=255)
    email = peewee.CharField(max_length=255)
    tel_number = peewee.CharField(max_length=15)
    full_name = peewee.CharField(max_length=255)
    pesel = peewee.CharField(max_length=30)
    address = peewee.CharField(max_length=255)
    hashed_password = peewee.CharField(max_length=255)

    disabled = peewee.BooleanField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = "user"

    @classmethod
    def get_user(cls, username):
        return cls.select().where(cls.username == username).get()

    @classmethod
    def get_user_as_dict(cls, username):
        user = cls.get_user(username)
        return model_to_dict(user)


db.connect()

if __name__ == "__main__":
    db.create_tables([UserModel])
