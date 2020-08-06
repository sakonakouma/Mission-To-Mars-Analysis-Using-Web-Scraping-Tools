from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# Creat Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")

# Route to connect index.html template using data from Mongo
@app.route("/")
def home():
# Explore data from the mongo database
    datam = mongo.db.collection.find_one()
# Return template and data
    return render_template("index.html", mars=datam)

# Route to the scrape function
@app.route("/scrape")
def scrape():
#datam = {}
# Run the scrape function
datam = scrape_mars.scrape()

# Update the Mongo database using update and upsert=True
mongo.db.collection.update({}, datam, upsert=True)

#Redirect back to home page
return redirect("/")

if __name__ == "__main__":
    app.run(debug=True) 
