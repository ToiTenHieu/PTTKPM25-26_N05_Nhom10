# 📚 Hệ thống Quản lý Thư viện Online

## 🎯 Mục tiêu hệ thống
Hệ thống hỗ trợ quản lý thư viện trực tuyến:
- Người dùng có thể tìm kiếm, mượn, trả và đánh giá sách.
- Quản trị viên quản lý sách, người dùng và hoạt động mượn – trả.
- Hệ thống cung cấp báo cáo, thống kê và gửi thông báo tự động.

---

## 👥 Các Actor chính
- **Người dùng (User / Độc giả)**
- **Quản trị viên (Admin)**
- **Hệ thống** (tác nhân phụ trợ: xử lý, gửi thông báo)

---

## 📌 Use Case

### Người dùng (User)
- Đăng ký / Đăng nhập
- Tìm kiếm sách
- Xem danh sách và chi tiết sách
- Mượn sách
- Trả sách
- Gia hạn sách
- Viết đánh giá / nhận xét

### Quản trị viên (Admin)
- Quản lý sách (thêm, cập nhật, xóa)
- Quản lý người dùng (tạo, khóa, mở tài khoản)
- Quản lý phiếu mượn – trả
- Xem báo cáo thống kê (sách mượn nhiều, tồn kho, người dùng vi phạm)

---

## ⚙️ Yêu cầu chức năng (Functional Requirements)
- Hệ thống cho phép người dùng đăng ký/đăng nhập tài khoản.
- Người dùng tìm kiếm sách theo tên, tác giả, thể loại.
- Người dùng mượn/trả/gia hạn sách trong thời gian quy định.
- Người dùng có thể viết nhận xét, đánh giá sách.
- Quản trị viên quản lý dữ liệu sách và người dùng.
- Quản trị viên theo dõi phiếu mượn – trả và xuất báo cáo.

---

## 🔒 Yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng**: Thời gian phản hồi ≤ 2 giây khi tra cứu.
- **Bảo mật**: Mật khẩu mã hóa, phân quyền User/Admin.
- **Khả dụng**: Hoạt động 24/7, downtime < 1%.
- **Thân thiện**: Giao diện dễ sử dụng, hỗ trợ tìm kiếm nhanh.
- **Mở rộng**: Hỗ trợ số lượng lớn sách và người dùng.

---

## 🔗 Mối quan hệ Actor – Use Case

| **Actor**    | **Use Case**                                                                 |
|--------------|------------------------------------------------------------------------------|
| Người dùng   | Đăng ký/Đăng nhập, Tìm kiếm sách, Xem chi tiết, Mượn, Trả, Gia hạn, Đánh giá |
| Quản trị viên| Quản lý sách, Quản lý người dùng, Quản lý mượn – trả, Xem báo cáo           |

---

## 📊 Biểu đồ Use Case (mô tả)
- **Người dùng** ↔ (Đăng ký/Đăng nhập, Tìm kiếm sách, Xem chi tiết, Mượn, Trả, Gia hạn, Đánh giá)  
- **Admin** ↔ (Quản lý sách, Quản lý người dùng, Quản lý mượn – trả, Xem báo cáo)  
