# Import Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set Up Flask Routes
# Recall Flask Routes bind URLs to funcitons

## Route for the HTML page
@app.route("/")
def index():
    # Use PyMongo to find the "mars" collection in our database
    mars = mongo.db.mars.find_one()
    # tells Flask to return an HTML template using an index.html file
    # mars = mars tells Python to use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

## Route for Scraping

@app.route("/scrape")
def scrape():
    # assign a new variable that point to our Mongo database
    mars = mongo.db.mars
    # assign a varibale to hold newly scraped data
    mars_data = scraping.scrape_all()
    # update the database
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # navigate back to where we can see the updated content
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run()