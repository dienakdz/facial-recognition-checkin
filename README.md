# Facial Recognition-Based Employee Attendance System

## 📌 Introduction
This project is an employee attendance system that utilizes facial recognition technology, built with Python and OpenCV. The system automatically records employees' check-in and check-out times, improving work time management efficiency.

## 🎥 Demo
Watch the demo video here: (https://www.youtube.com/watch?v=jxUpEntLMqk&t)

## 🚀 Features
- Automatic face detection and recognition.
- Real-time check-in and check-out logging.
- Stores attendance records for future reference.
- Easy-to-use interface for employees and administrators.

## 🛠️ Technologies Used
- **Python**: Main programming language.
- **OpenCV**: Used for image processing and face recognition.
- **NumPy & Pandas**: For data handling and analysis.
- **SQLite/CSV**: To store attendance records.

## 📥 Installation
### Prerequisites
Make sure you have the following installed:
- Python (>=3.7)
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/dienakdz/facial-recognition-checkin.git
   cd facial-recognition-checkin
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python main.py
   ```

## 📚 Usage
1. Register employees' faces in the system.
2. Start the application to detect and recognize faces.
3. The system will automatically log check-in and check-out times.
4. View attendance records in the generated CSV file.

## 🛡 Security Notice
Make sure **serviceAccountKey.json** and other sensitive credentials are not committed to the repository. Use a `.gitignore` file to prevent accidental commits.

## 📄 License
This project is licensed under the MIT License.

---
💡 **Feel free to contribute to the project or report any issues!** 🚀
