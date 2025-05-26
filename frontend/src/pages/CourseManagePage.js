import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css'; // Kiểu dáng cho editor soạn thảo

import { useAuth } from '../contexts/AuthContext';
import { getCourseDetails, createCourse, updateCourse } from '../api/courses'; // Mock API

const ManageCourseContainer = styled.div`
    display: flex;
    flex-direction: column;
    min-height: 100vh;
`;

const Content = styled.main`
    flex-grow: 1;
    padding: 40px;
    max-width: 1000px;
    margin: 0 auto;
    width: 100%;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
`;

const PageTitle = styled.h1`
    text-align: center;
    color: #333;
    margin-bottom: 40px;
    font-size: 2.5em;
`;

const StepIndicator = styled.div`
    display: flex;
    justify-content: center;
    margin-bottom: 40px;
    .step {
        padding: 10px 20px;
        border-radius: 25px;
        background-color: #e9ecef;
        color: #666;
        font-weight: 600;
        margin: 0 10px;
        opacity: 0.7;
        &.active {
            background-color: #007bff;
            color: white;
            opacity: 1;
        }
    }
`;

const FormSection = styled.div`
    margin-bottom: 40px;
    h3 {
        font-size: 1.8em;
        color: #333;
        margin-bottom: 25px;
        text-align: center;
    }
`;

const FormGroup = styled.div`
    margin-bottom: 25px;
    label {
        display: block;
        margin-bottom: 10px;
        font-weight: 600;
        color: #555;
        font-size: 1.1em;
    }
    input[type="text"],
    input[type="number"],
    textarea,
    select {
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
    textarea {
        min-height: 100px;
        resize: vertical;
    }
    .quill {
        background-color: #fcfcfc;
        border-radius: 8px;
        .ql-container {
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            min-height: 200px;
        }
        .ql-toolbar {
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            background-color: #eee;
        }
    }
`;

const CheckboxGroup = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    input[type="checkbox"] {
        margin-right: 10px;
        transform: scale(1.2);
    }
    label {
        font-weight: normal;
        color: #555;
        font-size: 1em;
    }
`;

const Actions = styled.div`
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 40px;
    button {
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease;
        &:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    }
    .primary {
        background-color: #007bff;
        color: white;
        &:hover {
            background-color: #0056b3;
        }
    }
    .secondary {
        background-color: #6c757d;
        color: white;
        &:hover {
            background-color: #5a6268;
        }
    }
    .success {
        background-color: #28a745;
        color: white;
        &:hover {
            background-color: #218838;
        }
    }
    .danger {
        background-color: #dc3545;
        color: white;
        &:hover {
            background-color: #c82333;
        }
    }
`;

// Chapter & Part Styling
const ChapterSection = styled.div`
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #fefefe;
`;

const ChapterHeader = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    h4 {
        margin: 0;
        font-size: 1.3em;
        color: #007bff;
    }
    button {
        background: none;
        border: none;
        color: #007bff;
        cursor: pointer;
        font-weight: 600;
        &:hover {
            text-decoration: underline;
        }
    }
`;

const PartsList = styled.ul`
    list-style: none;
    padding: 0;
    margin-top: 15px;
`;

const PartItemStyled = styled.li`
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    padding: 12px 20px;
    margin-bottom: 10px;
    border-radius: 5px;
    span {
        font-weight: 500;
        color: #444;
    }
    div {
        display: flex;
        gap: 10px;
    }
    button {
        background: none;
        border: none;
        color: #007bff;
        cursor: pointer;
        font-weight: 500;
        &:hover {
            color: #0056b3;
        }
        &.delete {
            color: #dc3545;
            &:hover {
                color: #c82333;
            }
        }
    }
`;

const CourseManagePage = () => {
    const { courseId } = useParams(); // Sẽ có nếu là edit, không có nếu là tạo mới
    const navigate = useNavigate();
    const { currentUser, isAuthenticated } = useAuth();
    const [currentStep, setCurrentStep] = useState(1);
    const [courseDetails, setCourseDetails] = useState({
        CourseName: '',
        Description: '',
        DetailCourse: '',
        IsFree: false,
        IsPublic: true,
        UserID: currentUser?.UserID, // Gán UserID mặc định
        CategoryID: '', // Để chọn từ danh mục
        Chapters: [], // Mảng Chapters và Parts
        imageUrl: '', // Thêm trường cho ảnh đại diện
    });
    const [categories, setCategories] = useState([]);
    const [editingChapter, setEditingChapter] = useState(null); // chapterId đang chỉnh sửa
    const [editingPart, setEditingPart] = useState(null); // { chapterId, partId } đang chỉnh sửa
    const [newChapterName, setNewChapterName] = useState('');
    const [newPartData, setNewPartData] = useState({ PartName: '', Document: '', type: 'video' }); // type: 'video', 'text'
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/auth'); // Yêu cầu đăng nhập nếu chưa
            return;
        }

        const fetchCourse = async () => {
            if (courseId) {
                setLoading(true);
                try {
                    const data = await getCourseDetails(courseId);
                    if (data.UserID !== currentUser?.UserID) {
                        setError('Bạn không có quyền chỉnh sửa khóa học này.');
                        setLoading(false);
                        return;
                    }
                    setCourseDetails({
                        ...data,
                        Chapters: data.Chapters || [] // Ensure Chapters is an array
                    });
                } catch (err) {
                    setError('Không thể tải dữ liệu khóa học.');
                }
                setLoading(false);
            } else {
                setLoading(false); // Creating new course
            }
        };

        const fetchCategories = async () => {
            // Mock categories
            setCategories([
                { CategoryID: 'cat1', CategoryName: 'Lập trình Web' },
                { CategoryID: 'cat2', CategoryName: 'Thiết kế đồ họa' },
                { CategoryID: 'cat3', CategoryName: 'Marketing số' },
            ]);
        };

        fetchCourse();
        fetchCategories();
    }, [courseId, isAuthenticated, currentUser, navigate]);

    // Step 1: Handle Basic Course Info
    const handleBasicInfoChange = (e) => {
        const { name, value, type, checked } = e.target;
        setCourseDetails(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSaveBasicInfo = async () => {
        setError('');
        if (!courseDetails.CourseName || !courseDetails.Description || !courseDetails.CategoryID) {
            setError('Vui lòng điền đầy đủ các trường bắt buộc.');
            return;
        }

        try {
            if (courseId) {
                await updateCourse(courseId, courseDetails);
                alert('Cập nhật thông tin cơ bản thành công!');
            } else {
                const newCourse = await createCourse(courseDetails);
                setCourseDetails(newCourse); // Cập nhật state với CourseID mới
                navigate(`/manage-course/${newCourse.CourseID}`, { replace: true }); // Chuyển sang URL mới
                alert('Tạo khóa học thành công! Bây giờ hãy thêm các chương và bài học.');
            }
            setCurrentStep(2); // Chuyển sang bước 2
        } catch (err) {
            setError('Lỗi khi lưu thông tin khóa học: ' + (err.message || ''));
        }
    };

    // Step 2: Handle Chapters & Parts
    const handleAddChapter = () => {
        if (newChapterName.trim()) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: [...prev.Chapters, {
                    ChapterID: `ch_${Date.now()}`, // ID tạm thời
                    ChapterName: newChapterName.trim(),
                    CourseID: courseDetails.CourseID,
                    Parts: []
                }]
            }));
            setNewChapterName('');
        }
    };

    const handleEditChapter = (chapterId) => {
        const chapter = courseDetails.Chapters.find(ch => ch.ChapterID === chapterId);
        if (chapter) {
            setNewChapterName(chapter.ChapterName);
            setEditingChapter(chapterId);
        }
    };

    const handleUpdateChapter = () => {
        if (editingChapter && newChapterName.trim()) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: prev.Chapters.map(ch =>
                    ch.ChapterID === editingChapter ? { ...ch, ChapterName: newChapterName.trim() } : ch
                )
            }));
            setEditingChapter(null);
            setNewChapterName('');
        }
    };

    const handleDeleteChapter = (chapterId) => {
        if (window.confirm('Bạn có chắc chắn muốn xóa chương này và tất cả các bài học trong đó?')) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: prev.Chapters.filter(ch => ch.ChapterID !== chapterId)
            }));
        }
    };

    const handleAddPart = (chapterId) => {
        if (newPartData.PartName.trim() && newPartData.Document.trim()) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: prev.Chapters.map(ch =>
                    ch.ChapterID === chapterId
                        ? {
                            ...ch,
                            Parts: [...ch.Parts, {
                                PartID: `pt_${Date.now()}`, // ID tạm thời
                                PartName: newPartData.PartName.trim(),
                                ChapterID: chapterId,
                                Document: newPartData.Document.trim(),
                                Type: newPartData.type // Lưu loại nội dung (video/text)
                            }]
                        }
                        : ch
                )
            }));
            setNewPartData({ PartName: '', Document: '', type: 'video' });
        } else {
            alert('Vui lòng điền tên bài học và nội dung.');
        }
    };

    const handleEditPart = (chapterId, partId) => {
        const chapter = courseDetails.Chapters.find(ch => ch.ChapterID === chapterId);
        if (chapter) {
            const part = chapter.Parts.find(p => p.PartID === partId);
            if (part) {
                setNewPartData({ PartName: part.PartName, Document: part.Document, type: part.Type || 'video' });
                setEditingPart({ chapterId, partId });
            }
        }
    };

    const handleUpdatePart = () => {
        if (editingPart && newPartData.PartName.trim() && newPartData.Document.trim()) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: prev.Chapters.map(ch =>
                    ch.ChapterID === editingPart.chapterId
                        ? {
                            ...ch,
                            Parts: ch.Parts.map(p =>
                                p.PartID === editingPart.partId
                                    ? { ...p, PartName: newPartData.PartName.trim(), Document: newPartData.Document.trim(), Type: newPartData.type }
                                    : p
                            )
                        }
                        : ch
                )
            }));
            setEditingPart(null);
            setNewPartData({ PartName: '', Document: '', type: 'video' });
        } else {
            alert('Vui lòng điền tên bài học và nội dung.');
        }
    };

    const handleDeletePart = (chapterId, partId) => {
        if (window.confirm('Bạn có chắc chắn muốn xóa bài học này?')) {
            setCourseDetails(prev => ({
                ...prev,
                Chapters: prev.Chapters.map(ch =>
                    ch.ChapterID === chapterId
                        ? { ...ch, Parts: ch.Parts.filter(p => p.PartID !== partId) }
                        : ch
                )
            }));
        }
    };

    const handleFinalSave = async () => {
        setError('');
        try {
            await updateCourse(courseDetails.CourseID, courseDetails); // Lưu toàn bộ chapters/parts
            alert('Lưu khóa học thành công!');
            navigate('/dashboard');
        } catch (err) {
            setError('Lỗi khi lưu khóa học: ' + (err.message || ''));
        }
    };

    if (loading) {
        return (
            <ManageCourseContainer>
                <Header />
                <Content>Đang tải dữ liệu khóa học...</Content>
                <Footer />
            </ManageCourseContainer>
        );
    }

    if (error && !courseDetails.CourseID) { // Only show error if no course loaded/created
        return (
            <ManageCourseContainer>
                <Header />
                <Content><p style={{ color: 'red', textAlign: 'center' }}>{error}</p></Content>
                <Footer />
            </ManageCourseContainer>
        );
    }

    return (
        <ManageCourseContainer>
            <Header />
            <Content>
                <PageTitle>{courseId ? 'Chỉnh sửa Khoá học' : 'Tạo Khoá học mới'}</PageTitle>

                <StepIndicator>
                    <span className={`step ${currentStep === 1 ? 'active' : ''}`}>1. Thông tin cơ bản</span>
                    <span className={`step ${currentStep === 2 ? 'active' : ''}`}>2. Chương & Bài học</span>
                </StepIndicator>

                {error && <p style={{ color: 'red', textAlign: 'center', marginBottom: '20px' }}>{error}</p>}

                {currentStep === 1 && (
                    <FormSection>
                        <h3>Thông tin cơ bản của Khoá học</h3>
                        <FormGroup>
                            <label htmlFor="course-name">Tên khoá học</label>
                            <input
                                type="text"
                                id="course-name"
                                name="CourseName"
                                value={courseDetails.CourseName}
                                onChange={handleBasicInfoChange}
                                required
                            />
                        </FormGroup>
                        <FormGroup>
                            <label htmlFor="course-desc">Mô tả ngắn</label>
                            <textarea
                                id="course-desc"
                                name="Description"
                                value={courseDetails.Description}
                                onChange={handleBasicInfoChange}
                                required
                            ></textarea>
                        </FormGroup>
                        <FormGroup>
                            <label htmlFor="course-detail">Mô tả chi tiết (Nội dung khoá học)</label>
                            <ReactQuill
                                theme="snow"
                                value={courseDetails.DetailCourse}
                                onChange={(content) => setCourseDetails(prev => ({ ...prev, DetailCourse: content }))}
                            />
                        </FormGroup>
                        <FormGroup>
                            <label htmlFor="course-category">Danh mục</label>
                            <select
                                id="course-category"
                                name="CategoryID"
                                value={courseDetails.CategoryID}
                                onChange={handleBasicInfoChange}
                                required
                            >
                                <option value="">-- Chọn danh mục --</option>
                                {categories.map(cat => (
                                    <option key={cat.CategoryID} value={cat.CategoryID}>{cat.CategoryName}</option>
                                ))}
                            </select>
                        </FormGroup>
                        <FormGroup>
                            <label htmlFor="course-image">Ảnh đại diện khoá học (URL)</label>
                            <input
                                type="text" // Hoặc input type="file" cho upload file thật
                                id="course-image"
                                name="imageUrl"
                                value={courseDetails.imageUrl}
                                onChange={handleBasicInfoChange}
                            />
                        </FormGroup>
                        <CheckboxGroup>
                            <input
                                type="checkbox"
                                id="is-free"
                                name="IsFree"
                                checked={courseDetails.IsFree}
                                onChange={handleBasicInfoChange}
                            />
                            <label htmlFor="is-free">Khoá học miễn phí</label>
                        </CheckboxGroup>
                        <CheckboxGroup>
                            <input
                                type="checkbox"
                                id="is-public"
                                name="IsPublic"
                                checked={courseDetails.IsPublic}
                                onChange={handleBasicInfoChange}
                            />
                            <label htmlFor="is-public">Công khai khoá học</label>
                        </CheckboxGroup>
                        <Actions>
                            <button className="primary" onClick={handleSaveBasicInfo}>
                                {courseId ? 'Cập nhật & Tiếp tục' : 'Tạo khoá học & Tiếp tục'}
                            </button>
                        </Actions>
                    </FormSection>
                )}

                {currentStep === 2 && (
                    <FormSection>
                        <h3>Quản lý Chương và Bài học</h3>
                        {!courseDetails.CourseID && (
                            <p style={{textAlign: 'center', color: '#dc3545', marginBottom: '20px'}}>
                                Vui lòng lưu thông tin cơ bản trước khi thêm chương và bài học.
                            </p>
                        )}
                        {courseDetails.CourseID && (
                            <>
                                <FormGroup>
                                    <label htmlFor="new-chapter-name">Tên chương mới</label>
                                    <input
                                        type="text"
                                        id="new-chapter-name"
                                        value={newChapterName}
                                        onChange={(e) => setNewChapterName(e.target.value)}
                                        placeholder="Ví dụ: Chương 1: Giới thiệu"
                                    />
                                    {editingChapter ? (
                                        <Actions style={{justifyContent: 'flex-start', marginTop: '10px'}}>
                                            <button className="primary" onClick={handleUpdateChapter}>Cập nhật Chương</button>
                                            <button className="secondary" onClick={() => {setEditingChapter(null); setNewChapterName('');}}>Hủy</button>
                                        </Actions>
                                    ) : (
                                        <Actions style={{justifyContent: 'flex-start', marginTop: '10px'}}>
                                            <button className="success" onClick={handleAddChapter} disabled={!newChapterName.trim()}>Thêm Chương</button>
                                        </Actions>
                                    )}
                                </FormGroup>

                                {courseDetails.Chapters.map(chapter => (
                                    <ChapterSection key={chapter.ChapterID}>
                                        <ChapterHeader>
                                            <h4>{chapter.ChapterName}</h4>
                                            <div>
                                                <button onClick={() => handleEditChapter(chapter.ChapterID)}>Sửa</button>
                                                <button className="delete" onClick={() => handleDeleteChapter(chapter.ChapterID)}>Xoá</button>
                                            </div>
                                        </ChapterHeader>

                                        <PartsList>
                                            {chapter.Parts.map(part => (
                                                <PartItemStyled key={part.PartID}>
                                                    <span>{part.PartName} ({part.Type === 'video' ? 'Video' : 'Text'})</span>
                                                    <div>
                                                        <button onClick={() => handleEditPart(chapter.ChapterID, part.PartID)}>Sửa</button>
                                                        <button className="delete" onClick={() => handleDeletePart(chapter.ChapterID, part.PartID)}>Xoá</button>
                                                    </div>
                                                </PartItemStyled>
                                            ))}
                                        </PartsList>

                                        {editingPart && editingPart.chapterId === chapter.ChapterID ? (
                                            // Form chỉnh sửa Part
                                            <FormGroup>
                                                <label htmlFor={`part-name-${chapter.ChapterID}`}>Tên bài học</label>
                                                <input
                                                    type="text"
                                                    id={`part-name-${chapter.ChapterID}`}
                                                    value={newPartData.PartName}
                                                    onChange={(e) => setNewPartData(prev => ({ ...prev, PartName: e.target.value }))}
                                                    placeholder="Tên bài học"
                                                    required
                                                />
                                                <label htmlFor={`part-type-${chapter.ChapterID}`}>Loại nội dung</label>
                                                <select
                                                    id={`part-type-${chapter.ChapterID}`}
                                                    value={newPartData.type}
                                                    onChange={(e) => setNewPartData(prev => ({ ...prev, type: e.target.value }))}
                                                >
                                                    <option value="video">Video (YouTube URL)</option>
                                                    <option value="text">Văn bản</option>
                                                </select>

                                                {newPartData.type === 'video' ? (
                                                    <><label htmlFor={`part-document-${chapter.ChapterID}`}>URL Video YouTube</label>
                                                    <input
                                                        type="text"
                                                        id={`part-document-${chapter.ChapterID}`}
                                                        value={newPartData.Document}
                                                        onChange={(e) => setNewPartData(prev => ({ ...prev, Document: e.target.value }))}
                                                        placeholder="https://www.youtube.com/watch?v=..."
                                                        required
                                                    /></>
                                                ) : (
                                                    <><label htmlFor={`part-document-text-${chapter.ChapterID}`}>Nội dung văn bản</label>
                                                    <ReactQuill
                                                        theme="snow"
                                                        value={newPartData.Document}
                                                        onChange={(content) => setNewPartData(prev => ({ ...prev, Document: content }))}
                                                        placeholder="Nội dung bài học dạng văn bản..."
                                                    /></>
                                                )}
                                                <Actions style={{justifyContent: 'flex-start', marginTop: '10px'}}>
                                                    <button className="primary" onClick={handleUpdatePart}>Cập nhật Bài học</button>
                                                    <button className="secondary" onClick={() => {setEditingPart(null); setNewPartData({ PartName: '', Document: '', type: 'video' });}}>Hủy</button>
                                                </Actions>
                                            </FormGroup>
                                        ) : (
                                            // Form thêm Part mới
                                            <FormGroup>
                                                <label htmlFor={`new-part-name-${chapter.ChapterID}`}>Thêm bài học mới</label>
                                                <input
                                                    type="text"
                                                    id={`new-part-name-${chapter.ChapterID}`}
                                                    value={newPartData.PartName}
                                                    onChange={(e) => setNewPartData(prev => ({ ...prev, PartName: e.target.value }))}
                                                    placeholder="Tên bài học mới"
                                                />
                                                <label htmlFor={`new-part-type-${chapter.ChapterID}`}>Loại nội dung</label>
                                                <select
                                                    id={`new-part-type-${chapter.ChapterID}`}
                                                    value={newPartData.type}
                                                    onChange={(e) => setNewPartData(prev => ({ ...prev, type: e.target.value }))}
                                                >
                                                    <option value="video">Video (YouTube URL)</option>
                                                    <option value="text">Văn bản</option>
                                                </select>
                                                {newPartData.type === 'video' ? (
                                                    <><label htmlFor={`new-part-document-${chapter.ChapterID}`}>URL Video YouTube</label>
                                                    <input
                                                        type="text"
                                                        id={`new-part-document-${chapter.ChapterID}`}
                                                        value={newPartData.Document}
                                                        onChange={(e) => setNewPartData(prev => ({ ...prev, Document: e.target.value }))}
                                                        placeholder="https://www.youtube.com/watch?v=..."
                                                    /></>
                                                ) : (
                                                    <><label htmlFor={`new-part-document-text-${chapter.ChapterID}`}>Nội dung văn bản</label>
                                                    <ReactQuill
                                                        theme="snow"
                                                        value={newPartData.Document}
                                                        onChange={(content) => setNewPartData(prev => ({ ...prev, Document: content }))}
                                                        placeholder="Nội dung bài học dạng văn bản..."
                                                    /></>
                                                )}
                                                <Actions style={{justifyContent: 'flex-start', marginTop: '10px'}}>
                                                    <button className="success" onClick={() => handleAddPart(chapter.ChapterID)} disabled={!newPartData.PartName.trim() || !newPartData.Document.trim()}>Thêm Bài học</button>
                                                </Actions>
                                            </FormGroup>
                                        )}
                                    </ChapterSection>
                                ))}
                            </>
                        )}
                        <Actions>
                            <button className="secondary" onClick={() => setCurrentStep(1)}>Quay lại</button>
                            <button className="primary" onClick={handleFinalSave} disabled={!courseDetails.CourseID}>
                                Hoàn tất & Xuất bản
                            </button>
                        </Actions>
                    </FormSection>
                )}
            </Content>
            <Footer />
        </ManageCourseContainer>
    );
};

export default CourseManagePage;