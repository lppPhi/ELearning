import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import CourseCard from '../components/CourseCard';
import { useAuth } from '../contexts/AuthContext';
import { getUserRegisteredCourses, getUserCreatedCourses } from '../api/courses'; // Mock API
import { Link, useNavigate } from 'react-router-dom';

const DashboardContainer = styled.div`
    display: flex;
    flex-direction: column;
    min-height: 100vh;
`;

const DashboardContent = styled.main`
    flex-grow: 1;
    padding: 40px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
`;

const SectionHeader = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    h2 {
        font-size: 2em;
        color: #333;
    }
    button {
        background-color: #28a745; /* Màu xanh lá cây */
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        font-size: 1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
        &:hover {
            background-color: #218838;
        }
    }
`;

const CoursesGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-bottom: 60px;
`;

const DashboardPage = () => {
    const { currentUser } = useAuth();
    const [registeredCourses, setRegisteredCourses] = useState([]);
    const [createdCourses, setCreatedCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCourses = async () => {
            if (currentUser) {
                setLoading(true);
                const regCourses = await getUserRegisteredCourses(currentUser.UserID);
                const creCourses = await getUserCreatedCourses(currentUser.UserID);
                setRegisteredCourses(regCourses);
                setCreatedCourses(creCourses);
                setLoading(false);
            }
        };
        fetchCourses();
    }, [currentUser]);

    if (loading) {
        return (
            <DashboardContainer>
                <Header />
                <DashboardContent>Đang tải khóa học của bạn...</DashboardContent>
                <Footer />
            </DashboardContainer>
        );
    }

    return (
        <DashboardContainer>
            <Header />
            <DashboardContent>
                <SectionHeader>
                    <h2>Khoá học đã đăng ký</h2>
                </SectionHeader>
                {registeredCourses.length > 0 ? (
                    <CoursesGrid>
                        {registeredCourses.map((course) => (
                            <CourseCard key={course.CourseID || course.course_id} course={course} type="registered" />
                        ))}
                    </CoursesGrid>
                ) : (
                    <p>Bạn chưa đăng ký khóa học nào. <Link to="/">Khám phá ngay!</Link></p>
                )}

                <SectionHeader>
                    <h2>Khoá học của tôi (đã tạo)</h2>
                    <button onClick={() => navigate('/manage-course')}>Tạo khoá học mới</button>
                </SectionHeader>
                {createdCourses.length > 0 ? (
                    <CoursesGrid>
                        {createdCourses.map((course) => (
                            <CourseCard key={course.CourseID || course.course_id} course={course} type="created" />
                        ))}
                    </CoursesGrid>
                ) : (
                    <p>Bạn chưa tạo khóa học nào. Hãy bắt đầu xây dựng khóa học đầu tiên của bạn!</p>
                )}
            </DashboardContent>
            <Footer />
        </DashboardContainer>
    );
};

export default DashboardPage;