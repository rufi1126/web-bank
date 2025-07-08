import sqlite3

# Koneksi ke database
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance INTEGER DEFAULT 0
    )
''')
conn.commit()

def register():
    username = input("Masukkan username baru: ")
    password = input("Masukkan password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registrasi berhasil!")
    except sqlite3.IntegrityError:
        print("Username sudah digunakan!")

def login():
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Selamat datang, {username}!")
        menu_user(user[0], username)
    else:
        print("Login gagal.")

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()[0]

def menu_user(user_id, username):
    while True:
        print("\n[1] Cek Saldo\n[2] Setor Uang\n[3] Tarik Uang\n[4] Transfer\n[5] Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            saldo = get_balance(user_id)
            print(f"Saldo Anda: Rp{saldo}")

        elif pilihan == '2':
            jumlah = int(input("Jumlah setor: "))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (jumlah, user_id))
            conn.commit()
            print("Setor berhasil.")

        elif pilihan == '3':
            jumlah = int(input("Jumlah tarik: "))
            saldo = get_balance(user_id)
            if jumlah <= saldo:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (jumlah, user_id))
                conn.commit()
                print("Tarik berhasil.")
            else:
                print("Saldo tidak cukup.")

        elif pilihan == '4':
            tujuan = input("Username tujuan: ")
            jumlah = int(input("Jumlah transfer: "))
            cursor.execute("SELECT id FROM users WHERE username = ?", (tujuan,))
            penerima = cursor.fetchone()

            if penerima:
                saldo = get_balance(user_id)
                if jumlah <= saldo:
                    cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (jumlah, user_id))
                    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (jumlah, penerima[0]))
                    conn.commit()
                    print("Transfer berhasil.")
                else:
                    print("Saldo tidak cukup.")
            else:
                print("Username tujuan tidak ditemukan.")

        elif pilihan == '5':
            print("Logout berhasil.\n")
            break
        else:
            print("Pilihan tidak valid.")

def main():
    while True:
        print("\n=== MINI BANK TAZKIA ===")
        print("[1] Register\n[2] Login\n[3] Keluar")
        pilih = input("Pilih menu: ")

        if pilih == '1':
            register()
        elif pilih == '2':
            login()
        elif pilih == '3':
            print("Terima kasih telah menggunakan Mini Bank Tazkia.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()