from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""


    plants_data = plants.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':

        new_plant = {
            'name': request.form['plant_name'],
            'variety': request.form['variety'],
            'photo_url': request.form['photo'],
            'date_planted': request.form['date_planted'],
            'total_harvest': 0
        }

        plant = plants.insert_one(new_plant)
        plant_id = plant.inserted_id

        context = {
            'plant': plant,
            'plant_id': plant_id
        }

        return redirect(url_for('detail', plant_id=''))

    seeds_data = seeds.find()

    context = {
        'seeds': seeds_data
    }

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""


    plant_to_show = plants.find_one_or_404({'__id': ObjectId(plant_id)})
    harvests = = harvests.find({'plant_id': ObjectId(plant_id)})

    context = {
        'plant' : plant_to_show,
        'plant_id': plant_to_show['id']
        'harvests': harvests
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """
    plant_to_harvest = plants.find_one_or_404({'__id': ObjectId(plant_id)})
    quantity = int(request.form['harvested_amount'])
    name = p.plural(plant_to_harvest['name'].lower())

    new_harvest = {
        'quantity': quantity
        'date': request.form['date_harvested'],
        'plant_id': plant_to_harvest['id']
    }


    total_harvest = plant_to_harvest['total_harvest'] + quantity

    harvests.insert_one(next_harvest)
    plants.update_one(
        {'__id': ObjectId(plant_id)},
        {
            '$set': {
                'total_harvest': total_harvest
            }
        })

    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':

        plants.update_one(
            {'__id': ObjectId(plant_id)},
            {
                '$set': {
                    'name': request.form['plant_name'],
                    'variety': request.form['variety'],
                    'photo_url': request.form['photo'],
                    'date_planted': request.form['date_planted']
                }
            })

        
        return redirect(url_for('detail', plant_id=plant_id))
    else:

        plant_to_show = plants.find_one_or_404({'__id': ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):
    plants.delete_one({'_id': ObjectId(plant_id)})
    harvest.delete_many({'plant_id': ObjectID(plant_id)})

    
    return redirect(url_for('plants_list'))

if __name__ == '__main__':
    app.run(debug=True)

