import customtkinter as ctk
from time import perf_counter


class ModernStopwatch(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Секундомер byArina")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        try:
            self.iconbitmap("stopwatch.ico")
        except:
            print("Файл иконки не найден")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

        self.free_label = ctk.CTkLabel(self, text="")
        self.free_label.pack(pady=100)

        # Создание интерфейса
        self.time_label = ctk.CTkLabel(self, text="00:00.000",
                                       font=("Arial", 240), text_color="#ffffff")
        self.time_label.pack(pady=40)

        # Первый ряд кнопок: Старт, Стоп
        button_frame1 = ctk.CTkFrame(self)
        button_frame1.pack(pady=10)

        self.start_btn = ctk.CTkButton(button_frame1, text="Старт",
                                       command=self.start, fg_color="#bbd779", hover_color="#acf250", text_color="#000000")
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(button_frame1, text="Стоп",
                                      command=self.stop, fg_color="#f25a50", hover_color="#ed2626",
                                      state="disabled", text_color="#000000")
        self.stop_btn.pack(side="left", padx=5)

        # Второй ряд: кнопка сброса, круг
        button_frame2 = ctk.CTkFrame(self)
        button_frame2.pack(pady=10)

        self.lap_btn = ctk.CTkButton(button_frame2, text="Круг",
                                     command=self.lap, fg_color="#e9cdf4", hover_color="#ce83ec",
                                     state="disabled", text_color="#000000")
        self.lap_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(button_frame2, text="Сброс",
                                       command=self.reset, fg_color="#f5e080", hover_color="#ffef1a",
                                       text_color="#000000")
        self.reset_btn.pack(side="left", padx=5)

        # Список кругов
        self.lap_frame = ctk.CTkScrollableFrame(self, height=200)
        self.lap_frame.pack(pady=20, fill="both", expand=True, padx=20)

        self.laps = []

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = perf_counter() - self.elapsed_time
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.lap_btn.configure(state="normal")
            self.update_time()

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = perf_counter() - self.start_time
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.lap_btn.configure(state="disabled")

    def reset(self):
        """Сброс таймера и очистка кругов"""
        self.running = False
        self.elapsed_time = 0
        self.start_time = 0

        self.time_label.configure(text="00:00.000")

        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.lap_btn.configure(state="disabled")

        for lap in self.laps:
            lap.destroy()
        self.laps.clear()

    def lap(self):
        if self.running:
            current_time = perf_counter() - self.start_time
            lap_number = len(self.laps) + 1

            lap_label = ctk.CTkLabel(self.lap_frame,
                                     text=f"Круг {lap_number}: {self.format_time(current_time)}",
                                     font=("Arial", 48))
            lap_label.pack(pady=5)
            self.laps.append(lap_label)

    def format_time(self, seconds):
        minutes = int((seconds % 3600) // 60)
        seconds_int = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{minutes:02d}:{seconds_int:02d}.{milliseconds:03d}"

    def update_time(self):
        if self.running:
            current_time = perf_counter() - self.start_time
            self.elapsed_time = current_time
            self.time_label.configure(text=self.format_time(current_time))
            self.after(10, self.update_time)


if __name__ == "__main__":
    app = ModernStopwatch()
    app.mainloop()
