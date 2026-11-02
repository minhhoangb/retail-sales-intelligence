# Retail Sales Intelligence

Group project môn DHV301 – Option A: Retail / Sales Intelligence. Quy trình: chuẩn bị dữ liệu → EDA → hồi quy tuyến tính → dashboard Power BI → báo cáo và thuyết trình.

> **Trạng thái:** phần **Data Cleaning (D1–D8) + EDA (D9–D14)** và **Hồi quy tuyến tính (M1–M10)** đã hoàn thành và kiểm chứng. Mục còn thực hiện là dashboard Power BI (Hoàng).

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
| Dữ liệu sạch | [`data_cleaned/superstore_clean.csv`](data_cleaned/superstore_clean.csv) — 9.993 dòng × 21 cột, `utf-8-sig`, ngày `yyyy-mm-dd` (tạo từ notebook 01) |

## Quy trình

| Bước | Sản phẩm | Vị trí |
|---|---|---|
| 1. Làm sạch và EDA | Notebook chính, dữ liệu sạch, data dictionary, báo cáo insight | [`01_data_cleaning_eda.ipynb`](notebooks/01_data_cleaning_eda.ipynb) (**D1–D14 xong**), [`data_dictionary.md`](docs/data_dictionary.md), [`eda_insights.md`](reports/eda_insights.md) |
| 2. Hồi quy tuyến tính | Mô hình, chỉ số đánh giá, diễn giải | [`02_linear_regression.ipynb`](notebook/02_linear_regression.ipynb) (**M1–M10 xong**) |
| 3. Dashboard | File PBIX, ghi chú KPI/DAX, ảnh chụp | `pbix/`, [`kpi_dax_notes.md`](docs/kpi_dax_notes.md), `screenshots/` |

## Kết quả

- **Làm sạch dữ liệu (D1–D8):** ✅ xong. File sạch 9.993 dòng × 21 cột, đối chiếu 9.994 − 1 = 9.993. Chi tiết ở [`data_dictionary.md`](docs/data_dictionary.md) (bảng quyết định làm sạch) và notebook [`01_data_cleaning_eda.ipynb`](notebooks/01_data_cleaning_eda.ipynb).
- **EDA (D9–D14):** ✅ xong. Notebook 01 chạy từ đầu đến cuối **0 lỗi**, **11 biểu đồ**. 4 câu hỏi phân tích đều có câu trả lời kèm số liệu chứng minh, biểu đồ, diễn giải kinh doanh và giới hạn. Tóm tắt ở [`eda_insights.md`](reports/eda_insights.md), giả định & giới hạn ở [`assumptions_limitations.md`](docs/assumptions_limitations.md).

  **Tóm tắt 4 câu hỏi:**

  | Câu hỏi | Kết quả chính |
  |---|---|
  | **Q1** Xu hướng theo tháng/năm | Doanh thu **+51,5%**, lợi nhuận **+88,5%**, số đơn **+74,1%** (2014→2017) — nhưng **AOV giảm 13,0%**. Mùa vụ cực mạnh: tháng 11–12 chiếm **29,5%** doanh thu. |
  | **Q2** Nhóm sản phẩm | Tốt nhất **`Technology`** (biên LN 17,40%); kém nhất **`Furniture`** — doanh thu chỉ kém 11% nhưng lợi nhuận kém 87%, biên LN **2,49%**, 33,6% dòng lỗ. |
  | **Q3** Khu vực & phân khúc | Khác nhau rõ về **quy mô**, gần như không khác về **AOV** (vùng 426–484 USD; phân khúc 449–472 USD). `Central` biên LN thấp nhất (7,92%); `Home Office` cao nhất (14,05%). |
  | **Q4** Mức giảm giá | **Không** liên hệ với doanh thu (r = −0,028). Liên hệ **phân tầng theo ngưỡng** với lợi nhuận: biên LN +29,51% ở mức 0% → âm từ **30%**; 6 mức 0,32–0,80 có **100% dòng lỗ**. r = −0,219 (R² ≈ 4,8%) — **mối liên hệ quan sát, không phải nhân quả**. |
- **Hồi quy tuyến tính (M1–M10):** ✅ xong. Notebook [`02_linear_regression.ipynb`](notebook/02_linear_regression.ipynb) chạy hoàn tất **0 lỗi**, gồm biểu đồ thực tế vs dự đoán, biểu đồ phần dư và bảng phân tích hệ số. Chi tiết tại [`Hieu_dhv.md`](Hieu_dhv.md) và [`assumptions_limitations.md`](docs/assumptions_limitations.md) (mục 5).
  - **Biến Y:** `Sales` (Doanh thu mặt hàng).
  - **Biến X:** `Quantity`, `Discount`, `Sub-Category`, `Region`, `Segment`, `Ship Mode`, `Order_Year`, `Order_Month` (mã hóa One-Hot trong Pipeline; loại bỏ `Profit`, mã định danh và chuỗi ngày thô).
  - **Chia tập Train/Test:** `GroupShuffleSplit` theo `Order ID` (80:20, `random_state=42`) để chống rò rỉ dữ liệu khi một đơn có nhiều dòng (Train: 4.007 đơn / 7.958 dòng; Test: 1.002 đơn / 2.035 dòng; 0 đơn trùng lặp).
  - **Kết quả đánh giá trên tập kiểm tra:**
    - **Mô hình mốc (DummyRegressor - Mean):** $MAE = 273,26$ USD, $RMSE = 605,88$ USD, $R^2 = -0,0003$.
    - **Hồi quy đơn biến (`Quantity`):** $MAE = 261,03$ USD, $RMSE = 591,28$ USD, $R^2 = 0,0473$.
    - **Hồi quy đa biến (Pipeline OLS):** $MAE = 216,54$ USD (giảm 56,72 USD sai số so với mốc, tương đương giảm ~20,8%), $RMSE = 502,05$ USD, $R^2 = 0,3131$ (giải thích 31,31% phương sai).
    - **Mở rộng Log-Sales (kiểm tra ngoại lai):** Mô hình với $\ln(1+Sales)$ cho $R^2_{\log} = 0,5701$, hạ sai số $MAE$ trên USD gốc xuống $165,31$ USD.
  - **Yếu tố liên hệ rõ nhất:** Nhóm thiết bị kỹ thuật cao `Copiers` ($\beta \approx +2.035,40$ USD) và `Machines` ($\beta \approx +1.392,03$ USD) có liên hệ mạnh nhất tới doanh thu; `Discount` có liên hệ âm ($\beta \approx -303,48$ USD); `Quantity` có liên hệ dương ($\beta \approx +57,47$ USD/đơn vị). Vùng địa lý và phân khúc khách hàng có mức độ liên hệ rất thấp ($|\beta| < 50$ USD).
  - **Kết luận câu hỏi 5:** Mô hình đa biến ước lượng kết quả bán hàng vượt trội hơn rõ rệt so với mô hình mốc dự đoán trung bình. Độ phù hợp $R^2 \approx 31,31\%$ phản ánh đúng bản chất dữ liệu bán lẻ thiếu thông tin giá niêm yết đơn vị (`Unit Price`); mô hình phù hợp để phân tích xu hướng và tương quan, không dùng để dự báo cá thể.
- **KPI:** 11 measure; **66/66 kết quả DAX trên Power BI Desktop khớp phép tính độc lập trong 6 ngữ cảnh**. Toàn bộ: doanh thu **2.296.919,49 USD**, lợi nhuận **286.409,08 USD**, **5.009 đơn**, biên lợi nhuận **12,47%**, AOV **458,56 USD**. Xem [`kpi_dax_notes.md`](docs/kpi_dax_notes.md) và [`kpi_validation.csv`](docs/kpi_validation.csv).
- **Dashboard:** đã có [project Power BI](pbix/RetailSales.pbip) gồm 3 trang cho câu hỏi 1–4, Calendar và nguồn CSV sạch; Refresh đã chạy trên Desktop. **Còn xuất PBIX, kiểm tra hiển thị cuối, ảnh chụp và kiểm tra thông điệp với thành viên khác**, chưa hoàn thành toàn bộ DoD. Cách mở và xuất ở [`pbix/README.md`](pbix/README.md).

### Tóm tắt quyết định làm sạch

| Vấn đề | Số dòng | Xử lý |
|---|---:|---|
| Bản ghi trùng lặp hoàn toàn (bỏ `Row ID`) | 1 | Xoá `Row ID` 3407, giữ `Row ID` 3406 |
| Mã bưu chính mất số 0 đầu (4 chữ số) | 438 | `zfill(5)`, giữ kiểu chuỗi |
| `Customer Name` / `Customer ID` (PII) | 9.993 | Thay bằng mã giả tất định `CUST-001`…`CUST-793` |
| Giao dịch lỗ (`Profit` âm) | 1.871 | **Giữ nguyên** — là giao dịch thật, xoá sẽ làm sai lệch câu hỏi 4 |
| Khoảng trắng thừa ở `Product Name` | 16 | `str.strip()` |

**Không** có cột nào bị bỏ, thêm hay đổi tên. Ba cột đổi kiểu dữ liệu (`Order Date`, `Ship Date` → `datetime64`; `Postal Code` giữ là chuỗi).

## Giả định, giới hạn và dữ liệu cá nhân

Xem [`assumptions_limitations.md`](docs/assumptions_limitations.md) và [`privacy_note.md`](docs/privacy_note.md).

## Khai báo hỗ trợ AI

| Công cụ | Nội dung hỗ trợ | Nhóm kiểm tra thế nào |
|---|---|---|
| Claude Code | Gợi ý dataset, tạo khung thư mục và file mẫu | Xem các gợi ý đã được chuyển thành phần Data Cleaning và EDA trong notebook 01 |
| Cursor (AI Agent) | Hỗ trợ viết code Data Cleaning (D1–D8) và EDA (D9–D14), sinh notebook, kiểm chứng số liệu bằng script độc lập | Mọi con số trong báo cáo đều được **in ra từ dữ liệu** trong notebook; các điểm nghi ngờ (ví dụ ngưỡng giảm giá) đã được **kiểm chứng lại** bằng script độc lập trước khi ghi vào tài liệu |
| Codex | Hỗ trợ tạo project Power BI, Power Query, 11 DAX measure, bố cục 3 trang và tài liệu KPI | Đã Refresh bằng Power BI Desktop; đối chiếu 66 kết quả DAX thật với phép tính CSV dùng Decimal, tất cả PASS; phần xem cuối và ảnh chụp còn chờ |

## Cấu trúc thư mục

```text
data_raw/          Dữ liệu gốc (không chỉnh sửa)
data_cleaned/      Dữ liệu đã làm sạch dùng cho hồi quy và dashboard
notebooks/         Notebook làm sạch và EDA (01_data_cleaning_eda.ipynb)
notebook/          Notebook hồi quy tuyến tính (02_linear_regression.ipynb)
reports/           Báo cáo insight EDA dạng văn bản (eda_insights.md)
pbix/              File Power BI
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
jupyter notebook notebooks
```

Chạy notebook `notebooks/01_data_cleaning_eda.ipynb` trước để tạo dữ liệu sạch (Phần I) và chạy EDA (Phần II), sau đó chạy `notebook/02_linear_regression.ipynb`.

Notebook 01 gồm 11 mục: **1. Introduction → 2. Import Libraries → 3. Load Cleaned Dataset → 4. Data Overview → 5. Descriptive Statistics → 6. Group Comparison → 7. Relationship Analysis → 8. Time Series Analysis → 9. Business Insights → 10. Assumptions and Limitations → 11. Conclusion.** Phần Data Cleaning (D1–D8) nằm ở mục 1.1–1.7 và được giữ nguyên.

> **Yêu cầu khi đọc kết quả EDA:** số đơn hàng luôn đếm bằng `nunique("Order ID")`; AOV = tổng `Sales` ÷ số `Order ID` khác nhau; mọi phát hiện là **mối liên hệ quan sát** trên dữ liệu lịch sử 2014–2017, **không phải** quan hệ nhân quả và **không phải** kết quả dự báo tương lai.

> **Lưu ý khi đọc file sạch:**
> ```python
> df = pd.read_csv(
>     "data_cleaned/superstore_clean.csv",
>     encoding="utf-8-sig",                    # file có BOM
>     dtype={"Postal Code": str},              # tránh mất số 0 đầu
>     parse_dates=["Order Date", "Ship Date"],
> )
> ```
> - `Customer Name` và `Customer ID` đã được thay bằng **mã giả** `CUST-001`…`CUST-793` (xem [`privacy_note.md`](docs/privacy_note.md)).
> - `Order ID` có hai tiền tố `CA-`/`US-` không nhất quán — **đừng** suy ra bang hoặc năm từ nó.
> - Số đơn hàng phải đếm bằng `nunique("Order ID")`, không phải số dòng.

## Phân công

Xem [`role_allocation.md`](docs/role_allocation.md).
