import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Đường dẫn đến tệp chứng chỉ của tài khoản dịch vụ Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-f55c9-default-rtdb.firebaseio.com/",
})

# Tham chiếu đến đường dẫn 'Students' trong cơ sở dữ liệu
ref = db.reference('Students')
# Lấy thời gian thực và định dạng thành chuỗi theo định dạng 'YYYY-MM-DD HH:MM:SS'
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Dữ liệu sinh viên ban đầu dưới dạng từ điển
data = {
    "1111": {
        "name": "Dienne",
        "major": "Developer",
        "starting_year": 2019,
        "total_attendance": 8,
        "year": 4,
        "last_attendance_time": current_time
    },
    "2222": {
        "name": "ElonMuck",
        "major": "billionaire",
        "starting_year": 2019,
        "total_attendance": 7,
        "year": 4,
        "last_attendance_time": current_time
    },
    "5555": {
        "name": "Ngoc Thu",
        "major": "Developer",
        "total_attendance": 1,
        "starting_year": 2021,
        "year": 3,
        "last_attendance_time": current_time
    },
    "4444": {
        "name": "Thang",
        "major": "Developer",
        "total_attendance": 7,
        "starting_year": 2019,
        "year": 4,
        "last_attendance_time": current_time
    },
}




for key, value in data.items():
    ref.child(key).set(value)