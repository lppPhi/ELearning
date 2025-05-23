from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, course, chapter, part, category, registered_course
import logging

app = FastAPI()

# Thêm cấu hình CORS cho phép tất cả origin (hoặc chỉ định origin cụ thể)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(course.router, prefix="/courses", tags=["courses"])
app.include_router(chapter.router, prefix="/chapters", tags=["chapters"])
app.include_router(part.router, prefix="/parts", tags=["parts"])
app.include_router(category.router, prefix="/categories", tags=["categories"])
app.include_router(registered_course.router, prefix="/registrations", tags=["registrations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-learning API!"}