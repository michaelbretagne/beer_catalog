from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Country, Region, Brewery, Beer, Rating

engine = create_engine('sqlite:///beercatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Michael", email="michael.bretagne@gmail.com")
session.add(User1)
session.commit()

# Create Countries
countries=[{"id":"1", "name":"United States Of America"}]

for country in countries:
       newCountry= Country(id=country["id"], name=country["name"])
       session.add(newCountry)
       session.commit()

# Create states/regions
regions=[{"country_id":"1", "id":"1", "name":"Alabama"},
         {"country_id":"1", "id":"2", "name":"Alaska"},
         {"country_id":"1", "id":"3", "name":"Arizona"},
         {"country_id":"1", "id":"4", "name":"Arkansas"},
         {"country_id":"1", "id":"5", "name":"California"},
         {"country_id":"1", "id":"6", "name":"Colorado"},
         {"country_id":"1", "id":"7", "name":"Connecticut"},
         {"country_id":"1", "id":"8", "name":"Delaware"},
         {"country_id":"1", "id":"9", "name":"Florida"},
         {"country_id":"1", "id":"10", "name":"Georgia"},
         {"country_id":"1", "id":"11", "name":"Hawaii"},
         {"country_id":"1", "id":"12", "name":"Idaho"},
         {"country_id":"1", "id":"13", "name":"Illinois"},
         {"country_id":"1", "id":"14", "name":"Indiana"},
         {"country_id":"1", "id":"15", "name":"Iowa"},
         {"country_id":"1", "id":"16", "name":"Kansas"},
         {"country_id":"1", "id":"17", "name":"Kentucky"},
         {"country_id":"1", "id":"18", "name":"Louisiana"},
         {"country_id":"1", "id":"19", "name":"Maine"},
         {"country_id":"1", "id":"20", "name":"Maryland"},
         {"country_id":"1", "id":"21", "name":"Massachusetts"},
         {"country_id":"1", "id":"22", "name":"Michigan"},
         {"country_id":"1", "id":"23", "name":"Minnesota"},
         {"country_id":"1", "id":"24", "name":"Mississippi"},
         {"country_id":"1", "id":"25", "name":"Missouri"},
         {"country_id":"1", "id":"26", "name":"Montana"},
         {"country_id":"1", "id":"27", "name":"Nebraska"},
         {"country_id":"1", "id":"28", "name":"Nevada"},
         {"country_id":"1", "id":"29", "name":"New Hampshire"},
         {"country_id":"1", "id":"30", "name":"New Jersey"},
         {"country_id":"1", "id":"31", "name":"New Mexico"},
         {"country_id":"1", "id":"32", "name":"New York"},
         {"country_id":"1", "id":"33", "name":"North Carolina"},
         {"country_id":"1", "id":"34", "name":"North Dakota"},
         {"country_id":"1", "id":"35", "name":"Ohio"},
         {"country_id":"1", "id":"36", "name":"Oklahoma"},
         {"country_id":"1", "id":"37", "name":"Oregon"},
         {"country_id":"1", "id":"38", "name":"Pennsylvania"},
         {"country_id":"1", "id":"39", "name":"Rhode Island"},
         {"country_id":"1", "id":"40", "name":"South Carolina"},
         {"country_id":"1", "id":"41", "name":"South Dakota"},
         {"country_id":"1", "id":"42", "name":"Tennessee"},
         {"country_id":"1", "id":"43", "name":"Texas"},
         {"country_id":"1", "id":"44", "name":"Utah"},
         {"country_id":"1", "id":"45", "name":"Vermont"},
         {"country_id":"1", "id":"46", "name":"Virginia"},
         {"country_id":"1", "id":"47", "name":"Washington"},
         {"country_id":"1", "id":"48", "name":"West Virginia"},
         {"country_id":"1", "id":"49", "name":"Wisconsin"},
         {"country_id":"1", "id":"50", "name":"Wyoming"}]

for region in regions:
       newRegion = Region(name=region['name'],country_id=region['country_id'])
       session.add(newRegion)
       session.commit()

# Create breweries
breweries=[{"country_id":"1", "region_id":"1", "user_id":"1", "name":"Good People Brewing Company"},
           {"country_id":"1", "region_id":"2", "user_id":"1", "name":"Alaskan Brewing Co."},
           {"country_id":"1", "region_id":"3", "user_id":"1", "name":"Four Peaks Brewing Company"},
           {"country_id":"1", "region_id":"4", "user_id":"1", "name":"Diamond Bear Brewing Company"},
           {"country_id":"1", "region_id":"5", "user_id":"1", "name":"Russian River Brewing Company"},
           {"country_id":"1", "region_id":"6", "user_id":"1", "name":"New Belgium Brewing"},
           {"country_id":"1", "region_id":"7", "user_id":"1", "name":"New England Brewing Co."},
           {"country_id":"1", "region_id":"8", "user_id":"1", "name":"Dogfish Head Craft Brewery"},
           {"country_id":"1", "region_id":"9", "user_id":"1", "name":"Funky Buddha Brewery"},
           {"country_id":"1", "region_id":"10", "user_id":"1", "name":"Creature Comforts"},
           {"country_id":"1", "region_id":"11", "user_id":"1", "name":"Maui Brewing Co."},
           {"country_id":"1", "region_id":"12", "user_id":"1", "name":"Grand Teton Brewing Company"},
           {"country_id":"1", "region_id":"13", "user_id":"1", "name":"Lagunitas Brewing Company"},
           {"country_id":"1", "region_id":"14", "user_id":"1", "name":"3 Floyds Brewing Co"},
           {"country_id":"1", "region_id":"15", "user_id":"1", "name":"Toppling Goliath Brewing Company"},
           {"country_id":"1", "region_id":"16", "user_id":"1", "name":"Tallgrass Brewing Company"},
           {"country_id":"1", "region_id":"17", "user_id":"1", "name":"Against The Grain Brewery & Smokehouse"},
           {"country_id":"1", "region_id":"18", "user_id":"1", "name":"Parish Brewing Company"},
           {"country_id":"1", "region_id":"19", "user_id":"1", "name":"Maine Beer Company"},
           {"country_id":"1", "region_id":"20", "user_id":"1", "name":"Stillwater Artisanal Ales"},
           {"country_id":"1", "region_id":"21", "user_id":"1", "name":"Tree House Brewing Company"},
           {"country_id":"1", "region_id":"22", "user_id":"1", "name":"Founders Brewing Company"},
           {"country_id":"1", "region_id":"23", "user_id":"1", "name":"Surly Brewing Company"},
           {"country_id":"1", "region_id":"24", "user_id":"1", "name":"Southern Prohibition Brewing"},
           {"country_id":"1", "region_id":"25", "user_id":"1", "name":"Boulevard Brewing Co."},
           {"country_id":"1", "region_id":"26", "user_id":"1", "name":"Big Sky Brewing Company"},
           {"country_id":"1", "region_id":"27", "user_id":"1", "name":"Nebraska Brewing Company"},
           {"country_id":"1", "region_id":"28", "user_id":"1", "name":"Big Dog's Draft House"},
           {"country_id":"1", "region_id":"29", "user_id":"1", "name":"Smuttynose Brewing Company"},
           {"country_id":"1", "region_id":"30", "user_id":"1", "name":"Kane Brewing Company"},
           {"country_id":"1", "region_id":"31", "user_id":"1", "name":"La Cumbre Brewing Co."},
           {"country_id":"1", "region_id":"32", "user_id":"1", "name":"Other Half Brewing Co."},
           {"country_id":"1", "region_id":"33", "user_id":"1", "name":"Wicked Weed Brewing"},
           {"country_id":"1", "region_id":"34", "user_id":"1", "name":"Fargo Brewing Company"},
           {"country_id":"1", "region_id":"35", "user_id":"1", "name":"Fat Head's Brewery & Saloon"},
           {"country_id":"1", "region_id":"36", "user_id":"1", "name":"Prairie Artisan Ales"},
           {"country_id":"1", "region_id":"37", "user_id":"1", "name":"Deschutes Brewery"},
           {"country_id":"1", "region_id":"38", "user_id":"1", "name":"Troegs Brewing Company"},
           {"country_id":"1", "region_id":"39", "user_id":"1", "name":"Proclamation Ale Company"},
           {"country_id":"1", "region_id":"40", "user_id":"1", "name":"Westbrook Brewing Co."},
           {"country_id":"1", "region_id":"41", "user_id":"1", "name":"Crow Peak Brewing"},
           {"country_id":"1", "region_id":"42", "user_id":"1", "name":"Blackberry Farm Brewery"},
           {"country_id":"1", "region_id":"43", "user_id":"1", "name":"Jester King Brewery"},
           {"country_id":"1", "region_id":"44", "user_id":"1", "name":"Uinta Brewing Company"},
           {"country_id":"1", "region_id":"45", "user_id":"1", "name":"The Alchemist"},
           {"country_id":"1", "region_id":"46", "user_id":"1", "name":"Aslin Beer Company"},
           {"country_id":"1", "region_id":"47", "user_id":"1", "name":"Fremont Brewing Company"},
           {"country_id":"1", "region_id":"48", "user_id":"1", "name":"Bridge Brew Works LLC"},
           {"country_id":"1", "region_id":"49", "user_id":"1", "name":"New Glarus Brewing Company"},
           {"country_id":"1", "region_id":"50", "user_id":"1", "name":"Snake River Brewing Company & Brewpub  "}]
           # {"country_id":"1", "region_id":"1", "user_id":"1", "name":""},

for brewery in breweries:
       newBrewery = Brewery(name=brewery['name'], country_id=brewery['country_id'], region_id=brewery["region_id"], user_id=brewery["user_id"])
       session.add(newBrewery)
       session.commit()

# Create breweries
beers=[{"country_id":"1", "region_id":"1", "brewery_id":"1", "user_id":"1", "image":"static/uploads/snake-handler.jpg", "name":"Snake Handler Double IPA", "style":"American Double - Imperial IPA", "abv":"10.00", "ibu":"103", "description":"Dangerously drinkable, this Double IPA brew is a spirited celebration of all things hoppy. Aromas of pine, citrus, flowers, spice, pineapple, and grassiness complement a biscuit and caramel backbone. Hands down, our most requested beer."},
       {"country_id":"1", "region_id":"2", "brewery_id":"2", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Alaskan Smoked Porter", "style":"American Porter", "abv":"6.50", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"3", "brewery_id":"3", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Hop Knot", "style":"American IPA", "abv":"6.70", "ibu":"47", "description":"None"},
       {"country_id":"1", "region_id":"4", "brewery_id":"4", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Paradise Porter", "style":"American Porter", "abv":"6.24", "ibu":"38", "description":"None"},
       {"country_id":"1", "region_id":"5", "brewery_id":"5", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Supplication", "style":"American Wild Ale", "abv":"7.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"6", "brewery_id":"6", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Lips Of Faith - La Folie", "style":"Flanders Oud Bruin", "abv":"7.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"7", "brewery_id":"7", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Fuzzy Baby Ducks IPA", "style":"American IPA", "abv":"6.20", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"8", "brewery_id":"8", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"60 Minute IPA", "style":"American IPA", "abv":"6.00", "ibu":"60", "description":"None"},
       {"country_id":"1", "region_id":"9", "brewery_id":"9", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Last Snow", "style":"American Porter", "abv":"6.40", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"10", "brewery_id":"10", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Tropicalia", "style":"American IPA", "abv":"6.50", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"11", "brewery_id":"11", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Coconut Hiwa Porter", "style":"American Porter", "abv":"6.00", "ibu":"30", "description":"None"},
       {"country_id":"1", "region_id":"12", "brewery_id":"12", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Pursuit Of Hoppiness", "style":"American Amber - Red Ale", "abv":"8.50", "ibu":"100", "description":"None"},
       {"country_id":"1", "region_id":"13", "brewery_id":"13", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Born Yesterday Pale Ale", "style":"American Pale Ale", "abv":"", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"14", "brewery_id":"14", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Zombie Dust", "style":"American Pale Ale", "abv":"6.20", "ibu":"60", "description":"None"},
       {"country_id":"1", "region_id":"15", "brewery_id":"15", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"PseudoSue", "style":"American Pale Ale", "abv":"5.80", "ibu":"50", "description":"None"},
       {"country_id":"1", "region_id":"16", "brewery_id":"16", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Tallgrass Vanilla Bean Buffalo Sweat", "style":"Milk - Sweet Stout", "abv":"5.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"17", "brewery_id":"17", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Citra Ass Down!", "style":"American Double - Imperial IPA", "abv":"8.20", "ibu":"68", "description":"None"},
       {"country_id":"1", "region_id":"18", "brewery_id":"18", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Ghost In The Machine", "style":"American Double - Imperial IPA", "abv":"8.00", "ibu":"100", "description":"None"},
       {"country_id":"1", "region_id":"19", "brewery_id":"19", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"MO", "style":"American Pale Ale", "abv":"6.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"20", "brewery_id":"20", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Westbrook Gose Gone Wild", "style":"Gose", "abv":"4.60", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"21", "brewery_id":"21", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Julius", "style":"American IPA", "abv":"6.80", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"22", "brewery_id":"22", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Founders Breakfast Stout", "style":"American Double - Imperial Stout", "abv":"8.30", "ibu":"60", "description":"None"},
       {"country_id":"1", "region_id":"23", "brewery_id":"23", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Furious", "style":"American IPA", "abv":"6.60", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"24", "brewery_id":"24", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Crowd Control", "style":"American IPA", "abv":"8.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"25", "brewery_id":"25", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Saison-Brett", "style":"Saison - Farmhouse Ale", "abv":"8.50", "ibu":"38", "description":"None"},
       {"country_id":"1", "region_id":"26", "brewery_id":"26", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Ivan The Terrible Imperial Stout - Barrel-Aged", "style":"Russian Imperial Stout", "abv":"10.00", "ibu":"65", "description":"None"},
       {"country_id":"1", "region_id":"27", "brewery_id":"27", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Melange A Trois", "style":"Belgian Strong Pale Ale", "abv":"11.30", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"28", "brewery_id":"28", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Dirty Dog IPA", "style":"American IPA", "abv":"7.10", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"29", "brewery_id":"29", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Smuttynose Baltic Porter", "style":"Baltic Porter", "abv":"9.24", "ibu":"35", "description":"None"},
       {"country_id":"1", "region_id":"30", "brewery_id":"30", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"HopLab: Citra", "style":"American Pale Ale", "abv":"5.20", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"31", "brewery_id":"31", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Elevated IPA", "style":"American IPA", "abv":"7.20", "ibu":"100", "description":"None"},
       {"country_id":"1", "region_id":"32", "brewery_id":"32", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"All Green Everything", "style":"American Double - Imperial IPA", "abv":"10.50", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"33", "brewery_id":"33", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Freak Of Nature DIPA", "style":"American Double - Imperial IPA", "abv":"8.50", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"34", "brewery_id":"34", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Iron Horse", "style":"American Pale Ale", "abv":"4.80", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"35", "brewery_id":"35", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Fat Head's Head Hunter IPA", "style":"American IPA", "abv":"7.50", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"36", "brewery_id":"36", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"BOMB!", "style":"American Double - Imperial Stout", "abv":"13.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"37", "brewery_id":"37", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"The Abyss", "style":"American Double - Imperial Stout", "abv":"12.20", "ibu":"65", "description":"None"},
       {"country_id":"1", "region_id":"38", "brewery_id":"38", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Troegs Nugget Nectar", "style":"American Amber - Red Ale", "abv":"7.50", "ibu":"93", "description":"None"},
       {"country_id":"1", "region_id":"39", "brewery_id":"39", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Derivative: Galaxy", "style":"American Pale Ale", "abv":"6.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"40", "brewery_id":"40", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Mexican Cake", "style":"American Double - Imperial Stout", "abv":"10.50", "ibu":"50", "description":"None"},
       {"country_id":"1", "region_id":"41", "brewery_id":"41", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Pile O' Dirt Porter", "style":"American Porter", "abv":"6.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"42", "brewery_id":"42", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Classic Saison", "style":"Saison - Farmhouse Ale", "abv":"6.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"43", "brewery_id":"43", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Atrial Rubicite", "style":"American Wild Ale", "abv":"5.80", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"44", "brewery_id":"44", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Hop Nosh IPA", "style":"American IPA", "abv":"7.00", "ibu":"82", "description":"None"},
       {"country_id":"1", "region_id":"45", "brewery_id":"45", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Heady Topper", "style":"American Double - Imperial IPA", "abv":"8.00", "ibu":"75", "description":"None"},
       {"country_id":"1", "region_id":"46", "brewery_id":"46", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Master Of Karate", "style":"American Double - Imperial IPA", "abv":"8.40", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"47", "brewery_id":"47", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Bourbon Abominable Winter Ale", "style":"American Strong Ale", "abv":"14.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"48", "brewery_id":"48", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Peregrine Porter", "style":"Baltic Porter", "abv":"7.20", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"49", "brewery_id":"49", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Wisconsin Belgian Red", "style":"Fruit - Vegetable Beer", "abv":"4.00", "ibu":"", "description":"None"},
       {"country_id":"1", "region_id":"50", "brewery_id":"50", "user_id":"1", "image":"static/uploads/not_available.jpg", "name":"Zonker Stout", "style":"Foreign - Export Stout", "abv":"6.00", "ibu":"", "description":"None"}]

for beer in beers:
       newBeer = Beer(image=beer['image'], name=beer['name'], style=beer['style'], abv=beer['abv'], ibu=beer['ibu'], description=beer['description'], country_id=beer['country_id'], region_id=beer["region_id"], brewery_id=beer["brewery_id"], user_id=beer["user_id"])
       session.add(newBeer)
       session.commit()

# Create Ratings for beers
ratings=[{"id":"1", "num_of_stars":"5", "user_id":"1", "beer_id":"1"},
         {"id":"2", "num_of_stars":"3", "user_id":"1", "beer_id":"1"}]

for rating in ratings:
       newRating= Rating(id=rating["id"], num_of_stars=rating["num_of_stars"], user_id=rating["user_id"], beer_id=rating["beer_id"])
       session.add(newRating)
       session.commit()

print "added countries, regions/states and breweries"
