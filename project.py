from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Country, Region, Brewery, Beer
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
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


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
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
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
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
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


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
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

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

# DISCONNECT - Revoke a current user's token and reset their login_session


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


# Show all the country
@app.route('/')
@app.route('/country/')
def showCountry():
    countries = session.query(Country).order_by(asc(Country.name)).all()
    return render_template('country.html', countries=countries)


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
    if 'username' not in login_session:
        return redirect('/login')
    user_id = login_session['user_id']
    region = session.query(Region).filter_by(id=region_id).one()
    if request.method == 'POST':
        newBrewery = Brewery(name=request.form['name'], country_id=country_id, region_id=region_id, user_id=user_id)
        session.add(newBrewery)
        session.commit()
        flash('New Brewery %s Successfully Created' % (newBrewery.name))
        return redirect(url_for('showBrewery', country_id=country_id, region_id=region_id, user_id=user_id))
    else:
        return render_template('newBrewery.html', country_id=country_id, region_id=region_id)

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
        return redirect(url_for('showBrewery', country_id=country, region_id=region))
    else:
        return render_template('editBrewery.html', country_id=country, region_id=region, brewery=breweryToEdit)

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
    print brewery.id
    print brewery.name
    if beers:
        for beer in beers:
            beer_creator = getUserInfo(beer.user_id)
        return render_template('beer.html', country=country, region=region, brewery=brewery, beers=beers, brewery_creator=brewery_creator, beer_creator=beer_creator)
    else:
        return render_template('beer.html', country=country, region=region, brewery=brewery, brewery_creator=brewery_creator, beer_creator="")


# Create a new beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/new/', methods=['GET', 'POST'])
def newBeer(country_id, region_id, brewery_id):
    if 'username' not in login_session:
        return redirect('/login')
    # region = session.query(Region).filter_by(id=region_id).one()
    # brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    if request.method == 'POST':
        user_id = login_session['user_id']
        newBeer = Beer(name=request.form['name'], style=request.form['style'], abv=request.form['abv'], ibu=request.form['ibu'], country_id=country_id, region_id=region_id, brewery_id=brewery_id, user_id=user_id)
        session.add(newBeer)
        session.commit()
        flash('New Beer %s Successfully Created' % (newBeer.name))
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('newBeer.html', country_id=country_id, region_id=region_id, brewery_id=brewery_id)

# Edit a beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/beer/<int:beer_id>/edit', methods=['GET', 'POST'])
def editBeer(country_id, region_id, brewery_id, beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    beerToEdit = session.query(Beer).filter_by(id=beer_id).one()
    if login_session['user_id'] != beerToEdit.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this beer.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            beerToEdit.name = request.form['name']
        session.add(beerToEdit)
        session.commit()
        flash('Beer Successfully Edited')
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('editBeer.html', country_id=country_id, region_id=region_id, brewery_id=brewery_id, beer=beerToEdit)

# Delete a beer
@app.route('/country/<int:country_id>/region/<int:region_id>/brewery/<int:brewery_id>/<beer>/<int:beer_id>/delete', methods=['GET', 'POST'])
def deleteBeer(country_id, region_id, brewery_id, beer_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=country_id).one()
    region = session.query(Region).filter_by(id=region_id).one()
    brewery = session.query(Brewery).filter_by(id=brewery_id).one()
    beerToDelete = session.query(Brewery).filter_by(id=beer_id).one()
    if login_session['user_id'] != breweryToEdit.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this beer.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(beerToDelete)
        session.commit()
        flash('Beer Successfully Deleted')
        return redirect(url_for('showBeer', country_id=country_id, region_id=region_id, brewery_id=brewery_id))
    else:
        return render_template('deleteBeer.html', country=country, region=region, brewery=brewery, beer=beerToDelete)


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
        return redirect(url_for('showCountry'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCountry'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)