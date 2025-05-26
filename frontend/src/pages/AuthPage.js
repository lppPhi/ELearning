import React from 'react';
import styled from 'styled-components';
import AuthForm from '../components/AuthForm';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useEffect } from 'react';

const AuthPageContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(to right, #e0f2f7, #c9e7f7); /* Màu nền nhẹ nhàng */
`;

const AuthBox = styled.div`
    background-color: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    width: 100%;
    max-width: 450px;
    text-align: center;
`;

const AuthPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const initialTab = new URLSearchParams(location.search).get('tab') || 'login';

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard'); // Nếu đã đăng nhập, chuyển hướng về dashboard
        }
    }, [isAuthenticated, navigate]);

    return (
        <AuthPageContainer>
            <AuthBox>
                <AuthForm initialTab={initialTab} />
            </AuthBox>
        </AuthPageContainer>
    );
};

export default AuthPage;