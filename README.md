**<h1> CRUD Restaurant </h1>**
**<h2> Startup: </h2>**
**<h3> Via docker: </h3>**
- **<h4> Create .env file in the root dir by example (.env.example) </h3>**
- **<h4> ```cd docker``` </h4>**
- **<h4> ```docker compose up --build``` </h4>**

**<h3> Without docker: </h3>**
- **<h4> ```poetry install``` or ```pip install -r requirements.txt``` </h4>**
- **<h4> activate venv </h4>**
- **<h4> ```export db_uri=postgresql+asyncpg://user:pass@host:5432/db``` </h4>**
- **<h4> ```cd src``` </h4>**
- **<h4> ```uvicorn app.main.main:app``` </h4>**

**<h2> Testing: </h2>**
- **<h4> Create .env file in the root dir by example (.env.example) </h3>**
- **<h4> ```cd docker``` </h4>**
- **<h3> ```docker compose -f testing.yml up```</h3>**

**<h3> Django ```reverse()``` analogue located in tests/conftest.py </h3>**
