import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Pages
import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import CourseLearningPage from './pages/CourseLearningPage';
import CourseManagePage from './pages/CourseManagePage';
import CourseDetailPage from './pages/CourseDetailPage';

// Layout components (Header/Footer sẽ được dùng trong từng page)
import GlobalStyle from './styles/globalStyles'; // Đúng chuẩn

// Component bảo vệ route
const PrivateRoute = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
        return <div>Đang tải...</div>; // Hoặc một Loading Spinner đẹp hơn
    }

    return isAuthenticated ? children : <Navigate to="/auth" />;
};

function App() {
    return (
        <Router>
            <GlobalStyle /> {/* Áp dụng global styles */}
            <AuthProvider>
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<HomePage />} />
                    <Route path="/courses/:courseId" element={<CourseDetailPage />} />
                    <Route path="/auth" element={<AuthPage />} />

                    {/* Private Routes */}
                    <Route path="/dashboard" element={
                        <PrivateRoute>
                            <DashboardPage />
                        </PrivateRoute>
                    } />
                    <Route path="/learn/:courseId" element={
                        <PrivateRoute>
                            <CourseLearningPage />
                        </PrivateRoute>
                    } />
                    <Route path="/manage-course" element={
                        <PrivateRoute>
                            <CourseManagePage />
                        </PrivateRoute>
                    } />
                    <Route path="/manage-course/:courseId" element={
                        <PrivateRoute>
                            <CourseManagePage />
                        </PrivateRoute>
                    } />

                    {/* Redirect unknown paths */}
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            </AuthProvider>
        </Router>
    );
}

export default App;