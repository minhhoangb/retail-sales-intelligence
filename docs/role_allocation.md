# Phân công nhiệm vụ nhóm – Retail Sales Intelligence (DHV301)

Vai trò theo đề (được phép chồng lấn): Project lead / problem framing, Data preparation lead, EDA and visualization lead, BI dashboard lead. Cả nhóm phải hiểu toàn bộ logic dự án và cùng tham gia thuyết trình.

| Thành viên | Vai trò | Việc phụ trách | Sản phẩm bàn giao | Trạng thái |
|---|---|---|---|:---:|
| **Hưng** | Data preparation lead & EDA lead | Làm sạch dữ liệu (D1–D8), Thống kê mô tả & Khám phá dữ liệu EDA (D9–D14), trả lời Q1–Q4 | `notebooks/01_data_cleaning_eda.ipynb`, `data_cleaned/superstore_clean.csv`, `docs/data_dictionary.md`, `reports/eda_insights.md`, `Hung_dhv.md` | **Hoàn thành** |
| **Hiếu** | Machine Learning / Regression lead | Xây dựng mô hình hồi quy tuyến tính (M1–M10), kiểm định giả định & phần dư, trả lời Q5 | `notebook/02_linear_regression.ipynb`, `Hieu_dhv.md`, `docs/assumptions_limitations.md` (mục 5) | **Hoàn thành** |
| **Hoàng** | BI dashboard lead & Project lead | Xây dựng mô hình dữ liệu Power BI, DAX measure, thiết kế dashboard 3 trang, tài liệu KPI | `pbix/RetailSales.pbip`, `docs/kpi_dax_notes.md`, `docs/kpi_validation.csv`, `screenshots/` | **Đang thực hiện** |

---

## Bảng theo dõi tiến độ công việc của Hiếu (M1 – M10)

| Mã | Nhiệm vụ | Đầu ra | Trạng thái |
| :---: | :--- | :--- | :---: |
| **M1** | Xác nhận loại hồi quy: Hồi quy đa biến trọng tâm, đối chiếu đơn biến | Ghi ở đầu notebook `02_linear_regression.ipynb` | ✅ Hoàn thành |
| **M2** | Chọn biến đích $Y$ (`Sales`) và các biến đầu vào $X$ (loại trừ biến rò rỉ, mã định danh) | Bảng biến kèm lý do tại Mục 1 notebook 02 | ✅ Hoàn thành |
| **M3** | Chia tập Train/Test theo `Order ID` (GroupShuffleSplit, 80:20, `random_state=42`) | Code chia dữ liệu tại Mục 2 notebook 02 | ✅ Hoàn thành |
| **M4** | Xây dựng mô hình mốc DummyRegressor (Mean tập Train) | Code & kết quả tại Mục 3 notebook 02 | ✅ Hoàn thành |
| **M5** | Huấn luyện hồi quy tuyến tính với Pipeline (OneHotEncoder chỉ fit trên Train) | Pipeline tại Mục 4 notebook 02 | ✅ Hoàn thành |
| **M6** | Đánh giá trên tập kiểm tra bằng MAE, RMSE, R² (so sánh Baseline vs Đơn biến vs Đa biến) | Bảng đối sánh tại Mục 5 notebook 02 | ✅ Hoàn thành |
| **M7** | Biểu đồ Actual vs Predicted, Đồ thị phần dư, Phân phối phần dư & kiểm tra ngoại lai | 3 biểu đồ tại Mục 6 notebook 02, mở rộng log1p | ✅ Hoàn thành |
| **M8** | Diễn giải hệ số hồi quy theo ngôn ngữ nghiệp vụ ("có mối liên hệ") | Bảng hệ số tại Mục 7 notebook 02 | ✅ Hoàn thành |
| **M9** | Trả lời Câu hỏi 5; kết luận và nêu rõ các giới hạn mô hình | Mục 8 notebook 02, `assumptions_limitations.md`, `README.md` | ✅ Hoàn thành |
| **M10** | Chạy lại toàn bộ trên file sạch của Hưng (`superstore_clean.csv`) bằng Restart & Run All | Notebook 02 thực thi 100% không lỗi | ✅ Hoàn thành |
