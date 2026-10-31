# Dashboard Retail Sales Intelligence

Mở `RetailSales.pbip` bằng Power BI Desktop. Project này có mô hình import, lịch Calendar và 3 trang dashboard; đã Refresh từ file sạch 9.993 dòng, 5.009 đơn. Nguồn project ở định dạng text để review bằng Git; đầu ra PBIX vẫn cần lưu từ Desktop.

## Mở trên máy khác

1. Mở RetailSales.pbip (hoặc RetailSales.Report/definition.pbir).
2. Vào Transform data → Edit parameters, đổi `ProjectRoot` sang thư mục repo trên máy đó. Giá trị hiện tại là `D:\DHV301\retail-sales-intelligence`.
3. Refresh. Nguồn luôn là `data_cleaned/superstore_clean.csv`, UTF-8 BOM, ngày yyyy-MM-dd; giữ Postal Code kiểu text. Không thay bằng CSV gốc.
4. Khi bỏ hết bộ lọc, Total Orders phải là 5.009. Calendar lọc Sales theo Order Date.

## Kiểm chứng KPI bằng lệnh

Mở project và Refresh trong Desktop trước, rồi chạy từ thư mục gốc:

```powershell
pwsh -NoProfile -File pbix/export_kpi_results.ps1
python pbix/validate_kpis.py --actual docs/kpi_powerbi_actual.json
```

Script PowerShell chỉ đọc engine cục bộ và ghi kết quả vào docs; không sửa model, không điều khiển giao diện, không tải dependency. Script Python tính độc lập từ CSV bằng Decimal. Lần đã kiểm tra: 66/66 PASS trong 6 ngữ cảnh, kèm kiểm tra chia 0 trên engine. Xem docs/kpi_dax_notes.md.

## Xuất bản nộp

1. Kiểm tra hiển thị cả 3 trang và thao tác slicer; xóa bộ lọc trước khi lưu bản tổng quan.
2. File → Save as → Power BI Desktop (*.pbix), lưu `pbix/RetailSales.pbix`. Power BI Desktop hỗ trợ chuyển PBIP thành PBIX qua Save as; chưa có đường chuyển bằng lệnh được Microsoft hỗ trợ.
3. Mở lại PBIX, Refresh, kiểm tra Total Orders 5.009.
4. Chụp Model view và 3 trang vào screenshots/, từ chính bản dùng nguồn sạch. Chưa có ảnh chụp trong lần bàn giao này.
5. Nhờ người khác trong nhóm nêu thông điệp chính sau khi xem 10 giây; chỉ đánh dấu DoD đầy đủ khi đã đạt bước này.

Ba trang: Tổng quan (xu hướng doanh thu theo tháng, lợi nhuận và số đơn theo năm), Sản phẩm và thị trường (Category, Sub-Category, Region và Segment), Giảm giá và lợi nhuận (mối liên hệ quan sát; không kết luận nhân quả).

Mô tả và công thức từng measure, cách tính AOV khi lọc nhóm sản phẩm, quy tắc BLANK của kỳ trước và trạng thái DoD đều ở docs/kpi_dax_notes.md.
