from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from flask import send_from_directory

from werkzeug.utils import secure_filename

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Country, Region, Brewery, Beer, Rating

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import os
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Beer catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///beercatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'facebook']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['facebook']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s"% url
    print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3 style = "color: #fff">'
    output += ' Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 50px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output

# Facebook logout
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Google+ login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output = ''
    output += '<h3 style = "color: #fff">'
    output += ' Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 50px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output

# Google+ logout - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('mainPage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('mainPage'))

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view countries information
@app.route('/country/JSON')
def countriesJSON():
    countries = session.query(Country).all()
    return jsonify(Country=[c.serialize for c in countries])

# JSON APIs to view regions information
@app.route('/country/<int:country_id>/region/JSON')
def regionJSON(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    regions = session.query(Region).filter_by(country_id=country_id).all()
    return jsonify(Region=[r.serialize for r in regions])

# JSON APIs to view breweries information
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/JSON')
def breweryJSON(country_id, region_id):
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    breweries = session.query(Brewery).filter_by(region_id=region_id).all()
    return jsonify(Brewery=[b.serialize for b in breweries])

# JSON APIs to view beers information
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/JSON')
def beerJSON(country_id, region_id, brewery_id):
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    beers = session.query(Beer).filter_by(brewery_id=brewery_id).all()
    return jsonify(Beer=[beer.serialize for beer in beers])


# Path of the uploaded images
UPLOAD_FOLDER = 'static/img/uploaded_images'
# Extensions allowed for images
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the extension of image is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Show all the beers selected by style and show the top 5 rated of all beers in the db
@app.route('/style/<style>/', methods=['GET', 'POST'])
def beerStyle(style):
    if 'username' not in login_session:
        return redirect('/login')

    # Get all the beers by the style previoulsy selected
    beers = session.query(Beer).filter_by(style=style).all()

    if beers:
        countries = []
        regions = []
        breweries = []
        num_ratings = []
        avg_stars = []
        for beer in beers:
            # Insert in a list the id of the country
            country = session.query(Country.id).filter_by(id=beer.country_id).one()[0]
            countries.append(country)

            # Insert in a list the id of the region
            region = session.query(Region.id).filter_by(id=beer.region_id).one()[0]
            regions.append(region)

            # Insert in a list the id of the brewery
            brewery = session.query(Brewery.id).filter_by(id=beer.brewery_id).one()[0]
            breweries.append(brewery)

            # Insert in a list the id of the beer
            ratings = session.query(Rating.num_of_stars).filter_by(beer_id=beer.id).count()
            num_ratings.append(ratings)

            # Insert in a list the average numbers of stars
            stars = session.query(func.avg(Rating.num_of_stars)).filter_by(beer_id=beer.id).all()[0][0]
            # If there is no rating the value to append into the list should be 0
            if stars == None:
                stars = 0
            avg_stars.append(stars)

    # Get the top rated beers
    all_rated_beers = session.query(Beer).join(Rating).filter(Beer.id==Rating.beer_id).all()
    avg_beers_stars = []

    for beer in all_rated_beers:
        # Get the average numbers of stars for each beer
        avg_beer= session.query(func.avg(Rating.num_of_stars)).filter_by(beer_id=beer.id).all()[0][0]
        # Insert the details of the beer into a list
        beer_detail = [beer.image, beer.name, beer.style, avg_beer, beer.country_id, beer.region_id, beer.brewery_id, beer.id]
        avg_beers_stars.append(beer_detail)

    # Get the avg_beer key to use it for sorting the avg_beers_stars list
    def getKey(item):
        return item[3]
    # Get the 5 top rated beers
    top_beers=sorted(avg_beers_stars, key=getKey, reverse=True)[:5]

    return render_template('beerStyle.html', top_beers=top_beers, beers=beers, style=style, num_ratings=num_ratings, avg_stars=avg_stars, countries=countries, regions=regions, breweries=breweries)


# Show the home page with all the countries, selections by styles and regions
@app.route('/')
@app.route('/country/')
def mainPage():
    countries = session.query(Country).order_by(asc(Country.name)).all()
    regions = session.query(Region).order_by(asc(Region.name)).all()
    styles = session.query(Beer.style).group_by(Beer.style).order_by(asc(Beer.style)).all()
    return render_template('home.html', countries=countries, regions=regions, styles=styles)


# Show all the region of a country
@app.route('/country/<int:country_id>/')
@app.route('/country/<int:country_id>/region/')
def showRegion(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    regions = session.query(Region).filter_by(country_id=country_id).all()
    return render_template('region.html', country=country, regions=regions)


# Show all the breweries of a region/state
@app.route('/country/<int:country_id>/region/<int:region_id>/')
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery')
def showBrewery(country_id, region_id):
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    breweries = session.query(Brewery).filter_by(region_id=region_id).all()
    return render_template('brewery.html', country=country, region=region, breweries=breweries)


# Create a new brewery
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/new/', methods=['GET', 'POST'])
def newBrewery(country_id, region_id):
    user_id = login_session['user_id']
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()

    if 'username' not in login_session:
        flash('You need to be logged in to add a new brewery')
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['file']
        # check if the image has allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = UPLOAD_FOLDER + "/" + filename
        else:
            image = UPLOAD_FOLDER + "/" + "not_available.jpg"

        newBrewery = Brewery(image=image, name=request.form['name'], country_id=country_id, region_id=region_id, user_id=user_id)
        session.add(newBrewery)
        session.commit()
        flash('New Brewery %s Successfully Created' % (newBrewery.name))
        return redirect(url_for('showBrewery', country_id=country_id, region_id=region_id, user_id=user_id))
    else:
        return render_template('newBrewery.html', country=country, region=region)

# Edit a brewery
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/edit', methods=['GET', 'POST'])
def editBrewery(country_id, region_id, brewery_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    breweryToEdit = session.query(Brewery).filter_by(id=brewery_id).one()
    if login_session['user_id'] != breweryToEdit.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this brewery.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            breweryToEdit.name = request.form['name']
        session.add(breweryToEdit)
        session.commit()
        flash('Brewery Successfully Edited')
        return redirect(url_for('showBrewery', country_id=country_id, region_id=region_id))
    else:
        return render_template('editBrewery.html', country=country, region=region, brewery=breweryToEdit)

# Delete a brewery
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/delete', methods=['GET', 'POST'])
def deleteBrewery(country_id, region_id, brewery_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    breweryToDelete = session.query(Brewery).filter_by(id=brewery_id).one()
    if login_session['user_id'] != breweryToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this brewery.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(breweryToDelete)
        session.commit()
        flash('Brewery Successfully Deleted')
        return redirect(url_for('showBrewery', country_id=country_id, region_id=region_id))
    else:
        return render_template('deleteBrewery.html', country=country, region=region, brewery=breweryToDelete)


# Show all the beers for a brewery
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/')
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer')
def showBeer(country_id, region_id, brewery_id):
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    brewery_creator = getUserInfo(brewery.user_id)
    beers = session.query(Beer).filter_by(brewery_id=brewery_id).all()
    print brewery_creator.picture

    if beers:
        beer_creator = []
        num_ratings = []
        avg_stars = []
        for beer in beers:
            creator = getUserInfo(beer.user_id).name
            ratings = session.query(Rating.num_of_stars).filter_by(beer_id=beer.id).count()
            stars = session.query(func.avg(Rating.num_of_stars)).filter_by(beer_id=beer.id).all()[0][0]
            num_ratings.append(ratings)
            if stars == None:
                stars = 0
            avg_stars.append(stars)
            beer_creator.append(creator)
        return render_template('beer.html', country=country, region=region, brewery=brewery, beers=beers, brewery_creator=brewery_creator, beer_creator=beer_creator, num_ratings=num_ratings, avg_stars=avg_stars)
    else:
        return render_template('beer.html', country=country, region=region, brewery=brewery, beers="", brewery_creator=brewery_creator, beer_creator="")


# Create a new beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/new/', methods=['GET', 'POST'])
def newBeer(country_id, region_id, brewery_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    if request.method == 'POST':

        file = request.files['file']
        # check if the image has allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = UPLOAD_FOLDER + "/" + filename
        else:
            image = UPLOAD_FOLDER + "/" + "not_available.jpg"
            print image

        user_id = login_session['user_id']
        newBeer = Beer(image=image, name=request.form['name'], style=request.form['style'], abv=request.form['abv'], ibu=request.form['ibu'], description=request.form['description'], country_id=country_id, region_id=region_id, brewery_id=brewery_id, user_id=user_id)
        session.add(newBeer)
        session.commit()
        flash('New Beer %s Successfully Created' % (newBeer.name))
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('newBeer.html', country=country, region=region, brewery=brewery)

# Edit a beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/<int:beer_id>/edit', methods=['GET', 'POST'])
def editBeer(country_id, region_id, brewery_id, beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    beerToEdit = session.query(Beer).filter_by(id=beer_id).one()
    if login_session['user_id'] != beerToEdit.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this beer.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            beerToEdit.name = request.form['name']
        if request.form['style']:
            beerToEdit.style = request.form['style']
        if request.form['abv']:
            beerToEdit.abv = request.form['abv']
        if request.form['ibu']:
            beerToEdit.ibu = request.form['ibu']
        if request.form['description']:
            beerToEdit.description = request.form['description']
        session.add(beerToEdit)
        session.commit()
        flash('Beer Successfully Edited')
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('editBeer.html', country=country, region=region, brewery=brewery, beer=beerToEdit)

# Delete a beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/<int:beer_id>/delete', methods=['GET', 'POST'])
def deleteBeer(country_id, region_id, brewery_id, beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    beerToDelete = session.query(Beer).filter_by(id=beer_id).one()
    if login_session['user_id'] != beerToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this beer.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(beerToDelete)
        session.commit()
        flash('Beer Successfully Deleted')
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('deleteBeer.html', country=country, region=region, brewery=brewery, beer=beerToDelete)

# Show the details of a beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/<int:beer_id>/')
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/<int:beer_id>/details', methods=['GET', 'POST'])
def beerDetails(country_id, region_id, brewery_id, beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    beer = session.query(Beer).filter_by(id=beer_id).one()
    rating = session.query(Rating).filter_by(beer_id=beer_id).all()

    beer_creator = getUserInfo(beer.user_id)
    if rating:
        rated_by = session.query(Rating.user_id).filter_by(beer_id=beer_id).all()[0][0]
    else:
        rated_by = None
    if request.method == 'POST':
        user_id = login_session['user_id']
        if user_id != rated_by:
            newRating = Rating(num_of_stars=request.form['input-2'], beer_id=beer_id, user_id=user_id)
            session.add(newRating)
            session.commit()
            flash('Thank you for your rating')
            return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
        else:
            flash('Rating canceled! You already previously rate this beer')
    return render_template('beerDetails.html', country=country, region=region, brewery=brewery, beer=beer, beer_creator=beer_creator)














if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)