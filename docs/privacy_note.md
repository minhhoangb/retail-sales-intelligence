# Quyền riêng tư và chia sẻ dữ liệu có trách nhiệm

**Người phụ trách:** Hưng  
**Liên quan:** mục 5.4 (D6) của [`notebooks/01_data_cleaning_eda.ipynb`](../notebooks/01_data_cleaning_eda.ipynb)  
**Áp dụng cho:** `data_cleaned/superstore_clean.csv`

---

## 1. Nguồn và quyền sử dụng

- Nguồn: [Superstore Dataset – Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), người đăng `vivek468`.
- Mô tả trên Kaggle ghi dữ liệu **chỉ dùng cho mục đích giáo dục**. Nhóm dẫn nguồn này ở mọi nơi dùng dataset.
- Dữ liệu được lấy từ Tableau theo mô tả của người đăng, **chưa được kiểm chứng là dữ liệu của một doanh nghiệp bán lẻ thực tế**.
- Nhóm dùng dataset cho bài tập môn DHV301 và không dùng cho mục đích thương mại.

---

## 2. Đánh giá rủi ro theo từng trường

Đánh giá dựa trên **đặc điểm thực tế** của dữ liệu trong dataset, không chỉ trên tên cột.

| Trường | Đặc điểm trong dữ liệu | Loại thông tin | Rủi ro | Cách xử lý trong dữ liệu sạch |
|---|---|---|---|---|
| `Customer Name` | 793 tên thật; quan hệ 1–1 với `Customer ID`; 30 tên không theo quy tắc Title Case — chủ yếu do họ có tiền tố `Mc`/`Mac`/`De`/`La`; chỉ 2 tên lỗi thật sự (`Dean percer`, `Dorris liebe`); có tên trùng giữa nhiều người khác nhau | **Định danh cá nhân trực tiếp** | **Cao** | **Thay toàn bộ giá trị bằng mã giả `CUST-001`…`CUST-793`** |
| `Customer ID` | Mã dạng `CG-12520`; không chứa tên nhưng là **khóa ổn định** nối trực tiếp về bản gốc công khai trên Kaggle. 3 mã có tiền tố chữ thường (`Dp-13240`, `Co-12640`, `Dl-13600`) | Mã định danh gián tiếp | **Trung gian – Cao** | **Thay toàn bộ giá trị bằng cùng bộ mã giả `CUST-001`…`CUST-793`** |
| `City`, `State` | 531 thành phố, 49 tiểu bang | Địa lý cấp vùng | Thấp | Giữ nguyên — cần cho phân tích vùng thị trường; không định danh cá nhân khi tách khỏi thông tin khách hàng |
| `Postal Code` | 631 mã bưu chính | Địa lý đến cấp mã bưu chính | Thấp | Giữ nguyên (sau khi sửa mất số 0 đầu) |
| `Order ID` | Mã đơn hàng, không chứa thông tin cá nhân | Định danh giao dịch | Rất thấp | Giữ nguyên |
| `Sales`, `Quantity`, `Discount`, `Profit` | Số liệu giao dịch | Tài chính | Rất thấp | Giữ nguyên |

---

## 3. Quyết định xử lý

### 3.1. Ẩn danh `Customer Name` **và** `Customer ID`

**Quyết định:** thay giá trị của **cả hai cột** bằng mã giả `CUST-001` … `CUST-793`.

**Cơ sở và cách thực hiện:**

1. **Không xóa cột nào.** Giữ nguyên 21 cột và tên cột để không phá vỡ quy ước bàn giao với Hiếu (hồi quy) và Hoàng (dashboard). Các phép gom nhóm theo khách hàng vẫn chạy bình thường.
2. **Mã giả được sinh một cách tất định:** sắp xếp 793 mã `Customer ID` gốc tăng dần rồi gán `CUST-001`, `CUST-002`, … Bất kỳ ai chạy lại notebook đều ra cùng kết quả → có thể kiểm chứng độc lập.
3. **`Customer Name` nhận cùng mã với `Customer ID` tương ứng**, nên quan hệ 1–1 giữa hai cột được bảo toàn (kiểm chứng trong notebook mục 5.4.2).
4. **Vì sao thay cả `Customer ID`, không chỉ `Customer Name`?** Vì `Customer ID` là khóa nối ngược về file gốc công khai trên Kaggle. Nếu giữ nguyên `CG-12520`, bất kỳ ai có file gốc đều nối được `CUST-144` với tên thật → việc ẩn danh chỉ mang tính hình thức, không có tác dụng bảo vệ.
5. **Hiệu quả phụ có lợi:** cách này xử lý triệt để các lỗi định dạng đã phát hiện ở D2 — 3 mã `Customer ID` có tiền tố chữ thường (43 dòng) và 30 tên khách hàng không theo quy tắc Title Case (346 dòng) — vì giá trị gốc không còn tồn tại trong file sạch.

### 3.2. Giữ `City`, `State`, `Postal Code`

Giữ nguyên vì cần cho phân tích vùng thị trường (câu hỏi 3: khu vực nào bán tốt) và dashboard của Hoàng. Ở mức độ này, chúng **không định danh cá nhân**: tổng hợp theo bang/thành phố không truy ngược được tới một cá nhân cụ thể. Bản đồ vùng bán hàng là thông tin kinh doanh hợp lý.

### 3.3. Bảng ánh xạ

**Bảng ánh xạ gốc ↔ mã giả không được công bố** trong repository, trong bài nộp hay trong bản trình bày. Nhóm tái tạo lại được bảng ánh xạ từ file gốc bất cứ lúc nào thật sự cần (ví dụ để kiểm tra một nghiệp vụ cụ thể với doanh nghiệp). Đây là điểm khác biệt giữa "ẩn danh để chia sẻ" và "ẩn danh để phân tích".

---

## 4. Cách chia sẻ an toàn

| Kênh chia sẻ | Mức an toàn | Hành động |
|---|---|---|
| Repository nhóm (Git) | **An toàn** | Chỉ đưa `data_cleaned/superstore_clean.csv` (đã ẩn danh). File `data_raw/Sample - Superstore.csv` chứa tên thật — nhóm **không** push file này lên repo công khai; nếu bắt buộc phải lưu trữ, đặt trong kho nội bộ riêng, không public. |
| Bài nộp giảng viên | **Cần cẩn trọng** | Nộp bản đã ẩn danh. Nếu giảng viên cần file gốc để đối chiếu, gửi riêng kèm ghi chú nguồn Kaggle và mục đích giáo dục. |
| Dashboard Power BI (Hoàng) | **An toàn** | Dùng file đã ẩn danh. **Không** join với file gốc để hiện tên thật trên dashboard. |
| Notebook hồi quy (Hiếu) | **An toàn** | `Customer ID`/`Customer Name` chỉ dùng để gom nhóm, **không** đưa vào tập biến đầu vào `X` — chúng là định danh, không mang thông tin dự báo. |
| Thuyết trình | **An toàn** | Không đưa tên khách hàng thật lên slide. Dùng mã giả `CUST-nnn` khi cần ví dụ về một khách hàng cụ thể. |

---

## 5. Tự kiểm tra trước khi bàn giao

Các kiểm tra sau được chạy trong notebook 01 (mục 5.4.2 và 7.1) và kiểm chứng lại độc lập:

- [x] Mọi giá trị `Customer Name` khớp mẫu `CUST-\d{3}` — không còn tên thật
- [x] Mọi giá trị `Customer ID` khớp mẫu `CUST-\d{3}`
- [x] Số khách hàng giữ nguyên: **793** (không mất hay trùng khách hàng)
- [x] Quan hệ 1–1 giữa `Customer ID` và `Customer Name` vẫn giữ nguyên
- [x] Không có chuỗi nào trong `Customer Name` chứa khoảng trắng (tên thật luôn có dấu cách)
- [x] Không có NaN trong toàn bộ dữ liệu sạch
- [x] Số dòng khớp: 9.994 − 1 = 9.993

---

## 6. Ranh giới và điểm chưa giải quyết được

- **Ẩn danh ở cấp bản ghi, không ở cấp hành vi.** Dữ liệu vẫn cho phép suy ra hành vi mua hàng của từng khách hàng (thời điểm, sản phẩm, giá trị). Với một bộ dữ liệu công khai về hành vi mua hàng, đây là giới hạn không tránh được nếu muốn giữ dữ liệu ở mức chi tiết dòng.
- **Không thể ẩn danh hoàn toàn.** Vì đề tài cần phân tích theo khu vực, phân khúc và cả đơn hàng, nên bản ghi phải giữ nguyên cấu trúc. Nhóm chọn ẩn danh ở cấp **danh tính khách hàng** và giữ nguyên mọi thông tin giao dịch.
- **`Order ID` không chứa PII** nên được giữ nguyên; nếu giảng viên yêu cầu mức ẩn danh cao hơn, có thể thay cả `Order ID` bằng mã giả theo cùng nguyên tắc — nhưng phải báo cả nhóm trước vì ảnh hưởng đến việc nối dữ liệu giữa các thành phần.
- **Dữ liệu là mẫu giáo dục**, không phải dữ liệu khách hàng thật, nên rủi ro thực tế thấp hơn nhiều so với dữ liệu doanh nghiệp. Tuy vậy nhóm vẫn giữ nguyên nguyên tắc ẩn danh như với dữ liệu thật, để quy trình có thể dùng lại được.
