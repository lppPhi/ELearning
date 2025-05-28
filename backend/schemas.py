from pydantic import BaseModel, EmailStr # Thêm EmailStr để validate email tốt hơn
from typing import Optional, List
from datetime import datetime

# === User Schemas ===
class UserBase(BaseModel):
    UserName: str
    Email: EmailStr # Sử dụng EmailStr để Pydantic tự validate định dạng email
    Phone: Optional[str] = None
    Image: Optional[str] = None # Sẽ là URL của ảnh

class UserCreate(UserBase):
    Password: str # Sẽ được hash trước khi lưu vào DB

class UserUpdate(UserBase):
    UserName: Optional[str] = None # Cho phép cập nhật UserName
    Email: Optional[EmailStr] = None # Cho phép cập nhật Email
    Password: Optional[str] = None # Nếu muốn thay đổi mật khẩu
    # Phone và Image đã có trong UserBase và là Optional

    class Config:
        # Pydantic v2: from_attributes = True
        # Pydantic v1: orm_mode = True
        from_attributes = True # Hoặc orm_mode = True nếu bạn dùng Pydantic v1

class UserLogin(BaseModel):
    UserName: str
    Password: str

class UserInfo(UserBase): # Thông tin trả về cho client, không bao gồm password
    UserID: int

    class Config:
        from_attributes = True

# === Course Schemas ===
class CourseBase(BaseModel):
    CourseName: str
    Decription: Optional[str] = None # Mô tả ngắn
    IsPublic: Optional[bool] = True
    Price: Optional[float] = 0.0 # Nên dùng float hoặc Decimal từ 'decimal' module nếu cần độ chính xác cao
    Image: Optional[str] = None # URL ảnh bìa

class CourseCreate(CourseBase):
    UserID: int # ID của người tạo khóa học
    DetailCourse: Optional[str] = None # Mô tả chi tiết

class CourseUpdate(CourseBase): # Các trường có thể cập nhật
    CourseName: Optional[str] = None
    Decription: Optional[str] = None
    IsPublic: Optional[bool] = None
    Price: Optional[float] = None
    Image: Optional[str] = None
    DetailCourse: Optional[str] = None
    # Không cho phép thay đổi UserID (người tạo) của khóa học

    class Config:
        from_attributes = True

class CourseInfo(CourseBase): # Thông tin cơ bản của khóa học để hiển thị
    CourseID: int
    UserID: int # Thêm UserID để biết ai tạo, nhưng không nhất thiết phải hiển thị trực tiếp
    # NumberOfRegistrations có thể thêm ở đây nếu muốn lấy từ model Course
    NumberOfRegistrations: Optional[int] = 0

    class Config:
        from_attributes = True

class CourseDetail(CourseInfo): # Thông tin chi tiết hơn, kế thừa từ CourseInfo
    DetailCourse: Optional[str] = None
    # Có thể thêm danh sách chapters ở đây nếu muốn response lồng nhau
    # chapters: List['ChapterInfo'] = [] # Forward reference

    class Config:
        from_attributes = True


# === Chapter Schemas ===
class ChapterBase(BaseModel):
    ChapterName: str
    Document: Optional[str] = None # URL tài liệu/video của chương

class ChapterCreate(ChapterBase):
    CourseID: int

class ChapterUpdate(ChapterBase): # Các trường có thể cập nhật cho Chapter
    ChapterName: Optional[str] = None
    Document: Optional[str] = None

    class Config:
        from_attributes = True

class ChapterInfo(ChapterBase):
    ChapterID: int
    CourseID: int # Thêm CourseID để biết thuộc khóa học nào
    # parts: List['PartInfo'] = [] # Nếu muốn response lồng nhau

    class Config:
        from_attributes = True


# === Part Schemas ===
class PartBase(BaseModel):
    PartName: str
    Document: Optional[str] = None # URL tài liệu/video của phần học

class PartCreate(PartBase):
    ChapterID: int

class PartUpdate(PartBase): # Các trường có thể cập nhật cho Part
    PartName: Optional[str] = None
    Document: Optional[str] = None

    class Config:
        from_attributes = True

class PartInfo(PartBase):
    PartID: int
    ChapterID: int # Thêm ChapterID để biết thuộc chương nào

    class Config:
        from_attributes = True


# === RegisteredCourse Schemas ===
class RegisteredCourseBase(BaseModel):
    CourseID: int
    UserID: int

class RegisteredCourseCreate(RegisteredCourseBase):
    pass # Không cần thêm gì

class RegisteredCourseInfo(RegisteredCourseBase):
    RegisterID: int
    RegistrationDate: datetime

    class Config:
        from_attributes = True


# === File Upload Schema ===
class FileUploadResponse(BaseModel):
    filename: str # Tên file đã lưu trên server (có thể là tên duy nhất)
    file_url: str   # URL công khai để truy cập file

# === Token Schemas (Thường dùng với OAuth2) ===
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None # Hoặc user_id tùy theo cách bạn định danh user trong token

# --- Cập nhật forward references nếu có (cho response lồng nhau) ---
# Nếu bạn quyết định sử dụng response lồng nhau, ví dụ CourseDetail trả về list chapters,
# và ChapterInfo trả về list parts.
# CourseDetail.model_rebuild() # Pydantic v2
# ChapterInfo.model_rebuild()  # Pydantic v2
# Nếu dùng Pydantic v1 thì dùng:
# CourseDetail.update_forward_refs()
# ChapterInfo.update_forward_refs()
# Điều này cần được gọi sau khi tất cả các model đã được định nghĩa.
# Thường thì không cần gọi thủ công nếu không có lỗi circular import hoặc forward ref phức tạp.
# FastAPI thường tự xử lý tốt việc này.