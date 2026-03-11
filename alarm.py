import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
from pygame import mixer

mixer.init()
# ---------------- Puzzle Generator ----------------
def generate_puzzle(puzzle_type, difficulty):

    if puzzle_type == "Math":
        if difficulty == "Easy":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            question = f"What is {a} + {b}?"
            answer = str(a + b)

        elif difficulty == "Medium":
            a = random.randint(10, 50)
            b = random.randint(1, 10)
            question = f"What is {a} - {b}?"
            answer = str(a - b)

        else:  # Hard
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            question = f"What is {a} × {b}?"
            answer = str(a * b)

    elif puzzle_type == "Logic":
        seq = [random.randint(1, 10) for _ in range(4)]
        question = f"Find next number: {seq}"
        answer = str(seq[-1] + (seq[-1] - seq[-2]))

    return question, answer


# ---------------- Alarm Sound ----------------
def play_alarm_sound():
    mixer.music.load("alarm.mp3.mp3")
    mixer.music.play(-1)


def stop_alarm_sound():
    mixer.music.stop()


# ---------------- Alarm Trigger ----------------
def trigger_alarm(alarm_details):
    play_alarm_sound()
    show_puzzle_window(alarm_details["puzzle_type"], alarm_details["difficulty"])


# ---------------- Puzzle Window ----------------
def show_puzzle_window(puzzle_type, difficulty):

    question, correct_answer = generate_puzzle(puzzle_type, difficulty)

    puzzle_window = tk.Toplevel()
    puzzle_window.title("Solve Puzzle to Stop Alarm")
    puzzle_window.geometry("400x200")

    tk.Label(
        puzzle_window,
        text="Wake up! Solve this puzzle to stop the alarm",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Label(
        puzzle_window,
        text=question,
        font=("Arial", 14)
    ).pack(pady=10)

    answer_entry = tk.Entry(puzzle_window)
    answer_entry.pack(pady=5)

    def check_answer():
        user_answer = answer_entry.get().strip()

        if user_answer == correct_answer:
            stop_alarm_sound()
            messagebox.showinfo("Success", "Correct! Alarm stopped.")
            puzzle_window.destroy()
        else:
            messagebox.showwarning("Try Again", "Wrong answer. Try again!")

    tk.Button(
        puzzle_window,
        text="Submit Answer",
        command=check_answer
    ).pack(pady=10)


# ---------------- Alarm Monitor ----------------
def monitor_alarm(alarm_details):

    while True:
        current_time = time.strftime("%H:%M")

        if current_time == alarm_details["time"]:
            trigger_alarm(alarm_details)
            break

        time.sleep(1)


# ---------------- Save Alarm ----------------
def save_alarm():

    alarm_time = time_entry.get()
    puzzle_type = puzzle_type_var.get()
    difficulty = difficulty_var.get()

    if not alarm_time:
        messagebox.showwarning("Warning", "Please enter alarm time")
        return

    alarm_details = {
        "time": alarm_time,
        "puzzle_type": puzzle_type,
        "difficulty": difficulty
    }

    threading.Thread(
        target=monitor_alarm,
        args=(alarm_details,),
        daemon=True
    ).start()

    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")


# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Smart Alarm with Puzzle Solving")
root.geometry("400x300")

tk.Label(root, text="Set Alarm Time (HH:MM)", font=("Arial", 12)).pack(pady=5)

time_entry = tk.Entry(root)
time_entry.pack(pady=5)

tk.Label(root, text="Select Puzzle Type").pack(pady=5)

puzzle_type_var = tk.StringVar(value="Math")

tk.OptionMenu(root, puzzle_type_var, "Math", "Logic").pack()

tk.Label(root, text="Select Difficulty").pack(pady=5)

difficulty_var = tk.StringVar(value="Easy")

tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard").pack()

tk.Button(
    root,
    text="Save Alarm",
    command=save_alarm
).pack(pady=20)

root.mainloop()