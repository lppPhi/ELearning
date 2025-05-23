// Xử lý chuyển trang, load header/footer, layout
window.addEventListener('DOMContentLoaded', () => {
    loadComponent('components/header.html', '#header');
    loadComponent('components/footer.html', '#footer');
    route();
});

function loadComponent(url, selector) {
    fetch(url).then(r => r.text()).then(html => {
        document.querySelector(selector).innerHTML = html;
    });
}

function route() {
    // Đơn giản: route theo hash
    const page = location.hash.replace('#', '') || 'home';
    loadPage(page);
}

window.addEventListener('hashchange', route);

function loadPage(page) {
    fetch(`pages/${page}.html`).then(r => {
        if (r.ok) return r.text();
        return fetch('pages/home.html').then(r2 => r2.text());
    }).then(html => {
        document.querySelector('main').innerHTML = html;
        if (page === 'home') renderHome();
        if (page === 'course-list') renderCourseList();
        // ...thêm các trang khác nếu cần
    });
}

// Trang chủ: hiển thị khoá học phổ biến
async function renderHome() {
    try {
        const courses = await fetchCourses();
        const container = document.getElementById('popular-courses');
        if (!container) return;
        if (!courses || courses.length === 0) {
            container.innerHTML = '<div style="text-align:center;color:#888;">Chưa có khoá học nào.</div>';
            return;
        }
        container.innerHTML = courses.slice(0, 4).map(course => `
            <div class="card course-card">
                <img src="assets/logo.png" alt="Course" style="width:100px;height:100px;object-fit:cover;border-radius:8px;">
                <h3>${course.course_name}</h3>
                <p>${course.description || ''}</p>
                <div class="course-info">
                    <span>Đánh giá: <b>${course.evaluate ?? 'Chưa có'}</b></span>
                    <span>Đăng ký: <b>${course.number_of_registrations ?? 0}</b></span>
                </div>
                <a class="btn" href="#course-detail?id=${course.course_id}">Xem chi tiết</a>
            </div>
        `).join('');
    } catch (err) {
        console.error('Lỗi lấy khoá học:', err);
        const container = document.getElementById('popular-courses');
        if (container) container.innerHTML = '<div style="color:red;">Không thể tải danh sách khoá học.</div>';
    }
}

// Danh sách khoá học
async function renderCourseList() {
    try {
        const courses = await fetchCourses();
        const container = document.getElementById('course-list');
        if (!container) return;
        if (!courses || courses.length === 0) {
            container.innerHTML = '<div style="text-align:center;color:#888;">Chưa có khoá học nào.</div>';
            return;
        }
        container.innerHTML = courses.map(course => `
            <div class="card course-card">
                <h3>${course.course_name}</h3>
                <p>${course.description || ''}</p>
                <div class="course-info">
                    <span>Đánh giá: <b>${course.evaluate ?? 'Chưa có'}</b></span>
                    <span>Đăng ký: <b>${course.number_of_registrations ?? 0}</b></span>
                </div>
                <a class="btn" href="#course-detail?id=${course.course_id}">Xem chi tiết</a>
            </div>
        `).join('');
    } catch (err) {
        console.error('Lỗi lấy khoá học:', err);
        const container = document.getElementById('course-list');
        if (container) container.innerHTML = '<div style="color:red;">Không thể tải danh sách khoá học.</div>';
    }
}
