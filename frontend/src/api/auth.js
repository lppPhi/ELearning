// dataMocks.js
// import { mockUsers } from '../utils/dataMocks';

const API_URL = "http://localhost:8000";

// Giả lập API call
export const loginUser = async (email, password) => {
    const response = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });
    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || "Đăng nhập thất bại");
    }
    return await response.json();
};

export const registerUser = async (fullName, email, password) => {
    const response = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ full_name: fullName, email, password })
    });
    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || "Đăng ký thất bại");
    }
    return await response.json();
};

export const logoutUser = async () => {
    // Nếu có API logout thì gọi, còn không chỉ xóa localStorage phía client
    return true;
};