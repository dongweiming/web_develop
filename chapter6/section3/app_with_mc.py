# coding=utf-8
from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from sqlalchemy import create_engine
from mc import mc, cache

app = Flask(__name__)
DATABASE_URI = 'mysql://web:web@localhost:3306/r'
api = Api(app)

con = create_engine(DATABASE_URI).connect()

USER_KEY = 'web_develop:users:%s'


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String
}


class User(object):
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    @classmethod
    def add(cls, name, address):
        sql = ('insert into test_user(name, address) '
               'values(%s, %s)')
        id_ = con.execute(sql, (name, address)).lastrowid
        cls.clear_mc(id_)
        return cls.get(id_)

    @classmethod
    @cache(USER_KEY % '{id_}')
    # @cache(USER_KEY % '{id_}', 1800)  # 表示只缓存1800秒
    def get(cls, id_):
        if not id_:
            return None
        row = con.execute(
            'select id, name, address '
            'from test_user where id=%s', id_).fetchone()
        return cls(*row) if row else None

    @classmethod
    def get_user_by_name(cls, name):
        sql = ('select id from test_user '
               'where name=%s')
        rows = con.execute(sql, name).fetchall()
        return cls.get(*rows[0]) if rows else None

    def delete(self):
        con.execute(
            'delete from test_user where id=%s', self.id)
        self.clear_mc(self.id)

    @classmethod
    def clear_mc(cls, id_):
        mc.delete(USER_KEY % id_)


class UserResource(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        user = User.get_user_by_name(name=name)
        return user

    def put(self, name):
        address = request.form.get('address', '')
        User.add(name, address)
        return {'ok': 0}, 201

    def delete(self, name):
        user = User.get_user_by_name(name)
        if user:
            user.delete()
        return {'ok': 0}


api.add_resource(UserResource, '/users/<string:name>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
