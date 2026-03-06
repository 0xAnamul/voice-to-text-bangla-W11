<div align="center">

# 🎙️ ভয়েস টু টেক্সট
### Bengali & English Voice Recognition for Windows

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-e94560?style=for-the-badge)]()

**বাংলা ও ইংরেজি উভয় ভাষায় ভয়েস থেকে টেক্সট রূপান্তর করুন — একটি ক্লিকেই।**  
*Convert speech to text in Bengali & English with a single click.*

[⬇️ ডাউনলোড](#-ইন্সটল-করুন--installation) · [🚀 ব্যবহার](#-ব্যবহারের-নিয়ম--how-to-use) · [❓ সমস্যা?](#-সমস্যা-হলে--troubleshooting)

---

</div>

## ✨ ফিচারসমূহ | Features

| ফিচার | বিবরণ |
|-------|--------|
| 🇧🇩 **বাংলা সাপোর্ট** | সরাসরি বাংলায় কথা বলুন, বাংলা টেক্সট পাবেন |
| 🇺🇸 **English সাপোর্ট** | Full English speech recognition |
| 🔀 **Auto মোড** | দুটো ভাষা মিশিয়ে বলুন, অটো ডিটেক্ট করবে |
| ⌨️ **কার্সারে টাইপ** | যেকোনো অ্যাপে কার্সার রাখুন — সেখানেই টাইপ হবে |
| 📋 **ক্লিপবোর্ড কপি** | এক ক্লিকে সব টেক্সট কপি |
| 🎨 **সুন্দর UI** | Dark theme, বাংলা ফন্ট সাপোর্ট |
| 🖥️ **লাইটওয়েট** | কোনো ভারী মডেল নেই, ইন্টারনেটেই কাজ করে |

---

## 📸 স্ক্রিনশট | Screenshot

```
┌─────────────────────────────────────────────┐
│  🎙️ ভয়েস টু টেক্সট | Voice to Text         │
│       Bengali & English                      │
├─────────────────────────────────────────────┤
│  ভাষা: ● বাংলা  ○ English  ○ Auto          │
│  আউটপুট: ☑ কার্সারে টাইপ  ☐ ক্লিপবোর্ড    │
├─────────────────────────────────────────────┤
│                                             │
│     [ 🎙️ রেকর্ড শুরু করুন ]               │
│                                             │
│  ✅ প্রস্তুত | Ready                        │
├─────────────────────────────────────────────┤
│  ট্রান্সক্রিপ্ট:                            │
│  আমি বাংলায় কথা বলছি এবং এটি             │
│  সরাসরি টেক্সটে রূপান্তর হচ্ছে...         │
└─────────────────────────────────────────────┘
```

---

## ⬇️ ইন্সটল করুন | Installation

### পূর্বশর্ত | Prerequisites
- **Python 3.10+** — [python.org](https://python.org) থেকে ডাউনলোড করুন  
  ⚠️ ইন্সটলের সময় **"Add Python to PATH"** চেক করতে ভুলবেন না!
- **ইন্টারনেট সংযোগ** — Google Speech API ব্যবহার করে
- **মাইক্রোফোন** — যেকোনো USB বা built-in মাইক

### ধাপে ধাপে | Step by Step

```bash
# ১. এই রিপোজিটরি ক্লোন করুন
git clone https://github.com/YOUR_USERNAME/voice-to-text-bangla.git
cd voice-to-text-bangla

# ২. প্যাকেজ ইন্সটল করুন
pip install SpeechRecognition pyaudio pyperclip pyautogui

# ৩. অ্যাপ চালু করুন
python voice_to_text.py
```

### Windows-এ সহজ পদ্ধতি
1. `install.bat` — ডাবল ক্লিক করুন *(একবারই)*
2. `run.bat` — ডাবল ক্লিক করুন *(প্রতিবার চালু করতে)*

---

## 🚀 ব্যবহারের নিয়ম | How to Use

```
১ → ভাষা সিলেক্ট করুন (বাংলা / English / Auto)
২ → যে অ্যাপে লিখবেন সেখানে কার্সার রাখুন
৩ → "রেকর্ড শুরু করুন" বাটনে ক্লিক করুন
৪ → মাইক্রোফোনে কথা বলুন
৫ → "থামুন" বাটনে ক্লিক করুন → টেক্সট চলে আসবে!
```

---

## 📦 নির্ভরযোগ্যতা | Dependencies

| প্যাকেজ | কাজ |
|---------|-----|
| `SpeechRecognition` | Google Speech API দিয়ে ভয়েস রিকগনিশন |
| `pyaudio` | মাইক্রোফোন থেকে অডিও রেকর্ড |
| `pyperclip` | ক্লিপবোর্ডে টেক্সট কপি |
| `pyautogui` | কার্সারের জায়গায় টেক্সট টাইপ |
| `tkinter` | GUI (Python-এ বিল্ট-ইন) |

---

## ❓ সমস্যা হলে | Troubleshooting

<details>
<summary><b>PyAudio ইন্সটল হচ্ছে না</b></summary>

```bash
pip install pipwin
pipwin install pyaudio
```
</details>

<details>
<summary><b>মাইক কাজ করছে না</b></summary>

Windows Settings → Privacy & Security → Microphone → **Allow apps to access your microphone** চালু করুন
</details>

<details>
<summary><b>বাংলা টেক্সট ঠিকমতো দেখাচ্ছে না</b></summary>

Windows-এ **Vrinda** বা **Kalpurush** ফন্ট ইন্সটল করুন।
</details>

<details>
<summary><b>"Network error" দেখাচ্ছে</b></summary>

ইন্টারনেট সংযোগ চেক করুন। এই অ্যাপটি Google Speech API ব্যবহার করে, তাই ইন্টারনেট লাগবে।
</details>

---

## 🗺️ রোডম্যাপ | Roadmap

- [ ] অফলাইন মোড (Whisper AI দিয়ে)
- [ ] হটকি সাপোর্ট (Ctrl+Shift+V)
- [ ] সিস্টেম ট্রেতে মিনিমাইজ
- [ ] টেক্সট ফাইলে সেভ করার অপশন
- [ ] `.exe` ইন্সটলার

---

## 📄 লাইসেন্স | License

MIT License — বিস্তারিত [LICENSE](LICENSE) ফাইলে দেখুন।

---

<div align="center">

**তৈরি করেছেন Claude (Anthropic) — ❤️ দিয়ে**

*⭐ যদি কাজে লাগে, একটি Star দিন!*

</div>
