import pyodbc
from typing import Optional

# --- THÔNG TIN KẾT NỐI SQL SERVER ---
SERVER_NAME = r'LAPTOP-4N8UEI6E\SQLEXPRESS'
DATABASE_NAME = 'QL_KyTucXa'
ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}'

CONNECTION_STRING = (
    f'DRIVER={ODBC_DRIVER};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    'Trusted_Connection=yes;'
)

def connect_db() -> Optional[pyodbc.Connection]:
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as ex:
        print(f"❌ LỖI KẾT NỐI SQL SERVER: {ex}")
        return None

def check_credentials_in_sqlserver(username: str, password: str) -> Optional[str]:
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = "SELECT ChucVu FROM TaiKhoan WHERE TenDangNhap=? AND MatKhau=?"
        cursor.execute(sql, (username, password))

        result = cursor.fetchone()
        if result:
            return result[0].strip()
        return None

    except pyodbc.Error as ex:
        print(f"❌ LỖI TRUY VẤN SQL SERVER: {ex}")
        return None

    finally:
        conn.close()

# TEST
if __name__ == "__main__":
    print(check_credentials_in_sqlserver("QL001", "001"))
