# 🐘 Elephant Migration Simulation

## 📋 Mô tả dự án

Mô phỏng chân thực về hành trình di cư của đàn voi từ vùng khô cằn sang vùng phì nhiêu, được xây dựng trên nền tảng GAMA. Dự án này tập trung vào **câu chuyện sinh tồn** thay vì yếu tố combat, mang đến trải nghiệm như một bộ phim tài liệu National Geographic.

## 🌍 Môi trường mô phỏng

### **Vùng khô cằn (Western Zone - x: 0-25)**
- 🌵 Thực vật: 5-30% (rất ít cỏ)
- 💧 Nguồn nước: 1% (rất hiếm)
- 🟤 Màu sắc: Nâu khô cằn
- 🦁 Nguy hiểm: Sư tử có thể xuất hiện

### **Vùng sông (River Zone - x: 25-35)**
- 🌊 Đặc điểm: Sông lớn cần vượt qua
- 🐊 Nguy hiểm: Cá sấu (giảm số lượng)
- 🔵 Màu sắc: Xanh nước biển nhạt
- 🌿 Thực vật: 20-40%

### **Vùng phì nhiêu (Eastern Zone - x: 35-60)**
- 🌱 Thực vật: 60-100% (cỏ xanh tươi)
- 💧 Nguồn nước: 8% (nhiều)
- 🟢 Màu sắc: Xanh lá cây tươi
- 🛡️ An toàn: Không có sư tử

## 🐘 Hành vi đàn voi

### **Đặc điểm cá thể**
- **Thủ lĩnh (Leader)**: Màu vàng, kích thước lớn, đưa ra quyết định di cư
- **Voi trưởng thành**: Màu xám, theo đàn
- **Voi con (Baby)**: Màu hồng, kích thước nhỏ, di chuyển chậm hơn

### **Hành vi di cư**
- 🔍 **Đánh giá môi trường**: Thủ lĩnh kiểm tra thực vật và nước trong bán kính 10 ô
- 🚶 **Quyết định di cư**: Khi thực vật < 200, nước < 2, và đói > 40%
- 👥 **Đoàn kết đàn**: Voi lạc đàn sẽ tìm về với thủ lĩnh
- 🛤️ **Dấu vết di chuyển**: Hiển thị đường đi của từng cá thể

### **Sinh lý**
- ⚡ **Năng lượng**: Giảm theo thời gian, tăng khi ăn
- 🍽️ **Đói**: Tăng theo thời gian, giảm khi ăn
- 🎂 **Tuổi tác**: Voi con trưởng thành sau 200 chu kỳ
- 🐣 **Sinh sản**: Tỷ lệ sinh thấp khi năng lượng > 80%

## 🌦️ Chu kỳ mùa

### **Mùa khô**
- 🌵 Vùng khô cằn: Thực vật giảm nhanh (0-3 điểm/chu kỳ)
- 🌿 Vùng phì nhiêu: Thực vật giảm chậm (0-1 điểm/chu kỳ)
- 📉 Áp lực di cư tăng cao

### **Mùa mưa**
- 🌱 Vùng khô cằn: Thực vật tăng chậm (0-2 điểm/chu kỳ)
- 🌳 Vùng phì nhiêu: Thực vật tăng nhanh (0-4 điểm/chu kỳ)
- 📈 Điều kiện sống cải thiện

## 📊 Thống kê theo dõi

### **Thống kê chính**
- 🏆 **Voi đến vùng phì nhiêu**: Số lượng voi đã di cư thành công
- 🚶 **Số lần di cư**: Số lần đàn voi quyết định di cư
- 🤝 **Độ đoàn kết đàn (%)**: Mức độ gắn kết của đàn voi
- 🍃 **Dinh dưỡng trung bình**: Mức năng lượng trung bình của đàn

### **Thống kê phụ**
- 🐣 **Tổng số sinh**: Số voi con được sinh ra
- 💀 **Tổng số chết**: Số voi chết vì đói hoặc hết năng lượng
- 🌍 **Mùa hiện tại**: Mùa khô hoặc mùa mưa
- 🐘 **Voi sống**: Số voi còn sống

## 🎮 Cách sử dụng

### **Yêu cầu hệ thống**
- GAMA Platform phiên bản 1.8 trở lên
- Java 8 hoặc cao hơn

### **Chạy mô phỏng**
1. Mở GAMA Platform
2. Import file `elephant_migration.gaml`
3. Chạy experiment `elephant_migration_experiment`
4. Quan sát và điều chỉnh các tham số

### **Tham số có thể điều chỉnh**
- 🐘 **Số lượng voi**: 5-30 con
- 🦁 **Số lượng sư tử**: 0-5 con
- 🐊 **Số lượng cá sấu**: 0-3 con
- ⏰ **Thời gian mùa**: 50-200 chu kỳ

## 🎯 Mục tiêu học tập

### **Sinh thái học**
- Hiểu về hành vi di cư của động vật
- Tác động của môi trường đến sinh tồn
- Chu kỳ tự nhiên và thích nghi

### **Mô phỏng**
- Áp dụng agent-based modeling
- Thiết kế hành vi phức tạp
- Phân tích dữ liệu từ mô phỏng

### **Lập trình GAMA**
- Cấu trúc species và grid
- Reflexes và actions
- Visualization và monitoring

## 🏆 Kết quả mong đợi

- **Câu chuyện rõ ràng**: Voi phải di cư vì điều kiện khắc nghiệt
- **Hành trình cam go**: Vượt sông, đối mặt nguy hiểm
- **Đích đến hạnh phúc**: Vùng đất hứa với cỏ xanh
- **Bài học sinh thái**: Chu kỳ tự nhiên và sự thích nghi

## 🔧 Phát triển tiếp theo

- [ ] Thêm yếu tố thời tiết (mưa, nắng)
- [ ] Phát triển AI thông minh hơn cho thủ lĩnh
- [ ] Thêm các loài động vật khác
- [ ] Cải thiện graphics và animation
- [ ] Xuất dữ liệu để phân tích thêm

## 📞 Liên hệ

- **Tác giả**: Võ Văn Tài
- **Email**: vovantai2k4@gmail.com
- **Mục đích**: Học tập và nghiên cứu

---

*Elephant Migration Simulation* © 2025 - Phiên bản chân thực cho giáo dục sinh thái