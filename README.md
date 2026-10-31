# Retail Sales Intelligence

Group project môn DHV301 – Option A: Retail / Sales Intelligence. Quy trình: chuẩn bị dữ liệu → EDA → hồi quy tuyến tính → dashboard Power BI → báo cáo và thuyết trình.

> **Trạng thái:** mới có khung. Các mục `TODO` do nhóm hoàn thiện.

## Mục tiêu

- **Đề tài:** Retail / Sales Intelligence – phân tích hiệu quả bán hàng của Superstore giai đoạn 2014–2017, có sử dụng hồi quy tuyến tính.
- **Người dùng:** Quản lý kinh doanh của doanh nghiệp bán lẻ.
- **Phạm vi:** Dữ liệu bán hàng tại Hoa Kỳ từ 01/2014 đến 12/2017, xem theo thời gian, sản phẩm, khu vực và phân khúc khách hàng. Bài phân tích mô tả và tìm mối liên hệ; không dự báo tương lai và không kết luận quan hệ nhân quả.
- **Tính khả thi:** Dataset có đủ cột thời gian, sản phẩm, khu vực, phân khúc, `Sales`, `Quantity`, `Discount`, `Profit` để trả lời cả 5 câu hỏi.

**Câu hỏi phân tích**

1. Doanh thu, lợi nhuận và số đơn hàng thay đổi thế nào theo tháng và năm?
2. Nhóm sản phẩm nào hoạt động tốt nhất và kém nhất về doanh thu và lợi nhuận?
3. Khu vực và phân khúc khách hàng khác nhau thế nào về doanh thu, lợi nhuận và giá trị đơn trung bình?
4. Mức giảm giá có mối liên hệ thế nào với doanh thu và lợi nhuận?
5. Mô hình hồi quy tuyến tính ước lượng kết quả bán hàng tốt đến đâu trên dữ liệu chưa dùng để huấn luyện, và những yếu tố nào có liên hệ rõ nhất?

## Dữ liệu nguồn

| Mục | Thông tin |
|---|---|
| File | [`data_raw/Sample - Superstore.csv`](data_raw/Sample%20-%20Superstore.csv) (không chỉnh sửa file gốc) |
| Nguồn | [Superstore Dataset – Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| Quy mô | 9.994 dòng, 21 cột, 5.009 đơn hàng |
| Một dòng là | Một mặt hàng trong đơn hàng, nên số đơn phải đếm `Order ID` khác nhau |
| Bảng mã | Windows-1252 (cp1252), không phải UTF-8 |
| Dữ liệu sạch | `data_cleaned/superstore_clean.csv` (TODO: tạo từ notebook 01) |

## Quy trình

| Bước | Sản phẩm | Vị trí |
|---|---|---|
| 1. Làm sạch và EDA | Notebook chính, dữ liệu sạch, data dictionary | [`01_data_preparation_eda.ipynb`](notebook/01_data_preparation_eda.ipynb), [`data_dictionary.md`](docs/data_dictionary.md) |
| 2. Hồi quy tuyến tính | Mô hình, chỉ số đánh giá, diễn giải | [`02_linear_regression.ipynb`](notebook/02_linear_regression.ipynb) |
| 3. Dashboard | File PBIX, ghi chú KPI/DAX, ảnh chụp | `pbix/`, [`kpi_dax_notes.md`](docs/kpi_dax_notes.md), `screenshots/` |
| 4. Trình bày | Slide 7–10 trang | `slides/` |

## Kết quả

- **EDA:** TODO
- **Hồi quy tuyến tính:** TODO (biến Y, biến X, MAE, RMSE, R² trên tập kiểm tra, so với mốc dự đoán trung bình)
- **KPI:** TODO (tóm tắt từ [`kpi_dax_notes.md`](docs/kpi_dax_notes.md))
- **Dashboard:** TODO

## Giả định, giới hạn và dữ liệu cá nhân

Xem [`assumptions_limitations.md`](docs/assumptions_limitations.md) và [`privacy_note.md`](docs/privacy_note.md).

## Khai báo hỗ trợ AI

| Công cụ | Nội dung hỗ trợ | Nhóm kiểm tra thế nào |
|---|---|---|
| Claude Code | Gợi ý dataset, tạo khung thư mục và file mẫu | TODO |

## Cấu trúc thư mục

```text
data_raw/          Dữ liệu gốc
data_cleaned/      Dữ liệu đã làm sạch dùng cho hồi quy và dashboard
notebook/          Notebook làm sạch, EDA và hồi quy tuyến tính
pbix/              File Power BI
slides/            Slide thuyết trình
docs/              Data dictionary, KPI, giả định, quyền riêng tư, phân công
screenshots/       Ảnh mô hình dữ liệu và dashboard
milestones/        Bằng chứng từng mốc nếu giảng viên yêu cầu
```

## Cách chạy

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
jupyter notebook notebook
```

Chạy notebook `01` trước để tạo dữ liệu sạch, sau đó chạy `02`.

## Phân công

Xem [`role_allocation.md`](docs/role_allocation.md).
