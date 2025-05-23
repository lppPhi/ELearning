/Frontend/
│
├── /css/                        # Style cho toàn bộ giao diện
│   ├── style.css                # Giao diện chung
│   └── responsive.css           # Giao diện mobile, tablet
│
├── /js/                         # Script xử lý logic giao diện và gọi API
│   ├── main.js                  # Xử lý chuyển trang, menu, layout
│   ├── course.js                # Gọi API, xử lý logic liên quan đến khóa học
│   ├── user.js                  # Đăng nhập, đăng ký, cập nhật profile
│   └── api.js                   # Các hàm dùng chung để gọi API FastAPI
│
├── /assets/                     # Hình ảnh, icon
│   └── logo.png
│
├── /components/                 # Các thành phần HTML tái sử dụng
│   ├── header.html              # Thanh menu
│   ├── footer.html              # Chân trang
│   ├── course-card.html         # Giao diện 1 khoá học
│
├── /pages/                      # Các trang người dùng truy cập
│   ├── home.html                # Trang chủ (hiển thị khoá học phổ biến)
│   ├── login.html               # Đăng nhập
│   ├── register.html            # Đăng ký tài khoản
│   ├── dashboard.html           # Trang chính của người dùng sau khi đăng nhập
│   ├── course-list.html         # Danh sách khoá học
│   ├── course-detail.html       # Chi tiết 1 khoá học
│   ├── course-create.html       # Trang tạo khoá học (tuỳ chọn nếu user là giảng viên)
│   ├── learn.html               # Trang học (video, tài liệu, nội dung)
│   ├── progress.html            # Theo dõi tiến độ học
│   ├── profile.html             # Trang hồ sơ cá nhân
│   └── notifications.html       # Thông báo cho user
│
└── index.html                   # Trang landing hoặc tự động chuyển hướng
