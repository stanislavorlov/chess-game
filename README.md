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
4. Run unit tests:
   `python3 -m unittest discover chessapp/tests`
5. Run integration tests:
   `./scripts/run_e2e.sh`

### Front-end Client
1. Go to the frontend directory:
   `cd frontend`
2. Install dependencies (if needed):
   `npm install`
3. Run the development server:
   `npm start`
4. Run unit tests:
   `npm test -- --browsers=ChromeHeadless --no-watch`

## How to run integration tests
1. Run back-end API:
   * [Back-end API](#back-end-api)
2. Run fron-end:
   * [Front-end Client](#front-end-client)
3. Run the integration tests:
   `cd backend && ./scripts/run_e2e.sh`

## Docker
1. Go to the `backend/docker-compose` folder
- To start the application with infrastructure:
`docker compose -f backend/docker-compose/docker-compose.yml up -d`

- To start the infrastructure only:
`docker compose -f backend/docker-compose/docker-compose.infra.yml up -d`

### Stats app

#### Build (to verify dependencies)

#### Initial Setup & Updating Swagger
If you clone the repo or update any API comments, you must generate the docs first:
```bash
cd backend/statsapp
swag init
go mod tidy
```

#### Build & Run
To compile and launch the application:
```bash
cd backend/statsapp
go run main.go
```
The Swagger UI will be available at: http://localhost:8081/swagger/index.html