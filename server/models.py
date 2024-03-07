from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


# Platform Users and Accounts


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    account = db.relationship("Account", back_populates="user")
    voter = association_proxy("account", "voter")
    super_admin = association_proxy("account", "super_admin")
    admin = association_proxy("account", "admin")
    partner = association_proxy("account", "partner")
    member = association_proxy("account", "member")

    # add serialization rules
    serialize_rules = (
        "-account.user",
        "-voter.user",
        "-super_admin.user",
        "-admin.user",
        "-partner.user",
        "-member.user",
    )

    # add validation

    def __repr__(self):
        return f"<User {self.username}>"


# Individual User Account Types (Roles)


class Voter(db.Model, SerializerMixin):
    __tablename__ = "voters"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    profile_photo = db.Column(db.String)
    phone_number = db.Column(db.String)
    street_line1 = db.Column(db.String)
    street_line2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    postal_code = db.Column(db.String)
    county = db.Column(db.String)
    district = db.Column(db.String)
    country = db.Column(db.String)
    race = db.Column(db.String)
    ethnicity = db.Column(db.String)
    gender = db.Column(db.String)
    veteran_status = db.Column(db.String)
    birthdate = db.Column(db.Date)
    voter_registration_status = db.Column(db.String)
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    user = db.relationship("User", back_populates="voter")

    # add serialization rules
    serialize_rules = ("-user.voter",)

    # add validation

    def __repr__(self):
        return f"<Voter {self.id}, {self.name}>"


class Party(db.Model, SerializerMixin):
    __tablename__ = "parties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    overview = db.Column(db.String)

    # add relationships
    candidates = db.relationship("Candidate", back_populates="party")
    representatives = db.relationship("Representative", back_populates="party")
    voters = db.relationship("Voter", back_populates="party")
    follows = db.relationship("Follow", back_populates="party")
    feed_posts = db.relationship("Post", back_populates="party")
    challenger_campaigns = association_proxy("candidates", "campaigns")
    reelection_campaigns = association_proxy("representatives", "campaigns")

    # add serialization rules
    serialize_rules = (
        "-candidates.party",
        "-representatives.party",
        "-voters.party",
        "-challenger_campaigns.party",
        "-reelection_campaigns.party",
        "-follows.party",
        "-feed_posts.party",
    )

    # add validation

    def __repr__(self):
        return f"<Party {self.name}>"


# Elections and Election Information


class Election(db.Model, SerializerMixin):
    __tablename__ = "elections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    administration_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    super_admin_id = db.Column(db.Integer, db.ForeignKey("super_admin.id"))
    deadlines_id = db.Column(db.Integer, db.ForeignKey("election_deadlines.id"))
    options_id = db.Column(db.Integer, db.ForeignKey("voting_options.id"))
    overview = db.Column(db.String)
    election_type = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    county = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    options = db.relationship("Options", back_populates="election")
    deadlines = db.relationship("Deadlines", back_populates="election")
    polls = db.relationship("Poll", back_populates="election")
    propositions = db.relationship("Proposition", back_populates="election")

    ballots = db.relationship("Ballot", back_populates="election")
    guides = db.relationship("Guide", back_populates="election")
    administration = db.relationship("Admin", back_populates="elections")
    super_admin = db.relationship("SuperAdmin", back_populates="elections")
    follows = db.relationship("Follow", back_populates="election")
    feed_posts = db.relationship("Post", back_populates="election")

    voters = association_proxy("ballots", "voter")
    votes = association_proxy("ballots", "votes")
    campaigns = association_proxy("polls", "campaigns")
    bills = association_proxy("propositions", "bill")

    # add serialization rules
    serialize_rules = (
        "-polls.election",
        "-propositions.election",
        "-candidates.election",
        "-ballots.election",
        "-guides.election" "-bills.election",
        "-deadlines.election" "-voters.election",
        "-options.election",
        "-votes.election",
        "-administration.elections",
        "-super_admin.elections",
        "-follows.election",
        "-feed_posts.election",
    )

    # add validation

    def __repr__(self):
        return f"<Election {self.name}>"


class Options(db.Model, SerializerMixin):
    __tablename__ = "voting_options"

    id = db.Column(db.Integer, primary_key=True)
    early_voting = db.Column(db.Boolean)
    vote_by_mail = db.Column(db.Boolean)
    in_person_voting = db.Column(db.Boolean)
    mobile_voting = db.Column(db.Boolean)
    online_voting = db.Column(db.Boolean)

    # add relationships
    election = db.relationship("Election", back_populates="options")

    # add serialization rules
    serialize_rules = ("-election.options",)

    # add validation

    def __repr__(self):
        return f"<Voting Option Set {self.id}>"


class Deadlines(db.Model, SerializerMixin):
    __tablename__ = "election_deadlines"

    id = db.Column(db.Integer, primary_key=True)
    voter_registration_deadline = db.Column(db.Date)
    mail_in_ballot_deployment_date = db.Column(db.Date)
    mail_in_ballot_return_opening = db.Column(db.Date)
    mail_in_ballot_return_deadline = db.Column(db.Date)
    mail_in_ballot_postmark_deadline = db.Column(db.Date)
    early_in_person_voting_opening = db.Column(db.Date)
    early_in_person_voting_deadline = db.Column(db.Date)
    mobile_voting_opening = db.Column(db.Date)
    mobile_voting_deadline = db.Column(db.Date)
    online_voting_opening = db.Column(db.Date)
    online_voting_deadline = db.Column(db.Date)
    in_person_election_date = db.Column(db.Date)

    # add relationships
    election = db.relationship("Election", back_populates="deadlines")

    # add serialization rules
    serialize_rules = ("-election.deadlines",)

    # add validation

    def __repr__(self):
        return f"<Election Deadline Set {self.id}>"
