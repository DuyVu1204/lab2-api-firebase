# Lab 2: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## Thông tin sinh viên

- Họ và tên: Nguyễn Duy Vũ
- Môn học: Tư Duy Tính Toán
- Trường: Trường Đại học Khoa học Tự nhiên TP.HCM
- Khoa: Khoa Công nghệ Thông tin


## Mô tả ngắn về hệ thống

Đồ án xây dựng một ứng dụng ghi chú gồm backend FastAPI và frontend Streamlit, tích hợp Firebase để xác thực người dùng và lưu trữ dữ liệu trên Firestore. Người dùng có thể đăng ký, đăng nhập, tạo/sửa/xóa ghi chú và đồng bộ dữ liệu theo tài khoản đăng nhập. Hệ thống cũng hỗ trợ đăng nhập bằng Google và chỉ chấp nhận email `@gmail.com` cho luồng email/password.

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

### Cài trực tiếp (không dùng venv)

Trong thư mục gốc của dự án, chạy một trong hai lệnh sau:

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
python -m pip install -r requirements.txt
```

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

File `requirements.txt` hiện gồm các thư viện chính: FastAPI, Uvicorn, Transformers (`<5`), PyTorch, Requests, Pydantic, OmegaConf.

## Hướng dẫn chạy chương trình

Chạy backend:

```bash
uvicorn backend.app.main:app --reload
```

Chạy frontend:

```bash
=
```

Mở các đường dẫn kiểm tra:

- Local URL: `http://localhost:8501`
- Network URL: sẽ hiển thị trong terminal sau khi chạy `streamlit run frontend/app.py` (địa chỉ mạng thay đổi theo máy)


## Liên kết video demo

- Xem video: [Google Drive - Demo sản phẩm](https://drive.google.com/file/d/1hsmChZx0BkBiVTRFkVLv8iG3nnph_YzF/view?usp=sharing)
- Ghi chú: Vui lòng bật quyền `Anyone with the link` để giảng viên có thể xem trực tiếp.

