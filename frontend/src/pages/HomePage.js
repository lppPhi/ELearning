import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import CourseCard from '../components/CourseCard';

// Mock data (thực tế sẽ gọi API)
import { getPublicCourses } from '../api/courses';
import { getCategories } from '../utils/dataMocks';

const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    min-height: 100vh;
`;

const MainContent = styled.main`
    flex-grow: 1;
`;

const HeroSection = styled.section`
    background: linear-gradient(135deg, #007bff, #6a0dad); /* Màu nền gradient */
    color: white;
    text-align: center;
    padding: 100px 20px;
    h1 {
        font-size: 3.5em;
        margin-bottom: 20px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    p {
        font-size: 1.3em;
        margin-bottom: 40px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    button {
        background-color: #ffc107; /* Màu nhấn */
        color: #333;
        border: none;
        padding: 15px 30px;
        font-size: 1.2em;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.3s ease-in-out;
        &:hover {
            background-color: #e0a800;
        }
    }
`;

const SectionTitle = styled.h2`
    text-align: center;
    font-size: 2.5em;
    color: #333;
    margin-bottom: 50px;
    position: relative;
    &::after {
        content: '';
        display: block;
        width: 80px;
        height: 4px;
        background-color: #007bff;
        margin: 15px auto 0;
        border-radius: 2px;
    }
`;

const CoursesGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    padding: 0 40px;
    max-width: 1200px;
    margin: 0 auto 80px;
`;

const CategoryContainer = styled.div`
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
    padding: 0 40px;
    margin-bottom: 80px;
`;

const CategoryTag = styled.button`
    background-color: #e9ecef;
    color: #333;
    border: 1px solid #ced4da;
    padding: 10px 20px;
    border-radius: 25px;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    &:hover {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
    }
`;


const HomePage = () => {
    const [courses, setCourses] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);

    useEffect(() => {
        const fetchCoursesAndCategories = async () => {
            const fetchedCourses = await getPublicCourses();
            const fetchedCategories = await getCategories();
            setCourses(fetchedCourses);
            setCategories(fetchedCategories);
        };
        fetchCoursesAndCategories();
    }, []);

    const filteredCourses = selectedCategory
        ? courses.filter(course => course.CategoryID === selectedCategory)
        : courses;

    return (
        <PageContainer>
            <Header />
            <MainContent>
                <HeroSection>
                    <h1>Khám phá tri thức, khai phá tiềm năng</h1>
                    <p>Học hỏi từ những chuyên gia hàng đầu, mọi lúc, mọi nơi.</p>
                    <button onClick={() => window.scrollTo({ top: document.getElementById('featured-courses').offsetTop, behavior: 'smooth' })}>
                        Bắt đầu khám phá
                    </button>
                </HeroSection>

                <SectionTitle id="featured-courses">Các khoá học nổi bật</SectionTitle>
                <CategoryContainer>
                    <CategoryTag onClick={() => setSelectedCategory(null)}>Tất cả</CategoryTag>
                    {categories.map(cat => (
                        <CategoryTag key={cat.CategoryID} onClick={() => setSelectedCategory(cat.CategoryID)}>
                            {cat.CategoryName}
                        </CategoryTag>
                    ))}
                </CategoryContainer>
                <CoursesGrid>
                    {filteredCourses.map(course => (
                        <CourseCard key={course.CourseID} course={course} type="public" />
                    ))}
                </CoursesGrid>
            </MainContent>
            <Footer />
        </PageContainer>
    );
};

export default HomePage;