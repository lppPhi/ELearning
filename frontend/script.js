document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = 'http://127.0.0.1:8000'; // Backend API URL

    // --- DOM Elements ---
    const pageLoader = document.getElementById('page-loader');
    const courseListContainer = document.getElementById('course-list');
    const loadingCoursesIndicator = document.getElementById('loading-courses');
    const noCoursesMessage = document.getElementById('no-courses');

    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const closeLoginModalBtn = document.getElementById('closeLoginModal');
    const closeRegisterModalBtn = document.getElementById('closeRegisterModal');

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginMessageEl = document.getElementById('loginMessage');
    const registerMessageEl = document.getElementById('registerMessage');

    const switchToRegisterLink = document.getElementById('switchToRegister');
    const switchToLoginLink = document.getElementById('switchToLogin');

    const authButtonsDiv = document.querySelector('.auth-buttons');
    const userInfoDiv = document.getElementById('userInfo');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const userAvatar = document.getElementById('userAvatar');

    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileAuthButtonsContainer = document.querySelector('.mobile-menu .mobile-auth-buttons');

    // --- Page Loader ---
    window.addEventListener('load', () => {
        if (pageLoader) {
            pageLoader.style.opacity = '0';
            setTimeout(() => {
                pageLoader.style.display = 'none';
            }, 500); // Match CSS transition duration
        }
    });

    // --- API Helper ---
    async function apiRequest(endpoint, method = 'GET', data = null, token = null) {
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`; // Assuming Bearer token auth
        }
        if (data && (method === 'POST' || method === 'PUT')) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: response.statusText }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            if (response.status === 204 || response.headers.get("content-length") === "0") { // No content
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error(`API request to ${endpoint} failed:`, error);
            throw error;
        }
    }

    // --- Course Display ---
    async function fetchAndDisplayCourses() {
        if (!courseListContainer) return;
        if (loadingCoursesIndicator) loadingCoursesIndicator.style.display = 'block';
        if (noCoursesMessage) noCoursesMessage.style.display = 'none';
        courseListContainer.innerHTML = ''; // Clear previous courses

        try {
            const courses = await apiRequest('/courses/all');
            if (loadingCoursesIndicator) loadingCoursesIndicator.style.display = 'none';

            if (courses && courses.length > 0) {
                courses.forEach(course => {
                    // Fetch creator info for each course
                    apiRequest(`/courses/${course.CourseID}/creator`)
                        .then(creator => {
                            const courseCard = createCourseCard(course, creator);
                            courseListContainer.appendChild(courseCard);
                        })
                        .catch(error => {
                            console.warn(`Could not fetch creator for course ${course.CourseID}:`, error);
                            // Display course card even if creator info fails
                            const courseCard = createCourseCard(course, null);
                            courseListContainer.appendChild(courseCard);
                        });
                });
            } else {
                if (noCoursesMessage) noCoursesMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Error fetching courses:', error);
            if (loadingCoursesIndicator) loadingCoursesIndicator.style.display = 'none';
            if (courseListContainer) courseListContainer.innerHTML = `<p class="error-message">Không thể tải danh sách khóa học. Vui lòng thử lại sau.</p>`;
        }
    }

    function createCourseCard(course, creator) {
        const card = document.createElement('div');
        card.className = 'course-card';

        let imageUrl = 'images/nophoto.png'; 
        if (course.Image) {
            if (course.Image.startsWith('http://') || course.Image.startsWith('https://')) {
                imageUrl = course.Image;
            } else if (course.Image.startsWith('/static/')) {
                imageUrl = `${API_BASE_URL}${course.Image}`;
            }
        }

        const imgElement = document.createElement('img');
        imgElement.alt = course.CourseName;
        imgElement.onerror = function() {
            this.onerror = null; 
            this.src = 'images/nophoto.png'; // Fallback image if the course image fails to load
        };
        imgElement.src = imageUrl; 

        const priceSpan = document.createElement('span');
        priceSpan.className = 'course-price';
        if (course.Price && parseFloat(course.Price) > 0) { // Chuyển course.Price sang số trước khi so sánh
            priceSpan.textContent = `$${parseFloat(course.Price).toFixed(2)}`;
        } else {
            priceSpan.textContent = 'Miễn phí';
            priceSpan.classList.add('free'); 
        }

        const cardImageContainer = document.createElement('div');
        cardImageContainer.className = 'card-image-container';
        cardImageContainer.appendChild(imgElement);
        cardImageContainer.appendChild(priceSpan);

        const cardContent = document.createElement('div');
        cardContent.className = 'card-content';
        cardContent.innerHTML = `
            <h3 class="course-title">${course.CourseName}</h3>
            <p class="course-instructor">Giảng viên: ${creator ? creator.UserName : 'N/A'}</p>
            <p class="course-description">${course.Decription || 'Không có mô tả.'}</p>
            <div class="course-meta">
                <span><i class="fas fa-users"></i> ${course.NumberOfRegistrations || 0} học viên</span>
            </div>
            <a href="course-detail.html?id=${course.CourseID}" class="btn btn-primary btn-block">Xem Chi Tiết</a>
        `;

        card.appendChild(cardImageContainer);
        card.appendChild(cardContent);

        return card;
    }

    // --- Modal Handling ---
    function openModal(modal) {
        if (modal) modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scroll
    }

    function closeModal(modal) {
        if (modal) modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }

    if (loginBtn) loginBtn.addEventListener('click', () => openModal(loginModal));
    if (registerBtn) registerBtn.addEventListener('click', () => openModal(registerModal));
    if (closeLoginModalBtn) closeLoginModalBtn.addEventListener('click', () => closeModal(loginModal));
    if (closeRegisterModalBtn) closeRegisterModalBtn.addEventListener('click', () => closeModal(registerModal));

    // Close modal if clicked outside content
    window.addEventListener('click', (event) => {
        if (event.target === loginModal) closeModal(loginModal);
        if (event.target === registerModal) closeModal(registerModal);
    });

    // Switch between login and register modals
    if (switchToRegisterLink) {
        switchToRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal(loginModal);
            openModal(registerModal);
        });
    }
    if (switchToLoginLink) {
        switchToLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal(registerModal);
            openModal(loginModal);
        });
    }

    // --- Authentication ---
    function displayFormMessage(element, message, isSuccess = true) {
        if(element) {
            element.textContent = message;
            element.className = `form-message ${isSuccess ? 'success' : 'error'}`;
        }
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const userData = await apiRequest('/users/login', 'POST', data);
                displayFormMessage(loginMessageEl, 'Đăng nhập thành công!', true);
                localStorage.setItem('userToken', 'dummy_token'); // Replace with actual token from backend
                localStorage.setItem('userData', JSON.stringify(userData));
                updateUserUI(userData);
                setTimeout(() => {
                    closeModal(loginModal);
                    loginForm.reset();
                    loginMessageEl.textContent = '';
                }, 1500);
            } catch (error) {
                displayFormMessage(loginMessageEl, error.message || 'Đăng nhập thất bại. Vui lòng kiểm tra lại.', false);
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const data = {
                UserName: formData.get('UserName'),
                Email: formData.get('Email'),
                Password: formData.get('Password'),
                Phone: formData.get('Phone') || null,
                // Image: null // Handle image upload separately if needed, or on profile page
            };
            
            // Basic client-side validation (more robust validation should be on backend)
            if (data.Password.length < 6) {
                 displayFormMessage(registerMessageEl, 'Mật khẩu phải có ít nhất 6 ký tự.', false);
                 return;
            }

            try {
                await apiRequest('/users/', 'POST', data);
                displayFormMessage(registerMessageEl, 'Đăng ký thành công! Vui lòng đăng nhập.', true);
                setTimeout(() => {
                    closeModal(registerModal);
                    openModal(loginModal); // Switch to login modal
                    registerForm.reset();
                    registerMessageEl.textContent = '';
                }, 2000);
            } catch (error) {
                displayFormMessage(registerMessageEl, error.message || 'Đăng ký thất bại. Tên đăng nhập hoặc Email có thể đã tồn tại.', false);
            }
        });
    }

    function updateUserUI(userData) {
    const fallbackAvatar = `${API_BASE_URL}/static/uploads/avatars/nophoto.png`;

    if (userData) {
        const avatarURL = userData.Image ? `${API_BASE_URL}${userData.Image}` : fallbackAvatar;

        if (authButtonsDiv) authButtonsDiv.style.display = 'none';
        if (userInfoDiv) userInfoDiv.style.display = 'flex';
        if (usernameDisplay) usernameDisplay.textContent = userData.UserName;
        if (userAvatar) {
            userAvatar.src = avatarURL;
            userAvatar.onerror = function () {
                this.onerror = null;
                this.src = fallbackAvatar;
            };
        }

        // Mobile menu user info
        if (mobileAuthButtonsContainer) {
            mobileAuthButtonsContainer.innerHTML = `
                <div style="padding: 10px; text-align: center; border-bottom: 1px solid #eee;">
                    <img src="${avatarURL}" alt="Avatar" style="width: 50px; height: 50px; border-radius: 50%; margin-bottom: 5px;" onerror="this.src='${fallbackAvatar}'">
                    <p style="font-weight: bold;">${userData.UserName}</p>
                </div>
                <a href="profile.html" class="btn btn-secondary" style="margin-bottom:10px;">Hồ sơ</a>
                <a href="my-courses.html" class="btn btn-secondary" style="margin-bottom:10px;">Khóa học của tôi</a>
                <a href="create-course.html" class="btn btn-secondary" style="margin-bottom:10px;">Tạo khóa học</a>
                <button id="mobileLogoutBtn" class="btn btn-primary">Đăng Xuất</button>
            `;
            const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
            if (mobileLogoutBtn) mobileLogoutBtn.addEventListener('click', handleLogout);
        }

    } else {
        // Logged out UI
        if (authButtonsDiv) authButtonsDiv.style.display = 'flex';
        if (userInfoDiv) userInfoDiv.style.display = 'none';
        if (dropdownContent && dropdownContent.classList.contains('show')) {
            dropdownContent.classList.remove('show');
        }

        if (mobileAuthButtonsContainer) {
            mobileAuthButtonsContainer.innerHTML = `
                <button id="mobileLoginBtn" class="btn btn-secondary" style="margin-bottom:10px;">Đăng Nhập</button>
                <button id="mobileRegisterBtn" class="btn btn-primary">Đăng Ký</button>
            `;
            const mobileLoginBtn = document.getElementById('mobileLoginBtn');
            const mobileRegisterBtn = document.getElementById('mobileRegisterBtn');
            if (mobileLoginBtn) mobileLoginBtn.addEventListener('click', () => { openModal(loginModal); closeMobileMenu(); });
            if (mobileRegisterBtn) mobileRegisterBtn.addEventListener('click', () => { openModal(registerModal); closeMobileMenu(); });
        }
    }
}


    function handleLogout() {
        localStorage.removeItem('userToken');
        localStorage.removeItem('userData');
        updateUserUI(null);
        // Optionally: redirect to homepage or show a message
        // window.location.href = 'index.html';
        if (mobileMenu && mobileMenu.classList.contains('open')) {
            closeMobileMenu();
        }
    }

    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);

    // Check login state on page load
    function checkLoginState() {
        const storedUserData = localStorage.getItem('userData');
        // const token = localStorage.getItem('userToken'); // Check token validity if you have a /me endpoint
        if (storedUserData) {
            updateUserUI(JSON.parse(storedUserData));
        } else {
            updateUserUI(null);
        }
    }

    // --- Dropdown Menu ---
    if (dropdownBtn && dropdownContent) {
        dropdownBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent window click from closing immediately
            dropdownContent.classList.toggle('show');
        });

        // Close dropdown if clicked outside
        window.addEventListener('click', (e) => {
            if (!dropdownBtn.contains(e.target) && !dropdownContent.contains(e.target)) {
                if (dropdownContent.classList.contains('show')) {
                    dropdownContent.classList.remove('show');
                }
            }
        });
    }
    
    // --- Mobile Menu ---
    function closeMobileMenu() {
        if (mobileMenu) mobileMenu.classList.remove('open');
        if (mobileMenuToggle && mobileMenuToggle.querySelector('i')) {
            mobileMenuToggle.querySelector('i').classList.remove('fa-times');
            mobileMenuToggle.querySelector('i').classList.add('fa-bars');
        }
        document.body.style.overflow = 'auto';
    }

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
            const icon = mobileMenuToggle.querySelector('i');
            if (mobileMenu.classList.contains('open')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
                document.body.style.overflow = 'hidden'; // Prevent background scroll
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
                document.body.style.overflow = 'auto';
            }
        });
        // Close mobile menu when a link is clicked
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });
    }
    // Add styles for .mobile-menu.open
    const styleSheet = document.createElement("style");
    styleSheet.innerText = `
        .mobile-menu.open { display: block; animation: slideDownMobileMenu 0.3s ease-out; }
        @keyframes slideDownMobileMenu {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(styleSheet);


    // --- Footer Current Year ---
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }

    // --- Initializations ---
    fetchAndDisplayCourses();
    checkLoginState();

});