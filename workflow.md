# QUY TRÌNH THỰC THI CHUẨN (STANDARD OPERATING PROCEDURE - SOP)
Mã quy trình: SOP-DANANG-RENTAL-02 (Phiên bản Ponytail Ultra - Tách Bạch Dữ Liệu & Giao Bộ Lọc Cho Người Dùng)

Triết lý cốt lõi: **Agent chỉ làm nhiệm vụ thu thập sự thật khách quan (không đoán mò, không gán ghép giá giả định), ghi nhận đầy đủ nguồn gốc thô, số điện thoại, địa chỉ cụ thể. Mọi việc phân loại và lọc chi tiết sẽ do người dùng chủ động điều khiển qua Dashboard HTML.**

---

### BƯỚC 1: TRUY CẬP & VÉT CẠN NGUỒN SỐNG (LIVE INGESTION)
1. Đọc danh mục URL từ `sources.json`.
2. Mở phiên duyệt trang thực tế qua browser/web fetch.
3. Thu thập mọi bài đăng và bình luận phát sinh mới trong ngày từ DOM thực tế.
4. Ghi toàn bộ dữ liệu thô vào `phong_tro_da_nang_Sheet1_Goc.csv` và Tab "Nội Dung Thô Đa Nguồn" trên Dashboard HTML:
   - Cột bắt buộc: [Mã Tin, Tiêu Đề / Nội Dung Quét Được, Nguồn Quét, Link Nguồn, Người Đăng / SĐT, Giá Đề Xuất, Địa Điểm, Bình Luận / Đánh Giá Bước Đầu].

---

### BƯỚC 2: KIỂM SOÁT TÍNH XÁC THỰC (ZERO-ASSUMPTION VERIFICATION)
1. **Tuyệt đối không đoán giá (No Inferred Price):**
   - Nếu bài đăng trên Facebook hoặc Chợ Tốt không ghi giá công khai -> **Ghi rõ: "Giá Thỏa thuận / Cần hỏi chủ"**, cấm tiệt việc tự điền số tiền 2.2M hoặc bất kỳ con số suy đoán nào.
2. **Khóa cứng thời gian `<= 7 ngày`:**
   - Đọc ngày đăng hoặc mốc thời gian cập nhật của bài viết. Quá 7 ngày -> Loại bỏ ngay.
3. **Kiểm tra trạng thái còn phòng:**
   - Có nhãn `tin_het_han`, "đã cho thuê", hoặc bài viết bị xóa -> Loại ngay.
4. **4 Trường Dữ Liệu Xác Thực Bắt Buộc:**
   - Link Canonical sống 100% (bấm vào là mở đúng bài viết).
   - Số điện thoại người đăng / chủ trọ.
   - Địa chỉ cụ thể (tên đường, phường, quận).
   - Mốc thời gian đăng thực tế.

---

### BƯỚC 3: ĐỒNG BỘ DỮ LIỆU ĐẦU RA (OUTPUT SYNCHRONIZATION)
1. Đồng bộ tệp `dashboard_phong_tro.html` thành Cổng Khảo Sát Công Khai (Public Portal):
   - **Dữ liệu thô nguyên bản làm nền tảng:** Không gán ép tiêu chí cá nhân (như mốc 222 Nguyễn Hữu Thọ). Dữ liệu thể hiện khách quan theo Quận/Huyện, tên đường, loại hình, diện tích, giá niêm yết/thỏa thuận.
   - **Cockpit Filters Toàn Diện:** Cung cấp bộ lọc đa chiều để bất kỳ ai cũng có thể tự lọc theo nhu cầu riêng:
     + Tìm kiếm từ khóa (tên đường, tiện ích, SĐT).
     + Phân loại Quận/Huyện (Hải Châu, Cẩm Lệ, Thanh Khê, Liên Chiểu, Sơn Trà, Ngũ Hành Sơn).
     + Loại hình lưu trú (Nhà C4 nguyên căn, Phòng trọ riêng khép kín).
     + Khoảng giá (Dưới 2M, 2M - 2.5M, Trên 2.5M, Thỏa thuận).
     + Diện tích (< 20m², 20 - 50m², > 50m²).
     + Tiện ích đặc thù (Cho nuôi mèo/thú cưng, Có điều hòa, Có gác lửng/đúc, Không chung chủ/giờ tự do).
2. Cập nhật `phong_tro_da_nang_Sheet1_Goc.csv` và `phong_tro_da_nang_Sheet2_DatChuan.csv`.
3. Cập nhật `phong_tro_da_nang.xls` (SpreadsheetML native).
