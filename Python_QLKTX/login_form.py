# login_form.py
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

# --- Import font từ file app_styles ---
try:
    from app_styles import FONT_TITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON, FONT_CHECKBOX
except ImportError:
    messagebox.showerror("Lỗi Khởi tạo Style", "Không tìm thấy file app_styles.py.")
    exit()

# --- Import các thành phần khác ---
try:
    from db_connector import check_credentials_in_sqlserver
    from student_dashboard import StudentForm
    from admin_dashboard import AdminDashboard
except ImportError as e:
    messagebox.showerror(
        "Lỗi Khởi tạo Module",
        f"Không tìm thấy một file .py cần thiết.\n\nChi tiết lỗi: {e}\n\nVui lòng đảm bảo các file đều nằm chung một thư mục."
    )
    exit()


# ------------------ HÀM TẠO NÚT BO GÓC ------------------
def create_rounded_button(parent, text, command=None, radius=20,
                          bg_color="#8A2BE2", fg_color="white",
                          font=None, width=180, height=45):

    canvas = tk.Canvas(parent, width=width, height=height,
                       bg=parent["bg"], highlightthickness=0)

    r = radius
    # 4 góc bo tròn
    canvas.create_arc((2, 2, 2 + r*2, 2 + r*2), start=90, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width - r*2 - 2, 2, width - 2, 2 + r*2), start=0, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((2, height - r*2 - 2, 2 + r*2, height - 2), start=180, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width - r*2 - 2, height - r*2 - 2, width - 2, height - 2), start=270, extent=90, fill=bg_color, outline=bg_color)

    # Thân nút
    canvas.create_rectangle(2 + r, 2, width - r - 2, height - 2, fill=bg_color, outline=bg_color)
    canvas.create_rectangle(2, 2 + r, width - 2, height - r - 2, fill=bg_color, outline=bg_color)

    # Text
    canvas.create_text(width / 2, height / 2, text=text, fill=fg_color, font=font)

    # Sự kiện click
    canvas.bind("<Button-1>", lambda e: command() if command else None)

    return canvas


# ------------------ CLASS LOGIN FORM ------------------
class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập - Hệ thống kí túc xá")

        # 📌 Căn giữa màn hình
        self.center_window(480, 350)

        # --- ĐỔI MÀU NỀN ---
        self.root.configure(bg="#7EC8E3")

        # --- Frame chính ---
        main_frame = tk.Frame(root, pady=20, padx=20, bg="#7EC8E3")
        main_frame.pack(expand=True, fill="both")

        # Tiêu đề đỏ
        tk.Label(
            main_frame,
            text="ĐĂNG NHẬP HỆ THỐNG",
            font=FONT_TITLE,
            fg="red",
            bg="#7EC8E3"
        ).pack(pady=(0, 25))

        # --- Frame form ---
        form_frame = tk.Frame(main_frame, bg="#7EC8E3")
        form_frame.pack(padx=10, fill="x", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Username
        tk.Label(form_frame, text="Tên đăng nhập:", font=FONT_LABEL,
                 bg="#7EC8E3").grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.username_entry = tk.Entry(form_frame, font=FONT_ENTRY, width=30,
                                       relief="solid", bd=1)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Password
        tk.Label(form_frame, text="Mật khẩu:", font=FONT_LABEL,
                 bg="#7EC8E3").grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.password_entry = tk.Entry(form_frame, font=FONT_ENTRY, show="*",
                                       width=30, relief="solid", bd=1)
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Nhấn Enter để đăng nhập
        self.username_entry.bind("<Return>", self.validate_login_event)
        self.password_entry.bind("<Return>", self.validate_login_event)

        # Checkbox show password
        self.show_pass_var = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(form_frame, text="Hiện Mật khẩu",
                                         font=FONT_CHECKBOX,
                                         variable=self.show_pass_var,
                                         command=self.toggle_password,
                                         bg="#7EC8E3", activebackground="#7EC8E3")
        show_pass_check.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 10))

        # --- NÚT ĐĂNG NHẬP BO GÓC ---
        rounded_btn = create_rounded_button(
            parent=main_frame,
            text="Đăng nhập",
            command=self.validate_login,
            radius=18,
            bg_color="#8A2BE2",
            fg_color="white",
            font=FONT_BUTTON,
            width=200,
            height=48
        )
        rounded_btn.pack(pady=20)

        # Focus mặc định
        self.username_entry.focus_set()

    # ====== HÀM CĂN GIỮA MÀN HÌNH ======
    def center_window(self, width=480, height=350):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_pass_var.get() else "*")

    def clear_credentials(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.show_pass_var.set(False)
        self.toggle_password()
        self.username_entry.focus_set()

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        user_role = check_credentials_in_sqlserver(username, password)

        if user_role == "ERROR_DB_CONNECTION":
            messagebox.showerror("Lỗi Kết nối CSDL", "Không thể kết nối đến SQL Server...")
            self.password_entry.delete(0, tk.END)
            return

        if user_role:
            self.root.withdraw()
            if user_role == 'Sinh viên':
                StudentForm(self.root, username, self)
            elif user_role == 'Quản lý':
                AdminDashboard(self.root, username, self)
            else:
                messagebox.showerror("Lỗi Vai trò", f"Vai trò '{user_role}' không được hỗ trợ.")
                self.root.destroy()
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng.")
            self.password_entry.delete(0, tk.END)

    def validate_login_event(self, event):
        self.validate_login()


# ------------------ RUN ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()
