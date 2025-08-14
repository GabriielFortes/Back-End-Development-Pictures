# 🎵 Concerts API – CRUD with Flask and MongoDB
This project is a RESTful API built with Flask and MongoDB, enabling complete CRUD (Create, Read, Update, Delete) operations for managing concerts and pictures.

It was developed as part of a practical learning exercise on backend development, containerization with Docker, and MongoDB integration.

## 🚀 Features
- CRUD operations for concerts and pictures
- Data storage using MongoDB
- Flask as the web framework
- JSON-based communication between client and server
- Containerized with Docker for local deployment

## 📂 Project Structure
```
.
Back-End-Development-Pictures/
├── app.py               # Main application file
├── backend              # 
│   ├── data             # Dados estáticos (ex: pictures.json)
│   ├── __init__.py      
│   └── routes.py        # Routes API
├── tests                # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Local orchestration with MongoDB
├── LICENSE              # Licence
├── pytest.ini           # Pytest config
├── README.md            # Documentation
└── requirements.txt     # Python dependencies
```

## 🛠️ Installation & Execution
1. Clone the repository
```
git clone https://github.com/GabriielFortes/Back-End-Development-Pictures.git
cd concerts-api
```

2. Run with Docker Compose
```
docker-compose up --build
```

This will start:
- API running on http://localhost:3000
- MongoExpress http://localhost:8082  # Interface MongoDB
- MongoDB running on mongodb://localhost:27018

## 🔧 Environment Variables
These variables can be set in the .env file or directly in docker-compose.yml:
```ini
ME_CONFIG_MONGODB_SERVER=mongodb
ME_CONFIG_MONGODB_ENABLE_ADMIN=true
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=admin
ME_CONFIG_MONGODB_ADMINUSERNAME=admin
ME_CONFIG_MONGODB_ADMINPASSWORD=admin
ME_CONFIG_MONGODB_AUTH_DATABASE=admin
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin
MONGO_INITDB_DATABASE=api_concerts_pictures
```

## 📌 API Endpoints
### 🎤 Concerts
#### Method      Endpoint        Description
GET	        /concerts	    List all concerts
GET	        /concerts/<id>	Retrieve a specific concert
POST	    /concerts	    Create a new concert
PUT	        /concerts/<id>	Update a concert by ID
DELETE	    /concerts/<id>	Delete a concert by ID

## 🖼️ Pictures
Method      Endpoint        Description
GET	        /picture    	List all pictures
GET	        /picture/<id>	Retrieve a specific picture
POST	    /picture	    Upload a new picture
PUT	        /picture/<id>	Update a picture by ID
DELETE	    /picture/<id>	Delete a picture by ID

## 🧪 Testing
▶️ Running Tests inside the backend container
After starting the containers, open a terminal inside the backend container:
To run the tests:
```bash
docker exec -it api_concerts_songs sh

pytest
```

##🤝 Credits
This project was developed as a final project for the IBM Backend Development Capstone Project course:
https://www.coursera.org/professional-certificates/ibm-backend-development

All implementations, modular architecture, tests, and MongoDB integration were completed by me based on the course foundations and further customization.