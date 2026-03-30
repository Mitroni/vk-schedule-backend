from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schedule, students, admin, auth, bell

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки; при деплое укажите домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedule.router)
app.include_router(students.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(bell.router)

@app.get("/")
def root():
    return {"message": "VK Mini App API"}