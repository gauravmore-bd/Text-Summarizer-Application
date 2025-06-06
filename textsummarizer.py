from transformers import pipeline
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import threading


def create_gui():
    global input_text, output_text, max_length_slider, min_length_slider, progress
    root = tk.Tk()
    root.title("Text Summarizer")
    root.geometry("800x600")

    # Set a dark theme
    style = ttk.Style()
    style.theme_use("clam")  # Or create a custom theme

    # Main Frame
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Input Frame
    input_frame = ttk.Frame(main_frame, style="TFrame")
    input_frame.grid(row=0, column=0, sticky="nsew")

    input_label = ttk.Label(input_frame, text="Original Text:", style="TLabel")
    input_label.grid(row=0, column=0, sticky="w")

    input_text = scrolledtext.ScrolledText(
        input_frame, wrap=tk.WORD, width=60, height=10, style="TScoredText"
    )
    input_text.grid(row=1, column=0, padx=10, pady=10)
    input_text.insert(tk.INSERT, "Enter text here...")  # Placeholder text

    clear_input_button = ttk.Button(
        input_frame, text="Clear", command=lambda: input_text.delete(1.0, tk.END), style="TButton"
    )
    clear_input_button.grid(row=2, column=0, sticky="e", padx=10, pady=5)

    browse_button = ttk.Button(
        input_frame,
        text="Select Text File",
        command=browse_file,
        style="TButton"
    )
    browse_button.grid(row=3, column=0, sticky="e", padx=10, pady=5)
# Initialize the summarization pipeline
print("Loading summarization model. This may take a few seconds...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Model loaded successfully.\n")

def read_text_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def summarize_text(text, max_length=130, min_length=30, do_sample=False):
    max_input_length = 1024 * 4  # Approximate character limit
    if len(text) > max_input_length:
        # Split text into smaller chunks
        chunks = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]
        summaries = []
        for chunk in chunks:
            summary = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample
            )[0]['summary_text']
            summaries.append(summary)
        # Combine summaries of chunks
        final_summary = ' '.join(summaries)
        return final_summary
    else:
        summary = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=do_sample
        )[0]['summary_text']
        return summary

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        title="Select a Text File"
    )
    if file_path:
        try:
            text = read_text_file(file_path)
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, text)
            output_text.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def summarize_gui():
    def run_summarization():
        progress.start()
        text = input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Input Required", "Please select a text file or enter text to summarize.")
            progress.stop()
            return
        try:
            max_length = max_length_slider.get()
            min_length = min_length_slider.get()
            summary = summarize_text(text, max_length=max_length, min_length=min_length)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            progress.stop()
    
    threading.Thread(target=run_summarization).start()

def save_summary():
    summary = output_text.get(1.0, tk.END).strip()
    if not summary:
        messagebox.showwarning("No Summary", "There is no summary to save.")
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save Summary As"
    )
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(summary)
            messagebox.showinfo("Success", f"Summary saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def create_gui():
    global input_text, output_text, max_length_slider, min_length_slider, progress
    root = tk.Tk()
    root.title("Text Summarizer")
    root.geometry("800x800")
    
    # Input Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    input_label = tk.Label(input_frame, text="Original Text:")
    input_label.pack(anchor='w')
    
    input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=90, height=15)
    input_text.pack()
    
    browse_button = tk.Button(
        input_frame,
        text="Select Text File",
        command=browse_file,
        bg='green',
        fg='white',
        font=("Arial", 12, "bold")
    )
    browse_button.pack(pady=5)
    
    # Summary Length Frame
    length_frame = tk.Frame(root)
    length_frame.pack(pady=5, padx=10, fill=tk.X)
    
    max_length_label = tk.Label(length_frame, text="Max Summary Length:")
    max_length_label.pack(side='left', padx=(0, 5))
    
    max_length_slider = tk.Scale(
        length_frame,
        from_=50,
        to=300,
        orient='horizontal'
    )
    max_length_slider.set(130)
    max_length_slider.pack(side='left', padx=(0, 15))
    
    min_length_label = tk.Label(length_frame, text="Min Summary Length:")
    min_length_label.pack(side='left', padx=(0, 5))
    
    min_length_slider = tk.Scale(
        length_frame,
        from_=10,
        to=150,
        orient='horizontal'
    )
    min_length_slider.set(30)
    min_length_slider.pack(side='left', padx=(0, 15))
    
    # Progress Bar
    progress = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
    progress.pack(pady=5, padx=10, fill=tk.X)
    
    # Summarize Button
    summarize_button = tk.Button(
        root,
        text="Generate Summary",
        command=summarize_gui,
        bg='blue',
        fg='white',
        font=("Arial", 14, "bold")
    )
    summarize_button.pack(pady=10)
    
    # Output Frame
    output_frame = tk.Frame(root)
    output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    output_label = tk.Label(output_frame, text="Summary:")
    output_label.pack(anchor='w')
    
    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=90, height=15)
    output_text.pack()
    
    # Save Summary Button
    save_button = tk.Button(
        root,
        text="Save Summary",
        command=save_summary,
        bg='purple',
        fg='white',
        font=("Arial", 12, "bold")
    )
    save_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
