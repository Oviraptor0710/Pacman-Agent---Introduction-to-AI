🎮 Pac-Man AI Agent
Project Intro to AI : Đánh giá và kiểm thử thuật toán cho tác tử Pacman.
Project được phát triển bằng Python và Pygame. Dự án triển khai nhiều thuật toán Search AI khác nhau để điều khiển Pac-Man tự động di chuyển và thu thập thức ăn trong khi tránh ma quái.

📋 Mục lục
- Tính năng chính
- Thuật toán AI
- Cài đặt
- Cách sử dụng
- Tùy chỉnh

🚀 Tính năng chính
- Game Pac-Man hoàn chỉnh: Giao diện đồ họa với Pygame
- AI Agent thông minh: Pac-Man tự động di chuyển dựa trên thuật toán được chọn
- Nhiều thuật toán AI: BFS, Local Search, Minimax
- Ghost Move: Ma quái di chuyển bằng thuật toán No moving/ Random/ A*
- Nhiều map: 5 map với địa hình khác nhau
- Hệ thống điểm số: Theo dõi điểm số trong game
- Menu tương tác: Giao diện menu để chọn map và thuật toán cho Pacman và Ghost

🧠 Thuật toán AI
1. BFS (Breadth-First Search)
Thuật toán tìm kiếm theo chiều rộng
Tìm đường đi ngắn nhất đến thức ăn gần nhất
2. Local Search
Thuật toán tìm kiếm cục bộ
Tối ưu hóa di chuyển trong vùng lân cận
3. Minimax
Thuật toán game theory
Dự đoán và đối phó với di chuyển của ma quái
4. A* cho Ghost
Ghost sử dụng thuật toán A* để truy đuổi Pac-Man


🛠 Cài đặt
Yêu cầu hệ thống
- Python 3.7+
- Pygame
Cách cài đặt
```bash
# Clone repository
git clone https://github.com/Oviraptor0710/Pacman-Agent---Introduction-to-AI.git

# Cài đặt dependencies
pip install pygame

# Thay đổi working directory sang thư mục con Pacman-Agent---Introduction-to-AI
cd Pacman-Agent---Introduction-to-AI

# Chạy game
python Source/main.py
```

🎯 Cách sử dụng
Khởi chạy game:
```bash
python Source/main.py
```

Chọn map: Sử dụng menu để chọn 1 trong 5 map có sẵn

Chọn thuật toán cho Ghost:
- No moving
- Random Move
- A* Move

Chọn thuật toán cho Pacman:
- BFS
- Local Search
- Minimax
Quan sát AI: Xem Pac-Man tự động di chuyển và thu thập thức ăn
Điều khiển: Game chạy tự động, không cần control từ người dùng


🔧 Tùy chỉnh

Thêm map mới
- Tạo file .txt mới trong thư mục Map/
- Định dạng theo cấu trúc map hiện tại
- Cập nhật menu trong main.py
