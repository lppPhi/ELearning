# Contents of the file: /Backend/app/routers/__init__.py

from fastapi import APIRouter

router = APIRouter()

from . import user, course, chapter, part, category, registered_course

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(course.router, prefix="/courses", tags=["courses"])
router.include_router(chapter.router, prefix="/chapters", tags=["chapters"])
router.include_router(part.router, prefix="/parts", tags=["parts"])
router.include_router(category.router, prefix="/categories", tags=["categories"])
router.include_router(registered_course.router, prefix="/registrations", tags=["registrations"])