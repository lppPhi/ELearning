import React, { useState } from 'react';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const TabContainer = styled.div`
    display: flex;
    margin-bottom: 30px;
    border-bottom: 2px solid #eee;
`;

const Tab = styled.button`
    flex: 1;
    padding: 15px 0;
    border: none;
    background-color: transparent;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    color: ${({ $isActive }) => ($isActive ? '#007bff' : '#666')};
    border-bottom: ${({ $isActive }) => ($isActive ? '3px solid #007bff' : 'none')};
    transition: all 0.3s ease-in-out;
    &:hover {
        color: #007bff;
    }
`;

const FormGroup = styled.div`
    margin-bottom: 20px;
    text-align: left;
    label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #555;
    }
    input {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1em;
        &:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
        }
    }
`;

const SubmitButton = styled.button`
    width: 100%;
    padding: 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
    &:hover {
        background-color: #0056b3;
    }
    &:disabled {
        background-color: #a0c3e7;
        cursor: not-allowed;
    }
`;

const ErrorMessage = styled.p`
    color: #dc3545;
    font-size: 0.9em;
    margin-top: 10px;
`;

const AuthForm = ({ initialTab = 'login' }) => {
    const [activeTab, setActiveTab] = useState(initialTab);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const { login, register, isLoading } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        const result = await login(email, password);
        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.message);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        if (password !== confirmPassword) {
            setError('Mật khẩu xác nhận không khớp.');
            return;
        }
        const result = await register(fullName, email, password);
        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.message);
        }
    };

    return (
        <>
            <TabContainer>
                <Tab $isActive={activeTab === 'login'} onClick={() => setActiveTab('login')}>
                    Đăng nhập
                </Tab>
                <Tab $isActive={activeTab === 'register'} onClick={() => setActiveTab('register')}>
                    Đăng ký
                </Tab>
            </TabContainer>

            {activeTab === 'login' ? (
                <form onSubmit={handleLogin}>
                    <FormGroup>
                        <label htmlFor="login-email">Email</label>
                        <input
                            type="email"
                            id="login-email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="login-password">Mật khẩu</label>
                        <input
                            type="password"
                            id="login-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </FormGroup>
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <SubmitButton type="submit" disabled={isLoading}>
                        {isLoading ? 'Đang đăng nhập...' : 'Đăng nhập'}
                    </SubmitButton>
                </form>
            ) : (
                <form onSubmit={handleRegister}>
                    <FormGroup>
                        <label htmlFor="register-fullname">Họ và tên</label>
                        <input
                            type="text"
                            id="register-fullname"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            required
                        />
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="register-email">Email</label>
                        <input
                            type="email"
                            id="register-email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="register-password">Mật khẩu</label>
                        <input
                            type="password"
                            id="register-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="register-confirm-password">Xác nhận mật khẩu</label>
                        <input
                            type="password"
                            id="register-confirm-password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </FormGroup>
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <SubmitButton type="submit" disabled={isLoading}>
                        {isLoading ? 'Đang đăng ký...' : 'Đăng ký'}
                    </SubmitButton>
                </form>
            )}
        </>
    );
};

export default AuthForm;