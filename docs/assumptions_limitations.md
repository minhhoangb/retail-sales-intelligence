# Giả định và giới hạn

**Người phụ trách:** Hưng  
**Phạm vi:** áp dụng cho toàn bộ phần Data Cleaning (D1–D8) + EDA (D9–D14) và cho phần hồi quy tuyến tính của nhóm  
**Dữ liệu:** `data_cleaned/superstore_clean.csv` (9.993 dòng × 21 cột, xuất từ `data_raw/Sample - Superstore.csv`)  
**Cập nhật:** sau khi hoàn tất EDA — bổ sung các giả định, giới hạn và kiểm chứng định lượng cho D9–D14  
**Notebook tham chiếu:** `notebooks/01_data_cleaning_eda.ipynb` (mục 10 — Assumptions and Limitations)

---

## 1. Giả định khi xử lý dữ liệu

Mỗi giả định dưới đây là một **quyết định có ảnh hưởng đến kết quả phân tích**. Chúng được nêu ra ở đây để người đọc biết kết luận nào dựa trên tiền đề nào.

### G1. Một dòng là một mặt hàng trong một đơn hàng

Mỗi dòng là **một line item**, không phải một đơn hàng. Vì vậy:

- Số đơn hàng phải tính bằng `nunique("Order ID")` → **5.009 đơn**, không phải 9.993 dòng.
- Giá trị đơn trung bình phải gom theo `Order ID` rồi mới trung bình. Trung bình trên cấp dòng cho kết quả khác và là sai về mặt ngữ nghĩa.
- Doanh thu, lợi nhuận, số lượng và giảm giá ở cấp dòng vẫn **cộng dồn được** vì chúng là số liệu cộng dồn.
- **Average Order Value (AOV) = tổng `Sales` của nhóm ÷ số `Order ID` khác nhau trong nhóm.** Không dùng `mean(Sales)` cấp dòng. Kiểm chứng cụ thể cho `Technology`: 836.154,03 / 1.544 đơn = **541,55 USD/đơn**, trong khi `mean(Sales)` cấp dòng chỉ là 452,71 USD — lệch 19,6%.

### G2. `Postal Code` bị mất số 0 đầu, và việc khôi phục là có cơ sở

438 dòng có mã bưu chính 4 chữ số. Nhóm giả định số `0` đầu bị mất trong quy trình xuất dữ liệu và **khôi phục bằng `zfill(5)`**.

Cơ sở: (1) đúng 438 dòng như đề nêu; (2) các dòng này thuộc 6 bang dùng mã bắt đầu bằng `0` (MA, NJ, CT, RI, NH, ME); (3) mỗi `(City, State)` chỉ có đúng một mã 4 chữ số → không có tín hiẳng số; (4) mã khôi phục không trùng mã 5 chữ số nào đã có; (5) file gốc **đã giữ** số 0 ở mã `05408` (Burlington, Vermont) → cơ chế mất số 0 là không nhất quán trong chính nguồn dữ liệu.

**Đây là suy luận, không phải dữ liệu khôi phục từ nguồn ngoài.** Nhóm không có bảng tra mã bưu chính chính thức để đối chiếu độc lập. Nếu một số trong 438 mã này thực ra là mã 4 chữ số hợp lệ (không phải mất số 0), thì giá trị đó sẽ sai. Tuy nhiên, `Postal Code` **không tham gia** vào bất kỳ phép tính kinh doanh nào trong bài phân tích — nó chỉ phục vụ mô tả địa lý — nên rủi ro này không ảnh hưởng kết luận nào.

### G3. `Profit` âm là giao dịch thật, không phải nhiễu

1.871 dòng (18,72%) có `Profit` âm, tổng −156.119,23, trên 1.318 đơn hàng. Nhóm **giữ nguyên toàn bộ** và hiểu đây là hậu quả của giảm giá sâu, thanh lý, hoặc hàng hư hỏng.

Cơ sở: cấu trúc lỗ rất đều theo mức giảm giá — ở **6 mức** `Discount` = 0,32 / 0,45 / 0,50 / 0,60 / 0,70 / 0,80, **100% dòng đều lỗ** (còn mức 0,30 là 91,6% và mức 0,40 là 87,4%); ở mức `Discount = 0` không có dòng lỗ nào. Đó là hành vi kinh doanh có cấu trúc, không phải nhiễu ngẫu nhiên.

**Nếu nhóm đã xóa các dòng này**, phân tích câu hỏi 4 sẽ mất sạch bằng chứng và kết luận "giảm giá sâu không liên quan đến lợi nhuận" sẽ hoàn toàn sai. Vì vậy giữ nguyên là bắt buộc, không phải tùy chọn.

### G4. Trùng lặp thật là trùng trên **toàn bộ** 20 cột còn lại

Nhóm chỉ xóa bản ghi trùng **hoàn toàn** (bỏ `Row ID`), không xóa dòng chỉ trùng `(Order ID, Product ID)`.

Cơ sở: 8 nhóm có cùng `(Order ID, Product ID)`, nhưng 7 nhóm khác nhau về `Quantity`/`Sales`/`Profit` → đó là các dòng tách hợp lệ trong cùng một đơn (mua nhiều lần, hoặc tách dòng theo giá). Chỉ có 1 nhóm trùng khớp tuyệt đối.

### G5. Dữ liệu là dữ liệu lịch sử, không phải dữ liệu dự báo

Toàn bộ bài phân tích mô tả **điều đã xảy ra** trong giai đoạn 2014–2017. Không có mô hình nào được dùng để dự báo doanh thu, lợi nhuận hay số đơn cho giai đoạn sau.

### G6. `Order ID` là mã đơn hàng, không phải mã địa lý

Tiền tố `CA-` và `US-` trong `Order ID` **không phải** mã bang. Phân bố của chúng theo bang rất không đều (`CA-` xuất hiện ở cả 4 vùng), nên suy ra vị trí từ `Order ID` là sai. Mã bưu chính và cột `State` mới là nguồn địa lý đúng.

### G7. Năm trong `Order ID` là năm hệ thống gán mã, không phải năm đặt hàng

7 dòng có `Order Date` là 2016-12-31 nhưng năm trong `Order ID` là 2017. Nhóm hiểu đây là quy ước gán mã (đơn đặt cuối năm mang mã năm giao hàng) và **giữ nguyên**. Khi phân tích theo thời gian, dùng `Order Date`, không dùng năm trong `Order ID`.

### G8. Biên lợi nhuận của nhóm = tổng `Profit` ÷ tổng `Sales`

Dùng tỉ số **cộng dồn trước, chia sau**, không trung bình các tỉ lệ từng dòng. Hai cách cho kết quả khác nhau khi phân phối lệch mạnh — và `Profit` lệch mạnh (skew 7,56). Với `Technology`, cách dùng trong EDA cho 17,40%.

### G9. `Order Date` là mốc thời gian nghiệp vụ chính

Mọi phân tích xu hướng, mùa vụ và so sánh năm dùng `Order Date`, **không** dùng năm trong `Order ID` (xem G7). `Ship Date` chỉ dùng cho thời gian giao hàng; `Ship Date` tới 05/01/2018 là do đơn đặt cuối năm 2017.

### G10. Các giá trị ngoại lì trong `Sales`/`Profit` là giao dịch thật

Giữ nguyên toàn bộ 1.870 dòng lỗ sau khử trùng lặp. Vì vậy khi so sánh nhóm, nhóm phải báo cáo **kèm** trung vị hoặc tỉ lệ, không chỉ tổng và trung bình — xem L13.

### G11. `Ship Date` phản ánh thời điểm giao hàng thực tế

Dùng để tính thời gian giao hàng (`Ship Date` − `Order Date`): trung vị 4 ngày, tối đa 7 ngày, không có giá trị âm.

### G12. Không suy luận nhân quả từ tương quan

Mọi phát hiện trong EDA là **mối liên hệ quan sát**. Ngôn ngữ bắt buộc: "có mối liên hệ", "đi kèm", "xuất hiện cùng". Cấm: "gây ra", "làm nên", "dẫn tới" — xem mục 4.

---

## 1b. Giới hạn riêng khi tính **Order Value** (điểm cần đọc kỹ)

Đây là nhóm giới hạn quan trọng nhất trong phần EDA, vì AOV là chỉ số được dùng để so sánh khu vực và phân khúc.

| # | Giới hạn | Hệ quả |
|---|---|---|
| OV1 | **AOV không phải giá trị vòng đời khách hàng (CLV).** Nó chỉ là giá trị của các đơn **quan sát được trong 01/2014 – 12/2017**. | Doanh nghiệp không biết một khách hàng sẽ quay lại bao nhiêu lần. Không được viết "khách hàng `Home Office` có giá trị 472 USD/đơn" như một thuộc tính bền vững của phân khúc. |
| OV2 | **AOV bị ảnh hưởng bởi cơ cấu nhóm sản phẩm.** Một vùng có AOV thấp có thể chỉ vì bán nhiều sản phẩm giá trị thấp, không phải vì khách mua kém. | Ví dụ `Office Supplies` có AOV thấp nhất (192,16 USD) nhưng biên lợi nhuận lại cao (17,04%). **Không dùng AOV một mình để kết luận về "chất lượng khách hàng".** |
| OV3 | **Số đơn của một nhóm là số đơn *chứa* nhóm đó**, không phải số đơn *chỉ gồm* nhóm đó. Một đơn hỗn hợp xuất hiện ở cả 3 nhóm Category. | Tổng số đơn của 3 nhóm Category (1.544 + 1.764 + 3.742 = **7.050**) **lớn hơn** tổng số đơn thực tế (5.009). Vì vậy AOV phải tính **trên tập đơn của từng nhóm**, tuyệt đối không cộng lại hay trung bình hoá. |
| OV4 | **AOV không có trọng số đơn.** Một đơn 5.000 USD và một đơn 20 USD đều được tính là 1 đơn. | AOV phụ thuộc mạnh vào vài đơn lớn. Với `Technology`, AOV 541,55 USD trong khi trung vị giá trị đơn thấp hơn nhiều — nên báo cáo kèm trung vị. |
| OV5 | **Không có cột chi phí vận chuyển hay giá vốn** → không tính được biên lợi nhuận gốc. | Không tách được ảnh hưởng của chi phí khỏi ảnh hưởng của giảm giá trong `Profit` âm. |
| OV6 | **Giá trị đơn trung bình cấp nhóm khác nhau rất ít** (vùng 426–484 USD; phân khúc 449–472 USD). | Chênh lệch nhỏ, trong khi sai số thống kê có thể lớn hơn chênh lệch. Vì vậy EDA **không** kết luận "vùng này có đơn giá trị cao hơn" một cách khẳng định — chỉ mô tả chênh lệch. |
| OV7 | **Không có dữ liệu khách hàng mới / quay lại.** | Không phân tích được thu hút và giữ chân khách hàng. |

---

## 2. Giới hạn của dataset

| # | Giới hạn | Hệ quả đối với phân tích |
|---|---|---|
| L1 | **Dữ liệu mẫu do người đăng trên Kaggle dẫn từ Tableau**, chỉ dùng cho mục đích giáo dục; không phải dữ liệu đã xác minh của một doanh nghiệp bán lẻ thực tế | Không thể dùng kết quả để ra quyết định kinh doanh ngoài đời. Mọi kết luận chỉ có giá trị trong phạm vi bài tập. |
| L2 | **Chỉ một quốc gia** (`United States`), 49 tiểu bang, 531 thành phố | Không có cơ sở để so sánh với thị trường quốc tế hoặc kết luận về xu hướng toàn cầu. |
| L3 | **Chỉ 4 vùng** (`Central`, `East`, `South`, `West`) — phân vùng nội bộ Tableau | Phân tích theo vùng chỉ có 4 mức, độ lực thống kê thấp; không thể suy ra xu hướng vùng từ n = 4. |
| L4 | **Gian lệch mạt độ theo thời gian**: doanh thu tăng từ 483.966 (2014) lên 733.215 (2017); tháng 11–12 chiếm **29,5%** doanh thu cả 4 năm (riêng tháng 12 là 14,2%) | Kết luận "tăng trưởng" phải đi kèm cảnh báo về tính mùa vụ rất mạnh. Tháng 1–2 thường thấp nhất. |
| L5 | **Không có cột chi phí, khách hàng mới/quay lại, mã khuyến mãi, hay lịch sử tồn kho** | Không tính được lợi nhuận biên trên doanh thu (chỉ có `Profit` sản phẩm), không phân tích được thu hút khách hàng hay hiệu quả khuyến mãi. |
| L6 | **Không có cột giá niêm yết / giá vốn** | `Profit` được cho sẵn, không kiểm chứng lại được. Không tách được "giảm giá" và "chi phí tăng" trong `Profit` âm. |
| L7 | **Một dòng = một mặt hàng, nhưng đơn hàng không có bảng đầu đơn riêng** | 2.471 trong 5.009 đơn có từ 2 dòng trở lên (tối đa 14 dòng/đơn). Không có trường "số sản phẩm khác nhau trong đơn" hay "số nhóm sản phẩm trong đơn" một cách trực tiếp — phải suy ra bằng groupby. |
| L8 | **Dữ liệu kết thúc 31/12/2017** (`Ship Date` tới 05/01/2018) | Không thể kiểm tra hiệu ứng mùa năm 2018, không có dữ liệu cho giai đoạn COVID để so sánh. |
| L9 | **Chỉ 4 năm dữ liệu (48 tháng, đủ đủ các tháng)** | Đủ để mô tả xu hướng và mùa vụ; **không đủ** để xác định chu kỳ dài hạn hoặc kiểm định xu hướng thống kê chắc chắn. |
| L10 | **16 tên sản phẩm dùng chung nhiều `Product ID`** (tối đa 10 mã cho một tên) | Gom nhóm theo `Product Name` có thể gộp nhầm sản phẩm khác nhau. Phân tích sản phẩm nên dùng `Product ID` hoặc `Sub-Category`. |
| L11 | **`Row ID` là số thứ tự dòng, không mang ý nghĩa nghiệp vụ** | Dùng `Row ID` làm biến đầu vào của mô hình là sai — nó chỉ là mã định danh, và tương quan nghịch với thứ tự thời gian. |
| L12 | **`Sales` lệch phải mạnh** (median 54,48, max 22.638,48; 1.167 dòng ngoài IQR 1.5×) | Hồi quy tuyến tính trên `Sales` không có phép biến đổi nào sẽ cho phần dư ổn định; cần cân nhắc log hoặc mô hình khác — xem giới hạn mô hình bên dưới. |
| L13 | **Ngoại lì chi phối mạnh các hệ số tương quan** — kiểm chứng định lượng trong EDA | r(`Sales`,`Profit`) = 0,479 toàn bộ dữ liệu nhưng chỉ còn **0,313** khi giới hạn `Sales ≤ 5.000` và **0,204** với `log1p(Sales)`. Tương tự, r(`Discount`,`Profit`) = −0,219 giảm còn **−0,071** khi loại dòng lỗ. → **Bắt buộc báo cáo cả hai cách**, không báo cáo một con số đơn lẻ. |
| L14 | **`Profit` âm chi phối mọi thống kê trung bình của nhóm lỗ.** Dòng lỗ tệ nhất −6.599,98 USD bằng **761 lần** giá trị trung vị lợi nhuận một dòng (8,67 USD) | Các nhóm có tỉ lệ dòng lỗ cao (`Furniture` 33,6%, `Central` 31,9%) phải được đánh giá bằng **biên lợi nhuận** và **trung vị lợi nhuận**, không chỉ bằng tổng lợi nhuận. |
| L15 | **`Discount` là biến rời rạc có thứ tự (12 mức), phân bố lệch** (48,01% bằng 0; skew 1,68) | Không phải biến liên tục thuần. So sánh giữa các mức giảm giá **không cân bằng về đặc tính sản phẩm** (giảm giá chỉ xảy ra ở một số nhóm) → mức giảm giá không thể tách khỏi nhóm sản phẩm khi diễn giải. |
| L16 | **Các mức giảm giá 0,32 / 0,45 / 0,60 chỉ có 11–138 dòng** | Kết luận cho từng mức riêng lẻ có độ tin cậy thấp. Đáng tin hơn là **xu hướng theo ngưỡng ~30%**. |
| L17 | **`Quantity` có đa dạng thấp** (chỉ 1–14, tập trung 2–5; 14 giá trị duy nhất) | r(`Quantity`,`Profit`) = 0,066 → gần như không có thông tin cho phân tích ở cấp dòng. |
| L18 | **`Customer ID` / `Customer Name` đã ẩn danh** thành `CUST-nnn` | Dùng để gom nhóm và đếm khách hàng (793 khách) là tốt, nhưng **không** dùng làm biến dự báo, và không thể kiểm tra lại tính đúng đắn của việc khử trùng lặp ở cấp khách hàng. |
| L19 | **`Order ID` có tiền tố `CA-`/`US-` không nhất quán** | Không dùng để suy ra bang hoặc năm (xem G6, G7). |
| L20 | **`Sub-Category` có 17 nhóm nhưng 3 nhóm âm** (`Tables` −17.725,48; `Bookcases` −3.472,56; `Supplies` −1.189,10) — hai nhóm đầu thuộc `Furniture`, `Supplies` thuộc `Office Supplies` | Kết luận cấp nhóm (`Furniture` biên LN 2,49%) là trung bình của các phần rất khác nhau → phải đào sâu cấp sub-category trước khi ra quyết định. |
| L21 | **Không có đánh giá hài lòng, tỉ lệ hoàn trả hay mã khuyến mãi** | Không đánh giá được tác động của tốc độ giao hàng (`Ship Mode`) hay hiệu quả từng chiến dịch khuyến mãi cụ thể. |

---

## 3. Những trường hợp **không đủ dữ liệu để kết luận**

| Câu hỏi | Trạng thái | Vì sao |
|---|---|---|
| "Giảm giá **một tỷ lệ** bao nhiêu thì lợi nhuận vẫn dương?" | **Không kết luận được** | Dataset không có cột giá niêm yết hay giá vốn → không tách được "doanh thu giảm vì giảm giá" khỏi "chi phí tăng". Chỉ mô tả được **tương quan quan sát** giữa mức giảm giá và lợi nhuận. |
| "Đơn hàng có nhiều sản phẩm khác nhau thì lợi nhuận tốt hơn?" | **Không kết luận được** | Không có bảng đầu đơn; số nhóm sản phẩm trong đơn phải suy ra. Có thể báo cáo như một phát hiện mô tả, không khẳng định quan hệ nhân quả. |
| "Khách hàng `Home Office` có giá trị đơn cao hơn vì mua ít lần hơn?" | **Không kết luận được** | Không có dữ liệu lịch sử mua theo thời gian của từng khách hàng (chỉ có 1 lần mua ghi nhận trong giai đoạn này cho nhiều khách). |
| "Nguyên nhân doanh thu tăng 2014→2017 là gì?" | **Không kết luận được** | Không có dữ liệu chi phí, đầu tư, mở rộng cửa hàng hay thay đổi giá → không phân rã được động lực tăng trưởng. |
| "Chiến lược giảm giá nào tối ưu?" | **Không kết luận được** | Thiếu quan hệ giữa giảm giá và lượng bán, chi phí, và doanh thu hồi (repeat). Dataset không đủ để tối ưu. |
| "Mối liên hệ giữa tốc độ giao hàng và hài lòng khách hàng?" | **Không đủ dữ liệu** | Không có cột đánh giá hài lòng hay tỉ lệ hoàn trả. |

---

## 4. Giới hạn về cách diễn giải: tương quan **KHÔNG** phải nhân quả

Đây là điểm quan trọng nhất khi đọc kết quả của nhóm.

- Mọi phát hiện trong bài này là **mối liên hệ quan sát** (association) trên dữ liệu lịch sử, được mô tả bằng từ "có liên hệ", "đi kèm", "xuất hiện cùng".
- **Không** dùng các cụm "giảm giá **gây ra** lỗ", "khu vực **làm nên** doanh thu cao", "chính sách giảm giá **đã dẫn tới**…" — những cách diễn giải đó vượt quá mức dữ liệu có thể chứng minh.
- Lý do cụ thể:
  1. **Không có thí nghiệm.** Không có nhóm đối chứng, không có phân phối ngẫu nhiên.
  2. **Có thể có yếu tố gây nhiễu (confounder)** không có trong dataset: chi phí vận chuyển, giá vốn, chương trình khuyến mãi theo mùa, sự khác biệt giữa các cửa hàng.
  3. **Tương quan ngược có thể xảy ra.** Ví dụ: sản phẩm giảm giá mạnh thường là sản phẩm **đã sắp hết hàng** hoặc **chủ động hạ giá để xả tồn kho** → "giảm giá nhiều đi kèm lợi nhuận thấp" có thể là hệ quả của tình huống hàng hóa, không phải của chính mức giảm giá.  4. **Hồi quy tuyến tính không chứng minh quan hệ nhân quả.** Hệ số mô hình chỉ mô tả mức phù hợp tuyến tính trong dữ liệu đã quan sát. Ngay cả khi mô hình dự đoán tốt trên tập kiểm tra thì cũng không chứng minh được tác động can thiệp.
- Hệ quả với phần hồi quy của nhóm: kết luận nên viết là *"biến X có mối liên hệ với doanh thu, với hệ số ước lượng …"*, **không** viết *"tăng X làm doanh thu tăng …"*.

### 4.1 Áp dụng cụ thể cho phát hiện chính của EDA

**Phát hiện:** từ mức giảm giá 0,32 trở lên, **100% số dòng đều lỗ**; biên lợi nhuận chuyển từ +29,51% (mức 0) sang âm từ mức 0,30.

| Cách viết **SAI** (không được dùng) | Cách viết **ĐÚNG** |
|---|---|
| "Giảm giá sâu **gây ra** lỗ trên 100% dòng ở mức từ 32%." | "Ở các mức giảm giá từ 32% trở lên, **100% số dòng quan sát được đều lỗ**; biên lợi nhuận nhóm **đi kèm** với mức giảm giá cao và chuyển sang âm từ mức 30%." |
| "Chính sách giảm giá 40% **làm nên** lỗ 16.187,40 USD ở `Furniture`." | "Nhóm dòng có giảm giá 40% **ghi nhận** tổng lỗ 23.057,05 USD; **tương quan quan sát** giữa mức giảm giá và lợi nhuận là yếu (r = −0,219)." |
| "Khu vực `Central` **làm nên** biên lợi nhuận thấp 7,92%." | "`Central` **có** biên lợi nhuận quan sát thấp nhất (7,92%) cùng tỉ lệ dòng lỗ cao nhất (31,9%); nguyên nhân **không xác định được** từ dữ liệu này." |

**Ba lý do cụ thể không thể kết luận nhân quả cho cặp Discount–Profit** (chi tiết nhất ở câu hỏi 4, mục 9 của notebook):

1. **Tương quan ngược rất dễ xảy ra.** Sản phẩm bị giảm giá mạnh thường là sản phẩm **sắp hết hàng** hoặc **chủ động xả tồn kho**. Khi đó "giảm giá nhiều" và "lợi nhuận thấp" là **hai hệ quả của cùng một nguyên nhân** (tình trạng hàng hóa) — không phải giảm giá sinh ra lỗ.
2. **Thiếu biến kiểm soát.** Không có cột chi phí vốn, chi phí vận chuyển, tồn kho hay chi phí thanh lý → không tách được "doanh thu giảm vì giảm giá" khỏi "chi phí tăng".
3. **Không có thí nghiệm, không có nhóm đối chứng, không có phân phối ngẫu nhiên.** Mọi giải thích nhân quả đều không kiểm chứng được.

**Ràng buộc định lượng:** r(`Discount`,`Profit`) = −0,219 tương ứng **R² ≈ 4,8%** → mức giảm giá chỉ giải thích rất ít biến động lợi nhuận ở cấp dòng. Không thể dùng mức giảm giá để dự báo lợi nhuận của một dòng.

**Lưu ý quan trọng:** dữ liệu **không** cho thấy giảm giá làm mất doanh thu — r(`Discount`,`Sales`) = −0,028 (gần như không có mối liên hệ tuyến tính), và tổng doanh thu ở mức giảm giá 0,50 vẫn là 58.918,54 USD trên 66 dòng (TB 892,71 USD/dòng, cao hơn TB chung 229,85 USD). Vấn đề nằm ở **hiệu quả**, không phải ở **quy mô**.

---

## 5. Giới hạn riêng cho phần hồi quy tuyến tính (phần của thành viên khác)

Để thành viên phụ trách hồi quy tham chiếu khi đọc file sạch:

| # | Giới hạn | Gợi ý xử lý |
|---|---|---|
| M1 | **Một đơn hàng có nhiều dòng** → các dòng trong cùng đơn không độc lập nhau. Chia tập ngẫu nhiên theo dòng rò rỉ thông tin giữa tập huấn luyện và kiểm tra, làm R² trông đẹp hơn thực tế | Giữ các dòng cùng `Order ID` trong cùng một tập, **hoặc** chia theo thời gian (train 2014–2016, test 2017) nếu mục tiêu là đánh giá trên giai đoạn mới |
| M2 | **`Sales` lệch phải mạnh** (L12) | Cân nhắc `log1p` cho `Sales`/`Profit`, hoặc báo cáo kèm MAE/RMSE (đơn vị tiền thật) bên cạnh R² |
| M3 | **Không được đưa vào `X`**: `Row ID`, `Order ID`, `Customer ID`, `Customer Name` (định danh), `Profit` (tính từ chính `Sales`), `Order Date`/`Ship Date` dạng thô (mã định danh tuyến tính) | Biến thời gian nên tách thành `Year`, `Month`, `Quarter` |
| M4 | **Mô hình mốc (DummyRegressor)** bắt buộc để so sánh | Nếu mô hình hồi quy không vượt mốc trung bình trên tập kiểm tra thì phải nói rõ là vậy |
| M5 | **`Discount` không độc lập với `Category`** — giảm giá chỉ xảy ra với nhóm cụ thể | Kiểm tra hệ số `Discount` trong từng nhóm, đừng diễn giải hệ số tổng một cách đơn giản |
| M6 | **R² cao không đồng nghĩa mô hình hữu ích** | Báo cáo thêm giá trị lợi nhuận theo mức giảm giá từ EDA (D11) để người đọc thấy bối cảnh |
| M7 | **Không ngoại suy ngoài phạm vi quan sát** (`Discount` 0–0.8, `Quantity` 1–14, năm 2014–2017) | Không dùng mô hình để dự báo ngoài các khoảng này |

---

## 6. Tính chất của bài phân tích

> **Đây là phân tích dữ liệu lịch sử, KHÔNG phải dự báo tương lai.**

- Mọi biểu đồ và con số trong bài mô tả **điều đã xảy ra** trong giai đoạn 01/2014 – 12/2017.
- Không có kết luận nào được đưa ra về doanh thu, lợi nhuận hay số đơn hàng của các năm sau 2017.
- Nếu bài trình bày cần một câu kết luận về tương lai, phải ghi rõ đó là **nhận định định tính dựa trên xu hướng quan sát được**, không phải kết quả dự báo có kiểm chứng.
- Mô hình hồi quy của nhóm **được dùng để đo độ khớp của mô hình tuyến tính trên dữ liệu quá khứ**, không phải để dự báo.

### 6.1 Áp dụng cho kết luận EDA (D9–D14)

| Kết luận trong EDA | Tại sao **không** phải dự báo |
|---|---|
| "Doanh thu tăng 51,5% từ 2014 đến 2017" | Mô tả **quá khứ**. Không có nghĩa doanh thu 2018 sẽ tăng tiếp 51,5% — mùa vụ, cung cầu và hành vi thị trường đều thay đổi. |
| "AOV giảm 13,0% từ 2014 đến 2017" | Không có cơ sở để nói AOV sẽ tiếp tục giảm. Có thể là dịch chuyển cơ cấu nhóm sản phẩm, cũng có thể là yếu tố một lần. |
| "Mùa vụ: tháng 11–12 chiếm 29,5% doanh thu" | Là đặc tính của **giai đoạn quan sát 2014–2017**. Lịch khuyến mãi, ngày lễ và hành vi mua có thể thay đổi. |
| "Từ mức giảm giá 30% trở lên, biên lợi nhuận âm" | Là **mối quan sát trong dữ liệu lịch sử**. Không phải ngưỡng tối ưu có thể áp dụng cho tương lai, vì cơ cấu chi phí và giá vốn có thể thay đổi. |
| "Tăng trưởng đến từ nhiều đơn giá trị nhỏ hơn" | Là **diễn giải của một quan sát mô tả**, không phải kết luận về cơ chế. Nguyên nhân thực sự không xác định được (xem L5, L6). |

**Nguyên tắc khi trình bày:** mọi câu chữ về tương lai phải ghi rõ là **nhận định định tính dựa trên xu hướng quan sát được**, kèm điều kiện "nếu xu hướng và cơ cấu kinh doanh không thay đổi đáng kể".

---

## 7. Ma trận truy vết: kết luận EDA ↔ giới hạn áp dụng

| Kết luận EDA | Số liệu | Giới hạn cần đọc kèm |
|---|---|---|
| `Technology` tốt nhất, `Furniture` kém nhất | Biên LN 17,40% vs 2,49%; 33,6% dòng lỗ | L14, L20, OV2 |
| `Central` biên LN thấp nhất | 7,92%, 31,9% dòng lỗ | L3 (n = 4 vùng), L5 |
| AOV gần như bằng nhau giữa các nhóm | 426–484 USD (vùng), 449–472 USD (phân khúc) | OV1–OV4, OV6 |
| Giảm giá liên hệ yếu với lợi nhuận | r = −0,219, R² ≈ 4,8% | L13, L15, L16, mục 4.1 |
| Tăng trưởng 2014→2017 | DT +51,5%, LN +88,5%, đơn +74,1% | L4, L9, mục 6.1 |
| AOV giảm 13,0% | 499,45 → 434,63 USD | OV4, mục 6.1 |
| Tháng 11–12 chiếm 29,5% doanh thu | 352.461 + 325.293 USD | L4, L9 |
