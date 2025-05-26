const API_URL = "http://localhost:8000";

function mapCourseApiToClient(course) {
    return {
        CourseID: course.course_id,
        CourseName: course.course_name,
        Description: course.description,
        DetailCourse: course.detail_course,
        IsFree: course.is_free,
        IsPublic: course.is_public,
        UserID: course.user_id,
        NumberOfRegistrations: course.number_of_registrations,
        Evaluate: course.evaluate,
        imageUrl: course.image_url || "",
        Chapters: course.chapters || [],
        // Thêm các trường khác nếu cần
    };
}

export const getPublicCourses = async () => {
    const response = await fetch(`${API_URL}/courses?skip=0&limit=100`);
    if (!response.ok) throw new Error("Không thể lấy danh sách khoá học");
    const data = await response.json();
    // Lọc IsPublic nếu backend chưa filter
    return data.filter(course => course.is_public).map(mapCourseApiToClient);
};

export const getUserRegisteredCourses = async (userId) => {
    const response = await fetch(`${API_URL}/registrations?skip=0&limit=100`);
    if (!response.ok) throw new Error("Không thể lấy danh sách khoá học đã đăng ký");
    const registrations = await response.json();
    const userRegs = registrations.filter(reg => reg.user_id === userId || reg.UserID === userId);
    const coursesRes = await fetch(`${API_URL}/courses?skip=0&limit=100`);
    const allCourses = await coursesRes.json();
    return userRegs.map(reg => {
        const course = allCourses.find(c => c.course_id === reg.course_id || c.CourseID === reg.CourseID);
        return course ? { ...mapCourseApiToClient(course), RegistrationDate: reg.registration_date || reg.RegistrationDate } : null;
    }).filter(Boolean);
};

export const getUserCreatedCourses = async (userId) => {
    const response = await fetch(`${API_URL}/courses?skip=0&limit=100`);
    if (!response.ok) throw new Error("Không thể lấy danh sách khoá học đã tạo");
    const data = await response.json();
    return data.filter(course => course.user_id === userId || course.UserID === userId).map(mapCourseApiToClient);
};

export const getCourseDetails = async (courseId) => {
    const response = await fetch(`${API_URL}/courses/${courseId}`);
    if (!response.ok) throw new Error("Không thể lấy chi tiết khoá học");
    const data = await response.json();
    return mapCourseApiToClient(data);
};

export const createCourse = async (newCourseData) => {
    const response = await fetch(`${API_URL}/courses/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newCourseData)
    });
    if (!response.ok) throw new Error("Không thể tạo khoá học");
    return await response.json();
};

export const updateCourse = async (courseId, updatedData) => {
    const response = await fetch(`${API_URL}/courses/${courseId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedData)
    });
    if (!response.ok) throw new Error("Không thể cập nhật khoá học");
    return await response.json();
};