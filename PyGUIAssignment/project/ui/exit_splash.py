"""Exit splash screen with animated MP4 video and skip button - Windows & project-structure aware"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
from pathlib import Path

# Dynamically find the project root (parent of 'ui' folder)
UI_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = UI_DIR.parent

# Try to import COLORS from config.py in project root
try:
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from config import COLORS
except ImportError:
    COLORS = {
        'base': '#1e1e2e',
        'mantle': '#181825',
        'text': '#cdd6f4',
        'mauve': '#cba6f7',
        'lavender': '#b4befe'
    }


class ExitSplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.splash_window = None
        self.cap = None
        self.animation_id = None
        self.video_label = None
        self.skip_button = None

    def show_exit_confirmation(self):
        """Show confirmation dialog before exit"""
        response = messagebox.askyesno(
            "Exit Confirmation",
            "Are you sure you want to exit?",
            icon='question'
        )
        if response:
            self.show_splash()
            return True
        return False

    def show_splash(self):
        """Display the exit splash screen with video and skip button"""
        self.splash_window = tk.Toplevel(self.parent)
        self.splash_window.title("Goodbye!")
        self.splash_window.configure(bg=COLORS['base'])
        self.splash_window.overrideredirect(True)
        self.splash_window.resizable(False, False)

        # Set fixed size: 400 (video) + 40 padding = 440 width; height includes title + video + small footer
        window_width, window_height = 440, 800
        screen_width = self.splash_window.winfo_screenwidth()
        screen_height = self.splash_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.splash_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main container
        main_frame = tk.Frame(self.splash_window, bg=COLORS['base'])
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=780)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Thank You for Using!",
            font=("Segoe UI", 22, "bold"),
            fg=COLORS['mauve'],
            bg=COLORS['base']
        )
        title_label.pack(pady=(0, 15))

        # Video container (400x700)
        video_container = tk.Frame(main_frame, bg=COLORS['mantle'], width=400, height=700)
        video_container.pack()
        video_container.pack_propagate(False)

        self.video_label = tk.Label(video_container, bg=COLORS['mantle'])
        self.video_label.pack(fill="both", expand=True)

        # Skip button — overlaid at bottom of video container
        self.skip_button = tk.Button(
            video_container,
            text="Skip → Exit Now",
            command=self.close_application,
            font=("Segoe UI", 10, "bold"),
            fg=COLORS['base'],
            bg=COLORS['mauve'],
            activebackground='#a37dff',
            activeforeground=COLORS['base'],
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2"
        )
        # Place at bottom center of video container
        self.skip_button.place(relx=0.5, rely=0.95, anchor="center")

        # Footer message
        message_label = tk.Label(
            main_frame,
            text="Group 2 - Enhanced Linked Lists\nClosing application...",
            font=("Segoe UI", 11),
            fg=COLORS['text'],
            bg=COLORS['base'],
            justify="center"
        )
        message_label.pack(pady=(15, 0))

        # Load and play video
        self.load_video()
        if not self.cap or not self.cap.isOpened():
            print("⚠️ Video failed to load. Using fallback.")
            self.show_fallback_animation()
            self.splash_window.after(3000, self.close_application)
        else:
            self.play_video()

    def load_video(self):
        """Load MP4 from expected locations"""
        video_paths = [
            PROJECT_ROOT / "exit.mp4",
            PROJECT_ROOT / "goodbye.mp4",
            PROJECT_ROOT / "assets" / "exit.mp4",
            PROJECT_ROOT / "assets" / "goodbye.mp4"
        ]

        for path in video_paths:
            if path.exists():
                self.cap = cv2.VideoCapture(str(path))
                if self.cap.isOpened():
                    print(f"✅ Loaded video: {path}")
                    return
                else:
                    print(f"⚠️ Could not open: {path}")
        print("❌ No valid video found.")

    def play_video(self):
        """Play video frame by frame at ~30 FPS"""
        if not self.cap or not self.splash_window or not self.video_label.winfo_exists():
            return

        ret, frame = self.cap.read()
        if ret:
            # Convert and resize to exact 400x700
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (400, 700), interpolation=cv2.INTER_AREA)
            img = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image=img)

            self.video_label.config(image=photo)
            self.video_label.image = photo  # Prevent garbage collection

            self.animation_id = self.splash_window.after(5, self.play_video)  
        else:
            # End of video
            self.cap.release()
            self.splash_window.after(500, self.close_application)

    def show_fallback_animation(self):
        """Show animated text if video fails"""
        messages = ["👋 Goodbye!", "✨ Thanks for using!", "🎯 See you soon!", "💚 Happy coding!"]
        index = 0

        def update_text():
            nonlocal index
            if self.splash_window and self.video_label.winfo_exists():
                self.video_label.config(
                    text=messages[index],
                    image='',  # Clear image
                    font=("Segoe UI", 24, "bold"),
                    fg=COLORS['lavender'],
                    bg=COLORS['mantle'],
                    justify="center"
                )
                index = (index + 1) % len(messages)
                self.animation_id = self.splash_window.after(800, update_text)

        update_text()

    def close_application(self):
        """Immediately close splash and exit app"""
        # Cancel pending callbacks
        if self.animation_id and self.splash_window:
            try:
                self.splash_window.after_cancel(self.animation_id)
            except Exception:
                pass

        # Release video
        if self.cap and self.cap.isOpened():
            self.cap.release()

        # Destroy splash
        if self.splash_window:
            self.splash_window.destroy()

        # Exit main app
        self.parent.quit()
        self.parent.destroy()