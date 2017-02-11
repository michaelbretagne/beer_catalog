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
User1 = User(name="Jerry Woods", email="jerry.woods31@example.com",
             picture="/static/img/user_1.jpg")
session.add(User1)
session.commit()

# Create Countries
countries = [{"id": "1", "name": "United States Of America"}]

for country in countries:
    newCountry = Country(id=country["id"], name=country["name"])
    session.add(newCountry)
    session.commit()

# Create states/regions
regions = [{"country_id": "1", "id": "1", "name": "Alabama"},
           {"country_id": "1", "id": "2", "name": "Alaska"},
           {"country_id": "1", "id": "3", "name": "Arizona"},
           {"country_id": "1", "id": "4", "name": "Arkansas"},
           {"country_id": "1", "id": "5", "name": "California"},
           {"country_id": "1", "id": "6", "name": "Colorado"},
           {"country_id": "1", "id": "7", "name": "Connecticut"},
           {"country_id": "1", "id": "8", "name": "Delaware"},
           {"country_id": "1", "id": "9", "name": "Florida"},
           {"country_id": "1", "id": "10", "name": "Georgia"},
           {"country_id": "1", "id": "11", "name": "Hawaii"},
           {"country_id": "1", "id": "12", "name": "Idaho"},
           {"country_id": "1", "id": "13", "name": "Illinois"},
           {"country_id": "1", "id": "14", "name": "Indiana"},
           {"country_id": "1", "id": "15", "name": "Iowa"},
           {"country_id": "1", "id": "16", "name": "Kansas"},
           {"country_id": "1", "id": "17", "name": "Kentucky"},
           {"country_id": "1", "id": "18", "name": "Louisiana"},
           {"country_id": "1", "id": "19", "name": "Maine"},
           {"country_id": "1", "id": "20", "name": "Maryland"},
           {"country_id": "1", "id": "21", "name": "Massachusetts"},
           {"country_id": "1", "id": "22", "name": "Michigan"},
           {"country_id": "1", "id": "23", "name": "Minnesota"},
           {"country_id": "1", "id": "24", "name": "Mississippi"},
           {"country_id": "1", "id": "25", "name": "Missouri"},
           {"country_id": "1", "id": "26", "name": "Montana"},
           {"country_id": "1", "id": "27", "name": "Nebraska"},
           {"country_id": "1", "id": "28", "name": "Nevada"},
           {"country_id": "1", "id": "29", "name": "New Hampshire"},
           {"country_id": "1", "id": "30", "name": "New Jersey"},
           {"country_id": "1", "id": "31", "name": "New Mexico"},
           {"country_id": "1", "id": "32", "name": "New York"},
           {"country_id": "1", "id": "33", "name": "North Carolina"},
           {"country_id": "1", "id": "34", "name": "North Dakota"},
           {"country_id": "1", "id": "35", "name": "Ohio"},
           {"country_id": "1", "id": "36", "name": "Oklahoma"},
           {"country_id": "1", "id": "37", "name": "Oregon"},
           {"country_id": "1", "id": "38", "name": "Pennsylvania"},
           {"country_id": "1", "id": "39", "name": "Rhode Island"},
           {"country_id": "1", "id": "40", "name": "South Carolina"},
           {"country_id": "1", "id": "41", "name": "South Dakota"},
           {"country_id": "1", "id": "42", "name": "Tennessee"},
           {"country_id": "1", "id": "43", "name": "Texas"},
           {"country_id": "1", "id": "44", "name": "Utah"},
           {"country_id": "1", "id": "45", "name": "Vermont"},
           {"country_id": "1", "id": "46", "name": "Virginia"},
           {"country_id": "1", "id": "47", "name": "Washington"},
           {"country_id": "1", "id": "48", "name": "West Virginia"},
           {"country_id": "1", "id": "49", "name": "Wisconsin"},
           {"country_id": "1", "id": "50", "name": "Wyoming"}]

for region in regions:
    newRegion = Region(name=region['name'], country_id=region['country_id'])
    session.add(newRegion)
    session.commit()

# For this project I copied all the breweries and beers information/images on the website https://untappd.com/beer/top_rated
# The website I created has no commercial purpose.

# Create breweries
breweries = [{"country_id": "1", "region_id": "1", "user_id": "1",
              "name": "Good People Brewing Company",
              "image": "static/img/brewery_images/1.jpeg"},

             {"country_id": "1", "region_id": "2", "user_id": "1",
              "name": "Alaskan Brewing Co.",
              "image": "static/img/brewery_images/2.jpeg"},

             {"country_id": "1", "region_id": "3", "user_id": "1",
              "name": "Four Peaks Brewing Company",
              "image": "static/img/brewery_images/3.jpeg"},

             {"country_id": "1", "region_id": "4", "user_id": "1",
              "name": "Diamond Bear Brewing Company",
              "image": "static/img/brewery_images/4.jpeg"},

             {"country_id": "1", "region_id": "5", "user_id": "1",
              "name": "Russian River Brewing Company",
              "image": "static/img/brewery_images/5.jpg"},

             {"country_id": "1", "region_id": "6", "user_id": "1",
              "name": "New Belgium Brewing",
              "image": "static/img/brewery_images/6.jpeg"},

             {"country_id": "1", "region_id": "7", "user_id": "1",
              "name": "New England Brewing Co.",
              "image": "static/img/brewery_images/7.jpeg"},

             {"country_id": "1", "region_id": "8", "user_id": "1",
              "name": "Dogfish Head Craft Brewery",
              "image": "static/img/brewery_images/8.jpeg"},

             {"country_id": "1", "region_id": "9", "user_id": "1",
              "name": "Funky Buddha Brewery",
              "image": "static/img/brewery_images/9.jpeg"},

             {"country_id": "1", "region_id": "10", "user_id": "1",
              "name": "Creature Comforts",
              "image": "static/img/brewery_images/10.jpeg"},

             {"country_id": "1", "region_id": "11", "user_id": "1",
              "name": "Maui Brewing Co.",
              "image": "static/img/brewery_images/11.jpeg"},

             {"country_id": "1", "region_id": "12", "user_id": "1",
              "name": "Grand Teton Brewing Company",
              "image": "static/img/brewery_images/12.jpeg"},

             {"country_id": "1", "region_id": "13", "user_id": "1",
              "name": "Lagunitas Brewing Company",
              "image": "static/img/brewery_images/13.jpeg"},

             {"country_id": "1", "region_id": "14",
              "user_id": "1", "name": "3 Floyds Brewing Co",
              "image": "static/img/brewery_images/14.jpeg"},

             {"country_id": "1", "region_id": "15",
              "user_id": "1", "name": "Toppling Goliath Brewing Company",
              "image": "static/img/brewery_images/15.jpeg"},

             {"country_id": "1", "region_id": "16",
              "user_id": "1", "name": "Tallgrass Brewing Company",
              "image": "static/img/brewery_images/16.jpeg"},

             {"country_id": "1", "region_id": "17",
              "user_id": "1", "name": "Against The Grain Brewery & Smokehouse",
              "image": "static/img/brewery_images/17.jpeg"},

             {"country_id": "1", "region_id": "18", "user_id": "1",
              "name": "Parish Brewing Company",
              "image": "static/img/brewery_images/18.jpeg"},

             {"country_id": "1", "region_id": "19", "user_id": "1",
              "name": "Maine Beer Company",
              "image": "static/img/brewery_images/19.jpeg"},

             {"country_id": "1", "region_id": "20", "user_id": "1",
              "name": "Stillwater Artisanal Ales",
              "image": "static/img/brewery_images/20.jpeg"},

             {"country_id": "1", "region_id": "21", "user_id": "1",
              "name": "Tree House Brewing Company",
              "image": "static/img/brewery_images/21.jpeg"},

             {"country_id": "1", "region_id": "22", "user_id": "1",
              "name": "Founders Brewing Company",
              "image": "static/img/brewery_images/22.jpeg"},

             {"country_id": "1", "region_id": "23", "user_id": "1",
              "name": "Surly Brewing Company",
              "image": "static/img/brewery_images/23.jpeg"},

             {"country_id": "1", "region_id": "24", "user_id": "1",
              "name": "Southern Prohibition Brewing",
              "image": "static/img/brewery_images/24.jpeg"},

             {"country_id": "1", "region_id": "25", "user_id": "1",
              "name": "Boulevard Brewing Co.",
              "image": "static/img/brewery_images/25.jpeg"},

             {"country_id": "1", "region_id": "26", "user_id": "1",
              "name": "Big Sky Brewing Company",
              "image": "static/img/brewery_images/26.jpeg"},

             {"country_id": "1", "region_id": "27", "user_id": "1",
              "name": "Nebraska Brewing Company",
              "image": "static/img/brewery_images/27.jpeg"},

             {"country_id": "1", "region_id": "28", "user_id": "1",
              "name": "Sierra Nevada Brewing Co.",
              "image": "static/img/brewery_images/28.jpeg"},

             {"country_id": "1", "region_id": "29", "user_id": "1",
              "name": "Smuttynose Brewing Company",
              "image": "static/img/brewery_images/29.jpeg"},

             {"country_id": "1", "region_id": "30", "user_id": "1",
              "name": "Kane Brewing Company",
              "image": "static/img/brewery_images/30.jpeg"},

             {"country_id": "1", "region_id": "31", "user_id": "1",
              "name": "La Cumbre Brewing Co.",
              "image": "static/img/brewery_images/31.jpeg"},

             {"country_id": "1", "region_id": "32", "user_id": "1",
              "name": "Other Half Brewing Co.",
              "image": "static/img/brewery_images/32.jpeg"},

             {"country_id": "1", "region_id": "33", "user_id": "1",
              "name": "Wicked Weed Brewing",
              "image": "static/img/brewery_images/33.jpeg"},

             {"country_id": "1", "region_id": "34", "user_id": "1",
              "name": "Fargo Brewing Company",
              "image": "static/img/brewery_images/34.jpeg"},

             {"country_id": "1", "region_id": "35", "user_id": "1",
              "name": "Fat Head's Brewery & Saloon",
              "image": "static/img/brewery_images/35.jpeg"},

             {"country_id": "1", "region_id": "36", "user_id": "1",
              "name": "Prairie Artisan Ales",
              "image": "static/img/brewery_images/36.jpeg"},

             {"country_id": "1", "region_id": "37", "user_id": "1",
              "name": "Deschutes Brewery",
              "image": "static/img/brewery_images/37.jpeg"},

             {"country_id": "1", "region_id": "38", "user_id": "1",
              "name": "Troegs Brewing Company",
              "image": "static/img/brewery_images/38.jpeg"},

             {"country_id": "1", "region_id": "39", "user_id": "1",
              "name": "Proclamation Ale Company",
              "image": "static/img/brewery_images/39.jpeg"},

             {"country_id": "1", "region_id": "40", "user_id": "1",
              "name": "Westbrook Brewing Co.",
              "image": "static/img/brewery_images/40.jpeg"},

             {"country_id": "1", "region_id": "41", "user_id": "1",
              "name": "Crow Peak Brewing",
              "image": "static/img/brewery_images/41.jpeg"},

             {"country_id": "1", "region_id": "42", "user_id": "1",
              "name": "Blackberry Farm Brewery",
              "image": "static/img/brewery_images/42.jpeg"},

             {"country_id": "1", "region_id": "43", "user_id": "1",
              "name": "Jester King Brewery",
              "image": "static/img/brewery_images/43.jpeg"},

             {"country_id": "1", "region_id": "44", "user_id": "1",
              "name": "Uinta Brewing Company",
              "image": "static/img/brewery_images/44.jpeg"},

             {"country_id": "1", "region_id": "45", "user_id": "1",
              "name": "The Alchemist",
              "image": "static/img/brewery_images/45.jpeg"},

             {"country_id": "1", "region_id": "46", "user_id": "1",
              "name": "The Veil Brewing Co.",
              "image": "static/img/brewery_images/46.jpeg"},

             {"country_id": "1", "region_id": "47", "user_id": "1",
              "name": "Fremont Brewing Company",
              "image": "static/img/brewery_images/47.jpeg"},

             {"country_id": "1", "region_id": "48", "user_id": "1",
              "name": "Bridge Brew Works LLC",
              "image": "static/img/brewery_images/48.jpeg"},

             {"country_id": "1", "region_id": "49", "user_id": "1",
              "name": "New Glarus Brewing Company",
              "image": "static/img/brewery_images/49.jpeg"},

             {"country_id": "1", "region_id": "50", "user_id": "1",
              "name": "Snake River Brewing Company & Brewpub",
              "image": "static/img/brewery_images/50.jpeg"}]


for brewery in breweries:
    newBrewery = Brewery(name=brewery['name'], image=brewery['image'],
                         country_id=brewery['country_id'],
                         region_id=brewery["region_id"],
                         user_id=brewery["user_id"])
    session.add(newBrewery)
    session.commit()

# Create breweries
beers = [{"country_id": "1", "region_id": "1", "brewery_id": "1",
          "user_id": "1", "image": "static/img/beer_images/1.jpeg",
          "name": "Snake Handler Double IPA",
          "style": "American Double - Imperial IPA", "abv": "10.00",
          "ibu": "103", "description": "Dangerously drinkable, this Double "
          "IPA brew is a spirited celebration of all things hoppy. Aromas "
          "of pine, citrus, flowers, spice, pineapple, and grassiness "
          "complement a biscuit and caramel backbone. Hands down, our most "
          "requested beer."},

         {"country_id": "1", "region_id": "2", "brewery_id": "2",
          "user_id": "1", "image": "static/img/beer_images/2.jpeg",
          "name": "Alaskan Smoked Porter", "style": "American Porter",
          "abv": "6.50", "ibu": "45", "description": 'The dark, robust body '
          'and pronounced smoky flavor of this limited edition beer make it '
          'an adventuresome taste experience. Alaskan Smoked Porter is '
          'produced in limited "vintages" each year on November 1 and unlike '
          'most beers, may be aged in the bottle much like fine wine.'},

         {"country_id": "1", "region_id": "3", "brewery_id": "3",
          "user_id": "1", "image": "static/img/beer_images/3.jpeg",
          "name": "Hop Knot", "style": "American IPA", "abv": "6.70",
          "ibu": "47", "description": "Our Hop Knot IPA is made only from "
          "American malt and lots of American hops. Hop Knot IPA get its "
          "peculiar name from the weaving of five different hops added at "
          "seven different times during the brewing process. Including our "
          "cavernous hop-back, which gets so stuffed with whole leaf hops "
          "that we feel genuine guilt for its excess. Hop Knot is an ale "
          "that is to be enjoyed with friends, spicy food or any time you "
          "need a good hop fix without the harsh bitterness. We hope you "
          "enjoy this pioneering beer made in the bold spirit of Americans "
          "everywhere."},

         {"country_id": "1", "region_id": "4", "brewery_id": "4",
          "user_id": "1", "image": "static/img/beer_images/4.jpeg",
          "name": "Paradise Porter", "style": "American Porter", "abv": "4.95",
          "ibu": "38", "description": "This medium bodied porter has notes "
          "of roasted and chocolate malts, making it a perfect balance of "
          "sweet and bitter. Generous hops give this brew a dry finish. "},

         {"country_id": "1", "region_id": "5", "brewery_id": "5",
          "user_id": "1", "image": "static/img/beer_images/5.jpeg",
          "name": "Supplication", "style": "American Wild Ale", "abv":
          "7.00", "ibu": "None", "description": "Brown ale aged in Pinot "
          "Noir wine barrels for one year with sour cherries, Brettanomyces "
          "yeast, and Lactobacillus & Pedicoccus bacteria."},

         {"country_id": "1", "region_id": "6", "brewery_id": "6",
          "user_id": "1", "image": "static/img/beer_images/6.jpeg",
          "name": "Lips Of Faith - La Folie", "style": "Flanders Oud Bruin",
          "abv": "7.00", "ibu": "18", "description": "La Folie Wood-Aged "
          "Biere, is our original wood-conditioned beer, resting in French "
          "Oak barrels between one and three years before being bottled. "
          "Peter Bouckaert, came to us from Rodenbach home of the fabled sour "
          "red. Our La Folie emulates the spontaneous fermentation beers of "
          "Peter s beloved Flanders with sour apple notes, a dry "
          "effervescence, and earthy undertones."},

         {"country_id": "1", "region_id": "7", "brewery_id": "7",
          "user_id": "1", "image": "static/img/beer_images/7.jpeg",
          "name": "Fuzzy Baby Ducks IPA", "style": "American IPA",
          "abv": "6.20", "ibu": "65", "description": "Citra single hop IPA"},

         {"country_id": "1", "region_id": "8", "brewery_id": "8",
          "user_id": "1", "image": "static/img/beer_images/8.jpeg",
          "name": "60 Minute IPA", "style": "American IPA", "abv": "6.00",
          "ibu": "60", "description": "Our flagship beer. A session India "
          "Pale Ale brewed with Warrior, Amarillo & 'Mystery Hop X.' "
          "A powerful East Coast I.P.A. with a lot of citrusy hop character. "
          "THE session beer for beer geeks like us!"},

         {"country_id": "1", "region_id": "9", "brewery_id": "9",
          "user_id": "1", "image": "static/img/beer_images/9.jpeg",
          "name": "Last Snow", "style": "American Porter", "abv": "6.50",
          "ibu": "35", "description": "Last Snow Porter is an ode to that "
          "special time in Florida where the needle dips just south of 75 "
          "- even for the briefest of moments. This rich, creamy porter is "
          "layered with coconut and freshly - roasted coffee for taste that "
          "recalls a winter wonderland - even if, in our state, that's just a "
          "state of mind."},

         {"country_id": "1", "region_id": "10", "brewery_id": "10",
          "user_id": "1", "image": "static/img/beer_images/10.jpeg",
          "name": "Tropicalia", "style": "American IPA", "abv": "6.50",
          "ibu": "65", "description": "Balanced, soft, and juicy. Hopped with "
          "Citra, Centennial, and Galaxy."},

         {"country_id": "1", "region_id": "11", "brewery_id": "11",
          "user_id": "1", "image": "static/img/beer_images/11.jpeg",
          "name": "Coconut Hiwa Porter", "style": "American Porter",
          "abv": "6.00", "ibu": "30", "description": "A robust dark ale with "
          "hand-toasted coconut and hints of mocha"},

         {"country_id": "1", "region_id": "12", "brewery_id": "12",
          "user_id": "1", "image": "static/img/beer_images/12.jpeg",
          "name": "Pursuit Of Hoppiness", "style": "American Amber - Red Ale",
          "abv": "8.50", "ibu": "100", "description": "Pursuit of Hoppiness "
          "Imperial Red Ale is brewed to showcase the brash beauty of "
          "American hops: Chinook, Centennial and Columbus at 100 "
          "International Bitterness Units (IBU). The hops grown in the United "
          "States are considered to be some of the best in the world. "
          "Compared to their more traditionally subdued, elegant European "
          "counterparts, American hops are bold, bright, piney and zesty."},

         {"country_id": "1", "region_id": "13", "brewery_id": "13",
          "user_id": "1", "image": "static/img/beer_images/13.jpeg",
          "name": "Born Yesterday Pale Ale", "style": "American Pale Ale",
          "abv": "7", "ibu": "110", "description": "Born Yesterday is a "
          "newborn verson of our reborn pale, New Dogtown Pale, with a fresh "
          "addition: Virgin hops from the trellised lands of the verdant "
          "Yakima Valley. Unkilned for an immaculate reception. Then deliver "
          "the resulting lil' brew in 24hrs. Congrats. Its a beer!"},

         {"country_id": "1", "region_id": "14", "brewery_id": "14",
          "user_id": "1", "image": "static/img/beer_images/14.jpeg",
          "name": "Zombie Dust", "style": "American Pale Ale", "abv": "6.20",
          "ibu": "50", "description": "This intensely hopped and gushing "
          "undead Pale Ale will be one's only respite after the zombie "
          "apocalypse. Created with our marvelous friends in the comic "
          "industry."},

         {"country_id": "1", "region_id": "15", "brewery_id": "15",
          "user_id": "1", "image": "static/img/beer_images/15.jpeg",
          "name": "PseudoSue", "style": "American Pale Ale", "abv": "5.80",
          "ibu": "50", "description": "This Citra hopped Pale Ale is loaded "
          "with tropical fruit flavors and has bright aromas of passion "
          "fruit, mango, and papaya. If you're seeking a refreshing, hoppy "
          "drink, seek no further."},

         {"country_id": "1", "region_id": "16", "brewery_id": "16",
          "user_id": "1", "image": "static/img/beer_images/16.jpeg",
          "name": "Tallgrass Vanilla Bean Buffalo Sweat",
          "style": "Milk - Sweet Stout", "abv": "5.00", "ibu": "20",
          "description": "Brewed with vanilla beans."},

         {"country_id": "1", "region_id": "17", "brewery_id": "17",
          "user_id": "1", "image": "static/img/beer_images/17.jpeg",
          "name": "Citra Ass Down!",
          "style": "American Double - Imperial IPA", "abv": "8.20",
          "ibu": "68", "description": "This beer is not candy or mother's "
          "milk. It is not brewed by gypsies or aliens, nor does it contain "
          "any zombie dirt. This is an American Style IPA brewed with Citra "
          "Hops. It is citrusy, sticky, hoppy and delicious. Simply drink it "
          "and enjoy it. Don't hoard this beer, Citra Ass Down and drink it "
          "now."},

         {"country_id": "1", "region_id": "18", "brewery_id": "18",
          "user_id": "1", "image": "static/img/beer_images/18.jpeg",
          "name": "Ghost In The Machine",
          "style": "American Double - Imperial IPA", "abv": "8.00",
          "ibu": "100", "description": "Welcome to the future. Our collective "
          "human consciousness, or Ghost in the Machine, has gained a "
          "tolerance for hops beyond what mankind has ever known before."},

         {"country_id": "1", "region_id": "19", "brewery_id": "19",
          "user_id": "1", "image": "static/img/beer_images/19.jpeg",
          "name": "MO", "style": "American Pale Ale", "abv": "6.00", "ibu": "",
          "description": "None"},

         {"country_id": "1", "region_id": "20", "brewery_id": "20",
          "user_id": "1", "image": "static/img/beer_images/20.jpeg",
          "name": "Westbrook Gose Gone Wild", "style": "Gose", "abv": "4.60",
          "ibu": "5", "description": 'This is our interpretation of Gose '
          '(pronounced "goes-uh"), a beer brewed with coriander and salt. '
          'Once nearly extinct, this very refreshing style is making a '
          'comeback.'},

         {"country_id": "1", "region_id": "21", "brewery_id": "21",
          "user_id": "1", "image": "static/img/beer_images/21.jpeg",
          "name": "Julius", "style": "American IPA", "abv": "6.80",
          "ibu": "72", "description": "Bursting with 1.6 oz per gallon of "
          "American hops, Julius is loaded with notes of passionfruit, mango, "
          "and citrus. At 6.8% alcohol, it is refreshing and freakishly "
          "drinkable."},

         {"country_id": "1", "region_id": "22", "brewery_id": "22",
          "user_id": "1", "image": "static/img/beer_images/22.jpeg",
          "name": "Founders Breakfast Stout", "style": "American Double - "
          "Imperial Stout", "abv": "8.30", "ibu": "60", "description": "The "
          "coffee lover's consummate beer. Brewed with an abundance of flaked "
          "oats, bitter and imported chocolates, and Sumatra and Kona coffee, "
          "this stout has an intense fresh-roasted java nose topped with a "
          "frothy, cinnamon-colored head that goes forever."},

         {"country_id": "1", "region_id": "23", "brewery_id": "23",
          "user_id": "1", "image": "static/img/beer_images/23.jpeg",
          "name": "Furious", "style": "American IPA", "abv": "6.60",
          "ibu": "100", "description": "This malt provides the backbone for "
          "the intense hop character. Four American hop varieties are used at "
          "a rate of over three pounds per barrel. The result is a rich malt "
          "sweetness infused with bright hop flavor and aroma from beginning "
          "to end. Oh yeah, it's about 6% alcohol and around 100 IBUs"},

         {"country_id": "1", "region_id": "24", "brewery_id": "24",
          "user_id": "1", "image": "static/img/beer_images/24.jpeg",
          "name": "Devil's Harvest", "style": "American Pale Ale",
          "abv": "5.80", "ibu": "60", "description": "This extra pale ale "
          "uses rich Munich malt to balance out the four hop additions. With "
          "a full mouth feel and bold aroma, Devil's Harvest is a flavorful "
          "hop bomb."},

         {"country_id": "1", "region_id": "25", "brewery_id": "25",
          "user_id": "1", "image": "static/img/beer_images/25.jpeg",
          "name": "Saison-Brett", "style": "Saison - Farmhouse Ale",
          "abv": "8.50", "ibu": "38", "description": "Saison-Brett, based on "
          "our very popular Tank 7, is assertively dry hopped, then bottle "
          "conditioned with various yeasts, including Brettanomyces, a wild "
          "strain that imparts a distinctive earthy quality. Though this "
          "farmhouse ale was given three months of bottle age prior to "
          "release, further cellaring will continue to enhance the 'Brett' "
          "character, if that's what you're after."},

         {"country_id": "1", "region_id": "26", "brewery_id": "26",
          "user_id": "1", "image": "static/img/beer_images/26.jpeg",
          "name": "Ivan The Terrible Imperial Stout - Barrel-Aged",
          "style": "Russian Imperial Stout", "abv": "10.00", "ibu": "65",
          "description": "Big Sky Brewing's Ivan the terrible Imperial Stout "
          "is brewed according to the traditional style using english hops "
          "and the finest american malt. It's aroma and flavor balance well "
          "between esters of dried fruit and roasted cocoa with a slight "
          "bourbon presence."},

         {"country_id": "1", "region_id": "27", "brewery_id": "27",
          "user_id": "1", "image": "static/img/beer_images/27.jpeg",
          "name": "Melange A Trois", "style": "Belgian Strong Pale Ale",
          "abv": "11.30", "ibu": "31", "description": "Melange A Trois begins "
          "with a wonderfully big Strong Belgian-Style Blonde Ale and moves "
          "into the extraordinary category through an additional 6 month "
          "French Oak Chardonnay Wine Barrel maturation. The essense of "
          "Chardonnay permeates while a subtle sweetness remains from the "
          "Ale itself. Oak tannins combine to create a fascinating mesh of "
          "dry, sweet, and wine-like character. GABF Bronze, 2 GABF Gold "
          "Medals (Wood & Barrel Aged Strong Beer) 2011, 2012, 2015 Great "
          "American Beer Festival!"},

         {"country_id": "1", "region_id": "28", "brewery_id": "28",
          "user_id": "1", "image": "static/img/beer_images/28.jpeg",
          "name": "Torpedo Extra IPA", "style": "American IPA", "abv":
          "7.20", "ibu": "65", "description": "Sierra Nevada Torpedo Ale is a "
          "big American IPA, bold, assertive and full of flavor and aromas "
          "highlighting the complex citrus, pine and herbal character of "
          "whole-cone American hops. Our obsession with harnessing huge hop "
          "flavor led to the development of what we call the hop torpedo, a "
          "revolutionary method of dry-hopping designed, built, and debuted "
          "here at the brewery. Our torpedo is a sleek, stainless-steel piece "
          "of hardware that delivers more pure hop aroma than any method of "
          "dry-hopping we've ever seen."},

         {"country_id": "1", "region_id": "29", "brewery_id": "29",
          "user_id": "1", "image": "static/img/beer_images/29.jpeg",
          "name": "Smuttynose Baltic Porter", "style": "Baltic Porter",
          "abv": "9", "ibu": "66", "description": "Indigenous to northern "
          "Europe, Baltic Porters historically stem from the shipping of "
          "British porters to the Russian hinterland. Unlike their British "
          "cousins, Baltic Porters are often brewed with lager yeast, which "
          "is the tradition we follow. Big & bold, with flavors of coffee, "
          "dark fruit & raisins, this black beer is smooth as a chocolate "
          "swirl."},

         {"country_id": "1", "region_id": "30", "brewery_id": "30",
          "user_id": "1", "image": "static/img/beer_images/30.jpeg",
          "name": "Head High", "style": "American IPA", "abv": "6.5",
          "ibu": "80", "description": "This beer is all about the hops, we "
          "use a blend of five different varieties all grown in the Pacific "
          "Northwest. A small charge of Chinook and Columbus early in the "
          "boil adds a smooth bitterness. A majority of the hops are then "
          "added late in the kettle or post-fermentation to produce a beer "
          "that is heavy on hop flavor and aroma. The combination of Cascade, "
          "Centennial, Citra and Columbus give Head High a noticeable "
          "grapefruit flavor with aromas of citrus, tropical fruits and pine. "
          "Our house American ale yeast ferments to a dry finish that "
          "accentuates the use of imported Pilsner and lightly kilned crystal "
          "malt resulting in Head High's straw color and crisp flavor."},

         {"country_id": "1", "region_id": "31", "brewery_id": "31",
          "user_id": "1", "image": "static/img/beer_images/31.jpeg",
          "name": "Elevated IPA", "style": "American IPA", "abv": "7.20",
          "ibu": "100", "description": "None"},

         {"country_id": "1", "region_id": "32", "brewery_id": "32",
          "user_id": "1", "image": "static/img/beer_images/32.jpeg",
          "name": "All Green Everything",
          "style": "American Triple - Imperial IPA", "abv": "10.50",
          "ibu": "120", "description": "A huge, but dry, triple IPA packed "
          "with Motueka, Amarillo, Citra and Mosaic"},

         {"country_id": "1", "region_id": "33", "brewery_id": "33",
          "user_id": "1", "image": "static/img/beer_images/33.jpeg",
          "name": "Freak Of Nature DIPA",
          "style": "American Double - Imperial IPA", "abv": "8.50",
          "ibu": "100", "description": " At 8% abv and who knows how many "
          "ibu's, this beer is our shrine to the Hop. Absurd amounts of the "
          "big West Coast hops gives this beer its citrusy, weedy nose and "
          "big, dank flavor. We dry hop with 48lbs per batch, which is over "
          "3lbs of hops per barrel. In keeping with the classic style of the "
          "West Coast double, sugar plays a large part in creating this dry "
          "and minimally bitter double IPA. The Freak is particularly "
          "pintable for the style, so if you dare to enter, we welcome you to "
          "the Freak Show."},

         {"country_id": "1", "region_id": "34", "brewery_id": "34",
          "user_id": "1", "image": "static/img/beer_images/34.jpeg",
          "name": "Stone's Throw Scottish Ale", "style": "Scottish Ale",
          "abv": "4.50", "ibu": "18", "description": "Sweet caramel and "
          "roasted malts come together in this crisp Scottish style ale. "
          "Nutty ale with slight chocolate and coffee undertones make this "
          "smooth a spectacular weeknight choice."},

         {"country_id": "1", "region_id": "35", "brewery_id": "35",
          "user_id": "1", "image": "static/img/beer_images/35.jpeg",
          "name": "Fat Head's Head Hunter IPA", "style": "American IPA",
          "abv": "7.50", "ibu": "87", "description": "Uncivilized and "
          "aggressive, this west coast style IPA packs wicked hop flavors and "
          "aroma. World Beer Cup Silver 2012. GABF Silver 2010. Bronze 2011. "
          "National IPA Championship IPA winner 2012, 2010."},

         {"country_id": "1", "region_id": "36", "brewery_id": "36",
          "user_id": "1", "image": "static/img/beer_images/36.jpeg",
          "name": "BOMB!", "style": "American Double - Imperial Stout",
          "abv": "13.00", "ibu": "65", "description": "Bomb! is an imperial "
          "stout aged on Nordaggio's espresso beans, chocolate, vanilla "
          "beans, and ancho chile peppers. All the flavors meld to create a "
          "truly unique beer. The peppers add just the right amount of heat "
          "to complement the intense coffee and chocolate flavors."},

         {"country_id": "1", "region_id": "37", "brewery_id": "37",
          "user_id": "1", "image": "static/img/beer_images/37.jpeg",
          "name": "The Abyss", "style": "American Double - Imperial Stout",
          "abv": "11.00", "ibu": "86", "description": "Imperial Stout aged in "
          "Bourbon, Oregon Oak, and Pinot Noir barrels."},

         {"country_id": "1", "region_id": "38", "brewery_id": "38",
          "user_id": "1", "image": "static/img/beer_images/38.jpeg",
          "name": "Nugget Nectar", "style": "American Amber - Red Ale",
          "abv": "7.50", "ibu": "93", "description": "Squeeze those hops for "
          "all they're worth and prepare to pucker up: Nugget Nectar Ale, "
          "will take hopheads to nirvana with a heady collection of Nugget, "
          "Warrior and Tomahawk hops. Starting with the same base ingredients "
          "of our flagship HopBack Amber Ale, Nugget Nectar intensifies the "
          "malt and hop flavors to create an explosive hop experience."},

         {"country_id": "1", "region_id": "39", "brewery_id": "39",
          "user_id": "1", "image": "static/img/beer_images/39.jpeg",
          "name": "Derivative: Galaxy", "style": "Australian Pale Ale",
          "abv": "6.00", "ibu": "", "description": "This beer is a unique "
          "snowflake; a Unicorn on a farm of Shetland ponies; a complete "
          "original that we at Proclamation Ale Company came up with entirely "
          "by ourselves, by our own creative volition, without any outside "
          "inspiration whatever! Wow! Check this out: we got this awesome "
          "idea to take barley, make a sugary tea with it, ferment it with "
          "yeast and then throw a ton of sexy, nouveau hops in it!!"},

         {"country_id": "1", "region_id": "40", "brewery_id": "40",
          "user_id": "1", "image": "static/img/beer_images/40.jpeg",
          "name": "Mexican Cake", "style": "American Double - Imperial Stout",
          "abv": "10.50", "ibu": "50", "description": "First anniversary "
          "imperial stout w/ cocoa nibs, vanilla beans, cinnamon, and "
          "habanero peppers."},

         {"country_id": "1", "region_id": "41", "brewery_id": "41",
          "user_id": "1", "image": "static/img/beer_images/41.jpeg",
          "name": "Pile O' Dirt Porter", "style": "American Porter",
          "abv": "6.00", "ibu": "40", "description": "Medium bodied beer, "
          "malty dominated, roasty flavor reminicent of cocoa."},

         {"country_id": "1", "region_id": "42", "brewery_id": "42",
          "user_id": "1", "image": "static/img/beer_images/42.jpeg",
          "name": "Classic Saison", "style": "Saison - Farmhouse Ale",
          "abv": "6.30", "ibu": "33", "description": "This medium bodied "
          "Saison pours with a voluminous head and releases bright notes of "
          "lemon and a crisp, spicy hop aroma. Finishes clean and dry."},

         {"country_id": "1", "region_id": "43", "brewery_id": "43",
          "user_id": "1", "image": "static/img/beer_images/43.jpeg",
          "name": "Atrial Rubicite", "style": "American Wild Ale",
          "abv": "5.80", "ibu": "", "description": "Atrial Rubicite is made "
          "from well water, barley, wheat, hops, farmhouse, native yeast from "
          "the Texas Hill Country, souring bacteria and raspberries. It's "
          "5.8% alcohol by volume, has a finishing gravity of 1.005 and is "
          "3.36 pH. It is unfiltered, unpasteurized and 100% bottle "
          "conditioned."},

         {"country_id": "1", "region_id": "44", "brewery_id": "44",
          "user_id": "1", "image": "static/img/beer_images/44.jpeg",
          "name": "Hop Nosh IPA", "style": "American IPA", "abv": "7.30",
          "ibu": "82", "description": "Our flagship IPA boasts an assertive "
          "bitterness and vibrant hop aromatics. Expect notes of pine, lime "
          "zest, and grapefruit supported by caramel malts."},

         {"country_id": "1", "region_id": "45", "brewery_id": "45",
          "user_id": "1", "image": "static/img/beer_images/45.jpeg",
          "name": "Heady Topper", "style": "American Double - Imperial IPA",
          "abv": "8.00", "ibu": "100", "description": "This Double IPA is not "
          "intended to be the strongest or most bitter DIPA. It is brewed to "
          "give you wave after wave of hop flavor without any astringent "
          "bitterness. We brew Heady Topper with a proprietary blend of six "
          "hops; each imparting its own unique flavor and aroma. Take a big "
          "sip of Heady and see what hop flavors you can pick out. Orange? "
          "Tropical Fruit? Pink Grapefruit? Pine? Spice? There is just enough "
          "malt to give this beer some backbone, but not enough to take the "
          "hops away from the center stage."},

         {"country_id": "1", "region_id": "46", "brewery_id": "46",
          "user_id": "1", "image": "static/img/beer_images/46.jpeg",
          "name": "Dirt Nap", "style": "American Double - Imperial IPA",
          "abv": "8.80", "ibu": "", "description": "This is the first double "
          "IPA that isn't Crucial Taunt that we've produced. Hopped intensely "
          "with Citra, Moasic, Galaxy, and Nelson. Aroma/flavor profile is "
          "insane on this one. We are extremely pleased with the final result "
          "and we hope you will be also."},

         {"country_id": "1", "region_id": "47", "brewery_id": "47",
          "user_id": "1", "image": "static/img/beer_images/47.jpeg",
          "name": "Bourbon Abominable Winter Ale",
          "style": "American Strong Ale", "abv": "11.00", "ibu": "",
          "description": "Lovingly referred to by Fremonters as the B-BOMB, "
          "this bourbon barrel-aged edition of our winter ale has a warming "
          "spicy aroma and rich carmelly notes of bourbon, wood and vanilla "
          "added to dark roasty chocolatey malt flavors and subtle hopping."},

         {"country_id": "1", "region_id": "48", "brewery_id": "48",
          "user_id": "1", "image": "static/img/beer_images/48.jpeg",
          "name": "Peregrine Porter", "style": "Baltic Porter", "abv": "7.20",
          "ibu": "", "description": "Malty, dark fruit, including figs, "
          "plums, raisins, alcohol warmth & rumminess. 7.0-7.2% Produced by "
          "the batch a few times a year."},

         {"country_id": "1", "region_id": "49", "brewery_id": "49",
          "user_id": "1", "image": "static/img/beer_images/49.jpeg",
          "name": "Wisconsin Belgian Red", "style": "Fruit - Vegetable Beer",
          "abv": "4.00", "ibu": "", "description": 'This beer is brewed with '
          'whole Montmorency Cherries, Wisconsin Farmed Wheat and Belgian '
          'Roasted Barleys, lagered in oak tanks and balanced by Hallertau '
          'hops we aged in our brewery one full year. Over a pound of Door '
          'County Cherries in every bottle makes this beer uniquely '
          '"Wisconsin". Expect this beer to be ruby red, with a medium body '
          'that is highly carbonated and intense with cherry flavor and '
          'bouquet.'},

         {"country_id": "1", "region_id": "50", "brewery_id": "50",
          "user_id": "1", "image": "static/img/beer_images/50.jpeg",
          "name": "Zonker Stout", "style": "Foreign - Export Stout",
          "abv": "6.00", "ibu": "36", "description": "A rich, well balanced "
          "foreign-style stout with a generous amount of roasted barley as "
          "well as chocolate, black, and caramel malts. Complex hop "
          "sequencing creates superbly balanced flavor."}]

for beer in beers:
    newBeer = Beer(image=beer['image'], name=beer['name'], style=beer['style'],
                   abv=beer['abv'], ibu=beer['ibu'],
                   description=beer['description'], user_id=beer["user_id"],
                   country_id=beer['country_id'], region_id=beer["region_id"],
                   brewery_id=beer["brewery_id"])
    session.add(newBeer)
    session.commit()

# Create Ratings for beers
ratings = [{"num_of_stars": "5", "user_id": "1", "beer_id": "1"},
           {"num_of_stars": "3", "user_id": "1", "beer_id": "1"}]

for rating in ratings:
    newRating = Rating(num_of_stars=rating[
                       "num_of_stars"], user_id=rating["user_id"],
                       beer_id=rating["beer_id"])
    session.add(newRating)
    session.commit()

print "added countries, regions/states and breweries"
