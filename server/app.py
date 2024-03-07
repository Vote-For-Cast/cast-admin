#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource
from datetime import datetime

# Local imports
from config import app, db, api, migrate

# Add your model imports
from models import (
    User,
    State,
    County,
    City,
    Ballot,
    Voter,
    Admin,
    Account,
    Enterprise,
    Administration,
    Member,
    Bill,
    Candidate,
    Representative,
    Election,
    Poll,
    Proposition,
    Campaign,
    Country,
    Options,
    Deadlines,
    Vote,
    Party,
    Partner,
    SuperAdmin,
    Guide,
    Term,
    Winner,
    Recommendation,
    Follow,
    Post,
    Notification,
)

# Views go here!


@app.route("/")
def index():
    return "<h1>Project Server</h1>"


# Resource Classes


class Elections(Resource):
    def get(self):
        return make_response(
            [election.to_dict() for election in Election.query.all()],
            200,
        )

    def post(self):
        data = request.get_json()
        election = Election()
        try:
            date_str = data["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            election.name = data["name"]
            election.date = date_obj
            election.election_type = data["election_type"]
            election.state = data["state"]
            election.county = data["county"]
            db.session.add(election)
            db.session.commit()
            return make_response(election.to_dict(), 201)
        except ValueError:
            return make_response({"error": "Invalid election"}, 400)


class ElectionById(Resource):
    def get(self, id):
        election = Election.query.get(id)
        if election:
            return make_response(election.to_dict(), 200)
        else:
            return make_response({"error": "Election not found"}, 404)

    def patch(self, id):
        election = Election.query.get(id)
        if election:
            try:
                election.name = name
                election.date = date
                election.election_type = election_type
                election.state = state
                election.county = county
                db.session.commit()
                return make_response(election.to_dict(), 200)
            except ValueError:
                return make_response({"error": "Invalid election"}, 400)
        else:
            return make_response({"error": "Election not found"}, 404)

    def delete(self, id):
        election = Election.query.get(id)
        if election:
            db.session.delete(election)
            db.session.commit()
            return make_response({"message": "Election deleted"}, 200)
        else:
            return make_response({"error": "Election not found"}, 404)


class Users(Resource):
    def get(self):
        return make_response([user.to_dict() for user in User.query.all()], 200)

    def post(self):
        user_data = request.get_json()
        try:
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )
            new_user.password = user_data["password"]
            db.session.add(new_user)
            commit_session(db.session)

            return make_response({"message": "User created successfully"}, 201)
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                return make_response(
                    {"error": "Username or email already exists."}, 409
                )
            else:
                return make_response({"error": "Database integrity error."}, 500)

        except Exception as error:
            db.session.rollback()
            return make_response({"error": "User creation failed: " + str(error)}, 500)

    def delete(self):
        try:
            data = request.get_json()
            if not all(key in data for key in ("username", "password")):
                return make_response(
                    {"error": "Username and password are required"}, 400
                )

            username = data["username"]
            password = data["password"]

            user = User.query.filter_by(username=username).first()

            if user and user.authenticate(password):
                user_to_delete = user
                db.session.delete(user_to_delete)
                commit_session(db.session)
                return make_response({"message": "User deleted successfully"}, 200)
            else:
                return make_response({"error": "Invalid credentials"}, 401)
        except Exception as error:
            return make_response({"error": str(error)}, 500)

    def patch(self):
        data = request.get_json()
        try:
            if not all(key in data for key in ("username", "password", "newPassword")):
                return make_response({"error": "Required fields are missing"}, 400)

            username = data["username"]
            password = data["password"]
            new_password = data["newPassword"]

            user = User.query.filter_by(username=username).first()

            if user and user.authenticate(password):
                user.password = new_password
                commit_session(db.session)
                return make_response({"message": "Password updated successfully"}, 200)
            else:
                return make_response({"error": "Invalid credentials"}, 401)
        except Exception as error:
            return make_response({"error": str(error)}, 500)


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not all(key in data for key in ("username", "password")):
            return make_response({"error": "Username and password are required"}, 400)

        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            return make_response(
                {"message": "Login successful", "user_id": user.id}, 200
            )
        else:
            return make_response({"error": "Invalid credentials"}, 401)


# API Resource Routing


api.add_resource(Elections, "/elections")
api.add_resource(ElectionById, "/elections/<int:id>")
api.add_resource(Login, "/login")
api.add_resource(Users, "/users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
