**Hưng: Làm sạch dữ liệu và EDA**

Phân công nhóm – Retail Sales Intelligence (DHV301)

**Yêu cầu của giảng viên:** dùng mô hình hồi quy tuyến tính để phân tích dữ liệu.

**Dataset:** data_raw/Sample - Superstore.csv (9.994 dòng, 21 cột; mỗi dòng là một mặt hàng trong đơn).

**Repo:** <https://github.com/minhhoangb/retail-sales-intelligence>

**DoD (Definition of Done)** là các điều kiện kiểm tra được để coi một phần việc là xong. Chỉ đánh dấu hoàn thành khi mọi ô DoD của phần đó đều đạt.

# Đề tài và câu hỏi đã chốt

**Đề tài:** Retail / Sales Intelligence – phân tích hiệu quả bán hàng của Superstore giai đoạn 2014–2017, có sử dụng hồi quy tuyến tính.

**Người dùng:** Quản lý kinh doanh của doanh nghiệp bán lẻ.

**Phạm vi:** Dữ liệu bán hàng tại Hoa Kỳ từ 01/2014 đến 12/2017. Bài phân tích mô tả và tìm mối liên hệ; không dự báo tương lai và không kết luận quan hệ nhân quả.

| **Câu** | **Câu hỏi**                                                                                                                                     | **Trả lời chính** |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| 1       | Doanh thu, lợi nhuận và số đơn hàng thay đổi thế nào theo tháng và năm?                                                                         | Hưng, Hoàng       |
| 2       | Nhóm sản phẩm nào hoạt động tốt nhất và kém nhất về doanh thu và lợi nhuận?                                                                     | Hưng, Hoàng       |
| 3       | Khu vực và phân khúc khách hàng khác nhau thế nào về doanh thu, lợi nhuận và giá trị đơn trung bình?                                            | Hưng, Hoàng       |
| 4       | Mức giảm giá có mối liên hệ thế nào với doanh thu và lợi nhuận?                                                                                 | Hưng, Hoàng       |
| 5       | Mô hình hồi quy tuyến tính ước lượng kết quả bán hàng tốt đến đâu trên dữ liệu chưa dùng để huấn luyện, và những yếu tố nào có liên hệ rõ nhất? | Hiếu              |

# Công việc

| **Mã** | **Việc**                                                                                          | **Đầu ra**                          |
| ------ | ------------------------------------------------------------------------------------------------- | ----------------------------------- |
| D1     | Nạp file gốc bằng encoding="cp1252", không sửa file trong data_raw/                               | Mục 1 của notebook 01               |
| D2     | Kiểm tra ban đầu: kiểu dữ liệu, giá trị thiếu, trùng lặp, miền giá trị, giá trị bất thường        | Mục 2 của notebook 01               |
| D3     | Đổi Order Date, Ship Date sang kiểu ngày                                                          | Mục 3 của notebook 01               |
| D4     | Xử lý Postal Code: 438 dòng chỉ còn 4 chữ số, nhiều khả năng do mất số 0 đầu                      | Mục 3 của notebook 01               |
| D5     | Xem xét 1 dòng trùng khi bỏ qua Row ID và các dòng có Profit âm, không tự động xóa dòng Profit âm | Mục 3 của notebook 01               |
| D6     | Quyết định cách xử lý Customer Name, Customer ID                                                  | `docs/privacy_note.md`              |
| D7     | Xuất dữ liệu sạch theo quy ước bàn giao bên dưới                                                  | `data_cleaned/superstore_clean.csv` |
| D8     | Viết data dictionary và bảng quyết định làm sạch                                                  | `docs/data_dictionary.md`           |
| D9     | Thống kê mô tả và phân phối của các biến quan trọng                                               | Mục 5 của notebook 01               |
| D10    | So sánh giữa các nhóm                                                                             | Mục 6 của notebook 01               |
| D11    | Phân tích mối quan hệ                                                                             | Mục 7 của notebook 01               |
| D12    | Xu hướng theo thời gian, số đơn đếm Order ID khác nhau                                            | Mục 8 của notebook 01               |
| D13    | Tóm tắt insight theo từng câu hỏi 1–4                                                             | Mục 9 của notebook 01               |
| D14    | Ghi giả định và giới hạn của dữ liệu                                                              | `docs/assumptions_limitations.md`   |

# DoD

## Làm sạch (D1–D8)

- Notebook 01 chạy hết bằng Restart & Run All, không lỗi, trên một máy khác trong nhóm
- File trong data_raw/ không thay đổi
- File sạch đúng đường dẫn, đúng quy ước bàn giao, và Hiếu, Hoàng đọc được
- Số dòng đối chiếu được: dòng gốc − dòng đã xóa = dòng sạch, in ra trong notebook
- Mọi dòng bị xóa hoặc sửa đều có số lượng và lý do trong bảng quyết định làm sạch
- Cột ngày đúng kiểu; mọi Postal Code có 5 ký tự, hoặc có ghi lý do nếu giữ khác
- Data dictionary đủ cả 21 cột gốc, ghi rõ cột nào bị bỏ hoặc đổi
- docs/privacy_note.md đã ghi quyết định với các trường cá nhân

## EDA (D9–D14)

- Có thống kê mô tả, ít nhất 1 so sánh nhóm và 1 phân tích mối quan hệ
- Có ít nhất 4 biểu đồ, mỗi biểu đồ có tiêu đề, nhãn trục và 1–2 câu nhận xét
- Mỗi câu hỏi 1–4 có câu trả lời kèm bằng chứng, hoặc ghi rõ dữ liệu chưa trả lời được
- Có giải thích ngắn lý do chọn loại biểu đồ
- Kết luận không nói quá dữ liệu; mối liên hệ không được viết thành nhân quả

# Quy ước bàn giao file sạch

Đây là điểm nối duy nhất giữa bạn với Hiếu và Hoàng. Bàn giao càng sớm, hai bạn càng ít phải làm lại; có thể đẩy bản đầu tiên rồi cập nhật sau, miễn là báo nhóm.

- Đường dẫn: data_cleaned/superstore_clean.csv
- Bảng mã UTF-8 (utf-8-sig), cột ngày dạng yyyy-mm-dd
- Giữ nguyên tên cột; nếu xóa hoặc đổi tên cột thì báo cả nhóm trước

# Mốc của bạn

**Milestone 2:** D1–D13, ít nhất 4 biểu đồ nháp, các vấn đề và giới hạn chính.

# Việc chung của bạn

| **Mã** | **Việc**                                              | **DoD**                                                                               |
| ------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| C6     | Tập thuyết trình và chuẩn bị câu hỏi cùng cả nhóm     | Tập đủ 8–10 phút; mỗi người có phần trình bày; có sẵn trả lời cho các câu hỏi dự kiến |
| C9     | Ghi lại phần bạn dùng AI hỗ trợ và gửi Hoàng tổng hợp | Hoàng đã nhận được nội dung và cách bạn kiểm tra                                      |