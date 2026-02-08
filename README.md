# Chess Game

## Project Structure (Clean Architecture)
- `/backend`: FastAPI service (including domain logic)
- `/frontend`: Angular client

## How to run locally

### Back-end API
1. Go to the backend directory:
   `cd backend`
2. Activate virtual environment:
   `source .venv/bin/activate`
3. Run the application:
   `uvicorn chessapp.interface.main:app --reload`

### Front-end Client
1. Go to the frontend directory:
   `cd frontend`
2. Install dependencies (if needed):
   `npm install`
3. Run the development server:
   `npm start`

## Docker (Work in Progress)
To kill existing processes on port 8000:
`sudo lsof -t -i tcp:8000 | xargs kill -9`

Best practices for FastAPI with MongoDB
https://www.mongodb.com/developer/products/mongodb/8-fastapi-mongodb-best-practices/

Clean Architecture using FastAPI
https://github.com/0xTheProDev/fastapi-clean-example/tree/main


Chess-engine
Chess-application

Best practices for FastAPI with MongoDB
https://www.mongodb.com/developer/products/mongodb/8-fastapi-mongodb-best-practices/
https://github.com/mongodb-labs/full-stack-fastapi-mongodb?tab=readme-ov-file

Clean Architecture using FastAPI
https://github.com/0xTheProDev/fastapi-clean-example/tree/main

Full Stack Fast API on React and MongoDD
https://github.com/mongodb-labs/full-stack-fastapi-mongodb/tree/main

Fast API on WebSocket and Kafka
https://github.com/AlexanderLukash/fastapi-websocket-chat-kafka/