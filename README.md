# CỔNG THÔNG TIN KHẢO SÁT PHÒNG TRỌ ĐÀ NẴNG (DANANG RENTAL INDEX)

Hệ thống mã nguồn mở tự động thu thập, kiểm định dữ liệu phòng trọ / căn hộ / nhà cấp 4 tại TP. Đà Nẵng, loại bỏ tin ảo giấu giá, hỗ trợ cộng đồng xác thực phòng đã thuê / đặt cọc theo thời gian thực.

---

## 🏗️ CẤU TRÚC HỆ THỐNG

Dự án được xây dựng theo kiến trúc **Serverless Data Pipeline + Static Jamstack**:

```text
├── .github/workflows/
│   └── crawl.yml             # GitHub Action tự động cào dữ liệu định kỳ mỗi ngày
├── crawler_pipeline.py       # Bộ máy Crawler & Data Cleaning (Chợ Tốt, Phongtro123, FB)
├── data/
│   └── database.json         # Cơ sở dữ liệu phòng trọ chuẩn hóa (JSON API cho Frontend)
├── phong_tro_da_nang_Sheet1_Goc.csv      # Bảng dữ liệu thô đối soát
├── phong_tro_da_nang_Sheet2_DatChuan.csv # Bảng dữ liệu đạt chuẩn đã duyệt
├── index.html                # Giao diện Web chính (Architectural Cockpit, tối ưu Mobile)
└── README.md                 # Tài liệu hệ thống
```

---

## ⚡ CƠ CHẾ HOẠT ĐỘNG

1. **Crawler Pipeline (`crawler_pipeline.py`)**:
   - Quét dữ liệu từ API Chợ Tốt / Nhà Tốt (region Đà Nẵng) và các hội nhóm.
   - **Quy tắc làm sạch khắt khe:** Loại bỏ 100% tin không có giá ("Thỏa thuận", "IB"), trích xuất số điện thoại chính chủ bằng Regex, phân loại quận huyện và diện tích.
   - Xuất dữ liệu sạch về `data/database.json`.

2. **Tự động hóa (GitHub Actions)**:
   - File `.github/workflows/crawl.yml` chạy tự động vào mỗi sáng để cập nhật các tin đăng mới nhất trong vòng 7 ngày.
   - Khi có dữ liệu mới, GitHub Action tự động commit và trigger Netlify build lại web.

3. **Giao diện & Tương tác Cộng đồng (`index.html`)**:
   - Được thiết kế theo chuẩn responsive, hỗ trợ chế độ Bottom-sheet Drawer trên điện thoại.
   - Tích hợp cơ chế **Kiểm chứng cộng đồng**: Người dùng sau khi gọi điện thoại có thể bấm đổi trạng thái (Còn phòng / Đã cọc / Đã thuê) và để lại ghi chú cảnh báo.

---

## 🚀 HƯỚNG DẪN TRIỂN KHAI LÊN NETLIFY

1. Push mã nguồn lên repo GitHub:
   ```bash
   git init
   git branch -M main
   git add .
   git commit -m "feat: Khoi tao he thong Danang Rental Pipeline"
   git remote add origin https://github.com/chusaubanh/TimPhongTroDaNang.git
   git push -u origin main --force
   ```
2. Đăng nhập [Netlify](https://app.netlify.com/), chọn **Add new site** -> **Import an existing project** -> Kết nối GitHub và chọn repo `TimPhongTroDaNang`.
3. Nhấn **Deploy** (Web sẽ tự động online sau 15 giây).
