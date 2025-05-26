// dataMocks.js (mock dữ liệu)

// Mock data definitions
export const mockUsers = [
    {
        UserID: 'user_1',
        FullName: 'Nguyen Van A',
        Email: 'a@gmail.com',
        Password: '123456'
    },
    {
        UserID: 'user_2',
        FullName: 'Tran Thi B',
        Email: 'b@gmail.com',
        Password: '123456'
    }
];

export const mockCourses = [
    {
        CourseID: 'course_1',
        CourseName: 'ReactJS Cơ bản',
        Description: 'Khoá học ReactJS cho người mới bắt đầu.',
        DetailCourse: '<p>Chi tiết khoá học ReactJS...</p>',
        IsFree: true,
        IsPublic: true,
        UserID: 'user_1',
        CategoryID: 'cat1',
        NumberOfRegistrations: 10,
        Evaluate: 4.5,
        imageUrl: '',
        Chapters: []
    },
    {
        CourseID: 'course_2',
        CourseName: 'Thiết kế Đồ hoạ Photoshop',
        Description: 'Học Photoshop từ cơ bản đến nâng cao.',
        DetailCourse: '<p>Chi tiết khoá học Photoshop...</p>',
        IsFree: false,
        IsPublic: true,
        UserID: 'user_2',
        CategoryID: 'cat2',
        NumberOfRegistrations: 5,
        Evaluate: 4.0,
        imageUrl: '',
        Chapters: []
    }
];

export const mockRegisteredCourses = [
    {
        UserID: 'user_1',
        CourseID: 'course_2',
        RegistrationDate: '2023-06-01'
    }
];

// Giả lập API call
export const getPublicCourses = async () => {
    await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
    return mockCourses.filter(c => c.IsPublic);
};

export const getUserRegisteredCourses = async (userId) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const userRegs = mockRegisteredCourses.filter(reg => reg.UserID === userId);
    return userRegs.map(reg => {
        const course = mockCourses.find(c => c.CourseID === reg.CourseID);
        return { ...course, RegistrationDate: reg.RegistrationDate, progress: Math.floor(Math.random() * 101) }; // Add mock progress
    }).filter(Boolean); // Remove undefined if course not found
};

export const getUserCreatedCourses = async (userId) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockCourses.filter(c => c.UserID === userId);
};

export const getCourseDetails = async (courseId) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const course = mockCourses.find(c => c.CourseID === courseId);
    // Kèm theo Chapters và Parts giả lập
    if (course) {
        return {
            ...course,
            Chapters: [
                { ChapterID: 'ch1', ChapterName: 'Chương 1: Khởi đầu', CourseID: course.CourseID,
                    Parts: [
                        { PartID: 'pt1_1', PartName: 'Bài 1.1: Giới thiệu khoá học', ChapterID: 'ch1', Document: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', Type: 'video' },
                        { PartID: 'pt1_2', PartName: 'Bài 1.2: Các khái niệm cơ bản', ChapterID: 'ch1', Document: '<p>Đây là nội dung <strong>văn bản</strong> của bài học.</p>', Type: 'text' }
                    ]
                },
                { ChapterID: 'ch2', ChapterName: 'Chương 2: Nâng cao', CourseID: course.CourseID,
                    Parts: [
                        { PartID: 'pt2_1', PartName: 'Bài 2.1: Kỹ thuật nâng cao', ChapterID: 'ch2', Document: 'https://www.youtube.com/watch?v=oHg5SJYRHA0', Type: 'video' }
                    ]
                }
            ]
        };
    }
    throw new Error('Course not found');
};

const genId = (prefix) => `${prefix}_${Date.now()}_${Math.floor(Math.random()*10000)}`;

export const createCourse = async (newCourseData) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const newCourse = { ...newCourseData, CourseID: genId('course'), NumberOfRegistrations: 0, Evaluate: 0 };
    mockCourses.push(newCourse); // Thêm vào mock data
    return newCourse;
};

export const updateCourse = async (courseId, updatedData) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const index = mockCourses.findIndex(c => c.CourseID === courseId);
    if (index !== -1) {
        mockCourses[index] = { ...mockCourses[index], ...updatedData };
        return mockCourses[index];
    }
    throw new Error('Course not found for update');
};

export const getCategories = async () => {
     await new Promise(resolve => setTimeout(resolve, 300));
     return [
        { CategoryID: 'cat1', CategoryName: 'Lập trình Web' },
        { CategoryID: 'cat2', CategoryName: 'Thiết kế đồ họa' },
        { CategoryID: 'cat3', CategoryName: 'Marketing số' },
     ]
}