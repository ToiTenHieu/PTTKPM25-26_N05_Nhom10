# 📄 Tài liệu Mô tả Yêu cầu Hệ thống
**Đề tài**: Hệ thống Quản lý Đăng ký Học theo Tín chỉ  

---

## 1. Mục tiêu hệ thống
Hệ thống hỗ trợ quản lý đăng ký học phần theo tín chỉ, giúp sinh viên dễ dàng đăng ký và theo dõi kết quả học tập; giảng viên có thể mở lớp, quản lý điểm; quản trị viên quản lý toàn bộ dữ liệu sinh viên, môn học và khóa học.  

---

## 2. Các Actor chính
- **Sinh viên**  
- **Giảng viên**  
- **Quản trị viên (Admin)**  
- **Hệ thống** (tác nhân phụ trợ, tự động xử lý, phản hồi).  

---

## 3. Các Use Case của hệ thống

### 3.1. Sinh viên
- Đăng ký môn học  
- Hủy đăng ký môn học  
- Xem thời khóa biểu  
- Xem kết quả học tập  

### 3.2. Giảng viên
- Mở lớp học  
- Cập nhật điểm  
- Xem danh sách sinh viên  

### 3.3. Quản trị viên (Admin)
- Quản lý sinh viên  
- Quản lý môn học  
- Quản lý khóa học  

---

## 4. Yêu cầu chức năng (Functional Requirements)
1. Hệ thống cho phép sinh viên đăng ký và hủy đăng ký môn học trong khoảng thời gian quy định.  
2. Hệ thống hiển thị thời khóa biểu của sinh viên theo học kỳ.  
3. Hệ thống hiển thị kết quả học tập và điểm số.  
4. Giảng viên có thể mở lớp học cho môn học.  
5. Giảng viên có thể nhập/cập nhật điểm cho sinh viên.  
6. Giảng viên xem được danh sách sinh viên đã đăng ký lớp.  
7. Quản trị viên có thể thêm, sửa, xóa thông tin sinh viên.  
8. Quản trị viên có thể thêm, sửa, xóa môn học.  
9. Quản trị viên có thể quản lý khóa học (mở, đóng, chỉnh sửa).  

---

## 5. Yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng**: Thời gian phản hồi ≤ 2 giây khi tra cứu thông tin.  
- **Bảo mật**: Yêu cầu đăng nhập để truy cập hệ thống; phân quyền theo vai trò (SV, GV, Admin).  
- **Khả dụng**: Hệ thống hoạt động 24/7, downtime < 1%.  
- **Dễ sử dụng**: Giao diện thân thiện, hỗ trợ tìm kiếm nhanh.  

---

## 6. Mối quan hệ Actor – Use Case

| Actor          | Use Case                              |
|----------------|---------------------------------------|
| **Sinh viên**  | Đăng ký môn học, Hủy đăng ký, Xem TKB, Xem kết quả học tập |
| **Giảng viên** | Mở lớp học, Cập nhật điểm, Xem danh sách SV |
| **Admin**      | Quản lý sinh viên, Quản lý môn học, Quản lý khóa học |

---

## 7. Biểu đồ Use Case (mô tả)
- **Sinh viên** ↔ (Đăng ký môn học, Hủy đăng ký, Xem TKB, Xem kết quả học tập)  
- **Giảng viên** ↔ (Mở lớp học, Cập nhật điểm, Xem danh sách SV)  
- **Admin** ↔ (Quản lý sinh viên, Quản lý môn học, Quản lý khóa học)  

