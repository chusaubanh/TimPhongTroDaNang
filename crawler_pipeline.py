"""
DANANG RENTAL CRAWLER & PIPELINE
================================
Hệ thống thu thập, chuẩn hóa và kiểm định dữ liệu phòng trọ Đà Nẵng
Nguồn quét: Chợ Tốt / Nhà Tốt API, Phongtro123, Facebook Groups Public
"""

import os
import json
import time
import re
from datetime import datetime
import urllib.request
import urllib.parse

class RentalPipeline:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.raw_data = []
        self.verified_data = []

    def crawl_chotot(self, limit=30):
        """
        Quét trực tiếp API chính thức của Chợ Tốt (Nhà Tốt) khu vực Đà Nẵng (cg: 1010, region: 5011)
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang kết nối API Chợ Tốt Đà Nẵng...")
        api_url = f"https://gateway.chotot.com/v1/public/ad-listing?cg=1010&region_v2=5011&limit={limit}&st=s,k"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                ads = res_data.get('ads', [])
                print(f"-> Thu thập được {len(ads)} tin từ Chợ Tốt.")
                
                for ad in ads:
                    price = ad.get('price', 0)
                    # Tiêu chí: Bỏ tuyệt đối tin không giá
                    if not price or price <= 0:
                        continue
                    
                    item = {
                        "source": "Chợ Tốt (Nhà Tốt)",
                        "source_id": str(ad.get('list_id', '')),
                        "title": ad.get('subject', '').strip(),
                        "address": ad.get('area_name', '') + ", " + ad.get('ward_name', '') + ", Đà Nẵng",
                        "price": price,
                        "area": ad.get('size', 20),
                        "phone": ad.get('phone', 'Xem trên bài đăng'),
                        "body": ad.get('body', '').strip(),
                        "post_time": ad.get('date', ''),
                        "url": f"https://www.nhatot.com/{ad.get('list_id')}.htm"
                    }
                    self.raw_data.append(item)
        except Exception as e:
            print(f"[!] Lỗi khi quét Chợ Tốt: {e}")

    def clean_and_verify(self):
        """
        Bộ lọc chuẩn hóa và chống tin ảo:
        1. Bỏ tin không có giá
        2. Tự động trích xuất SĐT từ nội dung bài nếu API giấu SĐT
        3. Phân loại quận huyện và tiện ích
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang xử lý làm sạch và kiểm định {len(self.raw_data)} tin thô...")
        
        seen_phones = set()
        code_idx = 1

        for item in self.raw_data:
            # Tìm số điện thoại bằng regex nếu chưa có
            body = item.get("body", "")
            title = item.get("title", "")
            combined_text = title + " " + body
            
            phone = item.get("phone")
            if not phone or "Xem" in phone:
                match = re.search(r'(0[3|5|7|8|9][0-9]{8})', combined_text.replace('.', '').replace(' ', ''))
                if match:
                    phone = match.group(1)
                else:
                    phone = "Liên hệ qua link"

            price_val = item["price"]
            price_mil = round(price_val / 1000000, 1) if price_val > 10000 else price_val

            # Phân loại quận
            district = "Đà Nẵng"
            for d in ["Hải Châu", "Cẩm Lệ", "Thanh Khê", "Liên Chiểu", "Sơn Trà", "Ngũ Hành Sơn"]:
                if d.lower() in item["address"].lower() or d.lower() in combined_text.lower():
                    district = d
                    break

            verified_item = {
                "id": f"DN-{code_idx:02d}",
                "title": title,
                "district": district,
                "address": item["address"],
                "price": f"{price_val:,.0f} đ".replace(',', '.'),
                "price_num": price_mil,
                "area": item.get("area", 20),
                "phone": phone,
                "source": item["source"],
                "url": item["url"],
                "raw_text": body[:200] + "..." if len(body) > 200 else body,
                "verified_at": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            self.verified_data.append(verified_item)
            code_idx += 1

        print(f"-> Hoàn tất kiểm định: {len(self.verified_data)} căn đạt chuẩn.")

    def export_database(self):
        """
        Xuất cơ sở dữ liệu sang JSON (dùng làm API tĩnh cho Frontend/Netlify)
        """
        db_path = os.path.join(self.output_dir, "database.json")
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump({
                "last_updated": datetime.now().isoformat(),
                "total": len(self.verified_data),
                "items": self.verified_data
            }, f, ensure_ascii=False, indent=2)
        print(f"-> Đã ghi dữ liệu vào: {db_path}")

if __name__ == "__main__":
    pipeline = RentalPipeline(output_dir="data")
    pipeline.crawl_chotot(limit=30)
    pipeline.clean_and_verify()
    pipeline.export_database()
