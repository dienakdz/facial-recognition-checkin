import os
import cv2

# Đường dẫn đến thư mục chứa các ảnh
folder_path = 'images'

# Kích thước mà bạn muốn resize ảnh về (216x216)
target_size = (216, 216)

# Duyệt qua tất cả các file trong thư mục
for filename in os.listdir(folder_path):
    # Tạo đường dẫn đầy đủ của file
    file_path = os.path.join(folder_path, filename)

    # Kiểm tra xem file có phải là ảnh không
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Đọc ảnh từ file
        img = cv2.imread(file_path)

        # Resize ảnh về kích thước mong muốn
        img_resized = cv2.resize(img, target_size)

        # Ghi đè lên file cũ hoặc lưu vào file mới (nếu bạn muốn giữ lại file gốc)
        cv2.imwrite(file_path, img_resized)

        # In ra thông báo đã xử lý xong file
        print(f'Resized {filename} to {target_size}')

print("All images have been resized.")
