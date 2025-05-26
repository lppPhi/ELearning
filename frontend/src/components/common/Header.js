import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../../contexts/AuthContext';
import { MdAccountCircle } from 'react-icons/md'; // Ví dụ icon

const HeaderContainer = styled.header`
    background-color: #ffffff;
    padding: 15px 40px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
`;

const Logo = styled(Link)`
    font-size: 24px;
    font-weight: bold;
    color: #333;
    text-decoration: none;
    span {
        color: #007bff; /* Màu nhấn */
    }
`;

const NavLinks = styled.nav`
    a {
        text-decoration: none;
        color: #555;
        margin-left: 30px;
        font-weight: 500;
        transition: color 0.2s ease-in-out;
        &:hover {
            color: #007bff;
        }
    }
`;

const AuthButtons = styled.div`
    button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: 600;
        transition: background-color 0.2s ease-in-out;
        &:hover {
            background-color: #0056b3;
        }
        &:first-child {
            background: none;
            color: #007bff;
            border: 1px solid #007bff;
            margin-right: 10px;
            &:hover {
                background-color: #e6f0ff;
            }
        }
    }
`;

const UserMenu = styled.div`
    position: relative;
    display: flex;
    align-items: center;
    cursor: pointer;
    span {
        margin-right: 10px;
        font-weight: 500;
        color: #333;
    }
`;

const DropdownContent = styled.div`
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    min-width: 150px;
    padding: 10px 0;
    display: ${({ $isOpen }) => ($isOpen ? 'block' : 'none')};
    a, button {
        display: block;
        width: 100%;
        padding: 10px 15px;
        text-align: left;
        border: none;
        background: none;
        cursor: pointer;
        text-decoration: none;
        color: #333;
        &:hover {
            background-color: #f5f5f5;
        }
    }
`;


const Header = () => {
    const { currentUser, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = React.useState(false);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <HeaderContainer>
            <Logo to="/">Elearn<span>Hub</span></Logo>
            <NavLinks>
                <Link to="/">Trang chủ</Link>
                <Link to="/courses">Khóa học</Link> {/* Sẽ là trang list tất cả khoá học */}
                {isAuthenticated && <Link to="/dashboard">Khoá học của tôi</Link>}
                {isAuthenticated && <Link to="/manage-course">Tạo khoá học</Link>}
            </NavLinks>
            {isAuthenticated ? (
                <UserMenu onClick={() => setIsMenuOpen(!isMenuOpen)}>
                    <span>{currentUser?.FullName || currentUser?.Email}</span>
                    <MdAccountCircle size={30} color="#007bff" />
                    <DropdownContent $isOpen={isMenuOpen}>
                        <Link to="/profile">Hồ sơ</Link>
                        <Link to="/settings">Cài đặt</Link>
                        <button onClick={handleLogout}>Đăng xuất</button>
                    </DropdownContent>
                </UserMenu>
            ) : (
                <AuthButtons>
                    <button onClick={() => navigate('/auth?tab=login')}>Đăng nhập</button>
                    <button onClick={() => navigate('/auth?tab=register')}>Đăng ký</button>
                </AuthButtons>
            )}
        </HeaderContainer>
    );
};

export default Header;