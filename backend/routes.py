import os
import sys
import json
from flask import jsonify, request
from bson import json_util
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from . import app

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

with open(json_url, "r") as f:
    try:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON must contain a list of documents.")
    except (json.JSONDecodeError, ValueError) as e:
        app.logger.error(f"Error loading JSON: {str(e)}")
        sys.exit(1)

# MongoDB connection in .env file
mongodb_service = os.environ.get("ME_CONFIG_MONGODB_SERVER")
mongodb_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongodb_password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongodb_useradmin = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongodb_initial_db = os.environ.get("MONGO_INITDB_DATABASE")

if mongodb_service is None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    URL = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}:" \
        f"27017/{mongodb_initial_db}?authSource={mongodb_useradmin}"
else:
    URL = f"mongodb://{mongodb_service}:27017"

print(f"MongoDB URL: {URL}")

try:
    client = MongoClient(URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    app.logger.info("Connected to MongoDB successfully.")
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")
    sys.exit(1)
except Exception as e:
    app.logger.error(f"MongoDB connection error: {str(e)}")
    sys.exit(1)

try:
    db = client.api_concerts_pictures
    db.api_concerts_pictures.drop()
    db.api_concerts_pictures.insert_many(data)
    app.logger.info(f"Initial {len(data)} documents inserted into the database.")
except Exception as e:
    app.logger.error(f"Error inserting initial data: {str(e)}")
    sys.exit(1)


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/health")
def health():
    """Return health of the app."""
    return {"status": 'OK'}, 200


@app.route("/count")
def count():
    """Return length of data."""
    count_pictures = db.api_concerts_pictures.count_documents({})
    if count_pictures:
        return jsonify(parse_json(count_pictures)), 200
    return {"message": "Internal server error"}, 500


@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures."""
    pictures = db.api_concerts_pictures.find({})
    return jsonify(parse_json(pictures)), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by id."""
    picture = db.api_concerts_pictures.find_one({"id": id})
    if picture:
        return jsonify(parse_json(picture)), 200
    return {"message": f"Picture with id {id} not found"}, 404


@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture."""
    json_picture = request.get_json()

    if not json_picture:
        return {"message": "Invalid JSON"}, 400

    search_picture_db = db.api_concerts_pictures.find_one({"id": json_picture['id']})

    if search_picture_db is not None:
        return {"Message": f"picture with id {json_picture['id']} already present"}, 302

    document_picture = {
        "id": json_picture['id'],
        "pic_url": json_picture['pic_url'],
        "event_country": json_picture['event_country'],
        "event_state": json_picture['event_state'],
        "event_city": json_picture['event_city'],
        "event_date": json_picture['event_date'],
    }
    insert_picture_db = db.api_concerts_pictures.insert_one(document_picture)
    return {"insert id": str(insert_picture_db.inserted_id)}, 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture by id."""
    json_picture = request.get_json()

    if not json_picture:
        return {"message": "Invalid JSON"}, 400

    search_picture_db = db.api_concerts_pictures.find_one({"id": json_picture['id']})

    if search_picture_db is not None:
        json_picture_db = parse_json(search_picture_db)
        keys = ['pic_url', 'event_country', 'event_state', 'event_city', 'event_date']
        if {k: json_picture[k] for k in keys} == {k: json_picture_db[k] for k in keys}:
            return {"message": "Picture found, but no changes made"}, 200

        document_picture = {
            "id": json_picture['id'],
            "pic_url": json_picture['pic_url'],
            "event_country": json_picture['event_country'],
            "event_state": json_picture['event_state'],
            "event_city": json_picture['event_city'],
            "event_date": json_picture['event_date'],
        }
        db.api_concerts_pictures.update_one({"id": id}, {"$set": document_picture})
        picture_updated = db.api_concerts_pictures.find_one({"id": id})

        json_picture_updated = parse_json(picture_updated)
        return jsonify(json_picture_updated), 201
    return {"message": f"Picture with id {id} not found"}, 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id."""
    db_picture = db.api_concerts_pictures.find_one({"id": id})

    if db_picture is None:
        return {"message": f"Picture with id {id} not found"}, 404

    db.api_concerts_pictures.delete_one({"id": id})
    return {"message": f"Picture with id {id} deleted successfully"}, 204
