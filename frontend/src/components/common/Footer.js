import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 40px;
    text-align: center;
    font-size: 14px;
    ul {
        list-style: none;
        padding: 0;
        margin-bottom: 20px;
        li {
            display: inline-block;
            margin: 0 15px;
            a {
                color: #ecf0f1;
                text-decoration: none;
                &:hover {
                    color: #007bff;
                }
            }
        }
    }
    p {
        margin: 0;
    }
`;

const Footer = () => {
    return (
        <FooterContainer>
            <ul>
                <li><a href="/about">Về chúng tôi</a></li>
                <li><a href="/terms">Điều khoản sử dụng</a></li>
                <li><a href="/privacy">Chính sách bảo mật</a></li>
                <li><a href="/faq">Câu hỏi thường gặp</a></li>
            </ul>
            <p>© 2023 ElearnHub. All rights reserved.</p>
        </FooterContainer>
    );
};

export default Footer;