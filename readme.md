# 📊 Bank Customer Churn – ETL Data Pipeline

## 📑 Mục lục (Table of Contents)

- [📌 1. Giới thiệu](#-1-giới-thiệu)
- [🏗 2. Kiến trúc hệ thống](#-2-kiến-trúc-hệ-thống)
- [📂 3. Cấu trúc dự án](#-3-cấu-trúc-dự-án)
- [🚀 4. Cài đặt & hướng dẫn sử dụng](#-4-cài-đặt--hướng-dẫn-sử-dụng)

---

## 📌 1. Giới thiệu

Dự án này triển khai một **ETL Data Pipeline end-to-end** nhằm phục vụ bài toán  
**phân tích khách hàng rời bỏ (Customer Churn)** trong lĩnh vực ngân hàng.

Hệ thống được xây dựng bằng **Python**, áp dụng tư duy **Lập trình hướng đối tượng (OOP)**  
kết hợp với kiến trúc **Medallion (Bronze → Silver → Gold)** nhằm đảm bảo:

- Tính mở rộng (Scalability)
- Dễ bảo trì (Maintainability)
- Chất lượng và tính nhất quán của dữ liệu

**Nguồn dữ liệu:**  
Dữ liệu thô đa định dạng (**CSV & Excel**) bao gồm thông tin nhân khẩu học, tài chính  
và lịch sử hoạt động của khách hàng.

### ✨ Các đặc điểm chính

#### 🔹 Data Engineering

- **Kiến trúc Medallion & OOP Architecture**
  - Áp dụng các lớp cơ sở trừu tượng:BaseExtractor, BaseTransformer, BaseLoader
  - Giúp pipeline dễ mở rộng và tái sử dụng

- **Bronze Layer**
  - Trích xuất dữ liệu thô từ nhiều nguồn file
  - Giữ nguyên dữ liệu gốc và thêm metadata (`_ingested_at`, `_source`)
- **Silver Layer**
  - Làm sạch dữ liệu (null handling, type casting)
  - Chuẩn hóa và làm giàu dữ liệu (JOIN)
  - Feature Engineering phục vụ phân tích
- **Gold Layer**
  - Chuẩn hóa dữ liệu thành **Star Schema**
  - Tối ưu cho BI & Analytics
#### 🔹Data Analytics

- **Mô hình hóa dữ liệu**: Thiết kế **Star Schema**, Fact trung tâm: `fact_churn`
- **Trực quan hóa**: Dashboard **Power BI** phân tích churn, chân dung khách hàng và yếu tố rủi ro

---

## 🏗 2. Kiến trúc hệ thống

### 2.1 Luồng dữ liệu (Data Flow)

![Flow](etl/flow.png)
### 2.2 Data Modeling

![Data_Model](etl/data_model.png)

---

## 📂 3. Cấu trúc dự án
```text

Bank_Project/
│
├── data/                      # Dữ liệu thô đầu vào
│   ├── Bank_Churn.csv
│   ├── Geography.xlsx
│   ├── Gender.xlsx
│   └── ...
│
├── etl/                       # Mã nguồn ETL
│   ├── core/                  # Base classes
│   │   ├── base_extractor.py
│   │   ├── base_transformer.py
│   │   ├── base_builder.py
│   │   └── base_loader.py
│   │
│   ├── bronze/                # Bronze layer
│   │   └── file_extractor.py
│   │
│   ├── silver/                # Silver layer
│   │   └── customer_transformer.py
│   │
│   ├── gold/                  # Gold layer
│   │   └── star_schema_builder.py
│   │
│   └── loaders/               # Database loaders
│       └── mysql_loader.py
│
├── dashboard/                 # Power BI assets
│   ├── Bank_Churn_Report.pbix
│   └── images/
│
├── run_pipeline.py            # Entry point
└── README.md
```

---
## 🚀 4. Cài đặt & hướng dẫn sử dụng
### 4.1 Yêu cầu tiên quyết
- Python 3.8+

- MySQL Server

- Power BI Desktop (khuyến nghị bản tải từ Web)

- Git


### 4.2 Thiết lập môi trường
**Bước 1:** Clone repository
```powershell

git clone https://github.com/username-cua-ban/bank-churn-etl.git
cd Bank_Project
```
**Bước 2:** Cài đặt thư viện
```powershell
pip install pandas sqlalchemy pymysql openpyxl
```



**Bước 3:** Tạo database
- sql
- CREATE DATABASE bank_db;



**Bước 4:** Cấu hình kết nối
- python
- mysql+pymysql://username:password@host/database
- DB_CONN_STR = "mysql+pymysql://root:your_password@localhost/bank_db"



### 4.3 Chạy pipeline ETL
```powershell
python run_pipeline.py
```


### 4.4 Dashboard Power BI
Trang tổng quan (Executive Overview) cung cấp bức tranh toàn cảnh về tình hình biến động khách hàng và các chỉ số sức khỏe của doanh nghiệp:

- **Các chỉ số hiệu suất chính (KPIs):** Theo dõi tổng số lượng khách hàng, so sánh tỷ lệ khách hàng đang hoạt động (Active), khách hàng không hoạt động và số lượng khách hàng đã rời bỏ (Exit Customer).

- **Phân bổ rủi ro theo nhân khẩu học:** Biểu đồ phân tích tỷ lệ rời bỏ dựa trên Quốc gia (Pháp, Đức, Tây Ban Nha), Giới tính và các Nhóm tuổi.

- **Xu hướng rời bỏ theo thời gian:** Diễn biến tỷ lệ khách hàng rời bỏ qua các năm (2016 - 2019) để nhận diện xu hướng tăng/giảm.

- **Tác động tài chính:** So sánh biến động tổng số dư (Balance) giữa nhóm khách hàng được giữ chân và nhóm đã rời bỏ, giúp đánh giá thiệt hại tài chính.
  
![Churn_Analysis](dashboard/Churn_Analysis.png)

---

Trang phân tích chuyên sâu (Churn Analysis) đi sâu vào các yếu tố và hành vi tương quan dẫn đến quyết định rời bỏ của khách hàng:

- **Tương quan Sản phẩm & Rời bỏ:** Phân tích mối quan hệ giữa số lượng sản phẩm khách hàng sử dụng với tỷ lệ rời bỏ (đặc biệt phát hiện điểm bất thường ở nhóm dùng 3-4 sản phẩm).

- **Phân tích đa chiều (Deep Dive):** So sánh chi tiết tỷ lệ rời bỏ khi kết hợp các yếu tố nhân khẩu học (Tỷ lệ rời bỏ của Nữ giới tại Đức cao bất thường).

- **Phân khúc theo số dư (Balance Segments):** Nhận diện nhóm khách hàng có khoảng số dư tài khoản nào đang có xu hướng rời bỏ cao nhất.

- **Phân bổ khách hàng theo trạng thái (Customer Distribution):** Biểu đồ tròn minh họa cơ cấu khách hàng dựa trên trạng thái Hoạt động (Active) kết hợp với tình trạng Rời bỏ (Exited), giúp nhận diện rõ tỷ trọng khách hàng rời bỏ nằm chủ yếu ở nhóm có hoạt động tích cực hay không tích cực.

- **Ma trận trạng thái hoạt động:** Bảng dữ liệu chi tiết phân loại khách hàng theo quốc gia và số dư để so sánh tỷ lệ Active/Inactive so với lượng rời bỏ thực tế.
  
![Executive_Overview](dashboard/Churn_Analysis.png)

---

Trang khuyến nghị hành động (Recommendation) cung cấp các cảnh báo sớm và đề xuất giải pháp cụ thể cho từng khách hàng:

- **Cảnh báo rủi ro (Critical Alert):** Phân khúc rủi ro cao nhất cần xử lý ngay lập tức Nhóm khách hàng Nữ tại Đức với số dư 100k-150k.

- **Phát hiện bất thường (Anomaly Detection):** Cảnh báo các mẫu hành vi bất thường trong hành trình khách hàng (Tỷ lệ rời bỏ 100% ở nhóm sở hữu 4 sản phẩm).

- **Danh sách hành động khuyến nghị:** Bảng chi tiết từng khách hàng (CustomerID) được gắn mức độ ưu tiên (Priority Level) kèm theo hành động cụ thể (Gửi khảo sát, Gọi điện giữ chân VIP...).

- **Mô phỏng kịch bản (Simulator):** Công cụ giả lập cho phép điều chỉnh tỷ lệ giảm rủi ro mong muốn, từ đó tính toán ngay lập tức số lượng khách hàng có thể giữ lại và dòng tiền (Revenue) được bảo toàn.
  
![Recommendation](dashboard/Recommendation.png)

---# bank-churn
