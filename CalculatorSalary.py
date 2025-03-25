import pandas as pd
from firebase_admin import credentials, db, initialize_app
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-f55c9-default-rtdb.firebaseio.com/"
})

# Truy xuất dữ liệu từ cơ sở dữ liệu Firebase
def get_attendance_data():
    ref = db.reference('Students')
    data = ref.get()
    return data

# Tính toán lương từ dữ liệu điểm danh
def calculate_salary(attendance_count):
    return attendance_count * 100

# Lấy dữ liệu điểm danh
attendance_data = get_attendance_data()

# Tạo danh sách các hàng để thêm vào DataFrame
rows = []

for student_id, info in attendance_data.items():
    total_attendance = info.get('total_attendance', 0)
    salary = calculate_salary(total_attendance)
    student_name = info.get('name', 'Unknown')  # Lấy tên sinh viên từ dữ liệu Firebase, mặc định là 'Unknown' nếu không có
    rows.append({'Student ID': student_id, 'Student Name': student_name, 'Total Attendance': total_attendance, 'Salary': str(salary) + ' $'})

# Tạo DataFrame từ danh sách các hàng
df = pd.DataFrame(rows)

# Lưu DataFrame vào file Excel
excel_filename = 'salary_report.xlsx'
df.to_excel(excel_filename, index=False)
print(f"Salary report saved to {excel_filename}")

