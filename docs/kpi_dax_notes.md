# KPI và DAX cho Retail Sales Intelligence

Nguồn: `data_cleaned/superstore_clean.csv`, UTF-8 BOM, 9.993 dòng, 21 cột, 5.009 đơn. Dữ liệu phân tích là lịch sử 2014–2017, đơn vị tiền USD. Một dòng là một mặt hàng trong đơn.

## Mô hình và nguồn dữ liệu

- `Sales`: import 21 cột từ CSV sạch; ngày parse theo en-US từ yyyy-mm-dd; Postal Code là text.
- `Calendar`: lịch đầy đủ 01/01/2014–31/12/2017, có Date duy nhất, Year và Month (yyyy-MM). Được đánh dấu bảng ngày bằng dataCategory Time và khóa Date.
- Quan hệ chủ động Calendar[Date] (1) → Sales[Order Date] (*), lọc một chiều từ lịch sang giao dịch. Slicer thời gian dùng Calendar, không dùng ngày trực tiếp từ Sales.
- `ProjectRoot` là tham số thư mục repo; đổi tham số trong Transform data → Edit parameters khi chuyển máy rồi Refresh.
- File sạch đã xóa một dòng trùng theo quyết định của Hưng; không tự xử lý lại dữ liệu. Không đổi nguồn về raw.

## Measure

### Total Sales

Tổng doanh thu trong ngữ cảnh lọc hiện tại.

```dax
Total Sales =
SUM ( Sales[Sales] )
```

Định dạng: `$#,0.00;($#,0.00);$0.00`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Total Profit

Tổng lợi nhuận, giữ cả giao dịch lỗ.

```dax
Total Profit =
SUM ( Sales[Profit] )
```

Định dạng: `$#,0.00;($#,0.00);$0.00`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Total Orders

Số Order ID khác nhau trong ngữ cảnh lọc; một đơn có thể có nhiều mặt hàng.

```dax
Total Orders =
DISTINCTCOUNT ( Sales[Order ID] )
```

Định dạng: `#,0`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Total Quantity

Tổng số lượng sản phẩm bán ra.

```dax
Total Quantity =
SUM ( Sales[Quantity] )
```

Định dạng: `#,0`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Line Items

Số dòng mặt hàng; không phải số đơn hàng.

```dax
Line Items =
COUNTROWS ( Sales )
```

Định dạng: `#,0`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Profit Margin

Biên lợi nhuận = tổng lợi nhuận / tổng doanh thu; không lấy trung bình biên theo dòng.

```dax
Profit Margin =
DIVIDE ( [Total Profit], [Total Sales] )
```

Định dạng: `0.00%;(0.00%);0.00%`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Average Order Value

Doanh thu của các mặt hàng được lọc / số đơn chứa các mặt hàng đó; không tính toàn bộ giỏ hàng ngoài bộ lọc.

```dax
Average Order Value =
DIVIDE ( [Total Sales], [Total Orders] )
```

Định dạng: `$#,0.00;($#,0.00);$0.00`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Loss Lines

Số dòng mặt hàng có lợi nhuận âm; trả 0 khi không có dòng lỗ.

```dax
Loss Lines =
COALESCE ( COUNTROWS ( FILTER ( Sales, Sales[Profit] < 0 ) ), 0 )
```

Định dạng: `#,0`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Loss Line Rate

Tỷ lệ dòng mặt hàng lỗ; không phải tỷ lệ đơn hàng lỗ.

```dax
Loss Line Rate =
DIVIDE ( [Loss Lines], [Line Items] )
```

Định dạng: `0.00%;(0.00%);0.00%`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Sales Previous Year

Doanh thu cùng kỳ năm trước; chỉ trả kết quả khi chọn đúng một năm hoặc một tháng. Trả BLANK khi thiếu lịch sử hoặc chọn nhiều năm.

```dax
Sales Previous Year =
IF ( HASONEVALUE ( 'Calendar'[Year] ), CALCULATE ( [Total Sales], DATEADD ( 'Calendar'[Date], -1, YEAR ) ) )
```

Định dạng: `$#,0.00;($#,0.00);$0.00`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

### Sales YoY %

Tăng trưởng doanh thu cùng kỳ; BLANK khi kỳ hiện tại/kỳ trước thiếu dữ liệu hoặc mẫu số bằng 0.

```dax
Sales YoY % =
VAR PriorSales = [Sales Previous Year]
VAR CurrentSales = [Total Sales]
RETURN IF ( ISBLANK ( CurrentSales ) || ISBLANK ( PriorSales ), BLANK (), DIVIDE ( CurrentSales - PriorSales, PriorSales ) )
```

Định dạng: `0.00%;(0.00%);0.00%`. Kiểm thử: so sánh với phép tính độc lập trên CSV trong từng ngữ cảnh ở bảng bên dưới.

## Kiểm tra trong các ngữ cảnh lọc

Ngày 03/11/2026, đã chạy lại 11 measure trên engine Analysis Services cục bộ của Power BI Desktop 2.159.1231.0, sau Refresh bằng TOM từ CSV sạch. Đã mở lại PBIX và kiểm chứng trên engine riêng của file nộp. Kết quả: **66/66 PASS** trong 6 ngữ cảnh; kiểm tra riêng `DIVIDE(100, 0)` trả BLANK và `DIVIDE(0, 100)` trả 0 đều PASS.

- [Kết quả DAX thật](kpi_powerbi_actual.json)
- [Bảng đối chiếu 66 kết quả, sai số và trạng thái](kpi_validation.csv)
- [Truy vấn DAX có thể chạy lại](../pbix/validate_kpis.dax)

Bảng dưới dùng giá trị hiển thị đã làm tròn; phép so sánh trong CSV dùng số chưa làm tròn.

| Measure | Toàn bộ | 2017 + West + Technology | Kết quả |
|---|---:|---:|---|
| Total Sales | 2,296,919.4883 | 95,959.1480 | PASS |
| Total Profit | 286,409.0805 | 18,983.8038 | PASS |
| Total Orders | 5,009 | 177 | PASS |
| Total Quantity | 37,871 | 851 | PASS |
| Line Items | 9,993 | 213 | PASS |
| Profit Margin | 12.4693% | 19.7832% | PASS |
| Average Order Value | 458.5585 | 542.1421 | PASS |
| Loss Lines | 1,870 | 16 | PASS |
| Loss Line Rate | 18.7131% | 7.5117% | PASS |
| Sales Previous Year | BLANK | 65,981.1790 | PASS |
| Sales YoY % | BLANK | 45.4341% | PASS |

Các ngữ cảnh bổ sung: 2017 toàn bộ; 2014-01 không có kỳ trước (Previous Year/YoY đều BLANK); 2015-01 có kỳ trước; khu vực không tồn tại (SUM, DISTINCTCOUNT, tỷ lệ và YoY đều BLANK, Loss Lines = 0). Các giá trị này đều đã đối chiếu trên engine thật.

Dung sai: tiền ≤ 0,01 USD; tỷ lệ ≤ 1e-8; số đếm khớp tuyệt đối. Chương trình đối chiếu dùng Python chuẩn (`csv`, `decimal`), không gọi DAX để tính kỳ vọng.

Chạy lại từ thư mục gốc sau khi mở project và Refresh trong Power BI:

```powershell
pwsh -NoProfile -File pbix/export_kpi_results.ps1
python pbix/validate_kpis.py --actual docs/kpi_powerbi_actual.json
```

Nếu chỉ chạy `python pbix/validate_kpis.py`, bảng kiểm tra sẽ trở về trạng thái Pending native DAX vì lúc đó chỉ có phép tính kỳ vọng. Muốn kiểm chứng lại kết quả đã lưu mà chưa mở Desktop, dùng lệnh có `--actual`; kết quả đó phản ánh lần chạy Desktop đã lưu, không phải model đang mở hiện tại.

Khi lọc Category/Region/Segment, AOV là doanh thu của các dòng được giữ chia số đơn chứa các dòng đó. Tổng số đơn giữa các nhóm sản phẩm có thể vượt số đơn toàn bộ do một đơn xuất hiện ở nhiều nhóm. Không cộng các tỷ lệ hoặc số đơn giữa các nhóm.

## Dashboard

Ba trang, mỗi trang 7 visual kể cả tiêu đề và 2 slicer: Tổng quan (Q1), Sản phẩm và thị trường (Q2–Q3), Giảm giá và lợi nhuận (Q4). Bảng và biểu đồ phản ánh cùng ngữ cảnh; nút tẩy trên slicer xóa lọc. Để so sánh năm, chọn một năm hoặc xóa bộ lọc. Biểu đồ theo tháng dùng Month yyyy-MM để tránh gộp tháng giữa nhiều năm.

## Trạng thái DoD

Phần kỹ thuật Dashboard đã hoàn tất; còn bài kiểm tra thông điệp với một thành viên khác để xác nhận toàn bộ DoD.

| Điều kiện | Trạng thái và bằng chứng |
|---|---|
| Nguồn sạch, Refresh không lỗi | Đạt: đã Refresh PBIP, xuất RetailSales.pbix, mở lại và Refresh PBIX; 9.993 dòng, 5.009 đơn |
| Ít nhất 5 measure, 2 measure vượt SUM/COUNT | Đạt: 11 measure, có AOV, Profit Margin, Loss Line Rate, Previous Year và YoY |
| 5.009 đơn; tỷ lệ tính lại đúng theo bộ lọc | Đạt: DAX thật khớp phép tính CSV trong 6 ngữ cảnh |
| Thiếu kỳ trước / mẫu số 0 | Đạt: 2014-01 và DIVIDE edge cases đã kiểm tra trên engine |
| Tiêu đề, người dùng, KPI nổi bật, ít visual | Đã xem cả 3 trang trong Desktop, mỗi trang 7 visual kể cả 2 slicer và tiêu đề; đã chọn/bỏ năm 2017, KPI và biểu đồ cập nhật đúng |
| Màu sắc, nhãn, định dạng thống nhất | Đã xem lại cả 3 trang; tiêu đề và KPI hiển thị đầy đủ, bảng/biểu đồ có cuộn ở nơi đã ghi rõ |
| Người khác nêu thông điệp trong 10 giây | Chưa thực hiện; cần một thành viên khác trong nhóm |
| Mỗi measure có định nghĩa và ghi chú kiểm thử | Đạt: 11 định nghĩa/công thức và bảng đối chiếu ở trên |
| Ảnh từ bản dùng dữ liệu sạch | Đạt: screenshots/01_overview.png, 02_products_regions.png, 03_discounts.png và 04_model.png, chụp trực tiếp từ Desktop dùng CSV sạch |

Phân công hiện có tại role_allocation.md. Chưa xác nhận bài kiểm tra thông điệp 10 giây, chạy trên máy thành viên khác, nhận bàn giao hay tập thuyết trình; những mục này cần nhóm xác nhận. Khai báo AI đã bổ sung phần Codex rà soát hồi quy, chưa tự xác nhận thay khai báo của từng thành viên.

## Tài liệu kỹ thuật

- [Power BI projects và lưu lại thành PBIX](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [DATEADD](https://learn.microsoft.com/en-us/dax/dateadd-function-dax)
- [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax)
