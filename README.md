
# HR Attrition Analyzer & Elephant Migration Simulation

![HR Attrition Analyzer](https://img.shields.io/badge/Status-Active-green)
![Elephant Migration](https://img.shields.io/badge/GAMA-Simulation-blue)

## 1. Giới thiệu dự án

Repository này chứa hai dự án chính:

### 🏢 **HR Attrition Analyzer**
**HR Attrition Analyzer** là một ứng dụng phân tích dữ liệu và dự đoán nghỉ việc nhân viên, giúp phòng nhân sự hiểu rõ các yếu tố ảnh hưởng đến nghỉ việc, đồng thời đưa ra cảnh báo sớm và đề xuất chiến lược giữ chân nhân viên.

Ứng dụng được xây dựng trên nền tảng Python, sử dụng thư viện **Streamlit** để tạo giao diện web tương tác, và áp dụng thuật toán **Random Forest Classifier** để dự đoán khả năng nghỉ việc của nhân viên dựa trên dữ liệu thực tế.

### 🐘 **Elephant Migration Simulation**
**Elephant Migration Simulation** là một mô phỏng chân thực về hành trình di cư của đàn voi từ vùng khô cằn sang vùng phì nhiêu, được xây dựng trên nền tảng GAMA. Dự án này tập trung vào câu chuyện sinh tồn thay vì yếu tố combat, mang đến trải nghiệm như một bộ phim tài liệu National Geographic.

**Đặc điểm nổi bật của mô phỏng:**
- 🌍 Môi trường ba vùng: Khô cằn (Tây) → Sông (Giữa) → Phì nhiêu (Đông)
- 🐘 Hành vi đàn voi thực tế với thủ lĩnh, voi trưởng thành, và voi con
- 🌦️ Chu kỳ mùa ảnh hưởng đến thực vật và quyết định di cư
- 📊 Thống kê tập trung vào hành trình thay vì combat
- 🎨 Hiệu ứng thị giác với gradient màu sắc và kích thước thay đổi theo sức khỏe

---

## 2. Mục tiêu dự án

### 🏢 HR Attrition Analyzer
- Phân tích các yếu tố liên quan đến nghỉ việc nhân viên trong tổ chức.
- Xây dựng mô hình học máy dự đoán xác suất nghỉ việc cho từng nhân viên.
- Phát triển giao diện trực quan, thân thiện để bộ phận nhân sự dễ dàng tương tác và theo dõi.
- Cung cấp các gợi ý và chiến lược nhằm giảm tỷ lệ nghỉ việc và giữ chân nhân viên.

### 🐘 Elephant Migration Simulation
- Mô phỏng chân thực hành vi di cư của đàn voi dựa trên điều kiện môi trường.
- Nghiên cứu tác động của chu kỳ mùa đến quyết định di cư.
- Phát triển mô hình agent-based modeling phức tạp với GAMA.
- Tạo công cụ giáo dục về sinh thái học và hành vi động vật.
- Cung cấp trải nghiệm trực quan về câu chuyện sinh tồn trong tự nhiên.

---

## 3. Dữ liệu sử dụng

- Bộ dữ liệu nhân viên được làm sạch, chứa các thuộc tính như:
  - Thông tin cá nhân: Tuổi, giới tính, tình trạng hôn nhân, ngành học,...
  - Thông tin công việc: Phòng ban, chức vụ, cấp bậc, thu nhập, làm thêm giờ,...
  - Các chỉ số liên quan khác: Số năm làm việc, số công ty từng làm, mức độ hài lòng,...

- Dữ liệu gốc lấy từ nguồn công khai trên Kaggle (có thể thay đổi tùy dataset thực tế bạn chọn).

---

## 4. Hướng dẫn cài đặt và chạy dự án

### 4.1 Yêu cầu hệ thống

- Python 3.8 trở lên
- Pip (trình quản lý gói Python)
- Môi trường ảo (virtualenv) khuyến khích sử dụng

### 4.2 Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
````

Nội dung `requirements.txt` có thể gồm:

```
streamlit
pandas
numpy
scikit-learn
joblib
matplotlib
seaborn
```

### 4.3 Cấu trúc thư mục dự án

```
HR_Attrition_Analyzer/
│
├── data/
│   └── employee_cleaned.csv           # File dữ liệu đã làm sạch
│
├── models/
│   └── rf_model.pkl                   # File mô hình Random Forest đã train
│
├── app/
│   └── app_streamlit.py               # File chạy ứng dụng Streamlit
│
├── utils/
│   └── preprocessing.py               # (Nếu có) các hàm tiền xử lý dữ liệu
│
├── requirements.txt                   # File liệt kê thư viện cần thiết
├── README.md                         # File hướng dẫn (này)
└── LICENSE                           # Giấy phép (nếu có)
```

### 4.4 Chạy ứng dụng

#### HR Attrition Analyzer
Ở thư mục `app/` hoặc thư mục gốc, chạy lệnh sau:

```bash
streamlit run app_streamlit.py
```

Sau đó mở trình duyệt web tại địa chỉ được hiển thị (thường là `http://localhost:8501`).

#### Elephant Migration Simulation
1. Cài đặt GAMA Platform (phiên bản 1.8 trở lên)
2. Mở GAMA và import các file `.gaml`:
   - `elephant_migration.gaml` - Mô phỏng chính
   - `elephant_migration_experiments.gaml` - Các thí nghiệm khác nhau
   - `elephant_migration_test.gaml` - Kiểm tra và xác thực
3. Chạy experiment mong muốn
4. Xem chi tiết tại `ELEPHANT_MIGRATION_README.md`

---

## 5. Các bước triển khai dự án

### Bước 1: Thu thập và làm sạch dữ liệu

* Lấy dataset nhân viên, kiểm tra các giá trị thiếu, sai định dạng.
* Xử lý biến định tính (label encoding) và biến số.
* Loại bỏ dữ liệu không cần thiết hoặc nhiễu.

### Bước 2: Phân tích dữ liệu thăm dò (EDA)

* Thống kê mô tả các biến.
* Tạo biểu đồ phân phối, tỷ lệ nghỉ việc theo phòng ban, theo giới tính,...
* Xác định các yếu tố có ảnh hưởng rõ ràng đến việc nghỉ việc.

### Bước 3: Xây dựng mô hình học máy

* Chia dữ liệu thành tập huấn luyện và kiểm tra.
* Sử dụng thuật toán Random Forest Classifier.
* Huấn luyện mô hình và đánh giá hiệu quả bằng các chỉ số accuracy, precision, recall, f1-score.
* Lưu mô hình đã train để sử dụng trong ứng dụng.

### Bước 4: Phát triển ứng dụng Streamlit

* Tạo giao diện nhập dữ liệu nhân viên.
* Hiển thị các biểu đồ phân tích tổng quan.
* Hiển thị kết quả dự đoán nghỉ việc.
* Cung cấp gợi ý và cảnh báo tương tác cho người dùng.

---

## 6. Phân tích kết quả

* Mô hình dự đoán có độ chính xác cao (\~90% tùy dữ liệu).
* Các yếu tố chính ảnh hưởng nghỉ việc gồm: Làm thêm giờ, thu nhập, cấp bậc, khoảng cách nhà đến công ty,...
* Dashboard trực quan giúp dễ dàng theo dõi xu hướng và phân tích sâu.
* Gợi ý giữ chân nhân viên dựa trên kết quả phân tích cụ thể.

---

## 7. Mở rộng và cải tiến

* Thêm mô hình học sâu (deep learning) hoặc các thuật toán khác để cải thiện dự đoán.
* Kết nối dữ liệu thời gian thực để cập nhật liên tục.
* Bổ sung module phân tích tâm lý, khảo sát nhân viên.
* Xây dựng hệ thống cảnh báo tự động gửi email hoặc thông báo qua Slack.

---

## 8. Liên hệ và đóng góp

* Nếu bạn muốn đóng góp, vui lòng fork repo và gửi pull request.
* Mọi thắc mắc hoặc báo lỗi xin vui lòng tạo issue trên GitHub.

---

## 9. Tài liệu tham khảo

* [Kaggle HR Analytics Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
* [Streamlit documentation](https://docs.streamlit.io/)
* [Scikit-learn documentation](https://scikit-learn.org/stable/)

---

## 📫 10. Liên hệ & Giấy phép

* **Tác giả:** Võ Văn Tài
* **Email liên hệ:** [vovantai2k4@gmail.com](mailto:vovantai2k4@gmail.com)
* **Bản quyền:** Dự án thuộc quyền sở hữu cá nhân của tác giả.
  Được phép sử dụng cho mục đích học tập và phi thương mại. Vui lòng ghi rõ nguồn nếu sử dụng lại nội dung/code.

---

*HR Attrition Analyzer* © 2025 by Võ Văn Tài

```


