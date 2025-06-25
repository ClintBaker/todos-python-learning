from fastapi import FastAPI
import db.models as models
from db.database import engine
from routers import auth, todos, admin

app = FastAPI()

# Create all tables in the database using SQLAlchemy / SQLite
models.Base.metadata.create_all(bind=engine)

# health check
@app.get('/health')
async def health_check():
    return {'status': 'ok'}

# routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)