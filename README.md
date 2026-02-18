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

## Docker
1. Go to the `backend/docker-compose` folder
- To start the application with infrastructure:
`docker compose -f backend/docker-compose/docker-compose.yml up -d`

- To start the infrastructure only:
`docker compose -f backend/docker-compose/docker-compose.infra.yml up -d`