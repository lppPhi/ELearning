import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { useParams } from 'react-router-dom';
import Header from '../components/common/Header'; // Có thể dùng Header tối giản hơn cho trang này
import VideoPlayer from '../components/VideoPlayer'; // Component để nhúng YouTube
import ReactQuill from 'react-quill'; // Hoặc thư viện rich text editor khác
import 'react-quill/dist/quill.bubble.css'; // Kiểu dáng cho editor đọc
import Footer from '../components/common/Footer'; // <-- Add this line

// Mock API
import { getCourseDetails } from '../api/courses';

const LearningLayout = styled.div`
    display: flex;
    min-height: calc(100vh - 70px); /* Trừ chiều cao header */
    background-color: #f8f9fa;
`;

const Sidebar = styled.aside`
    width: 300px;
    background-color: #ffffff;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    padding: 20px 0;
    overflow-y: auto; /* Cuộn nếu nội dung dài */
`;

const CourseTitleLearning = styled.h2`
    font-size: 1.8em;
    color: #333;
    padding: 0 20px 15px;
    margin-top: 0;
    border-bottom: 1px solid #eee;
    margin-bottom: 20px;
`;

const ChapterList = styled.ul`
    list-style: none;
    padding: 0;
`;

const ChapterItem = styled.li`
    margin-bottom: 10px;
    h3 {
        font-size: 1.2em;
        color: #007bff;
        padding: 10px 20px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        &:hover {
            background-color: #e6f0ff;
        }
    }
`;

const PartList = styled.ul`
    list-style: none;
    padding: 0 0 0 20px;
`;

const PartItem = styled.li`
    padding: 10px 20px;
    cursor: pointer;
    background-color: ${({ $isActive }) => ($isActive ? '#e6f0ff' : 'transparent')};
    color: ${({ $isActive }) => ($isActive ? '#0056b3' : '#555')};
    border-left: ${({ $isActive }) => ($isActive ? '3px solid #007bff' : '3px solid transparent')};
    transition: all 0.2s ease;
    &:hover {
        background-color: #f0f8ff;
    }
`;

const MainContentArea = styled.main`
    flex-grow: 1;
    padding: 30px;
    display: flex;
    flex-direction: column;
`;

const PartHeader = styled.div`
    margin-bottom: 20px;
    h2 {
        font-size: 2.2em;
        color: #333;
        margin-bottom: 10px;
    }
    p {
        font-size: 1.1em;
        color: #666;
    }
`;

const NavigationButtons = styled.div`
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
    button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1em;
        &:disabled {
            background-color: #a0c3e7;
            cursor: not-allowed;
        }
    }
`;

const CourseLearningPage = () => {
    const { courseId } = useParams();
    const [courseData, setCourseData] = useState(null);
    const [currentPart, setCurrentPart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!courseId || courseId === "undefined") {
            setError("Không tìm thấy mã khoá học trên đường dẫn URL.");
            setLoading(false);
            return;
        }
        const fetchCourseData = async () => {
            setLoading(true);
            try {
                const data = await getCourseDetails(courseId);
                // Đảm bảo Chapters là mảng
                data.Chapters = Array.isArray(data.Chapters) ? data.Chapters : [];
                setCourseData(data);
                if (data.Chapters.length > 0 && Array.isArray(data.Chapters[0].Parts) && data.Chapters[0].Parts.length > 0) {
                    setCurrentPart(data.Chapters[0].Parts[0]);
                }
            } catch (err) {
                setError("Không thể lấy chi tiết khoá học");
            }
            setLoading(false);
        };
        fetchCourseData();
    }, [courseId]);

    const findPartIndex = (part) => {
        let partIndex = -1;
        let chapterIndex = -1;
        for (let c = 0; c < courseData.Chapters.length; c++) {
            const chapter = courseData.Chapters[c];
            for (let p = 0; p < chapter.Parts.length; p++) {
                if (chapter.Parts[p].PartID === part.PartID) {
                    chapterIndex = c;
                    partIndex = p;
                    break;
                }
            }
            if (partIndex !== -1) break;
        }
        return { chapterIndex, partIndex };
    };

    const goToNextPart = () => {
        if (!currentPart) return;
        const { chapterIndex, partIndex } = findPartIndex(currentPart);

        if (chapterIndex === -1 || partIndex === -1) return; // Should not happen

        const currentChapter = courseData.Chapters[chapterIndex];
        if (partIndex < currentChapter.Parts.length - 1) {
            setCurrentPart(currentChapter.Parts[partIndex + 1]);
        } else if (chapterIndex < courseData.Chapters.length - 1) {
            const nextChapter = courseData.Chapters[chapterIndex + 1];
            if (nextChapter.Parts.length > 0) {
                setCurrentPart(nextChapter.Parts[0]);
            }
        }
    };

    const goToPreviousPart = () => {
        if (!currentPart) return;
        const { chapterIndex, partIndex } = findPartIndex(currentPart);

        if (chapterIndex === -1 || partIndex === -1) return; // Should not happen

        if (partIndex > 0) {
            const currentChapter = courseData.Chapters[chapterIndex];
            setCurrentPart(currentChapter.Parts[partIndex - 1]);
        } else if (chapterIndex > 0) {
            const prevChapter = courseData.Chapters[chapterIndex - 1];
            if (prevChapter.Parts.length > 0) {
                setCurrentPart(prevChapter.Parts[prevChapter.Parts.length - 1]);
            }
        }
    };

    const isFirstPart = currentPart && findPartIndex(currentPart).chapterIndex === 0 && findPartIndex(currentPart).partIndex === 0;
    const isLastPart = currentPart && findPartIndex(currentPart).chapterIndex === courseData?.Chapters.length - 1 &&
                      findPartIndex(currentPart).partIndex === courseData.Chapters[findPartIndex(currentPart).chapterIndex]?.Parts.length - 1;


    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                Đang tải khóa học...
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ textAlign: 'center', padding: '50px', color: 'red' }}>
                <b>ERROR</b>
                <div>{error}</div>
            </div>
        );
    }

    if (!courseData) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                Không tìm thấy khóa học này.
            </div>
        );
    }

    return (
        <>
            <Header /> {/* Hoặc một header tối giản hơn */}
            <LearningLayout>
                <Sidebar>
                    <CourseTitleLearning>{courseData.CourseName}</CourseTitleLearning>
                    <ChapterList>
                        {(Array.isArray(courseData.Chapters) ? courseData.Chapters : []).map(chapter => (
                            <ChapterItem key={chapter.ChapterID}>
                                <h3>{chapter.ChapterName}</h3>
                                <PartList>
                                    {(Array.isArray(chapter.Parts) ? chapter.Parts : []).map(part => (
                                        <PartItem
                                            key={part.PartID}
                                            $isActive={currentPart && currentPart.PartID === part.PartID}
                                            onClick={() => setCurrentPart(part)}
                                        >
                                            {part.PartName}
                                        </PartItem>
                                    ))}
                                </PartList>
                            </ChapterItem>
                        ))}
                    </ChapterList>
                </Sidebar>
                <MainContentArea>
                    {currentPart ? (
                        <>
                            <PartHeader>
                                <h2>{currentPart.PartName}</h2>
                                {/* Có thể hiển thị mô tả ngắn của Part ở đây */}
                            </PartHeader>
                            {/* Giả định Document là URL video hoặc rich text */}
                            {currentPart.Document && currentPart.Document.startsWith('http') ? (
                                <VideoPlayer youtubeUrl={currentPart.Document} />
                            ) : (
                                <div className="quill-reader"> {/* Sử dụng class để Quill áp dụng style đọc */}
                                    <ReactQuill
                                        value={currentPart.Document || ''}
                                        readOnly={true}
                                        theme="bubble" // Dùng bubble theme cho chế độ đọc
                                    />
                                </div>
                            )}

                            <NavigationButtons>
                                <button onClick={goToPreviousPart} disabled={isFirstPart}>
                                    Bài học trước
                                </button>
                                <button onClick={goToNextPart} disabled={isLastPart}>
                                    Bài học tiếp theo
                                </button>
                            </NavigationButtons>
                        </>
                    ) : (
                        <p>Vui lòng chọn một bài học để bắt đầu.</p>
                    )}
                </MainContentArea>
            </LearningLayout>
            <Footer />
        </>
    );
};

export default CourseLearningPage;