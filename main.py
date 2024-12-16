import tkinter as tk
from tkinter import messagebox # Untuk menampilkan messagebox
from PIL import Image, ImageTk # Untuk menampilkan gambar
import random # Untuk mengacak treat
from data_quiz import colors, users, questions, treats # Mengambil data dari tiap variabel (dalam dictionary dan list)

# Fungsi untuk registrasi dengan error handling
def register():
        # minta input pengguna
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password: # ketika un dan pw kosong
            messagebox.showerror("Error", "Username atau password tidak boleh kosong") # terlihat di gui
            raise ValueError("Username atau password kosong") # hanya akan terlihat di terminal

        if username in users: # jika username sudah ada dalam list users
            messagebox.showerror("Error", "Username sudah terdaftar") # terlihat di gui
            raise ValueError("Username sudah terdaftar") # terlihat di terminal
        
        else: # jika username belum ada
            users[username] = password
            messagebox.showinfo("Success", "Registrasi sukses")

# Fungsi untuk login dengan error handling
def login():
        username = username_entry.get()
        password = password_entry.get()

        if username not in users:
            messagebox.showerror("Error", "Akun anda belum terdaftar") # terlihat di gui
            raise ValueError("Akun belum dibuat")

        if users.get(username) == password:
            messagebox.showinfo("Welcome", "Login berhasil")
            main_menu() # masuk ke main menu
        else:
            messagebox.showerror("Error", "Username atau password salah")

# Fungsi untuk membersihkan current window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Fungsi untuk menampilkan menu
def main_menu():
    clear_window() # Membersihkan jendela saat ini

    # Label main menu
    tk.Label(root, text="Main Menu", font=("Arial", 24), bg=colors["cream"]).pack(pady=20)

    # Tombol buat main
    tk.Button(
        root, text="Play Game", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"],
        command=start_game # Memanggil fungsi untuk masuk ke game
    ).pack(pady=10)

    # Tombol untuk nambahin pertanyaan
    tk.Button(
        root, text="Add Questions", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"],
        command=add_question # Panggil fungsi untuk menambahkan pertanyaan
    ).pack(pady=10)

# Fungsi untuk menambahkan pertanyaan
def add_question():
    clear_window()

    def save_question(): # Fungsi untuk menyimpan pertanyaan
            question_text = question_entry.get() # Minta input pertanyaan
            answer = answer_var.get() # Ini boolean, true atau false
            if question_text:
                questions.append({"question": question_text, "answer": answer})
                messagebox.showinfo("Success", "Pertanyaan berhasil ditambahkan!")
                main_menu()
            else:
                messagebox.showerror("Error", "Pertanyaan masih kosong!")

    # Label untuk menambahkan pertanyaan
    tk.Label(root, text="Add a Question", font=("Arial", 24), bg=colors["cream"]).pack(pady=20)

    # Kotak inputan
    question_entry = tk.Entry(root, font=("Arial", 16))
    question_entry.pack(pady=10)

    # Boolean jawaban
    answer_var = tk.BooleanVar() 
    tk.Radiobutton(root, text="True", variable=answer_var, value=True).pack()
    tk.Radiobutton(root, text="False", variable=answer_var, value=False).pack()

    # Tombol submit
    tk.Button(
        root, text="Save", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"],
        command=save_question
    ).pack(pady=10)

# Fungsi untuk masuk ke game
def start_game():
    clear_window() # Membersihkan jendela
    play_quiz() # Memanggil fungsi play_quiz

# Fungsi untuk bermain game
def play_quiz():
    current_question_index = 0 # Inisiasi indeks pertanyaan dari dict. quesions
    score = 0 # Inisiasi nilai

    # Fungsi untuk move ke soal berikutnya
    def next_question():
        nonlocal current_question_index, score

        # Jika semua soal sudah selesai
        if current_question_index >= len(questions):
            show_result(score)
            return

        # Ambil soal sekarang
        question_label.config(
            text=f"Apakah kata berikut baku?\n\n{questions[current_question_index]['question']}"
        )
        question = questions[current_question_index]

        # Reset feedback
        feedback_label.config(text="")

        # Fungsi untuk mengecek jawaban
        def check_answer(user_answer):
            nonlocal current_question_index, score

            if user_answer == question["answer"]:
                feedback_label.config(text="Benar!", font=("Arial", 12, "bold"), fg="green")
                score += 1
            else:
                feedback_label.config(text="Salah!", font=("Arial", 12, "bold"), fg="red")

            # Update skor
            score_label.config(text=f"Score: {score}/{len(questions)}")

            # Lanjutkan ke soal berikutnya
            current_question_index += 1
            root.after(1000, next_question)

        # Tetapkan fungsi untuk jawaban
        true_button.config(command=lambda: check_answer(True))
        false_button.config(command=lambda: check_answer(False))


    # Label untuk menampilkan pertanyaan
    question_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg=colors["cream"])
    question_label.pack(pady=20)

    # Label untuk skor
    score_label = tk.Label(root, text=f"Score: {score}/{len(questions)}", font=("Arial", 14), bg=colors["cream"])
    score_label.pack(pady=5)

    # Label untuk feedback nilai
    feedback_label = tk.Label(root, text="", font=("Arial", 12), bg=colors["cream"])
    feedback_label.pack(pady=10)

    # Tombol pilihan
    true_button = tk.Button(root, text="True", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"])
    false_button = tk.Button(root, text="False", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"])
    true_button.pack(pady=5)
    false_button.pack(pady=5)

    # Mulai soal pertama
    next_question()

# Fungsi untuk menampilkan score di ahkir
def show_result(final_score):
    clear_window()

    # Jika nilai akhir > 50%
    if final_score > len(questions) // 2: 
        result_text = "Selamat! Kamu menjawab lebih dari 50% benar!"
    else: # Jika nilai akhir < 50%
        result_text = "Masih banyak salah, ini treat kamu!"
            
    # Label untuk score akhir
    tk.Label(
        root, text=f"Your score: {final_score}/{len(questions)}", font=("Arial", 24), bg=colors["cream"]
    ).pack(pady=20)

    # Label untuk hasil
    tk.Label(
            root, text=result_text, font=("Arial", 16), fg=colors["dark_purple"], bg=colors["cream"]
        ).pack(pady=10)
    
    if result_text == "Masih banyak salah, ini treat kamu!":
    # Label untuk treat
        tk.Label(
            root, text=random.choice(treats), font=("Arial", 18, "bold"), fg=colors["dark_purple"], bg=colors["cream"]
        ).pack(pady=10)

    # Tombol kembali ke menu utama
    tk.Button(
        root, text="Back to Menu", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"],
        command=main_menu
    ).pack(pady=20)

# Interface utama
# Root, sambungin semuanya ke root
root = tk.Tk()
root.geometry("800x600")
root.configure(bg=colors["cream"])

# Pengaturan untuk gambar
original_image = Image.open("C:/Users/User/OneDrive/Desktop/True or Treat/Logo1.png")
resized_image = original_image.resize((200, 200))
image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(root, image=image, bg=colors["cream"])
image_label.pack(pady=10)

# Subtitle dibawah gambar
tk.Label(root, text="Get all your answers true, or today will be your treat!", font=("Arial", 12, "italic"), fg=colors["dark_purple"], bg=colors["cream"]).pack(pady=5)

# Label & kotak username
tk.Label(root, text="Username:", font=("Arial", 16), bg=colors["cream"]).pack()
username_entry = tk.Entry(root, font=("Arial", 16))
username_entry.pack(pady=5)

# Label & kotak password
tk.Label(root, text="Password:", font=("Arial", 16), bg=colors["cream"]).pack()
password_entry = tk.Entry(root, font=("Arial", 16), show="*")
password_entry.pack(pady=5)

# Tombol register
tk.Button(
    root, text="Register", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"], command=register # Panggil fungsi register
).pack(pady=10)

# Tombol login
tk.Button(
    root, text="Login", font=("Arial", 16), bg=colors["dark_purple"], fg=colors["white"], command=login # Panggil fungsi login
).pack(pady=10)

root.mainloop() # Jalanin aplikasi
