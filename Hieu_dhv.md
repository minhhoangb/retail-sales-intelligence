# Hiếu: Hồi quy tuyến tính (Linear Regression)

Phân công nhóm – Retail Sales Intelligence (DHV301)

**Yêu cầu của giảng viên:** Dùng mô hình hồi quy tuyến tính để phân tích dữ liệu.

**Dataset:** `data_raw/Sample - Superstore.csv` (9.994 dòng, 21 cột; mỗi dòng là một mặt hàng trong đơn) / `data_cleaned/superstore_clean.csv` (9.993 dòng × 21 cột).

**Repo:** <https://github.com/minhhoangb/retail-sales-intelligence>

**DoD (Definition of Done)** là các điều kiện kiểm tra được để coi một phần việc là xong. Chỉ đánh dấu hoàn thành khi mọi ô DoD của phần đó đều đạt.

---

## Đề tài và câu hỏi đã chốt

**Đề tài:** Retail / Sales Intelligence – phân tích hiệu quả bán hàng của Superstore giai đoạn 2014–2017, có sử dụng hồi quy tuyến tính.  
**Người dùng:** Quản lý kinh doanh của doanh nghiệp bán lẻ.  
**Phạm vi:** Dữ liệu bán hàng tại Hoa Kỳ từ 01/2014 đến 12/2017. Bài phân tích mô tả và tìm mối liên hệ; không dự báo tương lai và không kết luận quan hệ nhân quả.

| Câu | Câu hỏi | Trả lời chính |
| :---: | :--- | :---: |
| 1 | Doanh thu, lợi nhuận và số đơn hàng thay đổi thế nào theo tháng và năm? | Hưng, Hoàng |
| 2 | Nhóm sản phẩm nào hoạt động tốt nhất và kém nhất về doanh thu và lợi nhuận? | Hưng, Hoàng |
| 3 | Khu vực và phân khúc khách hàng khác nhau thế nào về doanh thu, lợi nhuận và giá trị đơn trung bình? | Hưng, Hoàng |
| 4 | Mức giảm giá có mối liên hệ thế nào với doanh thu và lợi nhuận? | Hưng, Hoàng |
| 5 | Mô hình hồi quy tuyến tính ước lượng kết quả bán hàng tốt đến đâu trên dữ liệu chưa dùng để huấn luyện, và những yếu tố nào có liên hệ rõ nhất? | **Hiếu** |

---

## Công việc

| Mã | Việc | Đầu ra |
| :---: | :--- | :--- |
| **M1** | Hỏi giảng viên: hồi quy đơn biến hay được dùng đa biến | Câu trả lời ghi ở đầu notebook 02 |
| **M2** | Chọn biến đích Y và các biến đầu vào X | Bảng biến kèm lý do, mục 1 của notebook 02 |
| **M3** | Chia tập huấn luyện và kiểm tra; cân nhắc giữ các dòng cùng `Order ID` trong một tập | Mục 2 của notebook 02 |
| **M4** | Xây mô hình mốc dự đoán bằng giá trị trung bình của tập huấn luyện | Mục 3 của notebook 02 |
| **M5** | Huấn luyện hồi quy tuyến tính; mã hóa biến phân loại trong `Pipeline` | Mục 4 của notebook 02 |
| **M6** | Đánh giá trên tập kiểm tra bằng MAE, RMSE, R² | Bảng so sánh, mục 5 của notebook 02 |
| **M7** | Vẽ biểu đồ thực tế – dự đoán, phần dư; xem ảnh hưởng của giá trị ngoại lai | Mục 6 của notebook 02 |
| **M8** | Diễn giải hệ số | Bảng hệ số, mục 7 của notebook 02 |
| **M9** | Trả lời câu hỏi 5; viết kết luận và giới hạn của mô hình | Mục 8 của notebook 02, `docs/assumptions_limitations.md`, `README.md` |
| **M10** | Chạy lại toàn bộ trên file sạch của Hưng | Notebook 02 cập nhật số liệu |

---

## DoD (Definition of Done)

- [x] Loại hồi quy đúng với câu trả lời của giảng viên (Hồi quy đa biến làm trọng tâm kết hợp đối chiếu đơn biến)
- [x] Notebook 02 đọc từ `data_cleaned/superstore_clean.csv`, chạy hết bằng Restart & Run All, không lỗi
- [x] Mỗi biến trong mô hình có lý do; X không có biến tính từ chính Y, không có mã định danh (`Row ID`, `Order ID`, `Customer Name`)
- [x] Bước mã hóa chỉ học từ tập huấn luyện; tập kiểm tra không được dùng khi huấn luyện
- [x] Cách chia, tỷ lệ chia và `random_state` được ghi rõ, chạy lại ra cùng kết quả (GroupShuffleSplit theo `Order ID`, 80:20, `random_state=42`)
- [x] Có bảng MAE, RMSE, R² của cả mô hình hồi quy và mô hình mốc trên tập kiểm tra
- [x] Có nhận xét mô hình tốt hơn mốc hay không; nếu không tốt hơn thì ghi đúng như vậy, không chọn lại tập kiểm tra để số đẹp hơn
- [x] Có biểu đồ phần dư kèm nhận xét về các giả định và giá trị ngoại lai
- [x] Giải thích được ý nghĩa của ít nhất các hệ số chính bằng lời thường, dùng cách nói "có mối liên hệ"
- [x] Kết quả chính đã có trong README

---

## Bắt đầu ngay, không cần chờ Hưng
Khi chưa có dữ liệu sạch, ở ô đầu notebook 02, tạm thay đoạn kiểm tra và đọc file bằng dòng dưới, rồi đổi lại ở M10:
`df = pd.read_csv(RAW_PATH, encoding="cp1252")`  
File sạch Hưng bàn giao: `data_cleaned/superstore_clean.csv`, UTF-8 (`utf-8-sig`), cột ngày dạng `yyyy-mm-dd`, giữ nguyên tên cột. *(Hiện tại file sạch đã hoàn tất và được sử dụng trực tiếp trong notebook 02)*.

---

## Việc chung của bạn

| Mã | Việc | DoD |
| :---: | :--- | :--- |
| **C6** | Tập thuyết trình và chuẩn bị câu hỏi cùng cả nhóm | Tập đủ 8–10 phút; mỗi người có phần trình bày; có sẵn trả lời cho các câu hỏi dự kiến |
| **C9** | Ghi lại phần bạn dùng AI hỗ trợ và gửi Hoàng tổng hợp | Hoàng đã nhận được nội dung và cách bạn kiểm tra |

