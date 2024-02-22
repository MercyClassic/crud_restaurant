**<h1> CRUD Restaurant </h1>**

**<h2> Stack </h2>**
- **<h3> FastAPI </h3>**
- **<h3> Async SQLAlchemy </h3>**
- **<h3> Celery + Celery beat </h3>**
- **<h3> Redis (cache) </h3>**
- **<h3> Rabbitmq (broker) </h3>**
- **<h3> Docker </h3>**
- **<h3> pytest </h3>**


**<h2> Startup: </h2>**
**<h3> Via docker: </h3>**
- **<h4> Create .env file in the root dir by example (.env.example) </h4>**
- **<h4> Import credentials.json from google api in the application/synchronizer </h4>**
- **<h4> ```cd docker``` </h4>**
- **<h4> ```docker compose up --build``` </h4>**

**<h3> Without docker: </h3>**
- **<h4> Create .env file in the root dir by example (.env.example) </h3>**
- **<h4> Import credentials.json from google api in the application/synchronizer </h4>**
- **<h4> ```docker run -p 6379:6379 redis -d``` </h4>**
- **<h4> ```docker run -p 5672:5672 rabbitmq -d``` </h4>**
- **<h4> ```poetry install``` or ```pip install -r requirements.txt``` </h4>**
- **<h4> activate venv </h4>**
- **<h4> ```source .env``` </h4>**
- **<h4> ```cd src``` </h4>**
- **<h4> Create 3 terminals and run 3 commands: </h4>**
- - **<h4> ```uvicorn app.main.main:app``` </h4>**
- - **<h4> ```celery -A app.application.synchronizer.worker.main worker -l info``` </h4>**
- - **<h4> ```celery -A app.application.synchronizer.worker.main beat``` </h4>**

**<h2> Testing: </h2>**
- **<h4> Create .env file in the root dir by example (.env.example) </h3>**
- **<h4> ```cd docker``` </h4>**
- **<h4> Pytest: ```docker compose -f testing/pytest/pytest.yml up```</h4>**
- **<h4> Postman: ```docker compose -f testing/postman/postman.yml up```</h4>**

**<h4> Database synchronization service with google sheets located in ```app/application/synchronizer/synchronizer.py``` </h4>**
