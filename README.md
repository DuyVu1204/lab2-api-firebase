# Lab 1: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## Thông tin sinh viên

- Họ và tên: Nguyễn Duy Vũ
- Môn học: Tư Duy Tính Toán
- Trường: Trường Đại học Khoa học Tự nhiên TP.HCM
- Khoa: Khoa Công nghệ Thông tin

## Tên mô hình và liên kết Hugging Face


## Mô tả ngắn về hệ thống

Đồ án xây dựng một REST API để tóm tắt văn bản tiếng Anh. Server dùng FastAPI, còn phần suy luận dùng mô hình `facebook/bart-large-cnn` từ Hugging Face. Khi nhận text đầu vào, hệ thống sẽ tokenize, sinh câu tóm tắt và trả về JSON gồm `summary` và `model`.

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
streamlit run frontend/app.py
```

Mở các đường dẫn kiểm tra:

- Local URL: `http://localhost:8501`
- Network URL: `http://192.168.1.12:8501`


## Liên kết video demo

- Xem video: [Google Drive - Demo sản phẩm](https://drive.google.com/file/d/1KZavJ_0sfSAw3SeonUAnoASgT9hHWxXh/view?usp=sharing)
- Ghi chú: Vui lòng bật quyền `Anyone with the link` để giảng viên có thể xem trực tiếp.