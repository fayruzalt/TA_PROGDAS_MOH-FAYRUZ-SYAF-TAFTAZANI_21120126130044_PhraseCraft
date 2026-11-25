import random


class BaseGameSession:
    """Kelas dasar untuk sesi permainan PhraseCraft."""

    def __init__(self, levels_data: dict, mode: str = "Normal"):
        self.levels_data = levels_data
        self.mode = mode
        self.current_level = None
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.lives = 3

    def start_level(self, level_name: str) -> bool:
        """Memulai level tertentu dan mengembalikan True jika berhasil."""
        if level_name not in self.levels_data:
            return False

        self.current_level = level_name
        # Salin daftar soal agar urutan asli tidak rusak
        self.questions = list(self.levels_data[level_name])
        random.shuffle(self.questions)
        self.current_index = 0
        self.score = 0
        self.lives = 3
        return True

    def get_current_question(self) -> dict | None:
        """Mengambil soal aktif atau None jika level sudah selesai."""
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def get_shuffled_words(self) -> list:
        """Memecah kalimat jawaban menjadi potongan kata acak."""
        question = self.get_current_question()
        if not question:
            return []

        words = question["answer"].split()
        shuffled = list(words)
        random.shuffle(shuffled)
        return shuffled

    def check_answer(self, selected_words: list) -> tuple[bool, str]:
        """Memeriksa susunan kata dan memperbarui skor atau nyawa."""
        question = self.get_current_question()
        if not question:
            return False, "Tidak ada soal aktif."

        user_sentence = " ".join(selected_words).strip()
        target_sentence = question["answer"].strip()

        if user_sentence.lower() == target_sentence.lower():
            self.score += 10
            self.current_index += 1
            return True, "Hebat! Susunan kalimatmu tepat (+10 poin)."
        else:
            if self.mode == "Survival":
                self.lives -= 1
                if self.lives <= 0:
                    return False, "Nyawa habis! Mode Survival berakhir."
                return False, f"Kurang tepat. Sisa nyawa: {self.lives}"
            else:
                return False, "Belum tepat, coba susun ulang katanya ya!"

    def is_game_over(self) -> bool:
        """Mengecek apakah permainan berakhir (nyawa habis atau soal selesai)."""
        if self.mode == "Survival" and self.lives <= 0:
            return True
        if self.current_index >= len(self.questions):
            return True
        return False


class SurvivalGameSession(BaseGameSession):
    """Subclass yang mewarisi BaseGameSession khusus untuk mode Survival."""

    def __init__(self, levels_data: dict):
        super().__init__(levels_data=levels_data, mode="Survival")
        self.streak = 0

    def check_answer(self, selected_words: list) -> tuple[bool, str]:
        correct, message = super().check_answer(selected_words)
        if correct:
            self.streak += 1
            # Bonus poin ekstra jika beruntun benar di mode Survival
            if self.streak >= 2:
                self.score += 5
                message = f"{message} (+5 bonus streak!)"
        else:
            self.streak = 0
        return correct, message


class PhraseCraftManager:
    """Mengelola penyimpanan level/soal dan pembuatan sesi permainan."""

    def __init__(self):
        self.levels = {
            "Level 1: Daily Routine": [
                {
                    "clue": "Saya minum air setiap pagi.",
                    "answer": "I drink water every morning",
                },
                {
                    "clue": "Dia pergi ke sekolah dengan sepeda.",
                    "answer": "She rides a bicycle to school",
                },
            ],
            "Level 2: Animals & Nature": [
                {
                    "clue": "Kucing itu tidur di atas sofa.",
                    "answer": "The cat sleeps on the sofa",
                },
                {
                    "clue": "Burung-burung terbang di langit biru.",
                    "answer": "Birds fly in the blue sky",
                },
            ],
        }

    def add_question(self, level_name: str, clue: str, answer: str) -> tuple[bool, str]:
        """Menambahkan soal baru ke level yang ada atau membuat level baru."""
        clean_level = level_name.strip()
        clean_clue = clue.strip()
        clean_answer = " ".join(answer.strip().split())

        if not clean_level or not clean_clue or not clean_answer:
            return False, "Nama level, petunjuk, dan kalimat wajib diisi."

        if len(clean_answer.split()) < 2:
            return False, "Kalimat bahasa Inggris minimal terdiri dari 2 kata."

        if clean_level not in self.levels:
            self.levels[clean_level] = []

        self.levels[clean_level].append({
            "clue": clean_clue,
            "answer": clean_answer,
        })
        return True, f"Soal berhasil ditambahkan ke '{clean_level}'."

    def create_session(self, mode: str) -> BaseGameSession:
        """Membuat objek sesi sesuai mode yang dipilih."""
        if mode == "Survival":
            return SurvivalGameSession(self.levels)
        return BaseGameSession(self.levels, mode="Normal")