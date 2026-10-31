# Data dictionary

**Nguồn:** `data_raw/Sample - Superstore.csv` (9.994 dòng × 21 cột, bảng mã cp1252, **không bị chỉnh sửa**)  
**Đầu ra:** `data_cleaned/superstore_clean.csv` (9.993 dòng × 21 cột, `utf-8-sig`, ngày `yyyy-mm-dd`)  
**Công cụ tạo:** [`notebooks/01_data_cleaning_eda.ipynb`](../notebooks/01_data_cleaning_eda.ipynb) — mục 4 (kiểm tra) và mục 5 (làm sạch)  
**Người phụ trách:** Hưng

> **Quy ước bàn giao** (đã chốt với Hiếu và Hoàng trong `Hung_dhv.md`): đường dẫn cố định, bảng mã UTF-8 kèm BOM, ngày dạng `yyyy-mm-dd`, **giữ nguyên tên 21 cột**, không ghi index.

---

## 1. Bối cảnh: một dòng là gì?

Mỗi dòng trong dataset là **một mặt hàng (line item) trong một đơn hàng**, **không phải** một đơn hàng.

| Đặc điểm | Số lượng |
|---|---|
| Dòng dữ liệu (gốc) | 9.994 |
| Đơn hàng (`Order ID` khác nhau) | **5.009** |
| Sản phẩm (`Product ID` khác nhau) | 1.862 |
| Khách hàng (`Customer ID` khác nhau) | 793 |

**Hệ quả quan trọng:** mọi phép tính "số đơn hàng" phải dùng `nunique("Order ID")`, **không** được đếm số dòng. Ví dụ tháng 11/2017 có 459 dòng nhưng chỉ **261 đơn hàng**.

---

## 2. Mô tả 21 cột

Cột "Kiểu gốc" là kết quả đọc CSV bằng pandas (`encoding="cp1252"`, `dtype={"Postal Code": str}`), trước mọi thao tác làm sạch.

| # | Cột | Kiểu gốc | Kiểu trong file sạch | Mô tả | Ví dụ | Giá trị thiếu (gốc → sạch) | Xử lý đã áp dụng |
|---:|---|---|---|---|---|---|---|
| 1 | `Row ID` | int64 | int64 | Số thứ tự dòng trong file gốc, liên tục 1–9.994, duy nhất | `1` | 0 → 0 | Giữ nguyên. Dùng làm khóa định danh dòng; không đưa vào mô hình hồi quy. |
| 2 | `Order ID` | str | str | Mã đơn hàng, định dạng `AA-YYYY-NNNNNN`. Tiền tố không nhất quán: `CA-` (8.308 dòng) và `US-` (1.686 dòng) | `CA-2016-152156` | 0 → 0 | Giữ nguyên. Ghi nhận bất thường tiền tố và 7 dòng lệch năm — xem [`assumptions_limitations.md`](assumptions_limitations.md). |
| 3 | `Order Date` | str (`M/d/yyyy`) | datetime64 | Ngày đặt hàng. Khoảng 2014-01-03 → 2017-12-30 | `11/8/2016` → `2016-11-08` | 0 → 0 | `pd.to_datetime(format="%m/%d/%Y", errors="coerce")`. 0 `NaT`. Định dạng tường minh vì `M/d/yyyy` mơ hồ. |
| 4 | `Ship Date` | str (`M/d/yyyy`) | datetime64 | Ngày giao hàng. Tối đa 2018-01-05 (đơn đặt cuối 12/2017 giao sang 2018) | `11/11/2016` → `2016-11-11` | 0 → 0 | Như trên. 0 `NaT`, 0 dòng vi phạm `Ship Date < Order Date`. |
| 5 | `Ship Mode` | str | str | Phương thức vận chuyển, 4 giá trị | `Second Class` | 0 → 0 | Giữ nguyên. |
| 6 | `Customer ID` | str | str | Mã định danh khách hàng, dạng `AA-NNNNN`. Quan hệ 1–1 với `Customer Name` | `CG-12520` → `CUST-144` | 0 → 0 | **Giá trị thay bằng mã giả tất định** `CUST-001`…`CUST-793`. Giữ nguyên số khách hàng và cột. Xem [`privacy_note.md`](privacy_note.md). |
| 7 | `Customer Name` | str | str | Tên khách hàng. 793 tên, 30 tên không theo quy tắc Title Case (chủ yếu do họ có tiền tố `Mc`/`Mac`/`De`/`La`) | `Claire Gute` → `CUST-144` | 0 → 0 | **Giá trị thay bằng mã giả** (PII). Xem [`privacy_note.md`](privacy_note.md). |
| 8 | `Segment` | str | str | Phân khúc khách hàng: `Consumer`, `Corporate`, `Home Office` | `Consumer` | 0 → 0 | Giữ nguyên. |
| 9 | `Country` | str | str | Quốc gia. Chỉ có `United States` (duy nhất) | `United States` | 0 → 0 | Giữ nguyên. Không thông tin địa lý quốc tế. |
| 10 | `City` | str | str | Thành phố, 531 giá trị | `Henderson` | 0 → 0 | Giữ nguyên. Loại bỏ khoảng trắng thừa nếu có (không có). |
| 11 | `State` | str | str | Tiểu bang, 49 giá trị | `Kentucky` | 0 → 0 | Giữ nguyên. |
| 12 | `Postal Code` | str (đọc kiểu số sẽ mất số 0) | str | Mã bưu chính Hoa Kỳ, **luôn 5 ký tự** | `04240` (gốc `42420`) | 0 → 0 | **Thêm số `0` đầu bằng `zfill(5)` cho 438 dòng**. Giữ kiểu chuỗi, **không** chuyển thành số nguyên. Chi tiết ở mục 3. |
| 13 | `Region` | str | str | Vùng: `Central`, `East`, `South`, `West` | `South` | 0 → 0 | Giữ nguyên. |
| 14 | `Product ID` | str | str | Mã sản phẩm, định dạng `AAA-BB-NNNNNNNN`. 1.862 mã | `FUR-BO-10001798` | 0 → 0 | Giữ nguyên. Lưu ý: 16 tên sản phẩm dùng chung nhiều `Product ID` → **gom nhóm theo tên có thể gộp nhầm**. |
| 15 | `Category` | str | str | Nhóm sản phẩm: `Furniture`, `Office Supplies`, `Technology` | `Furniture` | 0 → 0 | Giữ nguyên. |
| 16 | `Sub-Category` | str | str | Nhóm sản phẩm con, 17 giá trị | `Bookcases` | 0 → 0 | Giữ nguyên. |
| 17 | `Product Name` | str | str | Tên sản phẩm, 1.850 tên | `Bush Somerset Collection Bookcase` | 0 → 0 | `str.strip()` cho **16 dòng** có khoảng trắng thừa ở cuối. |
| 18 | `Sales` | float64 | float64 | Doanh thu của dòng. min 0,444 – max 22.638,48 – TB 229,85. Lệch phải mạnh | `261.96` | 0 → 0 | Giữ nguyên. Giá trị lớn là hàng hóa giá trị cao hợp lý (máy photocopy Canon, thiết bị hội nghị Cisco, ghế da), **không** phải nhiễu. || 19 | `Quantity` | int64 | int64 | Số lượng bán. Giá trị 1–14 | `2` | 0 → 0 | Giữ nguyên. |
| 20 | `Discount` | float64 | float64 | Mức giảm giá, 12 mức từ 0,0 đến 0,8 | `0.0` | 0 → 0 | Giữ nguyên. |
| 21 | `Profit` | float64 | float64 | Lợi nhuận của dòng. min −6.599,978 – max 8.399,976 – TB 28,66. **1.870 dòng âm** trong file sạch (18,71%); file gốc có 1.871 dòng (18,72%) | `41.9136` | 0 → 0 | Giữ nguyên, **không xóa**. Là giao dịch thật từ giảm giá sâu — xem mục 3. |

### Tóm tắt kiểu dữ liệu trong file sạch

| Kiểu | Số cột | Danh sách |
|---|---:|---|
| `int64` | 2 | `Row ID`, `Quantity` |
| `float64` | 3 | `Sales`, `Discount`, `Profit` |
| `datetime64` | 2 | `Order Date`, `Ship Date` |
| `str` | 14 | còn lại (kể cả `Postal Code`) |

---

## 3. Cleaning Decision Log

Bảng quyết định làm sạch — **mọi** thay đổi đều có số lượng và lý do. Nguồn: mục 6.7 của notebook 01.

| # | Issue | Number of records | Action | Reason |
|---:|---|---:|---|---|
| 1 | **Bản ghi trùng lặp hoàn toàn** (bỏ qua `Row ID`) | **1** | Xoá `Row ID` 3407, giữ `Row ID` 3406 | 20/20 cột còn lại trùng khớp tuyệt đối (`Sales` 281,372; `Profit` −12,0588; cùng đơn `US-2014-150119`). Giữ bản ghi đầu tiên theo thứ tự gốc. |
| 2 | **Mã bưu chính mất số 0 đầu** (chỉ còn 4 chữ số) | **438** | Thêm số `0` đầu bằng `zfill(5)`; giữ kiểu chuỗi, không chuyển thành số nguyên | Cả 5 bước kiểm chứng đều ủng hộ: (1) đúng 438 dòng; (2) thuộc 6 bang dùng mã bắt đầu bằng 0 (MA, NJ, CT, RI, NH, ME); (3) mỗi `(City, State)` có đúng 1 mã 4 chữ số; (4) mã khôi phục không trùng mã 5 chữ số đã có; (5) file gốc **đã giữ** số 0 ở mã `05408` (Burlington, Vermont) → cơ chế mất số 0 là không nhất quán. |
| 3 | **Thông tin định danh cá nhân** (`Customer Name`, `Customer ID`) | **9.993** | Thay giá trị bằng mã giả tất định `CUST-001`…`CUST-793`; **giữ nguyên số lượng cột** | `Customer Name` là PII trực tiếp. `Customer ID` là khóa nối ngược với file gốc công khai trên Kaggle → ẩn danh cả hai, nếu không việc ẩn danh có thể bị đảo ngược. Cách này cũng xử lý triệt để 3 mã `Customer ID` có tiền tố chữ thường (`Dp-13240`, `Co-12640`, `Dl-13600` — 43 dòng) và 30 tên viết sai hoa/thường (346 dòng). Chi tiết ở [`privacy_note.md`](privacy_note.md). |
| 4 | **Giao dịch lỗ** (`Profit` âm) | **1.871** | **Giữ nguyên** — không xóa, không sửa | Đây là giao dịch thật từ giảm giá sâu, thanh lý hoặc hàng hư hỏng, không phải nhiễu kỹ thuật. Cấu trúc lỗ rất đều theo mức giảm giá: ở **6 mức** `Discount` = 0,32 / 0,45 / 0,50 / 0,60 / 0,70 / 0,80, **100% dòng đều lỗ** (còn mức 0,30 là 91,6% và mức 0,40 là 87,4%). Xóa sẽ xoá sạch bằng chứng cho câu hỏi 4 (quan hệ giảm giá – lợi nhuận). Tổng giá trị lỗ −156.119,23 trên 1.318 đơn (26,3% số đơn). |
| 5 | **Khoảng trắng thừa ở đầu/cuối** giá trị chuỗi | **16** | `str.strip()` trên các cột chuỗi | Lỗi nhập liệu ở `Product Name` (vd `"Iceberg Mobile Mega Data/Printer Cart "`). Gây trùng lặp giá trị khi gom nhóm theo `Product Name`. Thao tác không mất thông tin. |

### Các vấn đề phát hiện nhưng **quyết định giữ nguyên** (không sửa)

| Vấn đề | Số lượng | Quyết định | Lý do |
|---|---:|---|---|
| `Order ID` có 2 tiền tố `CA-` / `US-` không nhất quán, phân bố theo bang không đều | 8.308 / 1.686 dòng | **Không sửa** | `Order ID` là khóa đơn hàng, sửa tiền tố sẽ phá vỡ khóa. Chỉ ghi nhận cảnh báo. |
| Năm trong `Order ID` khác năm `Order Date` (đều là đơn 2016-12-31 có mã 2017) | 7 dòng | **Không sửa** | Quy ước đánh số đơn của hệ thống (đơn đặt cuối năm gán mã năm giao hàng), không phải lỗi. |
| 16 tên sản phẩm dùng chung nhiều `Product ID` | 16 tên | **Không sửa** | Có thể là sản phẩm cùng loại được mã hoá khác nhau. Không có cơ sở để gộp hoặc tách. Ghi nhận để các thành viên khác **gom nhóm theo `Product ID` hoặc `Sub-Category`, không theo `Product Name`** khi cần độ chính xác. |
| `Sales` lệch phải mạnh (max 22.638,48 vs median 54,48; 1.167 dòng ngoài IQR) | 1.167 dòng | **Không sửa** | Tương ứng với mặt hàng giá trị cao hợp lý (máy photocopy Canon, máy in, ghế da). Không phải nhiễu. |

---

## 4. Đối chiếu số dòng

```
Số dòng gốc (đọc từ data_raw)  : 9.994
Số dòng đã xóa                  : 1
Số dòng sạch                    : 9.993
Kiểm tra: 9.994 - 1 = 9.993  ->  KHỚP
```

Đối chiếu tổng tiền (chênh lệch quy về đúng dòng bị xoá `Row ID` 3407):

| Chỉ số | Gốc | Sạch | Chênh lệch |
|---|---:|---:|---:|
| Tổng `Sales` | 2.297.200,8603 | 2.296.919,4883 | 281,3720 (= `Sales` của dòng bị xoá) |
| Tổng `Profit` | 286.397,0213 | 286.409,0805 | −12,0588 (= `Profit` của dòng bị xoá) |
| Số dòng `Profit` âm | 1.871 | 1.870 | −1 (dòng bị xoá có `Profit` âm) |

---

## 5. Cột nào bị bỏ hoặc thay đổi

| Cột | Bị bỏ? | Giá trị có thay đổi? | Kiểu có thay đổi? |
|---|---|---|---|
| `Row ID` | Không | Không | Không |
| `Order ID` | Không | Không | Không |
| `Order Date` | Không | **Có** — định dạng `M/d/yyyy` → `yyyy-mm-dd` | **Có** — `str` → `datetime64` |
| `Ship Date` | Không | **Có** — định dạng `M/d/yyyy` → `yyyy-mm-dd` | **Có** — `str` → `datetime64` |
| `Ship Mode` | Không | Không | Không |
| `Customer ID` | Không | **Có** — thay bằng mã giả `CUST-nnn` | Không (`str`) |
| `Customer Name` | Không | **Có** — thay bằng mã giả `CUST-nnn` | Không (`str`) |
| `Segment` | Không | Không | Không |
| `Country` | Không | Không | Không |
| `City` | Không | Không | Không |
| `State` | Không | Không | Không |
| `Postal Code` | Không | **Có** — 438 dòng thêm số `0` đầu | Không (đã là `str`) |
| `Region` | Không | Không | Không |
| `Product ID` | Không | Không | Không |
| `Category` | Không | Không | Không |
| `Sub-Category` | Không | Không | Không |
| `Product Name` | Không | **Có** — 16 dòng bỏ khoảng trắng thừa | Không (`str`) |
| `Sales` | Không | Không | Không |
| `Quantity` | Không | Không | Không |
| `Discount` | Không | Không | Không |
| `Profit` | Không | Không | Không |

**Tóm lại:** không cột nào bị bỏ, không cột nào bị thêm, không tên cột nào bị đổi. Ba cột đổi kiểu dữ liệu (`Order Date`, `Ship Date` → datetime) và bốn cột đổi giá trị (`Postal Code`, `Customer ID`, `Customer Name`, `Product Name`).

---

## 6. Hướng dẫn đọc file sạch cho thành viên khác

```python
import pandas as pd

df = pd.read_csv(
    "data_cleaned/superstore_clean.csv",
    encoding="utf-8-sig",                    # bắt buộc: file có BOM
    dtype={"Postal Code": str},              # bắt buộc: tránh mất số 0 đầu
    parse_dates=["Order Date", "Ship Date"], # tuỳ chọn: để có kiểu datetime
)
```

| Cần làm gì | Cách làm đúng | Cảnh báo |
|---|---|---|
| Đếm số đơn hàng | `df["Order ID"].nunique()` | **Không** dùng `len(df)` hay `count()` |
| Tính giá trị đơn trung bình | gom theo `Order ID` rồi trung bình `Sales` | Trung bình trên dòng sẽ ra số khác |
| Gom nhóm theo khách hàng | `df["Customer ID"]` (đã là mã giả) | Không dùng `Customer Name` làm biến dự báo |
| Phân tích theo sản phẩm | `Product ID` hoặc `Sub-Category` | `Product Name` có 16 tên dùng chung nhiều mã |
| Suy ra bang/năm từ `Order ID` | **Không làm** | Tiền tố `CA-`/`US-` không nhất quán; 7 dòng lệch năm |
| Đọc cột ngày | `parse_dates=[...]` | Định dạng trong file là `yyyy-mm-dd` |
