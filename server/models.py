from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


# Platform Users and Accounts


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)
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


class Account(db.Model, SerializerMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        primary_key=True,
        nullable=False,
    )
    account_type = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    user = db.relationship("User", back_populates="account")
    voter = db.relationship("Voter", back_populates="account")
    super_admin = db.relationship("SuperAdmin", back_populates="account")
    admin = db.relationship("Admin", back_populates="account")
    partner = db.relationship("Partner", back_populates="account")
    member = db.relationship("Member", back_populates="account")
    administration = association_proxy("admin", "administration")
    enterprise = association_proxy("partner", "enterprise")

    # add serialization rules
    serialize_rules = (
        "-user.account",
        "-voter.account",
        "-super_admin.account",
        "-admin.account",
        "-partner.account",
        "-member.account",
        "-administration.account",
        "-enterprise.account",
    )

    # add validation

    def __repr__(self):
        return f"<Account {self.id}>"


# Individual User Account Types (Roles)


class Voter(db.Model, SerializerMixin):
    __tablename__ = "voters"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=True, nullable=False
    )
    profile_photo = db.Column(db.String)
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
    account = db.relationship("Account", back_populates="voter")
    ballots = db.relationship("Ballot", back_populates="voter")
    following = db.relationship("Follow", back_populates="voter")
    elections = association_proxy("ballots", "election")
    votes = association_proxy("ballots", "votes")
    user = association_proxy("account", "user")

    # add serialization rules
    serialize_rules = (
        "-account.voter",
        "-user.voter",
        "-ballots.voter",
        "-elections.voter",
        "-votes.voter",
        "-following.voter",
    )

    # add validation

    def __repr__(self):
        return f"<Voter {self.id}, {self.name}>"


class Partner(db.Model, SerializerMixin):
    __tablename__ = "partners"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=True, nullable=False
    )
    profile_photo = db.Column(db.String)
    title = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    account = db.relationship("Account", back_populates="partner")
    enterprise = db.relationship("Enterprise", back_populates="partner")
    user = association_proxy("account", "user")
    members = association_proxy("enterprise", "members")

    # add serialization rules
    serialize_rules = (
        "-account.partner",
        "-enterprise.partner",
        "-user.partner",
        "-members.partner",
    )

    # add validation

    def __repr__(self):
        return f"<Partner {self.name}>"


class Member(db.Model, SerializerMixin):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=True, nullable=False
    )
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    administration_id = db.Column(db.Integer, db.ForeignKey("administrations.id"))
    profile_photo = db.Column(db.String)
    title = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    account = db.relationship("Account", back_populates="member")
    enterprise = db.relationship("Enterprise", back_populates="member")
    administration = db.relationship("Admin", back_populates="member")
    user = association_proxy("account", "user")
    partner = association_proxy("enterprise", "partner")
    admin = association_proxy("administration", "admin")

    # add serialization rules
    serialize_rules = (
        "-team.members",
        "-admin.members",
        "-partner.members",
        "-account.members",
        "-enterprise.members",
        "-user.members",
    )

    # add validation

    def __repr__(self):
        return f"<Member {self.id}, Team: {self.team}>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=True, nullable=False
    )
    profile_photo = db.Column(db.String)
    title = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    account = db.relationship("Account", back_populates="admin")
    administration = db.relationship("Administration", back_populates="admin")
    members = association_proxy("administration", "members")
    user = association_proxy("account", "user")

    # add serialization rules
    serialize_rules = ("-account.admin", "-administration.admin", "-members.admin")

    # add validation

    def __repr__(self):
        return f"<Admin {self.username}>"


class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = "super_admin"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=True, nullable=False
    )
    profile_photo = db.Column(db.String)
    title = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    user = db.relationship("User", back_populates="super_admin")
    elections = db.relationship("Election", back_populates="super_admin")
    account = association_proxy("user", "account")

    # add serialization rules
    serialize_rules = (
        "-account.super_admin",
        "-user.super_admin",
        "-elections.super_admin",
    )

    # add validation

    def __repr__(self):
        return f"<Super Admin {self.username}>"


# Administrations and Enterprise Accounts


class Enterprise(db.Model, SerializerMixin):
    __tablename__ = "enterprises"

    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(
        db.Integer,
        db.ForeignKey("partners.id"),
        unique=True,
        primary_key=True,
        nullable=False,
    )
    name = db.Column(db.String, unique=True, nullable=False)
    enterprise_type = db.Column(db.String)
    website = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    partner = db.relationship("Partner", back_populates="enterprise")
    members = db.relationship("Member", back_populates="enterprise")
    guides = db.relationship("Guide", back_populates="enterprise")
    endorsements = db.relationship("Endorsement", back_populates="enterprise")
    follows = db.relationship("Follow", back_populates="enterprise")
    feed_posts = db.relationship("Post", back_populates="enterprise")
    recommendations = association_proxy("guides", "recommendations")
    member_accounts = association_proxy("members", "account")
    partner_account = association_proxy("partner", "account")

    # add serialization rules
    serialize_rules = (
        "-partner.enterprise",
        "-members.enterprise",
        "-guides.enterprise",
        "-recommendations.enterprise",
        "-member_accounts.enterprise",
        "-partner_accounts.enterprise",
        "-follows.enterprise",
        "-feed_posts.enterprise",
        "-endorsements.enterprise",
    )

    # add validation

    def __repr__(self):
        return f"<Enterprise {self.name}>"


class Administration(db.Model, SerializerMixin):
    __tablename__ = "administrations"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("admin.id"),
        unique=True,
        primary_key=True,
        nullable=False,
    )
    name = db.Column(db.String, unique=True, nullable=False)
    administration_type = db.Column(db.String)
    website = db.Column(db.String)
    verifification_status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    admin = db.relationship("Admin", back_populates="administration")
    members = db.relationship("Member", back_populates="administration")
    elections = db.relationship("Election", back_populates="administration")
    follows = db.relationship("Follow", back_populates="administration")
    feed_posts = db.relationship("Post", back_populates="administration")
    member_accounts = association_proxy("members", "account")
    admin_account = association_proxy("admin", "account")

    # add serialization rules
    serialize_rules = (
        "-admin.administration",
        "-members.administration",
        "-member_accounts.administration",
        "-admin_account.administration",
        "-elections.administration",
        "-follows.administration",
        "-feed_posts.administration",
    )


# Political Jurisdictions


class Country(db.Model, SerializerMixin):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # add relationships
    states = db.relationship("State", back_populates="country")
    counties = association_proxy("states", "counties")

    # add serialization rules
    serialize_rules = (
        "-states.country",
        "-counties.country",
    )

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
    follows = db.relationship("Follow", back_populates="state")
    feed_posts = db.relationship("Post", back_populates="state")
    cities = association_proxy("counties", "cities")

    # add serialization rules
    serialize_rules = (
        "-counties.state",
        "-country.states",
        "-follows.state",
        "-feed_posts.state",
        "-cities.state",
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
    follows = db.relationship("Follow", back_populates="county")
    feed_posts = db.relationship("Post", back_populates="county")
    country = association_proxy("state", "country")

    # add serialization rules
    serialize_rules = (
        "-state.counties",
        "-country.counties",
        "-follows.counties",
        "-feed_posts.counties",
    )

    # add validation

    def __repr__(self):
        return f"<County {self.name}>"


class City(db.Model, SerializerMixin):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey("counties.id"), nullable=False)

    # add relationships
    county = db.relationship("County", back_populates="cities")
    follows = db.relationship("Follow", back_populates="city")
    feed_posts = db.relationship("Post", back_populates="city")
    state = association_proxy("county", "state")

    # add serialization rules
    serialize_rules = (
        "-county.cities",
        "-follows.cities",
        "-feed_posts.cities",
        "-state.cities",
    )

    # add validation

    def __repr__(self):
        return f"<City {self.name}>"


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


# Ballots, Votes, and Voter Guides


class Ballot(db.Model, SerializerMixin):
    __tablename__ = "ballots"

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    polling_location_1 = db.Column(db.String)
    polling_location_2 = db.Column(db.String)
    polling_location_3 = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    election = db.relationship("Election", back_populates="ballots")
    voter = db.relationship("Voter", back_populates="ballots")
    votes = db.relationship("Vote", back_populates="ballot")
    polls = association_proxy("election", "polls")
    propositions = association_proxy("election", "propositions")
    account = association_proxy("voter", "account")
    deadlines = association_proxy("election", "deadlines")
    voting_options = association_proxy("election", "options")

    # add serialization rules
    serialize_rules = (
        "-election.ballots",
        "-voter.ballots",
        "-account.ballots",
        "-polls.ballots",
        "-propositions.ballots",
        "-deadlines.ballots",
        "-voting_options.ballots",
        "-votes.ballots",
    )

    # add validation

    def __repr__(self):
        return f"<Ballot {self.name}>"


class Vote(db.Model, SerializerMixin):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    ballot_id = db.Column(db.Integer, db.ForeignKey("ballots.id"), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    proposition_id = db.Column(db.Integer, db.ForeignKey("propositions.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    ballot = db.relationship("Ballot", back_populates="votes")
    campaign = db.relationship("Campaign", back_populates="votes")
    proposition = db.relationship("Proposition", back_populates="votes")
    election = association_proxy("ballot", "election")
    voter = association_proxy("ballot", "voter")
    bill = association_proxy("proposition", "bill")
    candidate = association_proxy("campaign", "candidate")
    representative = association_proxy("campaign", "representative")

    # add serialization rules
    serialize_rules = (
        "-ballot.votes",
        "-campaign.votes",
        "-proposition.votes",
        "-election.votes",
        "-voter.votes",
        "-bill.votes",
        "-candidate.votes",
        "-representative.votes",
    )

    # add validation

    def __repr__(self):
        return f"<Vote {self.id}, {self.voter}>"


class Guide(db.Model, SerializerMixin):
    __tablename__ = "voter_guides"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    election = db.relationship("Election", back_populates="guides")
    enterprise = db.relationship("Enterprise", back_populates="guides")
    recommendations = db.relationship("Recommendation", back_populates="guide")
    campaigns = association_proxy("recommendations", "campaign")
    propositions = association_proxy("recommendations", "proposition")
    partner = association_proxy("enterprise", "partner")

    # add serialization rules
    serialize_rules = (
        "-election.guides",
        "-enterprise.guides",
        "-recommendations.guide",
        "-campaigns.guide",
        "-propositions.guide",
        "-partner.guides",
    )

    # add validation

    def __repr__(self):
        return f"<Voter Guide {self.id}>"


class Recommendation(db.Model, SerializerMixin):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    guide_id = db.Column(db.Integer, db.ForeignKey("voter_guides.id"), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    proposition_id = db.Column(db.Integer, db.ForeignKey("propositions.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    guide = db.relationship("Guide", back_populates="recommendations")
    campaign = db.relationship("Campaign", back_populates="recommendations")
    proposition = db.relationship("Proposition", back_populates="recommendations")
    enterprise = association_proxy("guide", "enterprise")
    bill = association_proxy("proposition", "bill")
    candidate = association_proxy("campaign", "candidate")
    representative = association_proxy("campaign", "representative")

    # add serialization rules
    serialize_rules = (
        "-guide.recommendations",
        "-enterprise.recommendations",
        "-bill.recommendations",
        "-candidate.recommendations",
        "-representative.recommendations",
        "-proposition.recommendations",
        "-campaign.recommendations",
    )

    # add validation

    def __repr__(self):
        return f"<Recommendation {self.id}>"


class Endorsement(db.Model, SerializerMixin):
    __tablename__ = "endorsements"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    enterprise_id = db.Column(
        db.Integer, db.ForeignKey("enterprises.id"), nullable=False
    )
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    proposition_id = db.Column(db.Integer, db.ForeignKey("propositions.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    election = db.relationship("Election", back_populates="endorsements")
    enterprise = db.relationship("Enterprise", back_populates="endorsements")
    campaign = db.relationship("Campaign", back_populates="endorsements")
    proposition = db.relationship("Proposition", back_populates="endorsements")
    partner = association_proxy("enterprise", "partner")
    candidate = association_proxy("campaign", "candidate")
    bill = association_proxy("proposition", "bill")

    # add serialization rules
    serialize_rules = (
        "-partner.endorsements",
        "-campaign.endorsements",
        "-proposition.endorsements",
        "-bill.endorsements",
        "-candidate.endorsements",
        "-enterprise.endorsements",
        "-election.endorsements",
    )

    # add validation

    def __repr__(self):
        return f"<Endorsement {self.id}>"


# Candidates and Campaign Processes


class Poll(db.Model, SerializerMixin):
    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    position = db.Column(db.String)
    position_type = db.Column(db.String)
    position_term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))

    # add relationships
    election = db.relationship("Election", back_populates="polls")
    campaigns = db.relationship("Campaign", back_populates="poll")
    winners = db.relationship("Winner", back_populates="poll")
    candidates = association_proxy("campaigns", "candidate")
    votes = association_proxy("campaigns", "votes")

    # add serialization rules
    serialize_rules = (
        "-election.polls",
        "-campaigns.poll",
        "-candidates.poll",
        "-votes.poll",
        "-winners.poll",
    )

    # add validation

    def __repr__(self):
        return f"<Poll {self.name}>"


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
    recommendations = db.relationship("Recommendation", back_populates="campaign")
    votes = db.relationship("Vote", back_populates="campaign")
    wins = db.relationship("Winner", back_populates="campaign")
    election = association_proxy("poll", "election")
    voters = association_proxy("vote", "voters")

    # add serialization rules
    serialize_rules = (
        "-poll.campaigns",
        "-candidate.campaigns",
        "-representative.campaigns",
        "-election.campaigns",
        "-recommendations.campaign",
        "-votes.campaign",
        "-voters.campaign",
    )

    # add validation

    def __repr__(self):
        return f"<Campaign {self.id}>"


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
    follows = db.relationship("Follow", back_populates="candidate")
    feed_posts = db.relationship("Post", back_populates="candidate")
    polls = association_proxy("campaigns", "poll")
    wins = association_proxy("campaigns", "wins")
    votes = association_proxy("campaigns", "votes")

    # add serialization rules
    serialize_rules = (
        "-polls.candidates",
        "-campaigns.candidate",
        "-votes.candidate",
        "-wins.candidate",
        "-follows.candidate",
        "-feed_posts.candidate",
    )

    # add validation

    def __repr__(self):
        return f"<Candidate {self.name}>"


class Winner(db.Model, SerializerMixin):
    __tablename__ = "winners"

    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"), primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    poll = db.relationship("Poll", back_populates="winners")
    campaign = db.relationship("Campaign", back_populates="winners")
    votes = association_proxy("campaign", "votes")
    candidate = association_proxy("campaign", "candidate")
    representative = association_proxy("campaign", "representative")
    election = association_proxy("poll", "election")

    # add serialization rules
    serialize_rules = (
        "-poll.winners",
        "-campaign.winners",
        "-election.winners",
        "-candidate.winners",
        "-representative.winners",
        "-votes.winners",
    )

    # add validation

    def __repr__(self):
        return f"<Winner {self.id}>"


# Bills and Legislative Processes


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
    recommendations = db.relationship("Recommendation", back_populates="proposition")
    votes = db.relationship("Vote", back_populates="proposition")

    # add serialization rules
    serialize_rules = (
        "-election.propositions",
        "-bill.propositions",
        "-votes.propositions",
        "-recommendations.proposition",
    )

    # add validation

    def __repr__(self):
        return f"<Propositions {self.name}>"


class Bill(db.Model, SerializerMixin):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    category = db.Column(db.String)
    bill_type = db.Column(db.String)
    overview = db.Column(db.String)
    text = db.Column(db.String)
    state = db.Column(db.String)
    county = db.Column(db.String)

    # add relationships
    propositions = db.relationship("Proposition", back_populates="bill")
    follows = db.relationship("Follow", back_populates="bill")
    feed_posts = db.relationship("Post", back_populates="bill")
    elections = association_proxy("propositions", "election")

    # add serialization rules
    serialize_rules = (
        "-proposition.bill",
        "-election.bill",
        "-follows.bill",
        "-feed_posts.bill",
    )

    # add validation

    def __repr__(self):
        return f"<Legislation {self.name}>"


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
    re_election_campaigns = db.relationship("Campaign", back_populates="representative")
    terms = db.relationship("Term", back_populates="representative")
    follows = db.relationship("Follow", back_populates="representative")
    feed_posts = db.relationship("Post", back_populates="representative")
    polls = association_proxy("campaigns", "poll")
    wins = association_proxy("campaigns", "wins")
    votes = association_proxy("campaigns", "votes")

    # add serialization rules
    serialize_rules = (
        "-terms.representative",
        "-re_election_campaigns.representative",
        "-polls.representative",
        "-wins.representative",
        "-votes.representative",
        "-follows.representative",
        "-feed_posts.representative",
    )

    # add validation

    def __repr__(self):
        return f"<Representative {self.name}>"


class Term(db.Model, SerializerMixin):
    __tablename__ = "terms"

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"))
    representatives_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))
    term_name = db.Column(db.String)
    term_type = db.Column(db.String)
    term_start_date = db.Column(db.Date)
    term_end_date = db.Column(db.Date)
    term_length = db.Column(db.String)

    # add relationships
    representative = db.relationship("Representative", back_populates="terms")
    poll = db.relationship("Poll", back_populates="terms")

    # add serialization rules
    serialize_rules = ("-representative.terms", "-poll.terms")

    # add validation

    def __repr__(self):
        return f"<Term {self.id}>"


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


# Network and News Feed Connectivity


class Follow(db.Model, SerializerMixin):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"), primary_key=True)

    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    representative_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))

    administration_id = db.Column(db.Integer, db.ForeignKey("administrations.id"))
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))

    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    county_id = db.Column(db.Integer, db.ForeignKey("counties.id"))

    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    follower = db.relationship("Voter", back_populates="follows")
    election = db.relationship("Election", back_populates="follows")
    bill = db.relationship("Bill", back_populates="follows")
    candidate = db.relationship("Candidate", back_populates="follows")
    representative = db.relationship("Representative", back_populates="follows")
    administration = db.relationship("Administration", back_populates="follows")
    enterprise = db.relationship("Enterprise", back_populates="follows")
    state = db.relationship("State", back_populates="follows")
    county = db.relationship("County", back_populates="follows")
    party = db.relationship("Party", back_populates="follows")

    # add serialization rules
    serialize_rules = (
        "-follower.follows",
        "-election.follows",
        "-bill.follows",
        "-candidate.follows",
        "-representative.follows",
        "-administration.follows",
        "-enterprise.follows",
        "-state.follows",
        "-county.follows",
        "-party.follows",
    )

    # add validation

    def __repr__(self):
        return f"<Follow {self.id}>"


class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String)
    content = db.Column(db.String)

    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    representative_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))
    administration_id = db.Column(db.Integer, db.ForeignKey("administrations.id"))
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    county_id = db.Column(db.Integer, db.ForeignKey("counties.id"))
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    election = db.relationship("Election", back_populates="posts")
    bill = db.relationship("Bill", back_populates="posts")
    candidate = db.relationship("Candidate", back_populates="posts")
    representative = db.relationship("Representative", back_populates="posts")
    administration = db.relationship("Administration", back_populates="posts")
    enterprise = db.relationship("Enterprise", back_populates="posts")
    state = db.relationship("State", back_populates="posts")
    county = db.relationship("County", back_populates="posts")
    party = db.relationship("Party", back_populates="posts")

    # add serialization rules
    serialize_rules = (
        "-election.posts",
        "-bill.posts",
        "-candidate.posts",
        "-representative.posts",
        "-administration.posts",
        "-enterprise.posts",
        "-state.posts",
        "-county.posts",
        "-party.posts",
    )


class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    partner_id = db.Column(db.Integer, db.ForeignKey("partners.id"))
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    super_admin_id = db.Column(db.Integer, db.ForeignKey("super_admin.id"))

    notification_type = db.Column(db.String)
    content = db.Column(db.String)

    election_id = db.Column(db.Integer, db.ForeignKey("elections.id"))
    ballot_id = db.Column(db.Integer, db.ForeignKey("ballots.id"))
    guide_id = db.Column(db.Integer, db.ForeignKey("voter_guides.id"))
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    representative_id = db.Column(db.Integer, db.ForeignKey("representatives.id"))
    administration_id = db.Column(db.Integer, db.ForeignKey("administrations.id"))
    enterprise_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    county_id = db.Column(db.Integer, db.ForeignKey("counties.id"))
    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationships
    voter = db.relationship("Voter", back_populates="notifications")
    admin = db.relationship("Admin", back_populates="notifications")
    partner = db.relationship("Partner", back_populates="notifications")
    member = db.relationship("Member", back_populates="notifications")
    super_admin = db.relationship("SuperAdmin", back_populates="notifications")
    election = db.relationship("Election", back_populates="notifications")
    ballot = db.relationship("Ballot", back_populates="notifications")
    guide = db.relationship("Guide", back_populates="notifications")
    bill = db.relationship("Bill", back_populates="notifications")
    candidate = db.relationship("Candidate", back_populates="notifications")
    representative = db.relationship("Representative", back_populates="notifications")
    administration = db.relationship("Administration", back_populates="notifications")
    enterprise = db.relationship("Enterprise", back_populates="notifications")
    state = db.relationship("State", back_populates="notifications")
    county = db.relationship("County", back_populates="notifications")
    party = db.relationship("Party", back_populates="notifications")
    post = db.relationship("Post", back_populates="notifications")

    # add serialization rules
    serialize_rules = (
        "-voter.notifications",
        "-election.notifications",
        "-ballot.notifications",
        "-guide.notifications",
        "-bill.notifications",
        "-candidate.notifications",
        "-representative.notifications",
        "-administration.notifications",
        "-enterprise.notifications",
        "-state.notifications",
        "-county.notifications",
        "-party.notifications",
        "-post.notifications",
        "-admin.notifications",
        "-partner.notifications",
        "-member.notifications",
        "-super_admin.notifications",
    )

    # add validation

    def __repr__(self):
        return f"<Notification {self.id}>"
