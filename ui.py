import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from data_handler import load_data, clean_data, save_cleaned_data
from visualization import visualize_data
import time

df = None  # Global DataFrame to hold the dataset


def open_file():
    """Handles file selection and loads data."""
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("PDF files", "*.pdf")])
    if file_path:
        df = load_data(file_path)
        if df is not None:
            messagebox.showinfo("Success", "Dataset loaded successfully!")


def perform_cleaning():
    """Cleans the loaded dataset."""
    global df
    if df is not None:
        df = clean_data(df)
        messagebox.showinfo("Success", "Data cleaned successfully!")
    else:
        messagebox.showwarning("Warning", "No dataset loaded!")


def perform_visualization(chart_type_var, plot_frame):
    """Calls visualization function with the selected chart type."""
    global df
    if df is not None:
        visualize_data(df, chart_type_var.get(), plot_frame)
    else:
        messagebox.showwarning("Warning", "No dataset loaded!")


def perform_save():
    """Saves the cleaned dataset."""
    global df
    if df is not None:
        save_cleaned_data(df)
    else:
        messagebox.showwarning("Warning", "No dataset to save!")


def update_clock(clock_label):
    """Updates the clock display."""
    current_time = time.strftime('%A %b %Y  %H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock, clock_label)


def on_closing(root):
    """Handles window closing."""
    root.destroy()
    exit()


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """Creates a rounded rectangle on a Tkinter canvas."""
    points = [x1 + radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def create_main_window(root):
    """Builds the main GUI window."""
    global canvas

    root.title("Data Analysis Tool")
    root.geometry("1000x700")
    root.configure(bg="#ffffff")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Toolbar
    toolbar = tk.Frame(root, bg="#d8b6ff", height=60, padx=5)
    toolbar.pack(fill=tk.X)

    # Clock
    clock_label = tk.Label(toolbar, font=("Arial", 12, "bold"), bg="#d8b6ff", fg="brown")
    clock_label.pack(side=tk.TOP, pady=5)
    update_clock(clock_label)

    # Canvas for Buttons
    canvas = tk.Canvas(root, width=500, height=60, bg="#ffffff", highlightthickness=0)
    canvas.pack(anchor="w", padx=10)

    buttons = [
        ("Open", open_file, 10, 10, 110, 50),
        ("Clean", perform_cleaning, 130, 10, 230, 50),
        ("Save", perform_save, 250, 10, 350, 50)
    ]

    for text, command, x1, y1, x2, y2 in buttons:
        btn = create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=15, fill="#FFD700", outline="black")
        text_item = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, fill="black", font=("Arial", 10, "bold"))

        # Bind button clicks
        canvas.tag_bind(btn, "<Button-1>", lambda event, cmd=command: cmd())
        canvas.tag_bind(text_item, "<Button-1>", lambda event, cmd=command: cmd())

    # Chart Selection Frame
    frame = ttk.Frame(root, padding=20, style="GreyWhite.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.configure("GreyWhite.TFrame", background="white")

    ttk.Label(frame, text="Select Chart Type:", font=("Arial", 12, "bold"), foreground="brown", background="white").pack()
    
    chart_type_var = tk.StringVar()
    chart_type_dropdown = ttk.Combobox(frame, textvariable=chart_type_var, values=[
        "Heatmap", "Pair Plot", "Scatter Matrix", "Histogram", "Box Plot",
        "Violin Plot", "Density Plot", "Bar Chart", "Line Chart", "Swarm Plot", "Pie Chart"
    ], state="readonly")
    chart_type_dropdown.pack(pady=5)
    chart_type_dropdown.current(0)

    # Visualization Button
    visualize_btn = tk.Canvas(frame, width=120, height=60, bg="white", highlightthickness=0)
    visualize_btn.pack(pady=10)

    btn = create_rounded_rectangle(visualize_btn, 10, 10, 110, 40, radius=15, fill="#FFD700", outline="black")
    text_item = visualize_btn.create_text(60, 25, text="Visualize Data", fill="black", font=("Arial", 10, "bold"))

    # Bind visualization button
    visualize_btn.tag_bind(btn, "<Button-1>", lambda event: perform_visualization(chart_type_var, plot_frame))
    visualize_btn.tag_bind(text_item, "<Button-1>", lambda event: perform_visualization(chart_type_var, plot_frame))

    # Plot Frame
    global plot_frame
    plot_frame = ttk.Frame(root)
    plot_frame.pack(fill=tk.BOTH, expand=True)

