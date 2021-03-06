#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db) # Used for migrations

# DONE: connect to a local postgresql database -- done through config.py

#----------------------------------------------------------------------------#
# Relationship tables
#----------------------------------------------------------------------------#
# Relationship table between venues and genres
venues_genres = db.Table('venues_genres',
db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

# Relationship table between artists and genres
artists_genres = db.Table('artists_genres',
db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  # DONE: implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  # Relationships
  shows = db.relationship('Show', backref='venue', lazy=True)
  genres = db.relationship('Genre', secondary=venues_genres, backref=db.backref('venues', lazy=True))

  def __repr__(self):
    return f'<Venue {self.id}: {self.name}>'

class Artist(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  # DONE: implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  # Relationships
  genres = db.relationship('Genre', secondary=artists_genres, backref=db.backref('artists', lazy=True))
  shows = db.relationship('Show', backref='artist', lazy=True)

  def __repr__(self):
    return f'<Artist {self.id}: {self.name}>'

# DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# Values for this table are added through the migration script that introduces it
class Genre(db.Model):
  __tablename__ = 'genres'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

  def __repr__(self):
    return f'<Show {self.id}. Venue: {self.venue_id}, artist: {self.artist_id}. Start time: {self.start_time}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

# Dictionary for states and abbreviations
# Based on https://gist.github.com/rogerallen/1583593

state_abbrev_from_name = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'Washington,D.C': 'DC', # Changed this to fit the geodata list
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

state_name_from_abbrev = dict(map(reversed, state_abbrev_from_name.items()))


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  # Get all the different locations (city, state) from the database
  locations = db.session.query(Venue.state, Venue.city).group_by(Venue.state, Venue.city).order_by(Venue.state, Venue.city).all()
  for location in locations:
    state = location[0]
    city = location[1]
    location_object = {
      'city': city,
      'state': state,
      'venues': []
    }
    # Get all venues from this location
    venues = Venue.query.filter_by(city=city, state=state).all()
    for venue in venues:
      venue_object = {
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': len(venue.shows)
      }
      # Add the venue object to the location object
      location_object['venues'].append(venue_object)

    # Add the location object to data
    data.append(location_object)
  
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search_str = '%' + search_term + '%'
  results = Venue.query.filter(Venue.name.ilike(search_str)).all()

  # Initialize the response object
  response = {
    'count': len(results),
    'data': []
  }

  # Iterate through the resuls
  for venue in results:
    response['data'].append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len(venue.shows)
    })


  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  
  # Get genres
  genres = []
  for genre in venue.genres:
    genres.append(genre.name)

  # Get shows
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  for show in venue.shows:
    artist = show.artist
    show_object = {
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': datetime_to_str(show.start_time)
    }
    if show.start_time < current_time:
      past_shows.append(show_object)
    else:
      upcoming_shows.append(show_object)

  # Build the final data object
  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': genres,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows
  }
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
  form = VenueForm()
  # Deal with GET request
  if request.method == 'GET':
    return render_template('forms/new_venue.html', form=form)

  error = False
  # DONE: insert form data as a new Venue record in the db, instead
  try:
    if not form.validate_on_submit():
      errors = []
      for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
          errors.append(errorMessages)
      raise Exception(errors.__str__())

    # Get values from form
    name = request.form['name']
    state_abbrev = state_abbrev_from_name[request.form['state']]
    city = request.form['city']
    address = request.form['address']

    # Validate the venue
    potential_venue = Venue.query.filter_by(state=state_abbrev, city=city, address=address).first()
    if potential_venue is not None:
      if potential_venue.name == name:
        raise Exception("This venue already exists")
      else:
        raise Exception("This address is already taken by venue " + potential_venue.name)

    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website']
    seeking_talent = False
    if 'seeking_talent' in request.form and request.form['seeking_talent'] == 'y':
      seeking_talent = True
    seeking_description = request.form['seeking_description']
    genres = request.form.getlist('genres')

    # Check for empty optional values
    phone = phone if phone != '' else None
    facebook_link = facebook_link if facebook_link != '' else None
    image_link = image_link if image_link != '' else None
    seeking_description = seeking_description if seeking_description != '' else None
    website = website if website != "" else None

    # Create Venue model
    venue = Venue(
      name=name,
      state=state_abbrev,
      city=city,
      address=address,
      phone=phone,
      facebook_link=facebook_link,
      image_link=image_link,
      website=website,
      seeking_talent=seeking_talent,
      seeking_description=seeking_description
    )

    db.session.add(venue)

    # Add genres to the venue
    for genre in genres:
      genre_object = Genre.query.filter_by(name=genre).first()
      venue.genres.append(genre_object)

    # Commit
    db.session.commit()
  except Exception as e:
    error = True
    # DONE: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed. Reason: ' + e.__str__())
    db.session.rollback()
  finally:
    db.session.close()

  # TODO: modify data to be the data object returned from db insertion

  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data = []
  artists = Artist.query.all()
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
    })

  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')
  search_str = '%' + search_term + '%'
  results = Artist.query.filter(Artist.name.ilike(search_str)).all()

  # Initialize the response object
  response = {
    'count': len(results),
    'data': []
  }

  # Iterate through the resuls
  for artist in results:
    response['data'].append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len(artist.shows)
    })


  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artists table, using artist_id

  artist = Artist.query.get(artist_id)
  # Get genres
  genres = []
  for genre in artist.genres:
    genres.append(genre.name)

  # Get past and upcoming shows
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  for show in artist.shows:
    venue = show.venue
    show_object = {
        'venue_id': venue.id,
        'venue_name': venue.name,
        'venue_image_link': venue.image_link,
        'start_time': datetime_to_str(show.start_time)
      }
    if show.start_time < current_time:
      past_shows.append(show_object)
    else:
      upcoming_shows.append(show_object)

  # Build the final data object
  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows
  }
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_form():
  form = ArtistForm()
  # Deal with GET request
  if request.method == 'GET':
    return render_template('forms/new_artist.html', form=form)

  error = False
  # DONE: insert form data as a new Artist record in the db, instead
  try:
    if not form.validate_on_submit():
      errors = []
      for fieldName, errorMessages in form.errors.items():
        print(fieldName)
        for err in errorMessages:
          errors.append(errorMessages)
      raise Exception(errors.__str__())

    # Get values from form
    name = request.form['name']
    state_abbrev = state_abbrev_from_name[request.form['state']]
    city = request.form['city']

    # Validate if the artist already exists
    if len(Artist.query.filter_by(name=name, state=state_abbrev, city=city).all()) != 0:
      raise Exception("This artist already exists")

    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website']
    seeking_venue = False
    if 'seeking_venue' in request.form and request.form['seeking_venue'] == 'y':
      seeking_venue = True
    seeking_description = request.form['seeking_description']
    genres = request.form.getlist('genres')

    # Check for empty optional values
    phone = phone if phone != '' else None
    facebook_link = facebook_link if facebook_link != '' else None
    image_link = image_link if image_link != '' else None
    seeking_description = seeking_description if seeking_description != '' else None
    website = website if website != "" else None

    # Create Artist model
    artist = Artist(
      name=name,
      state=state_abbrev,
      city=city,
      phone=phone,
      facebook_link=facebook_link,
      image_link=image_link,
      website=website,
      seeking_venue=seeking_venue,
      seeking_description=seeking_description
    )

    db.session.add(artist)

    # Add genres to the artist
    for genre in genres:
      genre_object = Genre.query.filter_by(name=genre).first()
      artist.genres.append(genre_object)

    # Commit
    db.session.commit()

  except Exception as e:
    error = True
    # DONE: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed. Reason: ' + e.__str__())
    db.session.rollback()
  finally:
    db.session.close()

  # TODO: modify data to be the data object returned from db insertion

  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  shows = Show.query.all()
  for show in shows:
    venue = show.venue
    artist = show.artist
    data.append({
      'venue_id': venue.id,
      'venue_name': venue.name,
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': datetime_to_str(show.start_time)
    })


  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create', methods=['GET', 'POST'])
def create_shows():
  form = ShowForm()
  # Handle GET request
  if request.method == 'GET':
    return render_template('forms/new_show.html', form=form)

  error = False
  # DONE: insert form data as a new Show record in the db, instead
  try:
    if not form.validate_on_submit():
      errors = []
      for fieldName, errorMessages in form.errors.items():
        if fieldName == 'artist_id':
          errors.append('Artist ID must be an integer')
        if fieldName == 'venue_id':
          errors.append('Venue ID must be an integer')
        if fieldName == 'start_time':
          errors.append('Invalid start time')
          print(errorMessages)
      raise Exception(errors.__str__())

    # Get values from form
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    # Validate if show already exists
    if len(Show.query.filter_by(artist_id=artist_id, venue_id=venue_id, start_time=start_time).all()) != 0:
      raise Exception("This show already exists")

    # Create Show model
    show = Show(
      artist_id=artist_id,
      venue_id=venue_id,
      start_time=start_time
    )

    db.session.add(show)
    db.session.commit()
    
  except Exception as e:
    error = True
    # DONE: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Show could not be listed. Reason: ' + e.__str__())
    db.session.rollback()
  finally:
    db.session.close()

  if not error:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Helper for correct datetime format
def datetime_to_str(d):
  return d.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')

# Populate the genres table
with app.app_context():
  if db.session.query(Genre).count() == 0:
    genres = [
      {'id': 1, 'name': 'Alternative'},
      {'id': 2, 'name': 'Blues'},
      {'id': 3, 'name': 'Classical'},
      {'id': 4, 'name': 'Country'},
      {'id': 5, 'name': 'Electronic'},
      {'id': 6, 'name': 'Folk'},
      {'id': 7, 'name': 'Funk'},
      {'id': 8, 'name': 'Hip-Hop'},
      {'id': 9, 'name': 'Heavy Metal'},
      {'id': 10, 'name': 'Instrumental'},
      {'id': 11, 'name': 'Jazz'},
      {'id': 12, 'name': 'Musical Theatre'},
      {'id': 13, 'name': 'Pop'},
      {'id': 14, 'name': 'Punk'},
      {'id': 15, 'name': 'R&B'},
      {'id': 16, 'name': 'Reggae'},
      {'id': 17, 'name': 'Rock n Roll'},
      {'id': 18, 'name': 'Soul'},
      {'id': 19, 'name': 'Other'}
    ]
    for genre in genres:
      g = Genre(**genre)
      db.session.add(g)
    db.session.commit()

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
