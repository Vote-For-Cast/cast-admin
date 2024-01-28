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


class Representatives(Resource):
    def get(self):
        return make_response(
            [representative.to_dict() for representative in Representative.query.all()],
            200,
        )

    def post(self):
        data = request.get_json()
        representative = Representative()
        try:
            representative.name = data["name"]
            representative.rep_type = data["rep_type"]
            representative.state = data["state"]
            representative.county = data["county"]
            representative.affiliation = data["affiliation"]
            db.session.add(representative)
            db.session.commit()
            return make_response(representative.to_dict(), 201)
        except ValueError:
            return make_response({"error": "Invalid representative"}, 400)


class RepresentativesByState(Resource):
    def get(self, state):
        representatives = Representative.query.filter_by(state=state).all()
        if representatives:
            return make_response(
                [representative.to_dict() for representative in representatives],
                200,
            )
        else:
            return make_response({"error": "Representatives not found"}, 404)


class Bills(Resource):
    def get(self):
        return make_response(
            [bill.to_dict() for bill in Bill.query.all()],
            200,
        )

    def post(self):
        data = request.get_json()
        bill = Bill()
        try:
            bill.name = data["name"]
            bill.code = data["code"]
            bill.text = data["text"]
            bill.bill_type = data["bill_type"]
            bill.state = data["state"]
            bill.county = data["county"]
            db.session.add(bill)
            db.session.commit()
            return make_response(bill.to_dict(), 201)
        except ValueError:
            return make_response({"error": "Invalid bill"}, 400)


class BillsByCode(Resource):
    def get(self, code):
        bills = Bill.query.filter_by(code=code).all()
        if bills:
            return make_response(
                [bill.to_dict() for bill in bills],
                200,
            )
        else:
            return make_response({"error": "Bills not found"}, 404)


class Polls(Resource):
    def get(self):
        return make_response(
            [poll.to_dict() for poll in Poll.query.all()],
            200,
        )


class PollsByElection(Resource):
    def get(self, election_id):
        polls = Poll.query.filter_by(election_id=election_id).all()
        if polls:
            return make_response(
                [poll.to_dict() for poll in polls],
                200,
            )
        else:
            return make_response({"error": "Polls not found"}, 404)


class Propositions(Resource):
    def get(self):
        return make_response(
            [proposition.to_dict() for proposition in Proposition.query.all()],
            200,
        )


class PropositionsByElection(Resource):
    def get(self, election_id):
        propositions = Proposition.query.filter_by(election_id=election_id).all()
        if propositions:
            return make_response(
                [proposition.to_dict() for proposition in propositions],
                200,
            )
        else:
            return make_response({"error": "Propositions not found"}, 404)


# API Resource Routing


api.add_resource(Elections, "/elections")
api.add_resource(ElectionById, "/elections/<int:id>")
api.add_resource(Representatives, "/representatives")
api.add_resource(RepresentativesByState, "/representatives/<string:state>")
api.add_resource(Bills, "/bills")
api.add_resource(BillsByCode, "/bills/<string:code>")
api.add_resource(Polls, "/polls")
api.add_resource(PollsByElection, "/polls/<int:election_id>")
api.add_resource(Propositions, "/propositions")
api.add_resource(PropositionsByElection, "/propositions/<int:election_id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
