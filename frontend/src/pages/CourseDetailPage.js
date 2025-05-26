import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import { getCourseDetails } from '../api/courses';

const CourseDetailPage = () => {
    const { courseId } = useParams();
    const [course, setCourse] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const data = await getCourseDetails(courseId);
                setCourse(data);
            } catch (err) {
                setError('Không thể tải chi tiết khoá học');
            }
            setLoading(false);
        };
        fetchData();
    }, [courseId]);

    if (loading) return <div>Đang tải...</div>;
    if (error) return <div style={{ color: 'red' }}>{error}</div>;
    if (!course) return <div>Không tìm thấy khoá học.</div>;

    return (
        <>
            <Header />
            <div style={{ maxWidth: 900, margin: '40px auto', background: '#fff', borderRadius: 10, padding: 32 }}>
                <h1>{course.CourseName}</h1>
                <p>{course.Description}</p>
                <div dangerouslySetInnerHTML={{ __html: course.DetailCourse }} />
                {/* Thêm các thông tin khác nếu muốn */}
            </div>
            <Footer />
        </>
    );
};

export default CourseDetailPage;
