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

    # add relationships
    voter = db.relationship("Voter", back_populates="user")
    admin = db.relationship("Admin", back_populates="user")
    partner = db.relationship("Partner", back_populates="user")
    account = db.relationship("Account", back_populates="user")

    # add serialization rules
    serialize_rules = (
        "-voter.user",
        "-admin.user",
        "-partner.user",
        "-account.user",
    )

    # add validation

    def __repr__(self):
        return f"<User {self.username}>"


class Voter(db.Model, SerializerMixin):
    __tablename__ = "voters"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    profile_photo = db.Column(db.String)
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
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))

    # add relationships
    votes = db.relationship("Vote", back_populates="voter")
    account = db.relationship("Account", back_populates="voters")
    admin = association_proxy("account", "admin")

    # add serialization rules
    serialize_rules = ("-account.voters", "-admin.voters")

    # add validation

    def __repr__(self):
        return f"<Voter {self.username}>"


class Partner(db.Model, SerializerMixin):
    __tablename__ = "partners"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    profile_photo = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    account = db.relationship("Account", back_populates="partners")
    guides = db.relationship("Guide", back_populates="partner")
    ballots = association_proxy("guides", "ballot")

    # add serialization rules
    serialize_rules = ("-account.partners", "-guides.partner", "-ballots.partner")

    # add validation

    def __repr__(self):
        return f"<Partner {self.username}>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    profile_photo = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    account = db.relationship("Account", back_populates="admin")

    # add serialization rules
    serialize_rules = ("-voters.admin", "-account.admin")

    # add validation

    def __repr__(self):
        return f"<Admin {self.username}>"


class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = "super_admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    profile_photo = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)

    # add relationships
    account = db.relationship("Account", back_populates="super_admin")
    user = db.relationship("User", back_populates="super_admin")

    # add serialization rules
    serialize_rules = ("-voters.admin", "-account.admin")

    # add validation

    def __repr__(self):
        return f"<Super Admin {self.username}>"


class Account(db.Model, SerializerMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    partner_id = db.Column(db.Integer, db.ForeignKey("partners.id"))
    super_admin_id = db.Column(db.Integer, db.ForeignKey("super_admin.id"))
    account_photo = db.Column(db.String)
    account_name = db.Column(db.String, unique=True, nullable=False)
    account_type = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    super_admin = db.relationship("SuperAdmin", back_populates="account")
    admin = db.relationship("Admin", back_populates="account")
    partner = db.relationship("Partner", back_populates="account")
    voter = db.relationship("Voter", back_populates="account")
    user = db.relationship("User", back_populates="account")
    votes = association_proxy("voter", "votes")
    ballots = association_proxy("voter", "ballots")

    # add serialization rules
    serialize_rules = ("-voters.account", "-partner.account", "-admin.account")

    # add validation

    def __repr__(self):
        return f"<Account {self.id}>"


# Platform Jurisdictions


class Country(db.Model, SerializerMixin):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # add relationships
    states = db.relationship("State", back_populates="country")

    # add serialization rules
    serialize_rules = ("-states.country",)

    # add validation

    def __repr__(self):
        return f"<Country {self.name}>"


class State(db.Model, SerializerMixin):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)

    # add relationships
    country = db.relationship("Country", back_populates="states")
    counties = db.relationship("County", back_populates="state")

    # add serialization rules
    serialize_rules = (
        "-counties.state",
        "-country.states",
    )

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
    country = association_proxy("state", "country")

    # add serialization rules
    serialize_rules = ("-state.counties", "-country.counties")

    # add validation

    def __repr__(self):
        return f"<County {self.name}>"


# Elections and Election Processes


class Election(db.Model, SerializerMixin):
    __tablename__ = "elections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deadlines_id = db.Column(db.Integer, db.ForeignKey("election_deadlines.id"))
    options_id = db.Column(db.Integer, db.ForeignKey("voting_options.id"))
    overview = db.Column(db.String)
    election_type = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    options = db.relationship("Options", back_populates="election")
    deadlines = db.relationship("Deadlines", back_populates="election")
    polls = db.relationship("Poll", back_populates="election")
    propositions = db.relationship("Proposition", back_populates="election")
    ballots = db.relationship("Ballot", back_populates="election")
    candidates = association_proxy("polls", "candidates")
    bills = association_proxy("propositions", "bill")
    voters = association_proxy("ballots", "voter")

    # add serialization rules
    serialize_rules = (
        "-polls.election",
        "-propositions.election",
        "-candidates.election",
        "-ballots.election",
        "-bills.election",
        "-deadlines.election" "-voters.election",
        "-options.election",
    )

    # add validation

    def __repr__(self):
        return f"<Election {self.name}>"


class Options(db.Model, SerializerMixin):
    __tablename__ = "voting_options"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
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
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
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


# Ballots and Voting Processes


class Ballot(db.Model, SerializerMixin):
    __tablename__ = "ballots"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))
    polling_location_1 = db.Column(db.String)
    polling_location_2 = db.Column(db.String)
    polling_location_3 = db.Column(db.String)
    status = db.Column(db.String)

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


class Vote(db.Model, SerializerMixin):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))
    partner_id = db.Column(db.Integer, db.ForeignKey("partners.id"))
    ballot_id = db.Column(db.Integer, db.ForeignKey("ballots.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))

    # add relationships
    voter = db.relationship("Voter", back_populates="votes")
    partner = db.relationship("Partner", back_populates="votes")
    ballot = db.relationship("Ballot", back_populates="votes")
    candidate = db.relationship("Candidate", back_populates="votes")
    bill = db.relationship("Bill", back_populates="votes")

    # add serialization rules
    serialize_rules = (
        "-voter.votes",
        "-partner.votes",
        "-ballot.votes",
        "-candidate.votes",
        "-bill.votes",
    )

    # add validation

    def __repr__(self):
        return f"<Vote {self.id}, {self.voter}>"


class Guide(db.Model, SerializerMixin):
    __tablename__ = "voter_guides"

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey("partners.id"))
    ballot_id = db.Column(db.Integer, db.ForeignKey("ballots.id"), nullable=False)

    # add relationships
    partner = db.relationship("Partner", back_populates="guides")
    ballot = db.relationship("Ballot", back_populates="guides")
    election = association_proxy("ballot", "election")
    votes = association_proxy("ballot", "votes")

    # add serialization rules
    serialize_rules = (
        "-election.guides",
        "-partner.guides",
        "-ballot.guides",
        "-votes.guides",
    )


class Poll(db.Model, SerializerMixin):
    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=True)
    position = db.Column(db.String)

    # add relationships
    election = db.relationship("Election", back_populates="polls")
    campaigns = db.relationship("Campaign", back_populates="poll")
    votes = db.relationship("Vote", back_populates="poll")
    candidates = association_proxy("campaigns", "candidate")
    voters = association_proxy("vote", "voters")

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
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    email = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    twitter = db.Column(db.String)
    facebook = db.Column(db.String)
    instagram = db.Column(db.String)
    photo = db.Column(db.String)

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
    candidate_statement = db.Column(db.String)
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
    votes = db.relationship("Vote", back_populates="proposition")
    polls = association_proxy("election", "polls")
    voters = association_proxy("vote", "voters")

    # add serialization rules
    serialize_rules = (
        "-election.propositions",
        "-bill.propositions",
        "-polls.propositions",
        "-voters.propositions",
        "-votes.propositions",
    )

    # add validation

    def __repr__(self):
        return f"<Propositions {self.name}>"


class Bill(db.Model, SerializerMixin):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    bill_type = db.Column(db.String)
    overview = db.Column(db.String)
    text = db.Column(db.String)
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


# Political Affiliations


class Party(db.Model, SerializerMixin):
    __tablename__ = "parties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    overview = db.Column(db.String)

    # add relationships
    candidates = db.relationship("Candidate", back_populates="party")
    representatives = db.relationship("Representative", back_populates="party")
    voters = db.relationship("Voter", back_populates="party")

    # add serialization rules
    serialize_rules = ("-candidates.party", "-representatives.party", "-voters.party")

    # add validation

    def __repr__(self):
        return f"<Party {self.name}>"


# Elected Officials


class Representative(db.Model, SerializerMixin):
    __tablename__ = "representatives"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rep_type = db.Column(db.String, nullable=False)
    position = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    email = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    twitter = db.Column(db.String)
    facebook = db.Column(db.String)
    instagram = db.Column(db.String)
    photo = db.Column(db.String)

    # add relationships
    campaigns = db.relationship("Campaign", back_populates="representative")
    terms = db.relationship("Term", back_populates="representative")

    # add serialization rules
    serialize_rules = ("-campaigns.representative",)

    # add validation

    def __repr__(self):
        return f"<Representative {self.name}>"


class Term(db.Model, SerializerMixin):
    __tablename__ = "terms"

    id = db.Column(db.Integer, primary_key=True)
    representative_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))
    term_start_date = db.Column(db.Date)
    term_end_date = db.Column(db.Date)
    term_length = db.Column(db.String)

    # add relationships
    representative = db.relationship("Representative", back_populates="terms")

    # add serialization rules
    serialize_rules = ("-representative.terms",)

    # add validation

    def __repr__(self):
        return f"<Term {self.id}>"
