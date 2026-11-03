# Kiểm chứng cuối — 03/11/2026

## Kết quả đã thực hiện

| Hạng mục | Kết quả |
|---|---|
| Notebook 01 | Chạy lại bằng kernel Jupyter sạch trên bản sao: 65 cell code, 0 lỗi, 11 output biểu đồ PNG |
| Notebook 02 sau sửa | Chạy lại bằng kernel Jupyter sạch: 9 cell code, 0 lỗi, có output hình và bảng hệ số mới |
| Tái tạo CSV | 9.993 dòng × 21 cột, 5.009 đơn; file sinh lại giống hệt CSV hiện có; nguồn raw không đổi |
| Train/Test | GroupShuffleSplit theo Order ID; có assert không trùng đơn giữa hai tập |
| Hồi quy OLS | MAE 216,54 USD; RMSE 502,05 USD; R² 0,3131 |
| Hồi quy log | MAE 165,31 USD; RMSE 520,44 USD; R² log 0,5701. MAE tốt hơn nhưng RMSE kém hơn OLS |
| Nhóm tham chiếu | Sub-Category: Accessories; Region: Central; Segment: Consumer; Ship Mode: First Class |
| Power BI bằng lệnh | Mở PBIP, Refresh Full qua TOM; xuất DAX bằng export_kpi_results.ps1; đối chiếu Decimal 66/66 PASS; hai kiểm tra DIVIDE đều PASS |
| Kiểm tra hiển thị | Xem trực tiếp 3 trang và Model view; chọn năm 2017 trên trang sản phẩm cho 1.687 đơn, bỏ chọn trở lại 5.009 đơn |
| File nộp | pbix/RetailSales.pbix lưu bằng Desktop, mở lại trong tiến trình riêng; Refresh bằng TOM và kiểm chứng 66/66 KPI trên engine riêng; ZIP không có entry lỗi |
| Ảnh bằng chứng | screenshots/01_overview.png, 02_products_regions.png, 03_discounts.png, 04_model.png; ảnh chụp Desktop thật, có thể bao gồm lớp phủ desktop ngoài báo cáo |
| Milestone EDA | 4 PNG đầu tiên trích nguyên bản từ output notebook 01 đã thực thi trong milestones/eda/ |

Môi trường notebook: Python 3.14.7, dùng các thư viện đã cài trên máy. Power BI Desktop: 2.159.1231.0. Việc kiểm chứng bằng lệnh được ưu tiên; computer use dùng để Save as PBIX và kiểm tra hiển thị.

## Nội dung đã sửa

- Đồng bộ R² đơn biến (0,0473), hệ số Copiers (+2.035,40), Machines (+1.392,03), Quantity (+57,47) và trung bình phần dư (+6,55 USD).
- Sửa nhóm cơ sở Accessories; in trực tiếp nhóm tham chiếu từ encoder.
- Bỏ Category khỏi bảng biến vì code không dùng; ghi đúng giới hạn Order_Month tuyến tính.
- Bỏ giới hạn trục đang che một số điểm ngoại lai trong biểu đồ hồi quy.
- Báo cáo đầy đủ đánh đổi MAE/RMSE của mô hình log; không so sánh trực tiếp hai R² khác không gian.
- Sửa các kết luận về giá niêm yết/tồn kho thành giới hạn chưa được xác minh; cập nhật khai báo Codex hỗ trợ rà soát hồi quy.

## Mã kiểm tra file

- Raw SHA-256: `58fb59c63089e564d835e4aabe19d371757de1137a5bf1888243ae386c4b7a97`
- Clean SHA-256: `c4369518b088d54f0fb192e891f6c7d1b1d530721aa411df22f9f0754384973c`
- PBIX SHA-256: `21a566a50c1b3ce7c061d6368ea85f2e80aace920db7de624a853b7bc055f4a9`

Hash PBIX ghi nhận tại thời điểm chốt QA; lưu lại bằng Desktop có thể đổi hash dù số liệu không đổi.

## Còn cần nhóm xác nhận

- Chạy và đọc file sạch trên máy thành viên khác (P3.7, P6.2).
- Thành viên nhận bàn giao xác nhận (P6.5).
- Một thành viên khác nêu được thông điệp dashboard sau khi xem 10 giây.
- Tập thuyết trình 8–10 phút và kiểm tra khai báo AI của từng người.

Không đánh dấu hoàn tất thay cho các xác nhận này. Chưa commit hoặc push các thay đổi.
