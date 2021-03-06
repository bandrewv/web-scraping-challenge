from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
from jinja2 import Environment, PackageLoader, select_autoescape


# Creating an instance of Flask
app = Flask(__name__)

# Using PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    planet_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=planet_data)

# Route that triggers the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
