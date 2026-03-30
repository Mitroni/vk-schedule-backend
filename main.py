from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schedule, students, admin, auth, bell
import uvicorn

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
