# Ứng dụng Mã hóa/Giải mã DES

Ứng dụng web cho phép mã hóa và giải mã file sử dụng thuật toán DES (Data Encryption Standard).

## Tính năng

- Mã hóa file với khóa DES
- Giải mã file đã được mã hóa
- Giao diện web thân thiện với người dùng
- Hỗ trợ file có kích thước tối đa 16MB

## Yêu cầu hệ thống

- Python 3.x
- Flask
- pycryptodome

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install flask pycryptodome
```

2. Clone repository hoặc tải source code về máy

## Cách sử dụng

1. Chạy ứng dụng:
```bash
python DES.py
```

2. Mở trình duyệt web và truy cập địa chỉ: `http://localhost:5000`

3. Sử dụng giao diện web để:
   - Chọn file cần mã hóa/giải mã
   - Nhập khóa DES (8 ký tự)
   - Nhấn nút tương ứng để thực hiện mã hóa hoặc giải mã

## Lưu ý

- Khóa DES sẽ được tự động điều chỉnh thành 8 bytes:
  - Nếu khóa dài hơn 8 bytes, chỉ 8 bytes đầu tiên sẽ được sử dụng
  - Nếu khóa ngắn hơn 8 bytes, sẽ được bổ sung bằng ký tự '*'
- File sau khi mã hóa sẽ có tiền tố "encrypted_"
- File sau khi giải mã sẽ có tiền tố "decrypted_"

## Cấu trúc project

- `DES.py`: File chính chứa toàn bộ code của ứng dụng

## Bảo mật

- Ứng dụng sử dụng chế độ mã hóa ECB (Electronic Codebook)
- File tạm thời được lưu trong thư mục temp của hệ thống
- Không lưu trữ file đã mã hóa/giải mã trên server

## Xử lý lỗi

Ứng dụng sẽ hiển thị thông báo lỗi trong các trường hợp:
- Không chọn file
- Không nhập khóa
- File quá lớn (>16MB)
- Khóa không đúng khi giải mã
- Lỗi trong quá trình mã hóa/giải mã
