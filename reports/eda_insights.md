# EDA Insights — DHV301 Retail Sales Intelligence

**Người phụ trách:** Hưng
**Nguồn:** `data_cleaned/superstore_clean.csv` (9.993 dòng × 21 cột) — chỉ dùng file sạch, không đọc lại file thô.
**Notebook:** [`notebooks/01_data_cleaning_eda.ipynb`](../notebooks/01_data_cleaning_eda.ipynb) — mục 5–11.
**Giai đoạn phân tích:** 01/01/2014 – 31/12/2017 (48 tháng đầy đủ, không thiếu tháng nào).

> **Mọi con số trong báo cáo này đều được in ra từ chính dữ liệu trong notebook.**
> Mọi phát hiện là **mối liên hệ quan sát** trên dữ liệu lịch sử — không phải quan hệ nhân quả, và không phải kết quả dự báo tương lai.

---

## Tóm tắt nhanh

| Câu hỏi | Trả lời một câu |
|---|---|
| **Q1** Xu hướng theo tháng/năm | Doanh thu **+51,5%**, lợi nhuận **+88,5%**, số đơn **+74,1%** (2014→2017) — nhưng **AOV giảm 13,0%**, tức tăng trưởng đến từ nhiều đơn giá trị nhỏ hơn. Mùa vụ cực mạnh: tháng 11–12 chiếm **29,5%** doanh thu. |
| **Q2** Nhóm sản phẩm | Tốt nhất: **`Technology`** (biên LN 17,40%). Kém nhất: **`Furniture`** — doanh thu chỉ kém 11% nhưng lợi nhuận kém 87%, biên LN chỉ **2,49%**, 33,6% dòng lỗ. |
| **Q3** Khu vực & phân khúc | Khác nhau rõ về **quy mô**, gần như không khác nhau về **giá trị đơn** (AOV vùng 426–484 USD; phân khúc 449–472 USD). `Central` biên LN thấp nhất (**7,92%**); `Home Office` cao nhất (**14,05%**). |
| **Q4** Mức giảm giá | **Không** liên hệ với doanh thu (r = **−0,028**). Liên hệ **phân tầng theo ngưỡng** với lợi nhuận: biên LN +29,51% ở mức 0% → **âm từ 30%**; 6 mức (0,32–0,80) có **100% dòng lỗ**. r = −0,219 (R² ≈ 4,8%). |

---

## Q1 — Doanh thu, lợi nhuận và số đơn hàng thay đổi thế nào theo tháng và năm?

### Kết luận

Cả ba đại lượng đều tăng mạnh trong giai đoạn 2014–2017 theo ba nhịp khác nhau, và bị chi phối bởi mùa vụ cuối năm. Đáng chú ý nhất: **số đơn tăng nhanh hơn doanh thu, dẫn tới AOV giảm** — quy mô tăng trưởng đến từ *nhiều đơn giá trị nhỏ hơn*, không phải đơn lớn hơn.

### Số liệu chứng minh

| Năm | Doanh thu | Lợi nhuận | Số đơn | AOV | Biên LN | Doanh thu YoY | Lợi nhuận YoY |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 483.966 | 49.556 | 969 | 499,45 | 10,24% | — | — |
| 2015 | 470.533 | 61.619 | 1.038 | 453,31 | 13,10% | −2,78% | +24,34% |
| 2016 | 609.206 | 81.795 | 1.315 | 463,27 | 13,43% | +29,47% | +32,74% |
| 2017 | 733.215 | 93.439 | 1.687 | 434,63 | 12,74% | +20,36% | +14,24% |

**Cả giai đoạn 2014→2017:** doanh thu **+51,5%**, lợi nhuận **+88,5%**, số đơn **+74,1%**, AOV **−13,0%**.

**Điểm cực đại / cực điểm theo tháng:**

| | Cao nhất | Thấp nhất |
|---|---|---|
| Doanh thu | 11/2017 = 118.447,82 USD | 02/2014 = 4.519,89 USD (chênh **26 lần**) |
| Lợi nhuận | 12/2016 = 17.885,31 USD | 01/2015 = −3.281,01 USD |
| Số đơn | 11/2017 = 261 đơn | 02/2014 = 28 đơn |

**Mùa vụ:** tháng 11–12 chiếm **29,5%** doanh thu cả 4 năm (riêng tháng 12 là 14,2%). Theo quý: Q4 chiếm **38,23%**, Q1 chỉ 15,66%. Tỉ lệ doanh thu trung bình/tháng cao nhất / thấp nhất = **5,9 lần** (tháng 11: 88.115 USD; tháng 2: 14.938 USD). Hình dạng mùa vụ **lặp lại nhất quán qua cả 4 năm**.

**Rủi ro cấp tháng:** 2 tháng có lợi nhuận âm — 07/2014 (−841,48), 01/2015 (−3.281,01).

### Biểu đồ

* **Hình 9** — Xu hướng theo tháng: doanh thu, lợi nhuận, số đơn (`nunique Order ID`)
* **Hình 10** — So sánh theo năm + hình dạng mùa vụ qua 4 năm + đường trung bình theo tháng
* **Hình 11** (panel trên-trái) — Cột nhóm theo năm

**Vì sao chọn loại biểu đồ:** dữ liệu là chuỗi thời gian thủy thủ 48 tháng liên tục → **đường** thể hiện xu hướng và chu kỳ rõ ràng nhất (cột sẽ che mất tính liên tục). Để đặt doanh thu và số đơn cạnh nhau với thang đo khác nhau, dùng **2 trục y**.

### Diễn giải kinh doanh

Quy mô kinh doanh mở rộng đều đặn cả về doanh thu, lợi nhuận lẫn số lượng đơn. Biên lợi nhuận cải thiện từ 10,24% lên ~13% rồi giữ ổn định → tăng trưởng **không** phải do bán rủi ro hơn. Năm 2015 là năm duy nhất giảm doanh thu (−2,78%) nhưng lợi nhuận vẫn tăng +24,34% → cấu trúc đơn hàng tốt hơn.

### Giới hạn của nhận định

* Chỉ 4 năm dữ liệu → **không đủ** xác định chu kỳ dài hạn hay kiểm định xu hướng thống kê chắc chắn.
* Mùa vụ chi phối mạnh (max/min doanh thu trung bình/tháng = 5,9 lần) → **không nên so sánh tháng này với tháng khác trực tiếp**, phải so cùng tháng giữa các năm.
* 2 tháng lợi nhuận âm cho thấy biến động lớn ở cấp tháng → cần cẩn trọng khi ra quyết định theo tháng.
* Không có dữ liệu chi phí, khuyến mãi hay đầu tư → **không xác định được nguyên nhân** của tăng trưởng.
* "AOV giảm" là **hiện tượng quan sát**, không phải kết luận cơ chế. Có thể do dịch chuyển cơ cấu nhóm sản phẩm, cũng có thể là yếu tố một lần.

---

## Q2 — Nhóm sản phẩm nào hoạt động tốt nhất và kém nhất về doanh thu và lợi nhuận?

### Kết luận

`Technology` tốt nhất về **cả** doanh thu và lợi nhuận. Nhóm **kém nhất là `Furniture`** — không phải vì doanh thu thấp nhất, mà vì **biên lợi nhuận chỉ 2,49%**, thấp hơn ~7 lần so với hai nhóm còn lại dù doanh thu chỉ kém 11%.

### Số liệu chứng minh

| Nhóm | Doanh thu | Lợi nhuận | Số lượng | Số đơn | AOV | Biên LN | % dòng lỗ |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Technology** | **836.154** | **145.455** | 6.939 | 1.544 | **541,55** | **17,40%** | 14,7% |
| Furniture | 741.718 | 18.463 | 8.026 | 1.764 | 420,48 | **2,49%** | **33,6%** |
| Office Supplies | 719.047 | 122.491 | **22.906** | 3.742 | 192,16 | 17,04% | 14,7% |

* `Technology` chiếm **36,4%** doanh thu nhưng **50,8%** lợi nhuận.
* `Furniture`: doanh thu kém `Technology` **11,3%** nhưng lợi nhuận kém **87,3%**.
* `Furniture` có tỉ lệ dòng lỗ cao nhất: **33,6%** (713/2.120 dòng).

**Ba mô hình kinh doanh khác nhau:** `Technology` = giá trị đơn cao, số lượng thấp · `Office Supplies` = số lượng lớn, AOV thấp nhưng lượng lớn nên vẫn lợi nhuận tốt · `Furniture` = doanh thu lớn nhưng mất tiền ở các dòng giảm giá sâu.

**Cấp sub-category (đào sâu hơn):**

| Kém nhất | | Tốt nhất | |
|---|---:|---|---:|
| `Tables` | **−17.725,48** (biên −8,56%) | `Copiers` | **55.617,82** |
| `Bookcases` | −3.472,56 (biên −3,02%) | `Phones` | 44.515,73 |
| `Supplies` | −1.189,10 (biên −2,55%) | `Accessories` | 41.936,64 |

2 trong 3 sub-category âm thuộc `Furniture` (`Tables`, `Bookcases`); `Supplies` thuộc `Office Supplies`. Đáng chú ý: `Copiers` chỉ **68 đơn** nhưng tạo 55.618 USD lợi nhuận — AOV **2.198,94 USD/đơn**, cao nhất toàn bộ nhóm sản phẩm.

### Biểu đồ

* **Hình 3** — Cột nhóm doanh thu & lợi nhuận theo Category + biên lợi nhuận theo Category
* **Hình 11** (panel trên-phải) — Biên lợi nhuận theo nhóm sản phẩm

**Vì sao chọn loại biểu đồ:** **cột nhóm (grouped bar)** để so sánh hai đại lượng (doanh thu, lợi nhuận) trên cùng trục tiền cho ba nhóm rời rạc — độ dài cột so sánh trực tiếp, dễ đọc hơn đường. Panel thứ hai tách riêng **biên lợi nhuận (%)** vì đặt chung trục với doanh thu sẽ làm phát hiện quan trọng nhất bị chìm.

### Diễn giải kinh doanh

Vấn đề của `Furniture` nằm ở `Tables` và `Bookcases` — nhóm sản phẩm có giá trị đơn cao nhưng thường xuyên bị giảm giá mạnh (chi tiết ở Q4). (Xét toàn ngành hàng, `Binders` — `Office Supplies` — và `Machines` — `Technology` — là hai sub-category lỗ nặng nhất.) Đây là ứng viên rõ ràng nhất cho việc rà soát chính sách giảm giá.

### Giới hạn của nhận định

* `Furniture` có 33,6% dòng lỗ nhưng vẫn sinh lợi nhuận dương ở cấp nhóm → **không được nói "Furniture lỗ"**. Đây là nhóm *hiệu quả thấp*, không phải nhóm lỗ.
* Không có cột chi phí vận chuyển hay chi phí bán hàng → **không xác định được nguyên nhân gốc rễ**. "Chi phí vận chuyển hàng nặng" là giả thuyết hợp lý cho `Tables`/`Bookcases` nhưng **không kiểm chứng được** từ dữ liệu này.
* Phân tích cấp nhóm bị hiệu ứng Simpson → phải đào sâu cấp sub-category mới kết luận được, và kết luận ở cấp sub-category vẫn mang tính mô tả.

---

## Q3 — Khu vực và phân khúc khách hàng khác nhau thế nào?

### Kết luận

Khu vực và phân khúc **khác nhau rõ về quy mô** (doanh thu, số đơn) **nhưng gần như không khác nhau về giá trị đơn trung bình**. Điểm đáng chú ý nhất: `Central` (biên LN thấp nhất) và `Consumer` (biên LN thấp nhất dù doanh thu cao nhất).

### Số liệu chứng minh — theo khu vực

| Khu vực | Doanh thu | Lợi nhuận | Số đơn | **AOV** | Biên LN | % dòng lỗ |
|---|---:|---:|---:|---:|---:|---:|
| West | **725.458** | **108.418** | 1.611 | 450,32 | 14,94% | 9,9% |
| East | 678.500 | 91.535 | 1.401 | **484,30** | 13,49% | 19,4% |
| Central | 501.240 | 39.706 | 1.175 | 426,59 | **7,92%** | **31,9%** |
| South | **391.722** | 46.749 | 822 | 476,55 | 11,93% | 16,0% |

### Số liệu chứng minh — theo phân khúc

| Phân khúc | Doanh thu | Lợi nhuận | Số đơn | **AOV** | Biên LN | % dòng lỗ |
|---|---:|---:|---:|---:|---:|---:|
| Consumer | **1.161.401** | **134.119** | 2.586 | 449,11 | 11,55% | 19,3% |
| Corporate | 706.146 | 91.979 | 1.514 | 466,41 | 13,03% | 18,4% |
| Home Office | 429.372 | 60.311 | 909 | **472,36** | **14,05%** | 17,5% |

### Ba so sánh đáng chú ý

1. **AOV gần như bằng nhau giữa các phân khúc:** 449,11 / 466,41 / 472,36 USD — chênh tối đa **5,2%** — trong khi doanh thu chênh tới **2,7 lần** và số đơn chênh **2,8 lần**. → Phân khúc khác nhau về *số lượng khách hàng và tần suất mua*, gần như không khác về *giá trị mỗi lần mua*.
2. **AOV chênh nhỏ giữa các khu vực:** 426,59 – 484,30 USD (chênh 13,5%) so với doanh thu chênh 1,85 lần. → Quy mô vùng phụ thuộc nhiều vào *số khách hàng*, ít phụ thuộc vào *giá trị đơn*.
3. **`Central` là vùng cần chú ý:** doanh thu đứng thứ ba nhưng lợi nhuận thấp nhất (39.706) và biên LN thấp nhất (**7,92%**), với **31,9% dòng lỗ** — **gấp 3,2 lần** `West` (9,9%). Chiều ngược lại, `South` có doanh thu thấp nhất nhưng biên LN 11,93% lại **cao hơn `Central`**.

### Biểu đồ

* **Hình 4** — Cột ngang lợi nhuận theo khu vực và theo phân khúc
* **Hình 5** — Cột AOV theo khu vực và theo phân khúc
* **Hình 11** (panel dưới-trái) — AOV so sánh song song

**Vì sao chọn loại biểu đồ:** **cột ngang** cho tên nhóm dài ("Office Supplies", "Home Office") — nằm ngang dễ đọc hơn, và sắp xếp tăng dần giúp so sánh nhanh. Riêng AOV là **đại lượng đơn lẻ** so sánh giữa vài nhóm rời rạc → độ dài cột là trực quan nhất; đặt cạnh nhau để thấy ngay AOV gần như bằng nhau, ngược với chênh lệch lớn về doanh thu.

### Diễn giải kinh doanh

Vùng `West`/`East` và phân khúc `Consumer` là nơi tập trung doanh thu, nhưng **hiệu quả lợi nhuận nằm ở chỗ khác**: `Home Office` có biên LN cao nhất (14,05%) và AOV cao nhất. `Central` vừa doanh thu vừa biên LN đều thấp → ứng viên rà soát về chính sách giảm giá và chi phí vận chuyển.

### Giới hạn của nhận định

* Chỉ **4 khu vực** → độ lực thống kê rất thấp, **không thể kiểm định ý nghĩa thống kê** hay suy ra xu hướng vùng từ n = 4.
* Có 531 thành phố / 49 bang nhưng **không có dữ liệu chi phí theo địa lý** → không phân rã được vì sao `Central` kém.
* `Consumer` là phân khúc lớn nhất (50,6% doanh thu) → kết luận bị ảnh hưởng bởi trọng số mẫu.
* Thiếu dữ liệu khách hàng mới/quay lại → **không** kết luận được phân khúc nào "gia trì" tốt hơn.
* AOV ở đây là giá trị đơn **quan sát trong 2014–2017**, không phải giá trị vòng đời khách hàng (CLV).

---

## Q4 — Mức giảm giá có mối liên hệ thế nào với doanh thu và lợi nhuận?

### Kết luận

Giảm giá **không liên hệ đáng kể với doanh thu** ở cấp dòng (r = −0,028), nhưng **liên hệ với lợi nhuận theo kiểu phân tầng theo ngưỡng**: dưới 30% vẫn sinh lời, **từ 30% trở lên hơn 87% số dòng đều lỗ** (và 100% ở 6 mức 0,32/0,45/0,50/0,60/0,70/0,80). Doanh thu ở các mức giảm giá cao **không biến mất** — nó **chuyển thành doanh thu không sinh lời**.

### Số liệu chứng minh

| Discount | Số dòng | Doanh thu | Lợi nhuận | **Biên LN** | % dòng lỗ |
|---|---:|---:|---:|---:|---:|
| 0,00 | 4.798 | 1.087.908 | 320.988 | **+29,51%** | 0,0% |
| 0,10 | 94 | 54.369 | 9.029 | +16,61% | 4,3% |
| 0,15 | 52 | 27.559 | 1.419 | +5,15% | 32,7% |
| 0,20 | 3.657 | 764.594 | 90.337 | +11,82% | 13,7% |
| 0,30 | 226 | 102.945 | −10.357 | **−10,06%** | 91,6% |
| 0,32 | 27 | 14.493 | −2.391 | −16,50% | **100,0%** |
| 0,40 | 206 | 116.418 | −23.057 | −19,81% | 87,4% |
| 0,45 | 11 | 5.485 | −2.493 | −45,45% | **100,0%** |
| 0,50 | 66 | 58.919 | −20.506 | −34,80% | **100,0%** |
| 0,60 | 138 | 6.645 | −5.945 | −89,46% | **100,0%** |
| 0,70 | 418 | 40.620 | −40.075 | −98,66% | **100,0%** |
| 0,80 | 300 | 16.964 | −30.539 | **−180,03%** | **100,0%** |

**Hệ số tương quan:**

| Cặp | r | R² | Mức độ |
|---|---:|---:|---|
| `Discount` ↔ `Sales` | **−0,028** | 0,08% | Rất yếu — gần như không có mối liên hệ tuyến tính |
| `Discount` ↔ `Profit` | **−0,219** | 4,8% | Yếu, chiều âm |
| `Sales` ↔ `Profit` | **+0,479** | 23,0% | Trung bình, chiều dương |
| `Quantity` ↔ `Profit` | +0,066 | 0,4% | Rất yếu |

**Kiểm tra ảnh hưởng ngoại lì:**

* `Sales` ↔ `Profit`: r = 0,479 toàn bộ → **0,313** khi giới hạn `Sales ≤ 5.000` → **0,204** với `log1p(Sales)`.
* `Discount` ↔ `Profit`: r = −0,219 toàn bộ → **−0,071** khi chỉ xét dòng không lỗ.

→ Phần lớn tín hiệu đến từ chính nhóm dòng lỗ và vài dòng giá trị rất lớn. **Bắt buộc báo cáo cả hai cách.**

**Điểm quan trọng:** doanh thu ở mức giảm giá 0,50 vẫn là **58.918,54 USD trên 66 dòng** (TB 892,71 USD/dòng, cao hơn TB chung 229,85 USD) → dòng lỗ vẫn là dòng doanh thu lớn. **Không có bằng chứng giảm giá làm mất doanh thu.**

### Ngoại lại đáng chú ý

| Dòng | Category / Sub-Category | Sales | Discount | Profit |
|---|---|---:|---:|---:|
| Row ID 7773 | Technology / Machines | 4.499,99 | 0,70 | **−6.599,98** |
| Row ID 684 | Technology / Machines | 7.999,98 | 0,50 | −3.839,99 |
| Row ID 9775 | Office Supplies / Binders | 2.177,58 | 0,80 | −3.701,89 |
| Row ID 6827 | Technology / Copiers | 17.499,95 | **0,00** | **+8.399,98** |
| Row ID 2698 | Technology / Machines | **22.638,48** | 0,50 | −1.811,08 |

* Dòng lỗ tệ nhất (−6.599,98) bằng **761 lần** giá trị trung vị lợi nhuận một dòng (8,67 USD).
* Nghịch lý: `Copiers` bán **không giảm giá** với giá 17.499,95 USD → lãi 8.399,98 (lợi nhuận cao nhất). Cho thấy giảm giá không phải con đường duy nhất tới doanh thu lớn.

### Biểu đồ

* **Hình 7** — Scatter Discount vs Profit, hue theo Category (kèm panel thu nhỏ vùng lỗ)
* **Hình 8** — Scatter Sales vs Profit + đường hồi quy theo nhóm + boxplot Profit theo Discount
* **Hình 11** (panel dưới-phải) — Biên lợi nhuận theo mức giảm giá
* **Hình 6** — Heatmap ma trận tương quan

**Vì sao chọn loại biểu đồ:** **scatter plot** thể hiện từng cặp quan sát nên nhìn thấy cả xu hướng tổng thể *và* các điểm ngoại lại nổi bật — điều mà một con số tương quan không cho biết. Màu theo Category để kiểm tra mối quan hệ có khác nhau giữa các nhóm sản phẩm hay không. Panel thu nhỏ vùng lỗ là cần thiết vì phần lớn dữ liệu tụ về gần gốc, che khuất vùng −3.000…500. **Heatmap** cho cái nhìn toàn cảnh các cặp biến trong một bảng màu, dùng `center=0` để 0 nằm giữa nên màu dương/âm đối xứng nhau, tránh hiểu nhầm thang màu.

### Diễn giải kinh doanh

Có vẻ như một **ngưỡng rủi ro kinh doanh** rõ ràng ở khoảng 30%: dưới ngưỡng, giảm giá vẫn tạo lợi nhuận dương; từ ngưỡng trở lên, mức giảm giá vượt quá biên lợi nhuận gốc của sản phẩm và giao dịch gần như luôn lỗ. Vấn đề là **hiệu quả**, không phải **quy mô**.

### Giới hạn của nhận định — điểm cần nhấn mạnh

> **Không kết luận "giảm giá gây ra lỗ".** Dữ liệu chỉ cho phép nói **có mối liên hệ**. Ba lý do cụ thể:
>
> 1. **Tương quan ngược rất dễ xảy ra.** Sản phẩm bị giảm giá mạnh thường là sản phẩm **sắp hết hàng** hoặc **chủ động xả tồn kho**. Khi đó "giảm giá nhiều" và "lợi nhuận thấp" là **hai hệ quả của cùng một nguyên nhân** (tình trạng hàng hóa), không phải giảm giá sinh ra lỗ.
> 2. **Thiếu biến kiểm soát.** Không có cột chi phí vốn, chi phí vận chuyển, tồn kho hay chi phí thanh lý → không tách được "doanh thu giảm vì giảm giá" khỏi "chi phí tăng". Giảm giá sâu thường đi kèm **giảm giá vốn** khi hàng tồn kho.
> 3. **Không có thí nghiệm, không có nhóm đối chứng, không có phân phối ngẫu nhiên** → mọi giải thích nhân quả đều không kiểm chứng được.

* r = −0,219 là mối liên hệ **yếu**; R² ≈ 4,8% → mức giảm giá **chỉ giải thích ~5% biến động** lợi nhuận cấp dòng. Không thể dùng mức giảm giá để dự báo lợi nhuận.
* Mức giảm giá **không ngẫu nhiên**: 48,01% dòng không giảm giá, và giảm giá chỉ tập trung ở một số nhóm sản phẩm → so sánh giữa các mức giảm giá **không cân bằng về đặc tính sản phẩm**.
* Các mức 0,32 / 0,45 / 0,60 chỉ có 11–138 dòng → mẫu nhỏ, kết luận cho từng mức riêng lẻ có độ tin cậy thấp. Kết luận đáng tin hơn là **xu hướng ngưỡng ~30%**.
* Đây là phân tích **lịch sử**, không phải cơ sở để khẳng định khả năng dự báo lợi nhuận tương lai.

---

## Bảng tổng hợp con số chính

| Chỉ số | Giá trị |
|---|---|
| Số dòng / số đơn / số khách | 9.993 / 5.009 / 793 |
| Khoảng thời gian | 03/01/2014 – 30/12/2017 (48/48 tháng) |
| Tổng doanh thu / lợi nhuận | 2.296.919,49 / 286.409,08 USD |
| Biên lợi nhuận tổng | 12,47% |
| Dòng lỗ (`Profit` < 0) | 1.870 (18,71%) trên 1.318 đơn |
| `Sales`: TB / trung vị / max | 229,85 / 54,48 / 22.638,48 (skew 12,97) |
| `Profit`: TB / trung vị / min–max | 28,66 / 8,67 / −6.599,98 … 8.399,98 (skew 7,56) |
| `Discount`: TB / trung vị / % = 0 | 0,1562 / 0,20 / 48,01% |
| AOV toàn bộ | 458,56 USD |
| Số biểu đồ trong notebook | 11 |

---

## Bàn giao cho phần hồi quy tuyến tính (Hiếu)

Gợi ý biến, **không** phải kết quả mô hình (Linear Regression nằm ngoài phạm vi phần này):

1. **Biến nên đưa vào mô hình:** `Category`, `Sub-Category`, `Region`, `Segment`, `Ship Mode`, `Discount`, `Quantity`, và biến thời gian tách từ `Order Date` (`Year`, `Month`, `Quarter`).
2. **Không** đưa vào `X`: `Row ID`, `Order ID`, `Customer ID`, `Customer Name` (định danh), `Profit` (tính từ chính `Sales`), `Order Date`/`Ship Date` dạng thô.
3. Cân nhắc `log1p` cho `Sales` do phân phối lệch mạnh (skew 12,97).
4. Giữ các dòng cùng `Order ID` trong cùng một tập khi chia train/test (2.471/5.009 đơn có ≥2 dòng → rò rỉ thông tin nếu chia ngẫu nhiên theo dòng).
5. Nhớ mốc so sánh `DummyRegressor` và báo cáo MAE/RMSE bên cạnh R².
6. Bối cảnh từ EDA để diễn giải: `Discount` không độc lập với `Category` (M5 trong `assumptions_limitations.md`).

---

## Tài liệu liên quan

* [`docs/assumptions_limitations.md`](../docs/assumptions_limitations.md) — giả định G1–G12, giới hạn Order Value OV1–OV7, giới hạn dataset L1–L21
* [`docs/data_dictionary.md`](../docs/data_dictionary.md) — data dictionary + Cleaning Decision Log
* [`docs/privacy_note.md`](../docs/privacy_note.md) — đánh giá rủi ro PII và quyết định ẩn danh
* [`DEVELOPMENT_PLAN.md`](../DEVELOPMENT_PLAN.md) — kế hoạch triển khai và trạng thái từng task
