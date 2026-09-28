import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from pathlib import Path
import threading
from lecture_summarisation import process_audio

# Selecting audio file and processing it
def process_lecture():
    if selected_audio is None:
        status_label.config(text="Please select an audio file first.")
        return

    status_label.config(text="Status: Processing...")
    process_button.config(state="disabled")

    thread = threading.Thread(
        target=run_processing,
        daemon=True
    )
    thread.start()

# Processing the audio file
def run_processing():
    try:
        process_audio(selected_audio)

        root.after(
            0,
            lambda: status_label.config(text="Status: Complete")
            
        )
        root.after(0, display_outputs)

    except Exception as e:
        print("Error:", e)

        root.after(
            0,
            lambda: status_label.config(text="Status: Error")
        )

    finally:
        root.after(
            0,
            lambda: process_button.config(state="normal")
        )

# Selecting the audio file
def select_audio():
    global selected_audio

    file_path = filedialog.askopenfilename(
        title="Select Lecture Audio",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav *.m4a"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        selected_audio = Path(file_path)
        file_label.config(text=selected_audio.name)

        summary_text.config(state="normal")
        concepts_text.config(state="normal")
        revision_text.config(state="normal")

        summary_text.delete("1.0", tk.END)
        concepts_text.delete("1.0", tk.END)
        revision_text.delete("1.0", tk.END)

        summary_text.config(state="disabled")
        concepts_text.config(state="disabled")
        revision_text.config(state="disabled")

        status_label.config(text="Status: Ready")

# Displaying outputs after processing
def display_outputs():
    summary_text.config(state="normal")
    concepts_text.config(state="normal")
    revision_text.config(state="normal")

    summary_path = Path("output/summary.txt")
    concepts_path = Path("output/key_concepts.txt")
    revision_path = Path("output/revision_notes.txt")

    if summary_path.exists():
        summary = summary_path.read_text(encoding="utf-8")
        summary_text.delete("1.0", tk.END)
        summary_text.insert(tk.END, summary)

    if concepts_path.exists():
        concepts = concepts_path.read_text(encoding="utf-8")
        concepts_text.delete("1.0", tk.END)
        concepts_text.insert(tk.END, concepts)

    if revision_path.exists():
        revision = revision_path.read_text(encoding="utf-8")
        revision_text.delete("1.0", tk.END)
        revision_text.insert(tk.END, revision)

    summary_text.config(state="disabled")
    concepts_text.config(state="disabled")
    revision_text.config(state="disabled")


root = tk.Tk()
root.title("AI Lecture Summarisation Assistant")
root.geometry("800x600")

title_label = tk.Label(
    root,
    text="AI Lecture Summarisation Assistant",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=20)

select_button = tk.Button(
    root,
    text="Select Audio File",
    command=select_audio,
    width=20
)
select_button.pack(pady=10)

file_label = tk.Label(
    root,
    text="No audio file selected"
)
file_label.pack(pady=5)

process_button = tk.Button(
    root,
    text="Process Lecture",
    command=process_lecture,
    width=20
)
process_button.pack(pady=15)

status_label = tk.Label(
    root,
    text="Status: Ready"
)
status_label.pack(pady=5)

output_tabs = ttk.Notebook(root)
output_tabs.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# Generate summary for display
summary_tab = tk.Frame(output_tabs)
output_tabs.add(summary_tab, text="Summary")

summary_text = scrolledtext.ScrolledText(
    summary_tab,
    wrap="word"
)
summary_text.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

# Generate key concepts for display
concepts_tab = tk.Frame(output_tabs)
output_tabs.add(concepts_tab, text="Key Concepts")

concepts_text = scrolledtext.ScrolledText(
    concepts_tab,
    wrap="word"
)
concepts_text.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)

# Generate final revision notes for display
revision_tab = tk.Frame(output_tabs)
output_tabs.add(revision_tab, text="Revision Notes")

revision_text = scrolledtext.ScrolledText(
    revision_tab,
    wrap="word"
)
revision_text.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)


root.mainloop()