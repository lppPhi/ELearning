const API_BASE = 'http://127.0.0.1:8000';

// Xử lý lỗi API
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Đã có lỗi xảy ra');
    }
    return response.json();
};

// Auth APIs
const auth = {
    async login(username, password) {
        const response = await fetch(`${API_BASE}/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password })
        });
        return handleResponse(response);
    },

    async register(userData) {
        const response = await fetch(`${API_BASE}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return handleResponse(response);
    },

    async getProfile(token) {
        const response = await fetch(`${API_BASE}/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return handleResponse(response);
    }
};

// Course APIs
const courses = {
    async getAll(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`${API_BASE}/courses/?${queryString}`);
        return handleResponse(response);
    },

    async getById(id) {
        const response = await fetch(`${API_BASE}/courses/${id}`);
        return handleResponse(response);
    },

    async create(courseData, token) {
        const response = await fetch(`${API_BASE}/courses/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(courseData)
        });
        return handleResponse(response);
    },

    async register(courseId, token) {
        const response = await fetch(`${API_BASE}/courses/${courseId}/register`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return handleResponse(response);
    }
};

// Category APIs
const categories = {
    async getAll() {
        const response = await fetch(`${API_BASE}/categories/`);
        return handleResponse(response);
    }
};

// Chapter APIs
const chapters = {
    async getByCourse(courseId) {
        const response = await fetch(`${API_BASE}/courses/${courseId}/chapters`);
        return handleResponse(response);
    }
};

// Progress tracking
const progress = {
    async update(chapterId, progress, token) {
        const response = await fetch(`${API_BASE}/chapters/${chapterId}/progress`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ progress })
        });
        return handleResponse(response);
    }
};

// Lấy tất cả khoá học từ FastAPI
async function fetchCourses() {
    const res = await fetch(`${API_BASE}/courses/?skip=0&limit=100`);
    if (!res.ok) throw new Error('Không thể lấy danh sách khoá học');
    return res.json();
}

window.fetchCourses = fetchCourses;

// Thêm các hàm gọi API khác nếu cần
