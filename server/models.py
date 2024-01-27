from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


# Platform Users and Enterprise Accounts


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String, nullable=False)

    # add relationships
    voter = db.relationship("Voter", back_populates="user")
    admin = db.relationship("Admin", back_populates="user")
    voter_account = association_proxy("voter", "account")
    admin_account = association_proxy("admin", "account")

    # add serialization rules
    serialize_rules = (
        "-voter.user",
        "-admin.user",
        "-voter_account.user",
        "-admin_account.user",
    )

    # add validation

    def __repr__(self):
        return f"<User {self.username}>"


class Voter(db.Model, SerializerMixin):
    __tablename__ = "voters"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)
    street_line1 = db.Column(db.String)
    street_line2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    postal_code = db.Column(db.String)
    county = db.Column(db.String)
    country = db.Column(db.String)

    # add relationships
    account = db.relationship("Account", back_populates="voters")
    admin = association_proxy("account", "admin")

    # add serialization rules
    serialize_rules = ("-account.voters", "-admin.voters")

    # add validation

    def __repr__(self):
        return f"<Voter {self.username}>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)
    state = db.Column(db.String, db.ForeignKey("states.name"))
    county = db.Column(db.String)

    # add relationships
    account = db.relationship("Account", back_populates="admin")
    voters = association_proxy("account", "voters")

    # add serialization rules
    serialize_rules = ("-voters.admin", "-account.admin")

    # add validation

    def __repr__(self):
        return f"<Admin {self.username}>"


class Account(db.Model, SerializerMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    name = db.Column(db.String, unique=True, nullable=False)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    admin = db.relationship("Admin", back_populates="account")
    voters = db.relationship("Voter", back_populates="account")

    # add serialization rules
    serialize_rules = ("-voters.account", "-admin.account")

    # add validation

    def __repr__(self):
        return f"<Account {self.id}>"


# Platform Jurisdictions


class State(db.Model, SerializerMixin):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # add relationships
    counties = db.relationship("County", back_populates="state")

    # add serialization rules
    serialize_rules = ("-counties.state",)

    # add validation

    def __repr__(self):
        return f"<State {self.name}>"


class County(db.Model, SerializerMixin):
    __tablename__ = "counties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False)

    # add relationships
    state = db.relationship("State", back_populates="counties")

    # add serialization rules
    serialize_rules = ("-state.counties",)

    # add validation

    def __repr__(self):
        return f"<County {self.name}>"


# Election Processes


class Election(db.Model, SerializerMixin):
    __tablename__ = "elections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    election_type = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    polls = db.relationship("Poll", back_populates="election")
    propositions = db.relationship("Proposition", back_populates="election")
    candidates = association_proxy("polls", "candidates")
    bills = association_proxy("propositions", "bills")

    # add serialization rules
    serialize_rules = (
        "-polls.election",
        "-propositions.election",
        "-candidates.election",
        "-bills.election",
    )

    # add validation

    def __repr__(self):
        return f"<Election {self.name}>"


class Ballot(db.Model, SerializerMixin):
    __tablename__ = "ballots"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))

    # add relationships
    election = db.relationship("Election", back_populates="ballots")
    voter = db.relationship("Voter", back_populates="ballots")
    polls = association_proxy("election", "polls")
    propositions = association_proxy("election", "propositions")

    # add serialization rules
    serialize_rules = ("-election.ballots", "-voter.ballots")

    # add validation

    def __repr__(self):
        return f"<Ballot {self.name}>"


class Poll(db.Model, SerializerMixin):
    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    position = db.Column(db.String)

    # add relationships
    election = db.relationship("Election", back_populates="polls")
    campaigns = db.relationship("Campaign", back_populates="poll")
    candidates = association_proxy("campaigns", "candidate")

    # add serialization rules
    serialize_rules = ("-election.polls", "-candidates.poll", "-campaigns.poll")

    # add validation

    def __repr__(self):
        return f"<Poll {self.name}>"


class Candidate(db.Model, SerializerMixin):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    candidate_type = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.Integer)
    affiliation = db.Column(db.String)

    # add relationships
    campaigns = db.relationship("Campaign", back_populates="candidate")
    polls = association_proxy("campaigns", "poll")

    # add serialization rules
    serialize_rules = ("-polls.candidates", "-campaigns.candidate")

    # add validation

    def __repr__(self):
        return f"<Candidate {self.name}>"


class Campaign(db.Model, SerializerMixin):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"))
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    representative_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))
    votes = db.Column(db.Integer)

    # add relationships
    poll = db.relationship("Poll", back_populates="campaigns")
    candidate = db.relationship("Candidate", back_populates="campaigns")
    representative = db.relationship("Representative", back_populates="campaigns")
    election = association_proxy("poll", "election")

    # add serialization rules
    serialize_rules = (
        "-poll.campaigns",
        "-candidate.campaigns",
        "-representative.campaigns",
        "-election.campaigns",
    )

    # add validation

    def __repr__(self):
        return f"<Campaign {self.id}>"


class Proposition(db.Model, SerializerMixin):
    __tablename__ = "propositions"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    yes_votes = db.Column(db.Integer)
    no_votes = db.Column(db.Integer)

    # add relationships
    election = db.relationship("Election", back_populates="propositions")
    bill = db.relationship("Bill", back_populates="propositions")
    polls = association_proxy("election", "polls")

    # add serialization rules
    serialize_rules = (
        "-election.propositions",
        "-bill.propositions",
        "-polls.propositions",
    )

    # add validation

    def __repr__(self):
        return f"<Propositions {self.name}>"


class Bill(db.Model, SerializerMixin):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    text = db.Column(db.String)
    bill_type = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    propositions = db.relationship("Proposition", back_populates="bill")
    elections = association_proxy("propositions", "election")

    # add serialization rules
    serialize_rules = ("-proposition.bill", "-election.bill")

    # add validation

    def __repr__(self):
        return f"<Legislation {self.name}>"


# Elected Officials


class Representative(db.Model, SerializerMixin):
    __tablename__ = "representatives"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rep_type = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    county = db.Column(db.String)
    affiliation = db.Column(db.String)

    # add relationships
    campaigns = db.relationship("Campaign", back_populates="representative")

    # add serialization rules
    serialize_rules = ("-campaigns.representative",)
    # add validation

    def __repr__(self):
        return f"<Representative {self.name}>"
