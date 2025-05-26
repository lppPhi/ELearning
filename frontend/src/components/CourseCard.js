import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { FaStar, FaUserGraduate } from 'react-icons/fa'; // Icons

const Card = styled.div`
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease-in-out;
    &:hover {
        transform: translateY(-5px);
    }
`;

const CourseImage = styled.img`
    width: 100%;
    height: 180px;
    object-fit: cover;
`;

const CardContent = styled.div`
    padding: 20px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
`;

const CourseTitle = styled.h3`
    font-size: 1.4em;
    margin-top: 0;
    margin-bottom: 10px;
    color: #333;
`;

const CourseDescription = styled.p`
    font-size: 0.9em;
    color: #666;
    margin-bottom: 15px;
    flex-grow: 1;
    display: -webkit-box;
    -webkit-line-clamp: 3; /* Giới hạn 3 dòng */
    -webkit-box-orient: vertical;
    overflow: hidden;
`;

const CourseMeta = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85em;
    color: #777;
    margin-bottom: 15px;

    div {
        display: flex;
        align-items: center;
        svg {
            margin-right: 5px;
            color: #f39c12; /* Màu sao */
        }
    }
`;

const PriceTag = styled.span`
    background-color: #27ae60;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 0.8em;
`;

const ActionButton = styled(Link)`
    display: block;
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    color: white;
    text-align: center;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    transition: background-color 0.2s ease-in-out;
    margin-top: auto; /* Đẩy xuống cuối */
    &:hover {
        background-color: #0056b3;
    }
`;

const CourseCard = ({ course, type = 'public', onActionClick }) => {
    // type: 'public', 'registered', 'created'
    const defaultImage = process.env.PUBLIC_URL + '/logo192.png';

    return (
        <Card>
            <CourseImage src={course.imageUrl || course.image_url || defaultImage} alt={course.CourseName} />
            <CardContent>
                <CourseTitle>{course.CourseName}</CourseTitle>
                <CourseDescription>{course.Description}</CourseDescription>
                <CourseMeta>
                    {type === 'public' && (
                        <>
                            <div>
                                <FaStar /> {course.Evaluate ? course.Evaluate.toFixed(1) : 'N/A'}
                            </div>
                            <div>
                                <FaUserGraduate /> {course.NumberOfRegistrations || 0} học viên
                            </div>
                        </>
                    )}
                    {type === 'registered' && (
                        <div>Tiến độ: {course.progress || 0}%</div> // Thêm tiến độ học tập
                    )}
                    {type === 'created' && (
                         <div>
                            <FaUserGraduate /> {course.NumberOfRegistrations || 0} học viên
                        </div>
                    )}
                    {course.IsFree ? <PriceTag>Miễn phí</PriceTag> : <PriceTag>{course.price || '$$$'}</PriceTag>}
                </CourseMeta>
                {type === 'public' && (
                    <ActionButton to={`/courses/${course.CourseID}`}>
                        Xem chi tiết
                    </ActionButton>
                )}
                {type === 'registered' && (
                    <ActionButton to={`/learn/${course.CourseID}`}>Tiếp tục học</ActionButton>
                )}
                {type === 'created' && (
                    <ActionButton to={`/manage-course/${course.CourseID}`} onClick={(e) => onActionClick && onActionClick(course.CourseID)}>
                        Chỉnh sửa khoá học
                    </ActionButton>
                )}
            </CardContent>
        </Card>
    );
};

export default CourseCard;