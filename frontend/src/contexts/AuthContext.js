import React, { createContext, useContext, useState, useEffect } from 'react';

// Mock API calls (thực tế sẽ gọi backend)
import { loginUser, registerUser, logoutUser } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null); // Lưu thông tin User (UserID, FullName, Email)
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Giả lập kiểm tra trạng thái đăng nhập khi load ứng dụng
        const storedUser = localStorage.getItem('currentUser');
        if (storedUser) {
            setCurrentUser(JSON.parse(storedUser));
        }
        setIsLoading(false);
    }, []);

    const login = async (email, password) => {
        setIsLoading(true);
        try {
            const user = await loginUser(email, password); // Gọi API đăng nhập
            setCurrentUser(user);
            localStorage.setItem('currentUser', JSON.stringify(user));
            setIsLoading(false);
            return { success: true };
        } catch (error) {
            setIsLoading(false);
            return { success: false, message: error.message || 'Đăng nhập thất bại' };
        }
    };

    const register = async (fullName, email, password) => {
        setIsLoading(true);
        try {
            const user = await registerUser(fullName, email, password); // Gọi API đăng ký
            setCurrentUser(user);
            localStorage.setItem('currentUser', JSON.stringify(user));
            setIsLoading(false);
            return { success: true };
        } catch (error) {
            setIsLoading(false);
            return { success: false, message: error.message || 'Đăng ký thất bại' };
        }
    };

    const logout = () => {
        logoutUser(); // Gọi API đăng xuất nếu có
        setCurrentUser(null);
        localStorage.removeItem('currentUser');
    };

    const isAuthenticated = !!currentUser; // Kiểm tra đã đăng nhập chưa

    return (
        <AuthContext.Provider value={{ currentUser, isAuthenticated, isLoading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);