# DEVELOPMENT_PLAN — DHV301 Retail Sales Intelligence (phần Data Cleaning & EDA)

Người phụ trách phạm vi này: **Hưng** (D1–D8 làm sạch, D9–D14 EDA, chuẩn bị dữ liệu bàn giao).
Không thuộc phạm vi: xây dựng mô hình hồi quy tuyến tính (thuộc Hiếu) và dashboard Power BI (thuộc Hoàng).

Trạng thái mỗi task: `Pending` / `In Progress` / `Completed`.
Task chỉ chuyển sang `Completed` khi **đã kiểm chứng** theo tiêu chí kiểm tra tương ứng (không tự đánh dấu khi chưa chạy thật).

---

## 0. Quyết định về cấu trúc thư mục (chốt trước khi code)

Đề tài yêu cầu `notebooks/01_data_cleaning_eda.ipynb` (thư mục `notebooks/`, số nhiều). Repository ban đầu có `notebook/01_data_preparation_eda.ipynb` (thư mục `notebook/`, số ít) — một file **stub rỗng, toàn bộ cell là `TODO`** — cùng `notebook/02_linear_regression.ipynb` của Hiếu.

**Quyết định (đã thực hiện): dùng `notebooks/01_data_cleaning_eda.ipynb` làm notebook chính; xoá stub `notebook/01_data_preparation_eda.ipynb`.**

Lý do:
- **Khớp đúng đề tài:** đề yêu cầu `notebooks/01_data_cleaning_eda.ipynb`.
- **Không tạo notebook trùng lặp:** stub cũ chỉ chứa `TODO`, không có nội dung thực thi được. Giữ lại sẽ gây nhầm lẫn về việc nhóm nào đã làm phần nào.
- **`README.md` đã trỏ sang `notebooks/`** — nên xoá stub làm cấu trúc nhất quán với tài liệu, không tạo thêm việc phải sửa.
- **Không đụng vào `notebook/02_linear_regression.ipynb`** (phần của Hiếu) — file này đọc `data_cleaned/superstore_clean.csv` nên hoàn toàn không bị ảnh hưởng.

Thư mục bổ sung: `reports/eda_insights.md` (tóm tắt insight dạng văn bản để đối chiếu với notebook 01) — *xem mục 2.2 bên dưới*.

---

## 1. Kết quả kiểm tra hiện trạng (đã thực hiện, xem Phase 1)

Đã đọc toàn bộ repository, chạy profiling không sửa file nào (file gốc `data_raw/Sample - Superstore.csv` **không bị thay đổi**).

| Hạng mục | Kết quả |
|---|---|
| Kích thước | 9.994 dòng × 21 cột (khớp đề) |
| Encoding | cp1252; đọc bằng `encoding="cp1252"` OK |
| Missing values | 0 trên toàn bộ 21 cột; 0 dòng có bất kỳ giá trị thiếu |
| Trùng lặp toàn bộ | 0 |
| Trùng lặp bỏ `Row ID` | **1 cặp** (Row ID 3406 & 3407, mọi trường giống hệt) |
| Trùng `(Order ID, Product ID)` | 8 cặp — nhưng 7 cặp khác nhau về `Quantity`/`Sales`/`Profit` ⇒ dòng tách hợp lệ, **giữ nguyên** |
| `Postal Code` | 438 dòng có 4 chữ số (đúng như đề) **+ 11 dòng có `05408` (Burlington, Vermont) bị mất số 0 đầu khi đọc kiểu int** ⇒ tổng 449 dòng mất số 0 đầu nếu parse kiểu số |
| Ngày | `Order Date` 2014-01-03 → 2017-12-30; `Ship Date` tới 2018-01-05; **không có dòng nào Ship < Order**; độ trễ 0–7 ngày |
| Số đơn hàng | 5.009 `Order ID` khác nhau; 48/48 tháng có dữ liệu (không thiếu tháng) |
| `Customer Name` / `Customer ID` | 793 tên ↔ 793 mã, ánh xạ 1–1, không có tên trùng với nhiều mã |
| Ngoại lệ khác | `Order ID` tiền tố `CA-` (8.308) vs `US-` (1.686) không nhất quán; 7 dòng có năm trong `Order ID` lệch năm `Order Date` (đều là 2016-12-31 → `Order ID` 2017); 16 dòng `Product Name` có khoảng trắng thừa; 16 tên sản phẩm dùng chung nhiều `Product ID` |
| `Profit` âm | 1.871 dòng (18,7%), thuộc 1.318 đơn → **giữ nguyên**, không tự xóa |

---

## GIAI ĐOẠN 1 — Project inspection

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P1.1 | Đọc & kiểm kê cấu trúc repo | — (chỉ đọc) | `Get-ChildItem`, đọc README/docs/notebooks | Bảng hiện trạng (mục 1 ở trên) | Không file nào bị sửa; `git status` sạch (trừ file untracked có sẵn) | — | **Completed** |
| P1.2 | Profiling dữ liệu gốc, không ghi file | script tạm đã xoá sau khi chạy | pandas read cp1252 | Số liệu kiểm tra ở mục 1 | `git status` không đổi; hash file gốc không đổi | P1.1 | **Completed** |
| P1.3 | Chốt cấu trúc thư mục đầu ra | `DEVELOPMENT_PLAN.md` | Giữ `notebook/`, thêm `reports/` | Mục 0 + cấu trúc cây | Nhất quán với README | P1.1 | **Completed** |
| P1.4 | Chốt quy ước bàn giao file sạch | `docs/data_dictionary.md` (mục quy ước) | Văn bản | utf-8-sig, `yyyy-mm-dd`, giữ tên cột | Khớp `Hung_dhv.md` | P1.1 | **Completed** |

---

## GIAI ĐOẠN 2 — Data cleaning (D1–D8)

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P2.1 | **D1** Nạp file gốc, encoding cp1252, không sửa file gốc | `notebook/01_data_preparation_eda.ipynb` (Mục 1) | `pd.read_csv(RAW_PATH, encoding="cp1252", dtype={"Postal Code": str})` | `raw.shape == (9994, 21)`; in `raw.head()` | shape khớp; `git diff` trên `data_raw/` = rỗng | P1.3 | **Completed** |
| P2.2 | **D2** Kiểm tra ban đầu | cùng notebook (Mục 2) | In dtypes, `isna().sum()`, `duplicated()`, `value_counts()` cho biến phân loại, `describe()` cho biến số, độ dài `Postal Code`, thống kê ngoại lại IQR | 1–2 bảng kiểm tra + nhận xét | Mọi con số khớp mục 1 | P2.1 | **Completed** |
| P2.3 | **D3** Chuyển `Order Date`, `Ship Date` sang datetime | cùng notebook (Mục 3) | `pd.to_datetime(..., format="%m/%d/%Y", errors="coerce")` | 0 `NaT`; min/max đúng | `isna().sum() == 0`; `Ship Date >= Order Date` toàn bộ | P2.1 | **Completed** |
| P2.4 | **D4** Khôi phục `Postal Code` 5 ký tự | cùng notebook (Mục 3) + `docs/data_dictionary.md` | Giữ `Postal Code` là **string**; với token 4 ký tự: `zip = "0" + token`; với `05408`: giữ nguyên `"05408"` | 100% mã bưu chính dài 5 ký tự | 438 dòng 4 ký tự → "0"+token; 11 dòng `05408` giữ nguyên; **không** trùng lặp với mã 5 ký tự đã có (kiểm tra `0 clash`); mỗi `(City, State)` chỉ còn 1 mã; 6 bang (MA, NJ, CT, RI, NH, ME) đều có mã bưu chính bắt đầu bằng 0 | P2.3 | **Completed** |
| P2.5 | **D5** Xử lý trùng lặp & `Profit` âm | cùng notebook (Mục 3) | In cặp trùng bỏ `Row ID`; xác minh 7 cặp `(Order ID, Product ID)` còn lại là dòng tách hợp lệ; **xoá đúng 1 dòng** (giữ Row ID 3406) | `9994 − 1 = 9993` dòng | Cột `row_ban_bo` (nhãn lý do) được in ra; **không** xoá dòng `Profit < 0`; số dòng bị xoá khớp số dòng ghi trong bảng quyết định | P2.1 | **Completed** |
| P2.6 | **D6** Quyết định xử lý `Customer Name` / `Customer ID` | `docs/privacy_note.md` | Thay **cả `Customer Name` và `Customer ID`** bằng cùng bộ mã giả ổn định `CUST-001…` (giữ nguyên 21 cột); ghi rõ ánh xạ 1–1 793 khách hàng | File sạch không còn tên thật | Kiểm: `clean["Customer Name"]` không còn khớp tên gốc; số khách hàng giữ nguyên 793; khách hàng top doanh thu vẫn nhận diện được qua mã | P2.1 | **Completed** |
| P2.7 | **D7** Xuất dữ liệu sạch | `notebook/01_data_preparation_eda.ipynb` (Mục 4) → `data_cleaned/superstore_clean.csv` | `clean.to_csv(CLEAN_PATH, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")` | File CSV 9.993 dòng dữ liệu + header, 21 cột giữ nguyên tên | Đọc lại bằng `encoding="utf-8-sig"`: shape `(9993, 21)`; BOM đúng; ngày parse được; `data_raw/` không đổi | P2.3–P2.6 | **Completed** |
| P2.8 | **D8** Data dictionary + bảng quyết định | `docs/data_dictionary.md` | Bảng 21 cột: tên, kiểu gốc, kiểu sau sạch, mô tả, ví dụ, ghi chú xử lý; bảng quyết định (vấn đề / số dòng / cách xử lý / lý do) | 21/21 cột được mô tả; bảng quyết định có số dòng khớp thực tế | Đối chiếu từng số trong bảng với output notebook | P2.7 | **Completed** |

**Quy ước bảo toàn cho người nhận (Hiếu, Hoàng):** giữ nguyên 21 tên cột gốc; chỉ đổi *kiểu* của `Order Date`/`Ship Date` (→ ngày) và `Postal Code` (→ chuỗi 5 ký tự). Không thêm cột phụ trừ khi báo cả nhóm (nếu thêm cột phụ trợ EDA thì phải nằm ngoài file bàn giao hoặc được thông báo).

---

## GIAI ĐOẠN 3 — Data validation

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P3.1 | Đối chiếu số dòng | notebook (Mục 4) | In `len(raw)`, số dòng xoá, `len(clean)` | `9994 − 1 = 9993` | DoD "dòng gốc − dòng đã xoá = dòng sạch" in ra trong notebook | P2.7 | **Completed** |
| P3.2 | Kiểm tra kiểu dữ liệu & ngày | notebook (Mục 4) | `assert` / in `dtypes` | 2 cột ngày là datetime; `Postal Code` là str | Không `NaT`; không `Ship Date < Order Date` | P3.1 | **Completed** |
| P3.3 | Kiểm tra toàn vẹn mã bưu chính | notebook (Mục 4) | `len` mã bưu chính; kiểm tra 5 ký tự; không trùng mã sau khôi phục | 100% dài 5 | So khớp tập mã trước/sau | P3.1 | **Completed** |
| P3.4 | Kiểm tra không mất dữ liệu ngoài ý muốn | notebook (Mục 4) | So sánh tổng `Sales`/`Profit` trước–sau (chỉ khác do 1 dòng bị xoá) | Chênh lệch = giá trị của đúng dòng 3407 | Tổng `Sales` giảm đúng 281,372 và tổng `Profit` **tăng** đúng 12,0588 (vì dòng bị xoá có `Profit` âm) | P3.1 | **Completed** |
| P3.5 | Kiểm tra `Profit` âm được giữ | notebook (Mục 4) | Đếm lại dòng `Profit < 0` | 1.870 dòng còn lại trong file sạch (giảm 1 vì dòng trùng bị xoá có `Profit` âm) | Ghi rõ trong bảng quyết định: 1.870 + 1 dòng bị xoá = 1.871 | P3.1 | **Completed** |
| P3.6 | Kiểm tra file gốc bất biến | shell | `git diff --stat data_raw/`, hash file | Không thay đổi | Output rỗng | P3.1 | **Completed** |
| P3.7 | Chạy Restart & Run All trên máy khác | notebook 01 | Bàn giao cho Hiếu/Hoàng chạy lại | Chạy sạch, không lỗi | Không cảnh báo lỗi, file sạch sinh lại giống hệt | P3.1–P3.6 | **Pending** |

---

## GIAI ĐOẠN 4 — EDA (D9–D13)

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P4.1 | **D9** Thống kê mô tả & phân phối | `notebooks/01_data_cleaning_eda.ipynb` (Mục 5) | `describe()` + skew/kurtosis cho Sales/Profit/Quantity/Discount; phân vị & IQR; histogram + boxplot | Bảng thống kê đầy đủ + 2 biểu đồ (Hình 1, 2) | Đã in ra + nhận xét; **đã xác nhận không có cột chi phí vận chuyển** | P3.7 | **Completed** |
| P4.2 | **D10** So sánh nhóm | notebook (Mục 6) | Nhóm theo `Category`, `Region`, `Segment` (và `Sub-Category`, `Ship Mode`): doanh thu, lợi nhuận, số lượng, số đơn `nunique`, **AOV = tổng Sales ÷ số đơn**, biên LN, % dòng lỗ | 5 bảng so sánh + 3 biểu đồ (Hình 3, 4, 5) | **AOV kiểm chứng thủ công** cho Technology/4 vùng/3 phân khúc — in ra cả `mean(Sales)` cấp dòng để đối chiếu | P4.1 | **Completed** |
| P4.3 | **D11** Mối quan hệ Discount–Sales, Discount–Profit, Sales–Profit | notebook (Mục 7) | Ma trận tương quan; `corr()` có kiểm tra ảnh hưởng ngoại lì; heatmap; scatter hue theo Category; đường hồi quy; boxplot Profit theo Discount | Bảng theo mức giảm giá + 3 biểu đồ (Hình 6, 7, 8) | Ràng buộc ngôn ngữ "mối liên hệ"; **không** viết "gây ra" | P4.1 | **Completed** |
| P4.4 | **D12** Xu hướng theo thời gian | notebook (Mục 8) | Gom theo tháng/năm/quý: tổng Sales, tổng Profit, **`Order ID` nunique** (số đơn); pivot cùng tháng giữa các năm | Chuỗi 48 tháng đầy đủ + 2 biểu đồ (Hình 9, 10) | **Kiểm chứng tổng số đơn = 5.009**; có ô in đối chiếu "nếu dùng số dòng sẽ thổi phồng ~100%" | P4.1 | **Completed** |
| P4.5 | **D13** Tổng hợp insight 4 câu hỏi | notebook (Mục 9) | Mỗi câu hỏi: kết luận + số liệu chứng minh + biểu đồ + diễn giải kinh doanh + giới hạn của nhận định | 4 mục trả lời đầy đủ + Hình 11 | **11 biểu đồ** (vượt yêu cầu ≥4); mọi số trong nhận xét đều do cell code in ra | P4.2–P4.4 | **Completed** |

---

## GIAI ĐOẠN 5 — Insight documentation

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P5.1 | **D8** (nốt) Data dictionary | `docs/data_dictionary.md` | Bảng 21 cột + bảng quyết định | 2 bảng đầy đủ | Mọi cột có mô tả; số dòng ảnh hưởng khớp notebook | P4.5 | **Completed** |
| P5.2 | **D6** (nốt) Ghi chú quyền riêng tư | `docs/privacy_note.md` | Quyết định xử lý `Customer Name`, `Customer ID`, City/State/Postal Code; cách chia sẻ an toàn | Quyết định + lý do | Có dòng "cách chia sẻ" cụ thể, không còn TODO | P5.1 | **Completed** |
| P5.3 | **D14** Giả định & giới hạn | `docs/assumptions_limitations.md` | Giả định G1–G12, giới hạn Order Value OV1–OV7, giới hạn dataset L1–L21, giới hạn biến, trường hợp thiếu dữ liệu, ảnh hưởng ngoại lại, cảnh báo tương quan ≠ nhân quả, tính chất lịch sử không phải dự báo | 7 mục đầy đủ + ma trận truy vết kết luận ↔ giới hạn | Không còn TODO; nêu rõ "không dự báo tương lai"; có bảng "cách viết SAI / cách viết ĐÚNG" | P5.1 | **Completed** |
| P5.4 | Báo cáo insight tổng hợp | `reports/eda_insights.md` | Tóm tắt 4 câu hỏi + bảng số liệu chính | Báo cáo ngắn cho thuyết trình | Số liệu trùng với notebook | P5.3 | **Completed** |

---

## GIAI ĐOẠN 6 — Final testing & handover

| ID | Task | File tạo/sửa | Cách triển khai | Expected output | Validation | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|---|---|
| P6.1 | Restart & Run All từ kernel sạch | notebook 01 | Xoá output, chạy lại toàn bộ bằng `nbconvert --execute --inplace` | Chạy không lỗi | **0 lỗi, 11 ảnh PNG, 102 cell** — đã chạy thật | P5.4 | **Completed** |
| P6.2 | Kiểm tra file bàn giao từ máy khác | `data_cleaned/superstore_clean.csv` | Member khác đọc bằng `encoding="utf-8-sig"` | Đọc được, shape đúng | Đọc không lỗi encoding | P6.1 | **Pending** |
| P6.3 | Cập nhật README | `README.md` | Điền mục "Kết quả – EDA", link tới notebook/docs, bỏ TODO liên quan | README phản ánh thực tế | Không còn TODO ở phần EDA | P6.1 | **Completed** |
| P6.4 | Cập nhật phân công | `docs/role_allocation.md` | Ghi rõ vai trò Hưng / Hiếu / Hoàng | Bảng không còn TODO | Khớp `Hung_dhv.md` | P6.3 | **Pending** |
| P6.5 | Bàn giao cho Hiếu & Hoàng | thông báo nhóm + commit | Nêu rõ: 9.993 dòng, 21 cột, thay đổi duy nhất so với gốc, tên khách hàng đã ẩn danh | Nhóm nhận thông tin | Nhóm xác nhận đã đọc | P6.2–P6.4 | **Pending** |
| P6.6 | Milestone 2 | `milestones/` | Lưu bằng chứng (ảnh biểu đồ, log chạy) nếu giảng viên yêu cầu | Bằng chứng milestone | Có ≥4 biểu đồ | P6.1 | **Pending** |

---

## 2. Rủi ro cần xử lý trước khi triển khai

1. **Số 438 vs 449 ở `Postal Code`.** Đề bảo 438 dòng có 4 chữ số — đúng. Nhưng còn 11 dòng `05408` (Burlington, Vermont) vốn có số 0 đầu trong file mà bị mất khi parse kiểu số. Nếu chỉ đếm 438 và xử lý bằng `zfill(5)` thì `05408` biến thành `5408` → sai. **Bắt buộc đọc `Postal Code` dạng chuỗi ngay từ đầu.** Cần thống nhất với nhóm: khôi phục 438 dòng 4 ký tự bằng `"0" + token`.
2. **Không có cơ sở nội tại để đối chiếu 438 mã.** 51 thành phố bị ảnh hưởng không có mã 5 chữ số nào khác trong dataset để đối chiếu; cơ sở khôi phục là quy tắc mã bưu chính Hoa Kỳ (cả 6 bang đều dùng mã bắt đầu bằng 0) + mỗi `(City, State)` chỉ có đúng 1 mã 4 chữ số. Cần ghi rõ đây là *suy luận có cơ sở*, không phải dữ liệu khôi phục từ nguồn khác.
3. **`Order ID` có 2 hệ tiền tố `CA-`/`US-` không nhất quán** và 7 dòng lệch năm so với `Order Date`. Nếu thành viên khác dùng `Order ID` để suy ra bang/năm sẽ sai. Cần ghi vào `assumptions_limitations.md` và cảnh báo nhóm.
4. **Xoá dòng trùng ảnh hưởng số liệu.** Dòng bị xoá có `Sales = 281,372`, `Profit = −12,0588` (dòng lỗ). Nếu không in đối chiếu, thành viên khác có thể nghi ngờ số liệu lệch 1 dòng. Phải có bảng "dòng gốc − dòng xoá = dòng sạch".
5. **Từ chối xoá `Profit` âm.** 1.871 dòng lỗ là dữ liệu thật; xoá sẽ làm sai lệch phân tích giảm giá (trọng tâm câu hỏi 4). Phải giữ và giải thích.
6. **`Customer Name` là PII.** Quyết định đề xuất: thay **cả hai** cột bằng mã giả ổn định `CUST-001…` (giữ `Customer ID` gốc sẽ cho phép nối ngược về tên thật). Cần nhóm xác nhận trước khi ghi vào `docs/privacy_note.md`, vì điều này ảnh hưởng việc các thành viên khác có còn dùng tên để phân tích hay không.
7. **Tương thích môi trường.** `requirements.txt` yêu cầu `pandas>=3.0`; máy đang cài pandas 3.0.3 + Python 3.12.10. Thành viên khác có thể đang ở pandas 1.x/2.x — `dtype="str"` và `df.map` khác nhau. Cần kiểm tra lại `requirements.txt` trước khi bàn giao.
8. **Biểu đồ trong notebook.** ≥4 biểu đồ bắt buộc có tiêu đề, nhãn trục, nhận xét và giải thích lý do chọn loại biểu đồ. Cần cài `matplotlib`/`seaborn` đúng phiên bản, tránh lỗi font tiếng Việt trên Windows.
9. **Không được đụng vào `notebook/02_linear_regression.ipynb`** (phần của Hiếu) và không sửa `data_raw/`.

---

## 2.1 Cập nhật trạng thái — đợt 1 (D1–D8)

**Đã hoàn thành và kiểm chứng:** D1, D2, D3, D4, D5, D6, D7, D8 (mục 2 và 3, mục 5.1–5.2, P3.1–P3.6).

| Hạng mục | Kết quả kiểm chứng |
|---|---|
| File sạch | `data_cleaned/superstore_clean.csv` — 9.993 dòng × 21 cột, `utf-8-sig` (đã kiểm tra BOM), ngày `yyyy-mm-dd` |
| Đối chiếu số dòng | 9.994 − 1 = 9.993 → **KHỚP** (in trong notebook mục 6.1) |
| Cột | Đủ 21 cột gốc, đúng tên, đúng thứ tự, không bỏ/thêm cột |
| Kiểu dữ liệu | 2 cột ngày = `datetime64`; `Postal Code` = chuỗi; tổng NaN = 0 |
| Mã bưu chính | 100% dài 5 ký tự (9.993/9.993) |
| `Profit` âm | 1.870 dòng vẫn còn (1.871 − 1 dòng trùng bị xoá) → **không xóa giao dịch lỗ** |
| File gốc | SHA-256 **không đổi** (`58fb59c6…6c4b7a97`) trước và sau |
| Notebook | 102 cell (65 code + 37 markdown), chạy sạch bằng `nbconvert --execute`, **0 lỗi** |
| Chạy lại | Đã chạy lại từ kernel sạch và cho ra kết quả giống hệt |

**Phát hiện thêm trong quá trình làm D2** (ngoài dự kiến ban đầu):

1. **43 dòng có `Customer ID` với tiền tố chữ thường** (`Dp-13240`, `Co-12640`, `Dl-13600`) → được xử lý triệt để bằng cơ chế mã giả ở D6.
2. **346 dòng có `Customer Name` không theo quy tắc Title Case** (30 tên; chủ yếu do họ có tiền tố `Mc`/`Mac`/`De`/`La`, chỉ 2 tên lỗi thật sự như `Dean percer`) → xử lý triệt để bằng cơ chế mã giả ở D6.
3. **16 dòng `Product Name` có khoảng trắng thừa** ở cuối → thêm bước 5.5 (`str.strip()`).
4. **11 dòng mã bưu chính `05408` (Burlington, Vermont) đã có số 0 đầu trong file gốc** → dùng làm bằng chứng đối chiếu cho D4, chứng minh cơ chế mất số 0 là không nhất quán trong chính nguồn dữ liệu.

**Rủi ro đã xử lý trong quá trình triển khai:**

- **pandas 3.0 đổi kiểu chuỗi mặc định từ `object` sang `str`** → các bộ lọc `dtype == object` bị bỏ sót cột chuỗi (làm mất bước loại khoảng trắng thừa). Đã sửa bằng `select_dtypes(include=["object", "string"])`.
- **`Series.str.islower()` trả về `False` cho chuỗi hỗn hợp** như `"Dp"` → phát hiện tiền tố chữ thường bị bỏ sót. Đã sửa bằng so sánh trực tiếp `str(x) != str(x).upper()`.

---

## 2.2 Cập nhật trạng thái — đợt 2 (D9–D14 EDA)

**Đã hoàn thành và kiểm chứng:** D9, D10, D11, D12, D13, D14 (mục 5–11 của notebook, P4.1–P4.5, P5.3, P5.4, P6.1, P6.3).

### Kết quả kiểm chứng

| Hạng mục | Kết quả |
|---|---|
| Notebook | `notebooks/01_data_cleaning_eda.ipynb` — **102 cell** (65 code + 37 markdown), chạy sạch bằng `nbconvert --execute --inplace`, **0 lỗi** |
| Cấu trúc 11 mục | 1. Introduction → 2. Import Libraries → 3. Load Cleaned Dataset → 4. Data Overview → 5. Descriptive Statistics → 6. Group Comparison → 7. Relationship Analysis → 8. Time Series Analysis → 9. Business Insights → 10. Assumptions and Limitations → 11. Conclusion — **đủ và đúng thứ tự** |
| Phần Data Cleaning | **giữ nguyên toàn bộ** (Phần I, mục 1.1–1.7), không bị sửa nội dung |
| Biểu đồ | **11 ảnh PNG** render thành công; kiểm tra 4 viền mỗi ảnh → 0 pixel bị cắt (không có nhãn chồng lấn) |
| Font tiếng Việt | `DejaVu Sans` — đã kiểm tra **0 glyph thiếu** trên 28 ký tự có dấu; không phụ thuộc font hệ thống |
| Monthly Orders | dùng `nunique("Order ID")`; tổng 48 tháng = **5.009 đơn** khớp tổng số đơn trong file |
| Average Order Value | = tổng `Sales` ÷ số `Order ID` khác nhau; **kiểm chứng thủ công** cho Technology + 4 vùng + 3 phân khúc, in kèm `mean(Sales)` cấp dòng để thấy sai lệch (Technology: 541,55 vs 452,71) |
| Tính toàn vẹn | `assert` 6 điều kiện trước khi phân tích (9.993 dòng, 21 cột, 0 NaN, mã bưu chính 5 ký tự, `Ship Date ≥ Order Date`, tên khách hàng đã ẩn danh) — **PASS** |
| Số liệu trong nhận xét | **không có con số nào viết tay** — mọi con số đều do cell code in ra ngay trước |

### Các phát hiện chính

| # | Phát hiện | Số liệu |
|---|---|---|
| 1 | `Technology` tốt nhất, `Furniture` kém nhất (hiệu quả, không phải quy mô) | Biên LN 17,40% vs 2,49%; `Furniture` 33,6% dòng lỗ; `Tables` lỗ −17.725 USD |
| 2 | `Central` là vùng cần rà soát | Biên LN thấp nhất 7,92%, 31,9% dòng lỗ (vs `West` 9,9%) |
| 3 | AOV gần như bằng nhau giữa các nhóm → khác biệt nằm ở **số lượng**, không ở **giá trị đơn** | Vùng 426–484 USD; phân khúc 449–472 USD (chênh ≤ 13,5%) |
| 4 | Tăng trưởng đến từ **nhiều đơn giá trị nhỏ hơn** | Doanh thu +51,5%, lợi nhuận +88,5%, số đơn +74,1%, nhưng AOV **giảm 13,0%** |
| 5 | Mùa vụ chi phối mạnh | Tháng 11–12 chiếm 29,5% doanh thu; tỉ lệ max/min doanh thu trung bình/tháng 5,9 lần |
| 6 | Giảm giá **không** liên hệ với doanh thu | r = −0,028 |
| 7 | Giảm giá liên hệ **phân tầng theo ngưỡng** với lợi nhuận | Biên LN +29,51% (0%) → âm từ 30%; 6 mức có 100% dòng lỗ; r = −0,219 (R² ≈ 4,8%) |
| 8 | Doanh thu ở mức giảm giá cao **không mất**, mà chuyển thành doanh thu không sinh lời | Mức 0,50: 58.918 USD trên 66 dòng (TB 892,71 USD/dòng > TB chung 229,85) |

### Lỗi đã phát hiện & xử lý trong đợt 2

| # | Lỗi | Cách xử lý |
|---|---|---|
| E1 | `sns.set_theme(rc={"color": ...})` → `KeyError: 'color' is not a valid value for rcParam` (matplotlib cần tên đầy đủ `grid.color`) | Sửa thành `rc={"grid.color": ..., "grid.linewidth": ...}` |
| E2 | Inner docstring trong một `code(r'''...''')` làm chuỗi ngoài đóng sớm → `SyntaxError` khi sinh notebook bằng `nbformat` | Đổi inner docstring thành comment |
| E3 | Đánh số mục không nhất quán giữa Phần I (2–8) và Phần II (2–11) | Chuẩn hoá: Phần I thành mục `1.x`, Phần II giữ đúng 11 mục theo đề |
| E4 | **Claim sai**: "từ `Discount ≥ 0.32` 100% dòng lỗ" | Kiểm chứng lại: mức 0,40 chỉ 87,4% → sửa thành "6 mức 0,32/0,45/0,50/0,60/0,70/0,80 có 100%; mọi mức ≥ 0,30 lỗ trên 87%". Sửa ở notebook + 2 file docs |
| E5 | Stub `notebook/01_data_preparation_eda.ipynb` trùng lặp với `notebooks/01_data_cleaning_eda.ipynb` và mâu thuẫn README | Xoá stub (chỉ chứa `TODO`), giữ `notebook/02_linear_regression.ipynb` của Hiếu |

### Lỗi đã phát hiện & xử lý trong đợt 3 — đợt Final QA (audit độc lập)

| # | Lỗi | Cách xử lý |
|---|---|---|
| E6 | **Lỗi code**: cell 94 in `disc_tbl[[... "corr_disc_profit"]]` nhưng cột này đã bị gỡ ở cell 83 (tính tương quan trong nhóm có `Discount` hằng số → `NaN` + RuntimeWarning) → `KeyError` khi chạy lại từ kernel sạch | Gỡ cột khỏi lệnh in; chạy lại `nbconvert --execute --inplace` → **0 lỗi, 11 ảnh render** |
| E7 | **Claim sai**: `Furniture` 33,6% dòng lỗ — "gần gấp đôi" 2 nhóm kia (thực tế 14,7% → **2,3 lần**) | Sửa thành "gấp hơn 2,3 lần" (notebook) |
| E8 | **Claim sai**: `Consumer` "gần gấp đôi `Corporate`" (thực tế **1,6 lần**) | Sửa thành "1,6 lần `Corporate`" (notebook) |
| E9 | **Claim sai**: `Consumer` 19,3% dòng lỗ — "tỉ lệ thấp hơn hai nhóm còn lại" (thực tế **cao nhất** trong 3 phân khúc) | Sửa thành "tỉ lệ cao nhất trong ba phân khúc" (notebook) |
| E10 | **Claim sai**: "3 sub-category âm, **đều thuộc `Furniture`**" (thực tế `Supplies` thuộc `Office Supplies`) | Sửa: 2 thuộc `Furniture`, 1 thuộc `Office Supplies` (notebook + `reports/eda_insights.md` + `docs/assumptions_limitations.md` L20) |
| E11 | **Claim sai**: `Central` 31,9% dòng lỗ — "gần gấp đôi `West` 9,9%" (thực tế **3,2 lần**) | Sửa thành "gấp 3,2 lần `West`" (notebook + report) |
| E12 | **Claim mơ hồ**: "tỉ lệ max/min 5,9 lần" không nói rõ là của **doanh thu**; "tháng 11 188,25 đơn/tháng gần gấp đôi tháng thấp điểm" (thực tế **4,65 lần**) | Ghi rõ "doanh thu trung bình/tháng"; sửa tỉ lệ số đơn thành 4,65 lần (notebook + report + plan) |
| E13 | **Claim thiếu chính xác**: "các dòng lỗ nặng nhất tập trung ở `Tables` và `Bookcases`" (toàn ngành hàng thực tế là `Binders` và `Machines`) | Sửa thành "các dòng lỗ nặng nhất **của `Furniture`**"; thêm ghi chú `Binders`/`Machines` là 2 sub-category lỗ nặng nhất toàn ngành hàng (notebook + report) |

---

## 3. Định nghĩa hoàn thành (DoD)

### Phần làm sạch (D1–D8) — đã đạt

- [x] Notebook 01 chạy hết bằng Restart & Run All, không lỗi (102 cell, 0 lỗi; **cần Hiếu/Hoàng chạy lại trên máy mới để chốt điều kiện "máy khác trong nhóm"**)
- [x] File trong `data_raw/` không thay đổi (SHA-256 khớp trước/sau)
- [x] `data_cleaned/superstore_clean.csv` đúng đường dẫn, utf-8-sig, ngày `yyyy-mm-dd`, đọc lại được
- [x] Đối chiếu số dòng in ra trong notebook: `9994 − 1 = 9993`
- [x] Mọi dòng bị xoá/sửa có số lượng và lý do trong bảng quyết định làm sạch
- [x] 100% `Postal Code` dài 5 ký tự; không còn ngoại lệ
- [x] Data dictionary đủ 21 cột gốc, ghi rõ cột nào bị bỏ/đổi
- [x] `docs/privacy_note.md` có quyết định với các trường cá nhân
- [x] `docs/assumptions_limitations.md` ghi giả định, giới hạn, không diễn giải tương quan thành nhân quả, không dự báo tương lai

### Phần EDA (D9–D14) — đã đạt

- [x] Có thống kê mô tả đầy đủ (mean, median, std, min, max, Q1–Q3, IQR, skew, kurtosis) cho Sales, Profit, Quantity, Discount
- [x] Ghi nhận rõ dataset **không có cột chi phí vận chuyển**; dùng `Ship Mode` + thời gian giao hàng làm đặc điểm thay thế
- [x] ≥1 so sánh nhóm — thực tế có **5** (Category, Sub-Category, Region, Segment, Ship Mode)
- [x] ≥1 phân tích mối quan hệ — thực tế có **3** cặp (Discount–Sales, Discount–Profit, Sales–Profit) + ma trận tương quan + heatmap
- [x] Phân tích chuỗi thời gian 48 tháng + so sánh năm + mùa vụ + theo quý
- [x] **AOV tính đúng công thức** = tổng Sales ÷ `nunique("Order ID")`, có kiểm chứng thủ công cho 8 nhóm
- [x] **Số đơn hàng dùng `nunique("Order ID")`** — có ô in đối chiếu tổng 5.009 đơn
- [x] **≥4 biểu đồ** — thực tế **11 biểu đồ**, mỗi cái có tiêu đề + nhãn trục + chú giải + 1–2 câu nhận xét + giải thích lý do chọn loại biểu đồ
- [x] Mỗi biểu đồ dùng `plt.tight_layout()`, kiểm tra không có nhãn chồng lấn (kiểm tra 4 viền ảnh: 0 pixel bị cắt)
- [x] Mỗi câu hỏi 1–4 có câu trả lời kèm: kết luận + số liệu + biểu đồ + diễn giải kinh doanh + giới hạn
- [x] `docs/assumptions_limitations.md` đầy đủ 7 mục, không còn TODO
- [x] Notebook chạy từ đầu đến cuối: **0 lỗi**, 11 ảnh render đúng
