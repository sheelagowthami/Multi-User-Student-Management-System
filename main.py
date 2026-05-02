import streamlit as st
import os

# -------------------------------
# FILES & FOLDERS
# -------------------------------
USER_FILE = "users.txt"
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# -------------------------------
# USER HELPERS
# -------------------------------
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                username, password = line.strip().split(",")
                users[username] = password
    return users


def save_user(username, password):
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")


def get_user_file(username):
    return os.path.join(DATA_FOLDER, f"{username}_students.txt")


# -------------------------------
# STUDENT FUNCTIONS
# -------------------------------
def add_student(username, name, age, marks):
    if marks >= 90:
        grade = "A+"
    elif marks >= 75:
        grade = "A"
    elif marks >= 60:
        grade = "B"
    elif marks >= 40:
        grade = "C"
    else:
        grade = "Fail"

    file_path = get_user_file(username)

    with open(file_path, "a") as f:
        f.write(f"{name},{age},{marks},{grade}\n")

    return grade


def load_students(username):
    file_path = get_user_file(username)
    students = []

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                name, age, marks, grade = line.strip().split(",")
                students.append([name, age, marks, grade])

    return students


# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None


# -------------------------------
# LOGIN / SIGNUP PAGE
# -------------------------------
def login_page():
    st.title("🔐 Student Management System")

    menu = st.radio("Choose Option", ["Login", "Signup"])

    users = load_users()

    # SIGNUP
    if menu == "Signup":
        st.subheader("Create New Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if username in users:
                st.error("User already exists")
            else:
                save_user(username, password)
                st.success("Account created! Now login.")

    # LOGIN
    else:
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")


# -------------------------------
# DASHBOARD
# -------------------------------
def dashboard():
    st.title(f"🎓 Welcome {st.session_state.user}")

    menu = st.sidebar.selectbox("Menu", ["Add Student", "View Students", "Search Student", "Logout"])

    username = st.session_state.user

    # ADD STUDENT
    if menu == "Add Student":
        st.subheader("➕ Add Student")

        name = st.text_input("Name")
        age = st.number_input("Age", 1, 100)
        marks = st.number_input("Marks", 0, 100)

        if st.button("Add"):
            grade = add_student(username, name, age, marks)
            st.success(f"Student Added! Grade: {grade}")

    # VIEW STUDENTS
    elif menu == "View Students":
        st.subheader("📋 Your Students")

        students = load_students(username)

        if students:
            st.table(students)
        else:
            st.warning("No students found")

    # SEARCH STUDENT
    elif menu == "Search Student":
        st.subheader("🔍 Search Student")

        search = st.text_input("Enter name")

        if st.button("Search"):
            students = load_students(username)
            found = False

            for s in students:
                if s[0].lower() == search.lower():
                    st.success("Student Found!")
                    st.write("Name:", s[0])
                    st.write("Age:", s[1])
                    st.write("Marks:", s[2])
                    st.write("Grade:", s[3])
                    found = True
                    break

            if not found:
                st.error("Not found")

    # LOGOUT
    elif menu == "Logout":
        st.session_state.user = None
        st.rerun()


# -------------------------------
# APP CONTROLLER
# -------------------------------
if st.session_state.user is None:
    login_page()
else:
    dashboard()
