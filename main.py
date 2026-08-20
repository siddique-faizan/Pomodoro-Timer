from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
ORANGE = "#FFA500"
FONT_NAME = "Courier"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

SESSIONS_BEFORE_LONG_BREAK = 4


# ---------------------------- TIMER VARIABLES -------------------------- #

reps = 0
timer = None
is_running = False


# ---------------------------- TIMER RESET ------------------------------- #

def reset():
    global reps, timer, is_running

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    reps = 0
    is_running = False

    canvas.itemconfig(timer_text, text="00:00", fill=GREEN)
    window_label.config(text="TIMER", fg=GREEN)
    check_mark.config(text="")

    start_button.config(state="normal")


# ---------------------------- TIMER START ------------------------------ #

def start_timer():
    global reps, is_running

    if is_running:
        return

    is_running = True
    reps += 1

    # Long break
    if reps % (SESSIONS_BEFORE_LONG_BREAK * 2) == 0:
        timer_minutes = LONG_BREAK_MIN
        window_label.config(text="LONG BREAK", fg=RED)

    # Short break
    elif reps % 2 == 0:
        timer_minutes = SHORT_BREAK_MIN
        window_label.config(text="SHORT BREAK", fg=PINK)

    # Work session
    else:
        timer_minutes = WORK_MIN
        window_label.config(text="WORK", fg=RED)

    start_button.config(state="disabled")

    count_down(timer_minutes * 60)


# ---------------------------- COUNTDOWN MECHANISM ---------------------- #

def count_down(count):
    global timer, is_running

    count_min = math.floor(count / 60)
    count_sec = count % 60

    canvas.itemconfig(
        timer_text,
        text=f"{count_min:02}:{count_sec:02}"
    )

    # Change timer colour based on time remaining
    if count > 10 * 60:
        canvas.itemconfig(timer_text, fill=GREEN)

    elif count > 5 * 60:
        canvas.itemconfig(timer_text, fill="#FFD700")

    elif count > 60:
        canvas.itemconfig(timer_text, fill=ORANGE)

    else:
        canvas.itemconfig(timer_text, fill=RED)

    if count > 0:
        timer = window.after(
            1000,
            count_down,
            count - 1
        )

    else:
        timer = None
        is_running = False
        timer_finished()


# ---------------------------- TIMER FINISHED ---------------------------- #

def timer_finished():
    global reps

    window.bell()

    # Add a check mark after every completed work session
    if reps % 2 == 1:
        completed_sessions = (reps + 1) // 2
        check_mark.config(text="✓ " * completed_sessions)

    # Automatically start the next session
    start_timer()


# ---------------------------- UI SETUP ---------------------------------- #

window = Tk()
window.title("Pomodoro Timer")
window.config(
    padx=40,
    pady=30,
    bg=YELLOW
)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)


# ---------------------------- TITLE ------------------------------------- #

window_label = Label(
    text="TIMER",
    font=(FONT_NAME, 50, "bold"),
    bg=YELLOW,
    fg=GREEN
)

window_label.grid(
    column=1,
    row=0,
    pady=(0, 20)
)


# ---------------------------- CANVAS ------------------------------------ #

canvas = Canvas(
    width=300,
    height=320,
    bg=YELLOW,
    highlightthickness=0
)

tomato_image = PhotoImage(file="tomato.png")

canvas.create_image(
    150,
    160,
    image=tomato_image
)

timer_text = canvas.create_text(
    150,
    170,
    text="00:00",
    font=(FONT_NAME, 35, "bold"),
    fill=GREEN
)

canvas.grid(
    column=1,
    row=1,
    pady=(0, 20)
)


# ---------------------------- BUTTONS ----------------------------------- #

start_button = Button(
    text="Start",
    font=(FONT_NAME, 12, "bold"),
    width=10,
    height=1,
    command=start_timer
)

quit_button = Button(
    text="Quit",
    font=(FONT_NAME, 12, "bold"),
    width=10,
    fg=RED,
    command=window.destroy
)

reset_button = Button(
    text="Reset",
    font=(FONT_NAME, 12, "bold"),
    width=10,
    command=reset
)


# Place Start, Quit and Reset next to each other
start_button.grid(
    column=0,
    row=2,
    padx=10
)

quit_button.grid(
    column=1,
    row=2,
    padx=10
)

reset_button.grid(
    column=2,
    row=2,
    padx=10
)


# ---------------------------- CHECK MARKS ------------------------------- #

check_mark = Label(
    text="",
    font=(FONT_NAME, 18, "bold"),
    fg=GREEN,
    bg=YELLOW
)

check_mark.grid(
    column=1,
    row=3,
    pady=15
)


# ---------------------------- MAIN LOOP --------------------------------- #

window.mainloop()