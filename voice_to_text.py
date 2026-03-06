import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import pyperclip
import pyautogui
import time
import os
import sys

# Try to import speech recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

# Try to import whisper for better Bengali support
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

class VoiceToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ভয়েস টু টেক্সট | Voice to Text")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a2e")
        
        # State
        self.is_recording = False
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.language_var = tk.StringVar(value="bn-BD")
        self.status_var = tk.StringVar(value="প্রস্তুত | Ready")
        self.auto_type_var = tk.BooleanVar(value=True)
        self.auto_copy_var = tk.BooleanVar(value=False)
        
        self.setup_ui()
        self.check_dependencies()
        self.poll_results()
        
    def setup_ui(self):
        # Colors
        bg = "#1a1a2e"
        panel = "#16213e"
        accent = "#0f3460"
        btn_rec = "#e94560"
        btn_stop = "#4ecca3"
        text_col = "#eaeaea"
        muted = "#a0a0b0"
        
        self.root.configure(bg=bg)

        # Title
        title_frame = tk.Frame(self.root, bg=bg, pady=10)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="🎙️ ভয়েস টু টেক্সট", font=("Segoe UI", 18, "bold"),
                 bg=bg, fg=text_col).pack()
        tk.Label(title_frame, text="Voice to Text — বাংলা & English",
                 font=("Segoe UI", 10), bg=bg, fg=muted).pack()

        # Language selection
        lang_frame = tk.Frame(self.root, bg=panel, pady=12, padx=20)
        lang_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        tk.Label(lang_frame, text="ভাষা বেছে নিন | Select Language:",
                 font=("Segoe UI", 11, "bold"), bg=panel, fg=text_col).pack(side="left", padx=(0,15))

        langs = [("🇧🇩 বাংলা", "bn-BD"), ("🇺🇸 English", "en-US"), ("🔀 Both (Auto)", "auto")]
        for label, code in langs:
            rb = tk.Radiobutton(lang_frame, text=label, variable=self.language_var, value=code,
                                font=("Segoe UI", 10), bg=panel, fg=text_col,
                                selectcolor=accent, activebackground=panel,
                                activeforeground=text_col, cursor="hand2")
            rb.pack(side="left", padx=8)

        # Options
        opt_frame = tk.Frame(self.root, bg=panel, pady=8, padx=20)
        opt_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(opt_frame, text="আউটপুট অপশন:", font=("Segoe UI", 10, "bold"),
                 bg=panel, fg=text_col).pack(side="left", padx=(0,10))

        chk1 = tk.Checkbutton(opt_frame, text="কার্সারে টাইপ করবে", variable=self.auto_type_var,
                               font=("Segoe UI", 10), bg=panel, fg=text_col,
                               selectcolor=accent, activebackground=panel,
                               activeforeground=text_col, cursor="hand2")
        chk1.pack(side="left", padx=5)

        chk2 = tk.Checkbutton(opt_frame, text="ক্লিপবোর্ডে কপি", variable=self.auto_copy_var,
                               font=("Segoe UI", 10), bg=panel, fg=text_col,
                               selectcolor=accent, activebackground=panel,
                               activeforeground=text_col, cursor="hand2")
        chk2.pack(side="left", padx=5)

        # Record button
        btn_frame = tk.Frame(self.root, bg=bg, pady=5)
        btn_frame.pack()

        self.record_btn = tk.Button(btn_frame, text="🎙️ রেকর্ড শুরু করুন\nPress to Record",
                                     font=("Segoe UI", 13, "bold"),
                                     bg=btn_rec, fg="white", relief="flat",
                                     padx=30, pady=15, cursor="hand2",
                                     activebackground="#c73652", activeforeground="white",
                                     command=self.toggle_recording)
        self.record_btn.pack()

        # Status
        status_frame = tk.Frame(self.root, bg=bg, pady=5)
        status_frame.pack()
        self.status_label = tk.Label(status_frame, textvariable=self.status_var,
                                      font=("Segoe UI", 10), bg=bg, fg=btn_stop)
        self.status_label.pack()

        # Transcript area
        trans_frame = tk.Frame(self.root, bg=bg, padx=20)
        trans_frame.pack(fill="both", expand=True, pady=(5, 5))

        tk.Label(trans_frame, text="ট্রান্সক্রিপ্ট | Transcript:",
                 font=("Segoe UI", 10, "bold"), bg=bg, fg=muted).pack(anchor="w")

        self.transcript_box = scrolledtext.ScrolledText(
            trans_frame, font=("Vrinda", 13), wrap=tk.WORD,
            bg=panel, fg=text_col, insertbackground=text_col,
            relief="flat", padx=10, pady=10, height=8
        )
        self.transcript_box.pack(fill="both", expand=True)

        # Bottom buttons
        bottom_frame = tk.Frame(self.root, bg=bg, pady=8, padx=20)
        bottom_frame.pack(fill="x")

        tk.Button(bottom_frame, text="🗑️ মুছুন | Clear",
                  font=("Segoe UI", 10), bg=accent, fg=text_col,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  activebackground="#1a4a7a", activeforeground=text_col,
                  command=self.clear_transcript).pack(side="left", padx=5)

        tk.Button(bottom_frame, text="📋 সব কপি | Copy All",
                  font=("Segoe UI", 10), bg=accent, fg=text_col,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  activebackground="#1a4a7a", activeforeground=text_col,
                  command=self.copy_all).pack(side="left", padx=5)

    def check_dependencies(self):
        if not SR_AVAILABLE:
            self.status_var.set("⚠️ speech_recognition ইন্সটল নেই!")
            self.record_btn.config(state="disabled")
            self.show_install_message()

    def show_install_message(self):
        self.transcript_box.insert("end",
            "প্রথমে এই কমান্ডগুলো চালান:\n\n"
            "pip install SpeechRecognition\n"
            "pip install pyaudio\n"
            "pip install pyperclip\n"
            "pip install pyautogui\n\n"
            "তারপর আবার চালু করুন।\n"
        )

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_btn.config(
            text="⏹️ থামুন | Stop Recording",
            bg="#4ecca3", fg="#1a1a2e"
        )
        self.status_var.set("🔴 রেকর্ড হচ্ছে... | Recording...")
        self.status_label.config(fg="#e94560")
        
        thread = threading.Thread(target=self.record_audio, daemon=True)
        thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_btn.config(
            text="🎙️ রেকর্ড শুরু করুন\nPress to Record",
            bg="#e94560", fg="white"
        )
        self.status_var.set("⏳ প্রসেস হচ্ছে... | Processing...")
        self.status_label.config(fg="#f0c040")

    def record_audio(self):
        if not SR_AVAILABLE:
            return
        
        lang = self.language_var.get()
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Process in separate thread
                    t = threading.Thread(
                        target=self.process_audio,
                        args=(audio, lang),
                        daemon=True
                    )
                    t.start()
                    
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    self.result_queue.put(("error", str(e)))
                    break

    def process_audio(self, audio, lang):
        try:
            if lang == "auto":
                # Try Bengali first, then English
                try:
                    text = self.recognizer.recognize_google(audio, language="bn-BD")
                    self.result_queue.put(("text", text))
                except sr.UnknownValueError:
                    try:
                        text = self.recognizer.recognize_google(audio, language="en-US")
                        self.result_queue.put(("text", text))
                    except sr.UnknownValueError:
                        self.result_queue.put(("warn", "বোঝা যায়নি | Not understood"))
            else:
                text = self.recognizer.recognize_google(audio, language=lang)
                self.result_queue.put(("text", text))
                
        except sr.UnknownValueError:
            self.result_queue.put(("warn", "বোঝা যায়নি | Not understood"))
        except sr.RequestError as e:
            self.result_queue.put(("error", f"ইন্টারনেট সমস্যা | Network error: {e}"))

    def poll_results(self):
        try:
            while True:
                msg_type, content = self.result_queue.get_nowait()
                
                if msg_type == "text":
                    self.handle_recognized_text(content)
                elif msg_type == "warn":
                    self.status_var.set(f"⚠️ {content}")
                elif msg_type == "error":
                    self.status_var.set(f"❌ {content}")
                    self.is_recording = False
                    self.record_btn.config(
                        text="🎙️ রেকর্ড শুরু করুন\nPress to Record",
                        bg="#e94560", fg="white"
                    )
                    
                if not self.is_recording:
                    self.status_var.set("✅ প্রস্তুত | Ready")
                    self.status_label.config(fg="#4ecca3")
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.poll_results)

    def handle_recognized_text(self, text):
        # Update transcript box
        self.transcript_box.insert("end", text + " ")
        self.transcript_box.see("end")
        
        # Update status
        self.status_var.set(f"✅ শোনা হয়েছে | Heard: {text[:30]}...")
        self.status_label.config(fg="#4ecca3")
        
        # Auto copy to clipboard
        if self.auto_copy_var.get():
            pyperclip.copy(text)
        
        # Auto type at cursor position
        if self.auto_type_var.get():
            self.type_at_cursor(text)

    def type_at_cursor(self, text):
        def do_type():
            time.sleep(0.1)
            try:
                pyperclip.copy(text + " ")
                pyautogui.hotkey('ctrl', 'v')
            except Exception:
                pass
        
        t = threading.Thread(target=do_type, daemon=True)
        t.start()

    def clear_transcript(self):
        self.transcript_box.delete("1.0", "end")

    def copy_all(self):
        text = self.transcript_box.get("1.0", "end").strip()
        if text:
            pyperclip.copy(text)
            self.status_var.set("📋 ক্লিপবোর্ডে কপি হয়েছে | Copied!")


def main():
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
