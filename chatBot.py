import datetime
import random
import string
import threading
import tkinter as tk
from tkinter import messagebox, ttk

# User Credentials Storage (In-Memory Database)
USERS_DB = {"admin": "1234", "user": "1234"}

# Embedded Robot Window Icon Data
ICON_DATA = """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAnklEQVR4nO2WSw6AMAhEqfGseia9LK7qptOPARxj+lZGG2YchSBiYVOVTdVSYjGJo+vXDHwC6idwgm4gNZ8a4705U1WnnoCXeKcWNuAp3qlZGogQb9Sm/4R0A+vIIT3Ke2l/fgZBT2AaoBsoR2TkHBApxjI9AbqBoTmQQb2OGOn/DD0BugG8KER1AlhMcAKNDcZTvG7A20TEC00mv+ECj08uUjHiNEgAAAAASUVORK5CYII="""


# =========================================================
# CORE CHATBOT LOGIC (PURE RULE-BASED & MATH SOLVER)
# =========================================================
def get_chatbot_response(user_input):
    raw_input = user_input.strip()

    # Clean input ONLY for simple text keyword matching
    clean_input = (
        raw_input.lower()
        .translate(str.maketrans("", "", string.punctuation))
        .strip()
    )

    # 1. Math Evaluation (Uses raw_input so operators +, -, *, / are preserved)
    if any(char.isdigit() for char in raw_input) and any(
        op in raw_input for op in ["+", "-", "*", "/"]
    ):
        try:
            expr = "".join([c for c in raw_input if c in "0123456789+-*/(). "])
            return f"The answer is 🧮 {eval(expr)}"
        except Exception:
            pass

    # 2. Rule-Based Quick Responses
    if clean_input in ["hello", "hi", "hey", "halo", "greetings"]:
        return "Hi there! How can I help you today?"
    elif clean_input in [
        "how are you",
        "how are you doing",
        "hows it going",
        "kohomada",
    ]:
        return "I'm doing great, thank you! How are you feeling today?"
    elif "help" in clean_input or "options" in clean_input:
        return (
            "💡 Here is what I can do for you:\n"
            "• Say 'hello' or 'hi' to greet me\n"
            "• Ask 'time' or 'date'\n"
            "• Ask for a 'joke'\n"
            "• Solve Math: e.g. '25 * 4'\n"
            "• Ask 'who are you'"
        )
    elif "time" in clean_input:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is 🕒 {now}."
    elif "date" in clean_input or "day" in clean_input:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is 📅 {today}."
    elif "joke" in clean_input:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the Python developer need glasses? Because they couldn't C#! 😎",
            "There are 10 types of people in the world: those who understand binary, and those who don't. 😂",
        ]
        return random.choice(jokes)
    elif clean_input in ["who are you", "what is your name", "whats your name"]:
        return "I am PyBot, an advanced rule-based AI Assistant!"
    elif clean_input in ["bye", "goodbye", "exit", "see you"]:
        return "Goodbye! Have a productive and great day! 👋"

    # Default Fallback
    return "Sorry, I didn't catch that. Try asking 'hello', 'time', 'joke', 'help', '25 * 4', or 'bye'!"


# =========================================================
# MASTER APPLICATION FRAMEWORK
# =========================================================
class MasterApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("PyBot Chat")
        self.geometry("420x660")
        self.resizable(False, False)
        self.configure(bg="#0066ff")

        try:
            self.icon_img = tk.PhotoImage(data=ICON_DATA)
            self.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.current_user = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_splash_screen()

    def show_splash_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        splash = tk.Frame(self.container, bg="#0066ff")
        splash.pack(fill="both", expand=True)

        logo = tk.Label(
            splash,
            text="🤖",
            font=("Segoe UI Emoji", 50),
            bg="#0066ff",
            fg="white",
        )
        logo.pack(pady=(180, 10))

        title = tk.Label(
            splash,
            text="PyBot Chat",
            font=("Segoe UI", 18, "bold"),
            bg="#0066ff",
            fg="#ffffff",
        )
        title.pack()

        subtitle = tk.Label(
            splash,
            text="Loading AI Engine...",
            font=("Segoe UI", 9),
            bg="#0066ff",
            fg="#e0f2fe",
        )
        subtitle.pack(pady=(5, 20))

        progress = ttk.Progressbar(splash, mode="indeterminate", length=220)
        progress.pack()
        progress.start(15)

        self.after(2000, self.show_auth_screen)

    def show_auth_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        auth_frame = AuthFrame(self.container, self)
        auth_frame.pack(fill="both", expand=True)

    def show_chat_screen(self, username):
        self.current_user = username
        for widget in self.container.winfo_children():
            widget.destroy()

        chat_frame = ChatFrame(self.container, self)
        chat_frame.pack(fill="both", expand=True)


# =========================================================
# AUTHENTICATION FRAME
# =========================================================
class AuthFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f9ff")
        self.controller = controller
        self.is_login_mode = True

        self.setup_ui()

    def setup_ui(self):
        self.title_lbl = tk.Label(
            self,
            text="Welcome Back!",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f9ff",
            fg="#000000",
        )
        self.title_lbl.pack(pady=(60, 5))

        self.sub_lbl = tk.Label(
            self,
            text="Please log in to continue",
            font=("Segoe UI", 9),
            bg="#f0f9ff",
            fg="#334155",
        )
        self.sub_lbl.pack(pady=(0, 30))

        form = tk.Frame(self, bg="#0066ff", padx=20, pady=20)
        form.pack(padx=30, fill="x")

        tk.Label(
            form,
            text="Username",
            font=("Segoe UI", 9, "bold"),
            bg="#0066ff",
            fg="#ffffff",
        ).pack(anchor="w")
        self.username_entry = tk.Entry(
            form,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            relief="flat",
            bd=5,
        )
        self.username_entry.pack(fill="x", pady=(5, 15))

        tk.Label(
            form,
            text="Password",
            font=("Segoe UI", 9, "bold"),
            bg="#0066ff",
            fg="#ffffff",
        ).pack(anchor="w")
        self.password_entry = tk.Entry(
            form,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#000000",
            show="•",
            insertbackground="#000000",
            relief="flat",
            bd=5,
        )
        self.password_entry.pack(fill="x", pady=(5, 15))

        self.submit_btn = tk.Button(
            form,
            text="LOG IN",
            font=("Segoe UI", 10, "bold"),
            bg="#0044cc",
            fg="white",
            activebackground="#0033aa",
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.handle_auth,
        )
        self.submit_btn.pack(fill="x", pady=(10, 5))

        self.toggle_btn = tk.Button(
            self,
            text="Don't have an account? Register",
            font=("Segoe UI", 9, "bold"),
            bg="#f0f9ff",
            fg="#0066ff",
            bd=0,
            cursor="hand2",
            command=self.toggle_mode,
        )
        self.toggle_btn.pack(pady=20)

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.title_lbl.config(text="Welcome Back!")
            self.sub_lbl.config(text="Please log in to continue")
            self.submit_btn.config(text="LOG IN")
            self.toggle_btn.config(text="Don't have an account? Register")
        else:
            self.title_lbl.config(text="Create Account")
            self.sub_lbl.config(text="Register a new account to access PyBot")
            self.submit_btn.config(text="REGISTER")
            self.toggle_btn.config(text="Already have an account? Log In")

    def handle_auth(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        if self.is_login_mode:
            if username in USERS_DB and USERS_DB[username] == password:
                self.controller.show_chat_screen(username)
            else:
                messagebox.showerror(
                    "Login Failed", "Invalid username or password!"
                )
        else:
            if username in USERS_DB:
                messagebox.showerror("Error", "Username already exists!")
            else:
                USERS_DB[username] = password
                messagebox.showinfo("Success", "Registration successful!")
                self.controller.show_chat_screen(username)


# =========================================================
# CHATBOT GUI FRAME
# =========================================================
class ChatFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.dark_mode = False
        self.messages_history = []

        self.colors = {
            "light": {
                "bg": "#e0f2fe",
                "header": "#0066ff",
                "chat_bg": "#f0f9ff",
                "user_bubble": "#0066ff",
                "user_fg": "#ffffff",
                "bot_bubble": "#ffffff",
                "bot_fg": "#000000",
                "input_bg": "#ffffff",
                "input_fg": "#000000",
                "time_fg": "#475569",
                "pill_bg": "#ffffff",
                "pill_fg": "#000000",
            },
            "dark": {
                "bg": "#0f172a",
                "header": "#0284c7",
                "chat_bg": "#0b192c",
                "user_bubble": "#0066ff",
                "user_fg": "#ffffff",
                "bot_bubble": "#1e293b",
                "bot_fg": "#f8fafc",
                "input_bg": "#1e293b",
                "input_fg": "#ffffff",
                "time_fg": "#94a3b8",
                "pill_bg": "#1e293b",
                "pill_fg": "#38bdf8",
            },
        }

        self.setup_ui()

    def get_theme(self):
        return self.colors["dark"] if self.dark_mode else self.colors["light"]

    def setup_ui(self):
        theme = self.get_theme()
        self.configure(bg=theme["bg"])

        # 1. Header Bar
        self.header = tk.Frame(self, bg=theme["header"], height=70)
        self.header.pack(fill="x")

        avatar = tk.Label(
            self.header,
            text="🤖",
            font=("Segoe UI Emoji", 16),
            bg="#0044cc",
            fg="white",
            width=2,
        )
        avatar.pack(side="left", padx=(12, 8), pady=12)

        info = tk.Frame(self.header, bg=theme["header"])
        info.pack(side="left", pady=12)

        self.bot_title = tk.Label(
            info,
            text=f"PyBot ({self.controller.current_user})",
            font=("Segoe UI", 10, "bold"),
            bg=theme["header"],
            fg="#ffffff",
        )
        self.bot_title.pack(anchor="w")

        self.bot_status = tk.Label(
            info,
            text="● Online",
            font=("Segoe UI", 8),
            bg=theme["header"],
            fg="#e0f2fe",
        )
        self.bot_status.pack(anchor="w")

        logout_btn = tk.Button(
            self.header,
            text="🚪",
            font=("Segoe UI Emoji", 11),
            bg=theme["header"],
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.logout,
        )
        logout_btn.pack(side="right", padx=(0, 12), pady=12)

        self.theme_btn = tk.Button(
            self.header,
            text="🌙",
            font=("Segoe UI Emoji", 11),
            bg=theme["header"],
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=(0, 8), pady=12)

        clear_btn = tk.Button(
            self.header,
            text="🗑️",
            font=("Segoe UI Emoji", 11),
            bg=theme["header"],
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.clear_chat,
        )
        clear_btn.pack(side="right", padx=(0, 8), pady=12)

        # 2. Scrollable Canvas & Scrollbar Area
        chat_container = tk.Frame(self, bg=theme["chat_bg"])
        chat_container.pack(
            side="top", fill="both", expand=True, padx=10, pady=(10, 0)
        )

        self.canvas = tk.Canvas(
            chat_container, bg=theme["chat_bg"], highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            chat_container, orient="vertical", command=self.canvas.yview
        )

        self.chat_frame = tk.Frame(self.canvas, bg=theme["chat_bg"])
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width),
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            ),
        )

        # 3. Quick Suggestions Bar
        self.quick_frame = tk.Frame(self, bg=theme["bg"])
        self.quick_frame.pack(fill="x", padx=10, pady=5)
        self.render_quick_pills()

        # 4. Input Container
        self.input_container = tk.Frame(self, bg=theme["input_bg"])
        self.input_container.pack(fill="x", side="bottom")

        self.entry_box = tk.Entry(
            self.input_container,
            font=("Segoe UI", 10, "bold"),
            bg=theme["input_bg"],
            fg=theme["input_fg"],
            insertbackground=theme["input_fg"],
            relief="flat",
            bd=0,
        )
        self.entry_box.pack(
            side="left", fill="x", expand=True, padx=(15, 8), pady=12, ipady=6
        )
        self.entry_box.bind("<Return>", lambda e: self.send_user_message())

        self.send_btn = tk.Button(
            self.input_container,
            text="➔",
            font=("Segoe UI", 12, "bold"),
            bg="#0066ff",
            fg="white",
            activebackground="#0044cc",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=3,
            command=self.send_user_message,
        )
        self.send_btn.pack(side="right", padx=(0, 15), pady=12, ipady=1)

        self.add_message(
            f"👋 Welcome {self.controller.current_user}!\nHow can I help you today?",
            is_user=False,
        )

    def render_quick_pills(self):
        for widget in self.quick_frame.winfo_children():
            widget.destroy()

        theme = self.get_theme()
        options = ["hello", "time", "joke", "help", "bye"]

        for opt in options:
            btn = tk.Button(
                self.quick_frame,
                text=opt,
                font=("Segoe UI", 8, "bold"),
                bg=theme["pill_bg"],
                fg=theme["pill_fg"],
                activebackground="#0284c7" if self.dark_mode else "#bae6fd",
                relief="flat",
                bd=1,
                cursor="hand2",
                padx=8,
                pady=2,
                command=lambda val=opt: self.send_quick_reply(val),
            )
            btn.pack(side="left", padx=2)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        theme = self.get_theme()

        self.configure(bg=theme["bg"])
        self.header.configure(bg=theme["header"])
        self.bot_title.configure(bg=theme["header"])
        self.bot_status.configure(bg=theme["header"])
        self.theme_btn.configure(
            bg=theme["header"], text="☀️" if self.dark_mode else "🌙"
        )
        self.canvas.configure(bg=theme["chat_bg"])
        self.chat_frame.configure(bg=theme["chat_bg"])
        self.quick_frame.configure(bg=theme["bg"])
        self.input_container.configure(bg=theme["input_bg"])
        self.entry_box.configure(
            bg=theme["input_bg"],
            fg=theme["input_fg"],
            insertbackground=theme["input_fg"],
        )

        self.render_quick_pills()
        self.re_render_messages()

    def re_render_messages(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        for text, is_user, timestamp in self.messages_history:
            self._render_single_message(text, is_user, timestamp)

    def clear_chat(self):
        self.messages_history.clear()
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.add_message("Chat history cleared. How can I help?", is_user=False)

    def logout(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.controller.show_auth_screen()

    def send_quick_reply(self, text):
        self.entry_box.delete(0, tk.END)
        self.entry_box.insert(0, text)
        self.send_user_message()

    def send_user_message(self):
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        self.add_message(user_text, is_user=True)
        self.entry_box.delete(0, tk.END)

        threading.Thread(
            target=self.process_response, args=(user_text,), daemon=True
        ).start()

    def process_response(self, user_text):
        bot_text = get_chatbot_response(user_text)
        self.after(0, lambda: self.add_message(bot_text, is_user=False))

    def add_message(self, text, is_user=False):
        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        self.messages_history.append((text, is_user, timestamp))
        self._render_single_message(text, is_user, timestamp)

    def _render_single_message(self, text, is_user, timestamp):
        theme = self.get_theme()

        bubble_container = tk.Frame(self.chat_frame, bg=theme["chat_bg"])
        bubble_container.pack(fill="x", pady=4, padx=5)

        msg_frame = tk.Frame(bubble_container, bg=theme["chat_bg"])

        if is_user:
            msg_frame.pack(side="right", anchor="e")
            bubble = tk.Label(
                msg_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=theme["user_bubble"],
                fg=theme["user_fg"],
                wraplength=250,
                justify="left",
                padx=12,
                pady=7,
            )
            bubble.pack(anchor="e")

            time_lbl = tk.Label(
                msg_frame,
                text=timestamp,
                font=("Segoe UI", 7),
                bg=theme["chat_bg"],
                fg=theme["time_fg"],
            )
            time_lbl.pack(anchor="e", padx=2, pady=(2, 0))
        else:
            msg_frame.pack(side="left", anchor="w")
            bubble = tk.Label(
                msg_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=theme["bot_bubble"],
                fg=theme["bot_fg"],
                wraplength=250,
                justify="left",
                padx=12,
                pady=7,
            )
            bubble.pack(anchor="w")

            time_lbl = tk.Label(
                msg_frame,
                text=timestamp,
                font=("Segoe UI", 7),
                bg=theme["chat_bg"],
                fg=theme["time_fg"],
            )
            time_lbl.pack(anchor="w", padx=2, pady=(2, 0))

        self.update_idletasks()
        self.canvas.yview_moveto(1.0)


if __name__ == "__main__":
    app = MasterApp()
    app.mainloop()