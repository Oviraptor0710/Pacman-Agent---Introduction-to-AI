🎮 Pac-Man AI Agent
Project Intro to AI : Đánh giá và kiểm thử thuật toán cho tác tử Pacman.
Project được phát triển bằng Python và Pygame. Dự án triển khai nhiều thuật toán Search AI khác nhau để điều khiển Pac-Man tự động di chuyển và thu thập thức ăn trong khi tránh ma quái.

📋 Mục lục
Tính năng chính
Thuật toán AI
Cài đặt
Cách sử dụng
Cấu trúc dự án
Tùy chỉnh
🚀 Tính năng chính
Game Pac-Man hoàn chỉnh: Giao diện đồ họa với Pygame
AI Agent thông minh: Pac-Man tự động di chuyển dựa trên thuật toán được chọn
Nhiều thuật toán AI: BFS, Local Search, Minimax
Ghost Move: Ma quái di chuyển bằng thuật toán No moving/ Random/ A*
Nhiều map: 5 map với địa hình khác nhau
Hệ thống điểm số: Theo dõi điểm số trong game
Menu tương tác: Giao diện menu để chọn map và thuật toán cho Pacman và Ghost
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
Lưu ý: Giải thích chi tiết thuật toán có trong Report!

🛠 Cài đặt
Yêu cầu hệ thống
Python 3.7+
Pygame
Cách cài đặt
# Clone repository
git clone https://github.com/NeoCyber05/Pacman_Agent.git
cd Pacman_Agent

# Cài đặt dependencies
pip install pygame

# Chạy game
python Source/main.py
🎯 Cách sử dụng
Khởi chạy game:

python Source/main.py
Chọn map: Sử dụng menu để chọn 1 trong 5 map có sẵn

Chọn thuật toán cho Ghost:

No moving
Random Move
A* Move
Chọn thuật toán cho Pacman:

BFS
Local Search
Minimax
Quan sát AI: Xem Pac-Man tự động di chuyển và thu thập thức ăn

Điều khiển: Game chạy tự động, không cần control từ người dùng
📁 Cấu trúc dự án
Pacman_Agent/
├── Source/                 # Mã nguồn chính
│   ├── main.py            # File chính để chạy game
│   ├── Algorithms/        # Các thuật toán AI
│   │   ├── BFS.py        # Thuật toán BFS
│   │   ├── LocalSearch.py # Thuật toán Local Search
│   │   ├── Minimax.py    # Thuật toán Minimax
│   │   ├── Ghost_Move.py # Thuật toán A* cho ma quái
│   │   └── SearchAgent.py # Agent chính
│   ├── Object/           # Các đối tượng game
│   │   ├── Player.py     # Class Pac-Man và ma quái
│   │   ├── Wall.py       # Class tường
│   │   ├── Food.py       # Class thức ăn
│   │   └── Menu.py       # Class menu
│   ├── Utils/            # Các hàm tiện ích
│   ├── Images/           # Hình ảnh sprites
│   └── Constants/        # Các hằng số
│       └── constants.py  # Cấu hình game
├── Map/                  # Các file map
│   ├── map1.txt         # Map 1
│   ├── map2.txt         # Map 2
│   ├── map3.txt         # Map 3
│   ├── map4.txt         # Map 4
│   └── map5.txt         # Map 5  
└── README.md          

🔧 Tùy chỉnh
Thêm map mới
Tạo file .txt mới trong thư mục Map/
Định dạng theo cấu trúc map hiện tại
Cập nhật menu trong main.py
