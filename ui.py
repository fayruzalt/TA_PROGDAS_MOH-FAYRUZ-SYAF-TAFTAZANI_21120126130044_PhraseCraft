import customtkinter as ctk
from tkinter import messagebox
from logic import PhraseCraftManager


class PhraseCraftGUI(ctk.CTk):
    """Jendela utama aplikasi PhraseCraft berbasis CustomTkinter."""

    def __init__(self, manager: PhraseCraftManager):
        super().__init__()
        self.manager = manager
        self.session = None
        self.selected_words = []

        # Pengaturan tema dan jendela
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("PhraseCraft - Sentence Builder")
        self.geometry("820x560")
        self.minsize(720, 500)
        self.configure(fg_color="#F0F7FF")

        # Container utama
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=24, pady=20)

        self.show_start_screen()

    def clear_container(self):
        """Membersihkan semua widget di main_container sebelum ganti tampilan."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        """Menampilkan halaman awal: pilih level, mode, atau tambah materi."""
        self.clear_container()
        self.selected_words = []

        # Kartu header
        header_card = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#BAE6FD",
        )
        header_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            header_card,
            text="PhraseCraft",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#0369A1",
        ).pack(pady=(18, 4))

        ctk.CTkLabel(
            header_card,
            text="Susun kalimat bahasa Inggris dengan cara seru & interaktif!",
            font=ctk.CTkFont(size=14),
            text_color="#475569",
        ).pack(pady=(0, 18))

        # Kartu pengaturan main
        setup_card = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#E2E8F0",
        )
        setup_card.pack(fill="both", expand=True, pady=(0, 16))

        ctk.CTkLabel(
            setup_card,
            text="Pilih Level / Topik",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#1E293B",
        ).pack(pady=(22, 6))

        level_names = list(self.manager.levels.keys())
        self.level_var = ctk.StringVar(value=level_names[0] if level_names else "")
        self.level_menu = ctk.CTkOptionMenu(
            setup_card,
            values=level_names,
            variable=self.level_var,
            width=320,
            height=38,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color="#0284C7",
            button_color="#0369A1",
            button_hover_color="#075985",
        )
        self.level_menu.pack(pady=(0, 18))

        ctk.CTkLabel(
            setup_card,
            text="Pilih Mode Permainan",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#1E293B",
        ).pack(pady=(4, 6))

        self.mode_var = ctk.StringVar(value="Normal")
        mode_segment = ctk.CTkSegmentedButton(
            setup_card,
            values=["Normal", "Survival"],
            variable=self.mode_var,
            width=260,
            height=38,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            selected_color="#16A34A",
            selected_hover_color="#15803D",
        )
        mode_segment.pack(pady=(0, 24))

        # Tombol aksi
        btn_row = ctk.CTkFrame(setup_card, fg_color="transparent")
        btn_row.pack(pady=(8, 20))

        ctk.CTkButton(
            btn_row,
            text="Mulai Main",
            width=180,
            height=46,
            corner_radius=14,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=self.start_game,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_row,
            text="+ Tambah Soal / Level",
            width=200,
            height=46,
            corner_radius=14,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#F59E0B",
            hover_color="#D97706",
            text_color="#FFFFFF",
            command=self.open_add_question_modal,
        ).pack(side="left", padx=10)

    def start_game(self):
        """Memulai sesi permainan sesuai level dan mode yang dipilih."""
        selected_level = self.level_var.get()
        selected_mode = self.mode_var.get()

        self.session = self.manager.create_session(selected_mode)
        if not self.session.start_level(selected_level):
            messagebox.showwarning("Peringatan", "Level tidak tersedia.")
            return

        self.show_game_screen()

    def show_game_screen(self):
        """Menampilkan layar permainan aktif."""
        self.clear_container()
        self.selected_words = []

        if self.session.is_game_over():
            self.show_result_screen()
            return

        question = self.session.get_current_question()

        # Bar informasi atas
        top_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 12))

        ctk.CTkButton(
            top_bar,
            text="← Menu Awal",
            width=110,
            height=34,
            corner_radius=10,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.show_start_screen,
        ).pack(side="left")

        info_text = f"Mode: {self.session.mode}  |  Skor: {self.session.score}"
        if self.session.mode == "Survival":
            info_text += f"  |  Nyawa: {self.session.lives}"

        ctk.CTkLabel(
            top_bar,
            text=info_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#0F172A",
        ).pack(side="right")

        # Kartu soal
        question_card = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=2,
            border_color="#BAE6FD",
        )
        question_card.pack(fill="x", pady=(0, 14))

        progress_text = (
            f"{self.session.current_level} — Soal "
            f"{self.session.current_index + 1}/{len(self.session.questions)}"
        )
        ctk.CTkLabel(
            question_card,
            text=progress_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#0284C7",
        ).pack(pady=(14, 4))

        ctk.CTkLabel(
            question_card,
            text=question["clue"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1E293B",
        ).pack(pady=(0, 16))

        # Area susunan jawaban siswa
        answer_card = ctk.CTkFrame(
            self.main_container,
            fg_color="#EFF6FF",
            corner_radius=16,
            border_width=2,
            border_color="#93C5FD",
            height=90,
        )
        answer_card.pack(fill="x", pady=(0, 14))
        answer_card.pack_propagate(False)

        self.answer_label = ctk.CTkLabel(
            answer_card,
            text="Klik kata-kata di bawah untuk menyusun kalimat...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1D4ED8",
        )
        self.answer_label.pack(expand=True)

        # Area pilihan potongan kata
        words_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        words_frame.pack(fill="x", pady=(4, 16))

        shuffled_words = self.session.get_shuffled_words()
        for word in shuffled_words:
            btn = ctk.CTkButton(
                words_frame,
                text=word,
                height=42,
                corner_radius=12,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#38BDF8",
                hover_color="#0284C7",
                text_color="#0F172A",
            )
            btn.configure(command=lambda w=word, b=btn: self.pick_word(w, b))
            btn.pack(side="left", padx=6, pady=6)

        # Bar tombol kontrol jawaban
        action_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_bar.pack(fill="x", pady=(6, 0))

        ctk.CTkButton(
            action_bar,
            text="Reset Susunan",
            width=140,
            height=42,
            corner_radius=12,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#1E293B",
            command=self.show_game_screen,
        ).pack(side="left")

        ctk.CTkButton(
            action_bar,
            text="Periksa Jawaban",
            width=170,
            height=42,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=self.submit_answer,
        ).pack(side="right")

    def pick_word(self, word: str, button: ctk.CTkButton):
        """Menambahkan kata ke susunan jawaban dan menonaktifkan tombol asalnya."""
        self.selected_words.append(word)
        button.configure(state="disabled", fg_color="#CBD5E1")
        self.answer_label.configure(text=" ".join(self.selected_words))

    def submit_answer(self):
        """Mengirim susunan kata ke logika permainan dan menampilkan umpan balik."""
        if not self.selected_words:
            messagebox.showinfo("Info", "Pilih minimal satu kata terlebih dahulu.")
            return

        is_correct, feedback = self.session.check_answer(self.selected_words)
        if is_correct:
            messagebox.showinfo("Tepat Sekali!", feedback)
        else:
            messagebox.showwarning("Coba Lagi", feedback)

        self.show_game_screen()

    def show_result_screen(self):
        """Menampilkan ringkasan akhir sesi permainan."""
        self.clear_container()

        result_card = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#BAE6FD",
        )
        result_card.pack(fill="both", expand=True, padx=40, pady=30)

        title_text = "Permainan Selesai!"
        if self.session.mode == "Survival" and self.session.lives <= 0:
            title_text = "Survival Berakhir!"

        ctk.CTkLabel(
            result_card,
            text=title_text,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#0369A1",
        ).pack(pady=(36, 12))

        ctk.CTkLabel(
            result_card,
            text=f"Skor Akhir Kamu: {self.session.score}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#16A34A",
        ).pack(pady=(0, 28))

        ctk.CTkButton(
            result_card,
            text="Main Lagi",
            width=180,
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=self.start_game,
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            result_card,
            text="Kembali ke Menu Awal",
            width=180,
            height=40,
            corner_radius=12,
            fg_color="#0284C7",
            hover_color="#0369A1",
            command=self.show_start_screen,
        ).pack()

    def open_add_question_modal(self):
        """Membuka jendela pop-up untuk menambah soal atau level baru."""
        modal = ctk.CTkToplevel(self)
        modal.title("Tambah Soal / Level Baru")
        modal.geometry("420x340")
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Nama Level / Kategori",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(pady=(18, 4))
        level_entry = ctk.CTkEntry(modal, width=320, placeholder_text="Contoh: Level 3: School")
        level_entry.insert(0, self.level_var.get())
        level_entry.pack(pady=(0, 10))

        ctk.CTkLabel(
            modal,
            text="Petunjuk Bahasa Indonesia",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(pady=(4, 4))
        clue_entry = ctk.CTkEntry(modal, width=320, placeholder_text="Contoh: Saya membaca buku")
        clue_entry.pack(pady=(0, 10))

        ctk.CTkLabel(
            modal,
            text="Kalimat Bahasa Inggris Target",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(pady=(4, 4))
        answer_entry = ctk.CTkEntry(modal, width=320, placeholder_text="Contoh: I read a book")
        answer_entry.pack(pady=(0, 18))

        def save_new_item():
            ok, msg = self.manager.add_question(
                level_entry.get(), clue_entry.get(), answer_entry.get()
            )
            if ok:
                messagebox.showinfo("Berhasil", msg)
                modal.destroy()
                self.show_start_screen()
            else:
                messagebox.showwarning("Gagal", msg)

        ctk.CTkButton(
            modal,
            text="Simpan Materi",
            width=180,
            height=40,
            corner_radius=12,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=save_new_item,
        ).pack()