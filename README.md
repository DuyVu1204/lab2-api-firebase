# Lab 2: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## Thông tin sinh viên

- Họ và tên: Nguyễn Duy Vũ
- Môn học: Tư Duy Tính Toán
- Trường: Trường Đại học Khoa học Tự nhiên TP.HCM
- Khoa: Khoa Công nghệ Thông tin


## Mô tả ngắn về hệ thống

Đồ án xây dựng một ứng dụng ghi chú gồm backend FastAPI và frontend Streamlit, tích hợp Firebase để xác thực người dùng và lưu trữ dữ liệu trên Firestore. Người dùng có thể đăng ký, đăng nhập, tạo/sửa/xóa ghi chú và đồng bộ dữ liệu theo tài khoản đăng nhập. Hệ thống cũng hỗ trợ đăng nhập bằng Google và email.

## Các tính năng chính của hệ thống

- Đăng ký tài khoản bằng email/password (gửi email xác thực).
- Đăng nhập bằng email/password (trả về `idToken` và `refreshToken`).
- Đăng nhập bằng Google (OAuth flow + callback, sign in with Firebase).
- Lấy thông tin người dùng hiện tại (`/auth/me`).
- Tạo / Liệt kê / Cập nhật / Xoá ghi chú cho người dùng (endpoints `/notes`).
- Lưu trữ ghi chú trên Firestore theo từng user; ghi chú được sắp xếp theo `timestamp`.
- Backend kiểm tra và xác thực token bằng Firebase Admin SDK.
- Backend kiểm tra và xác thực token bằng Firebase Admin SDK.

## API Endpoints

Danh sách các endpoint chính của backend (base URL: `http://localhost:8000`):

- **GET /**
	- Mô tả: Root, liệt kê các endpoint hiện có.
	- Ví dụ:

```bash
curl http://localhost:8000/
```

- **GET /health**
	- Mô tả: Kiểm tra trạng thái service.
	- Ví dụ:

```bash
curl http://localhost:8000/health
```

- **POST /auth/signup**
	- Mô tả: Đăng ký tài khoản bằng email/password, gửi email xác thực.
	- Body (JSON): `{ "email": "user@gmail.com", "password": "secret" }` (chỉ chấp nhận `@gmail.com`).
	- Ví dụ:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@gmail.com","password":"secret"}' http://localhost:8000/auth/signup
```

- **POST /auth/login**
	- Mô tả: Đăng nhập bằng email/password.
	- Body (JSON): `{ "email": "user@gmail.com", "password": "secret" }`
	- Ví dụ:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@gmail.com","password":"secret"}' http://localhost:8000/auth/login
```

- **POST /auth/google**
	- Mô tả: Xác thực token Google từ frontend (gửi `id_token`) và trả về thông tin người dùng.
	- Body (JSON): `{ "id_token": "<google-id-token>" }`
	- Ví dụ:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id_token":"<google-id-token>"}' http://localhost:8000/auth/google
```

- **GET /auth/google/start** và **GET /auth/google/callback**
	- Mô tả: OAuth redirect flow — truy cập bằng trình duyệt (không dùng curl đơn giản).

- **POST /auth/resend-verification**
	- Mô tả: Tạo link xác thực email và trả về link.
	- Body (JSON): `{ "email": "user@gmail.com" }`
	- Ví dụ:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@gmail.com"}' http://localhost:8000/auth/resend-verification
```

- **GET /auth/me**
	- Mô tả: Lấy thông tin user hiện tại từ token.
	- Headers: `Authorization: Bearer <idToken>`
	- Ví dụ:

```bash
curl -H "Authorization: Bearer <idToken>" http://localhost:8000/auth/me
```

- **GET /notes/**
	- Mô tả: Lấy danh sách ghi chú của user, sắp xếp theo `timestamp`.
	- Headers: `Authorization: Bearer <idToken>`
	- Ví dụ:

```bash
curl -H "Authorization: Bearer <idToken>" http://localhost:8000/notes/
```

- **POST /notes/**
	- Mô tả: Tạo ghi chú mới cho user.
	- Headers: `Authorization: Bearer <idToken>`
	- Body (JSON): `{ "title": "Tiêu đề", "content": "Nội dung" }`
	- Ví dụ:

```bash
curl -X POST -H "Authorization: Bearer <idToken>" -H "Content-Type: application/json" -d '{"title":"Ghi chú 1","content":"Nội dung"}' http://localhost:8000/notes/
```

- **PUT /notes/{note_id}**
	- Mô tả: Cập nhật ghi chú (một hoặc nhiều trường).
	- Headers: `Authorization: Bearer <idToken>`
	- Body (JSON): `{ "title": "..." }` hoặc `{ "content": "..." }`
	- Ví dụ:

```bash
curl -X PUT -H "Authorization: Bearer <idToken>" -H "Content-Type: application/json" -d '{"title":"Tiêu đề mới"}' http://localhost:8000/notes/<note_id>
```

- **DELETE /notes/{note_id}**
	- Mô tả: Xoá ghi chú.
	- Headers: `Authorization: Bearer <idToken>`
	- Ví dụ:

```bash
curl -X DELETE -H "Authorization: Bearer <idToken>" http://localhost:8000/notes/<note_id>
```

Ghi chú: các endpoint yêu cầu xác thực dùng header `Authorization: Bearer <idToken>`; token được cấp khi gọi `/auth/login` hoặc từ Firebase Google sign-in.

## Cấu trúc dự án

Dưới đây là cấu trúc thư mục chính của dự án:

```
Lab2-API-Firebase/
├── README.md
├── requirements.txt
├── .gitignore
├── backend
│   └── app
│       ├── main.py
│       ├── core
│       │   └── firebase_config.py
│       ├── dependencies
│       │   └── auth.py
│       ├── routers
│       │   ├── auth.py
│       │   └── notes.py
│       ├── schemas
│       │   ├── auth.py
│       │   └── note.py
│       └── services
│           └── firestore_service.py
├── frontend
│   ├── api_client.py
│   └── app.py
└── .streamlit
	└── secrets.toml  # file cấu hình nhạy cảm, không commit
```

Mô tả ngắn:
- `backend/app`: mã nguồn FastAPI (API, xác thực, truy xuất Firestore).
- `frontend`: ứng dụng Streamlit (giao diện người dùng).
- `lab2-api-firebase` (nếu xuất hiện): thư mục sao lưu hoặc bản nộp; không bắt buộc để chạy project.

## Cấu hình Firebase - File secrets.toml

Dự án sử dụng file `secrets.toml` để lưu trữ thông tin nhạy cảm. **Bạn phải tạo file này thủ công** để ứng dụng hoạt động.

### Vị trí file
Tạo file tại: `.streamlit/secrets.toml` (trong thư mục gốc của dự án)

### Cấu trúc file
File `secrets.toml` cần chứa 3 phần chính:

#### 1. Firebase Client Config (để Pyrebase xác thực)
```toml
[firebase_client]
apiKey = "YOUR_API_KEY"
authDomain = "YOUR_PROJECT.firebaseapp.com"
projectId = "YOUR_PROJECT_ID"
storageBucket = "YOUR_PROJECT.appspot.com"
messagingSenderId = "YOUR_SENDER_ID"
appId = "1:YOUR_APP_ID:web:YOUR_WEB_ID"
measurementId = "G-YOUR_MEASUREMENT_ID"
databaseURL = "https://YOUR_PROJECT.firebaseio.com"
```

#### 2. Firebase Admin SDK Config (để backend lưu/đọc Firestore)
```toml
[firebase_admin]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = """
-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----
"""
client_email = "firebase-adminsdk-XXXXX@YOUR_PROJECT.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-XXXXX%40YOUR_PROJECT.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

#### 3. Google OAuth Config (để đăng nhập bằng Google)
```toml
[google-login]
google-url = "http://localhost:8000/auth/google/start"
google_client_id = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
google_client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
google_redirect_uri = "http://localhost:8000/auth/google/callback"
firebase_web_api_key = "YOUR_API_KEY"
frontend_url = "http://localhost:8501"
cookie_secure = false
```

### Cách lấy thông tin Firebase

1. Vào [Firebase Console](https://console.firebase.google.com/)
2. Chọn project của bạn
3. **Để lấy Client Config**: Vào **Project Settings** → tab **Your Apps** → chọn web app → copy config
4. **Để lấy Admin SDK Config**: Vào **Project Settings** → tab **Service Accounts** → tạo private key → copy JSON

### Cách lấy thông tin Google OAuth

1. Vào [Google Cloud Console](https://console.cloud.google.com/)
2. Chọn project
3. Vào **APIs & Services** → **Credentials**
4. Chọn OAuth 2.0 Client ID → copy Client ID và Client Secret

### Lưu ý bảo mật
- **Không commit** file `secrets.toml` lên GitHub (thêm vào `.gitignore`)
- Giữ bí mật các khóa và thông tin trong file này
- Mỗi máy/môi trường cần bản copy riêng của `secrets.toml`



## Cài đặt môi trường và thư viện

Khuyến nghị dùng Python `3.11.x` để đồng nhất với môi trường phát triển.

### Vì sao nên dùng môi trường ảo (`venv`)

Môi trường ảo giúp tách riêng thư viện của từng project, tránh xung đột phiên bản giữa các bài khác nhau trên cùng máy. Khi dùng `venv`, bạn có thể:

- Cài đúng dependency cho riêng project này mà không ảnh hưởng Python toàn cục.
- Dễ tái hiện môi trường trên máy khác chỉ với `requirements.txt`.
- Hạn chế lỗi kiểu `Import could not be resolved` do cài package nhầm interpreter.
- Dọn dẹp nhanh: chỉ cần xóa thư mục `.venv` khi muốn tạo lại môi trường sạch.

### Dùng môi trường ảo (`.venv`)

1. Tạo môi trường ảo:

```bash
python -m venv .venv
```

2. Kích hoạt theo hệ điều hành:

| Hệ điều hành | Lệnh |
| --- | --- |
| Windows (PowerShell) | `.\.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.\.venv\Scripts\activate.bat` |
| Linux / macOS | `source .venv/bin/activate` |

*PowerShell: nếu bị chặn script, chạy một lần `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.*

3. Cài dependencies:

```bash
pip install -r requirements.txt
```

4. Thoát venv:

```bash
deactivate
```

## Hướng dẫn chạy chương trình

Chạy backend:

```bash
uvicorn backend.app.main:app --reload
```

Chạy frontend:

```bash
streamlit run frontend/app.py
```

Mở các đường dẫn kiểm tra:

- Local URL: `http://localhost:8501`
- Network URL: sẽ hiển thị trong terminal sau khi chạy `streamlit run frontend/app.py` (địa chỉ mạng thay đổi theo máy)

## Các API Endpoint


## Liên kết video demo

- Xem video: [Google Drive - Demo sản phẩm](https://drive.google.com/file/d/1hsmChZx0BkBiVTRFkVLv8iG3nnph_YzF/view?usp=sharing)
