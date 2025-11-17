# gesture_volume_app.py
# Complete Windows App - Frontend + Backend Integrated
# No separate servers needed - everything runs in one Python script!

import cv2
import mediapipe as mp
import numpy as np
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading

class GestureVolumeApp:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("🖐️ Hand Gesture Volume Control")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.running = True
        self.current_volume = 50
        self.current_distance = 0
        self.hand_detected = False
        
        # Setup MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Setup Windows volume control
        self.setup_volume_control()
        
        # Build UI
        self.create_ui()
        
        # Start camera in separate thread
        self.camera_thread = threading.Thread(target=self.process_camera, daemon=True)
        self.camera_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_volume_control(self):
        """Setup Windows volume control using pycaw"""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.vol_range = self.volume.GetVolumeRange()
            print("✅ Volume control initialized")
        except Exception as e:
            print(f"❌ Volume control error: {e}")
            self.volume = None
    
    def set_system_volume(self, volume_percent):
        """Set Windows system volume (0-100)"""
        if self.volume:
            try:
                volume_percent = max(0, min(100, volume_percent))
                vol = np.interp(volume_percent, [0, 100], 
                               [self.vol_range[0], self.vol_range[1]])
                self.volume.SetMasterVolumeLevel(vol, None)
            except Exception as e:
                print(f"Volume error: {e}")
    
    def create_ui(self):
        """Create the integrated UI with all elements"""
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#16213e", height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🖐️ Hand Gesture Volume Control",
            font=("Arial", 24, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#1a1a2e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Camera feed
        left_frame = tk.Frame(content_frame, bg="#16213e", width=640)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        camera_label = tk.Label(
            left_frame,
            text="📹 Camera Feed",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="white"
        )
        camera_label.pack(pady=10)
        
        self.video_label = tk.Label(left_frame, bg="black")
        self.video_label.pack(padx=10, pady=10)
        
        # Right side - Controls and info
        right_frame = tk.Frame(content_frame, bg="#16213e", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Volume display
        volume_label = tk.Label(
            right_frame,
            text="🔊 Volume Control",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="white"
        )
        volume_label.pack(pady=20)
        
        # Volume percentage
        self.volume_text = tk.Label(
            right_frame,
            text="50%",
            font=("Arial", 48, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        self.volume_text.pack(pady=10)
        
        # Volume bar
        volume_bar_frame = tk.Frame(right_frame, bg="#16213e")
        volume_bar_frame.pack(pady=20)
        
        self.volume_bar = ttk.Progressbar(
            volume_bar_frame,
            orient=tk.VERTICAL,
            length=200,
            mode='determinate',
            maximum=100
        )
        self.volume_bar.pack()
        self.volume_bar['value'] = 50
        
        # Status info
        status_frame = tk.Frame(right_frame, bg="#0f3460", relief=tk.RAISED, bd=2)
        status_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(
            status_frame,
            text="Status",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="white"
        ).pack(pady=10)
        
        self.status_text = tk.Label(
            status_frame,
            text="● Initializing...",
            font=("Arial", 10),
            bg="#0f3460",
            fg="#ffff00"
        )
        self.status_text.pack(pady=5)
        
        self.distance_text = tk.Label(
            status_frame,
            text="Distance: 0 px",
            font=("Arial", 10),
            bg="#0f3460",
            fg="white"
        )
        self.distance_text.pack(pady=5)
        
        # Instructions
        instructions_frame = tk.Frame(right_frame, bg="#0f3460", relief=tk.RAISED, bd=2)
        instructions_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            instructions_frame,
            text="How to Use",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="white"
        ).pack(pady=10)
        
        instructions = [
            "1. Show your hand to camera",
            "2. Palm facing forward",
            "3. Pinch fingers = Lower volume",
            "4. Spread fingers = Higher volume"
        ]
        
        for instruction in instructions:
            tk.Label(
                instructions_frame,
                text=instruction,
                font=("Arial", 9),
                bg="#0f3460",
                fg="#cccccc",
                anchor="w"
            ).pack(pady=2, padx=10, anchor="w")
    
    def process_camera(self):
        """Process camera feed and hand tracking"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while self.running:
            success, frame = cap.read()
            if not success:
                continue
            
            # Flip for mirror view
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            self.hand_detected = False
            
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get finger positions
                    h, w, c = frame.shape
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]
                    
                    thumb_x = int(thumb_tip.x * w)
                    thumb_y = int(thumb_tip.y * h)
                    index_x = int(index_tip.x * w)
                    index_y = int(index_tip.y * h)
                    
                    # Calculate distance
                    distance = math.sqrt((index_x - thumb_x)**2 + 
                                       (index_y - thumb_y)**2)
                    
                    # Map to volume
                    volume = np.interp(distance, [30, 200], [0, 100])
                    volume = int(volume)
                    
                    # Update volume if changed significantly
                    if abs(volume - self.current_volume) > 3:
                        self.current_volume = volume
                        self.set_system_volume(volume)
                    
                    self.current_distance = distance
                    self.hand_detected = True
                    
                    # Draw visualization
                    cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), 
                            (255, 0, 255), 3)
                    cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 255), -1)
                    cv2.circle(frame, (index_x, index_y), 10, (255, 0, 255), -1)
                    
                    mid_x = (thumb_x + index_x) // 2
                    mid_y = (thumb_y + index_y) // 2
                    cv2.putText(frame, f'{int(distance)}px', (mid_x, mid_y - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            
            # Add instructions overlay
            cv2.putText(frame, 'Pinch to Control Volume', (20, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Convert for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((620, 465), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update video label
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
            # Update UI elements
            self.update_ui()
        
        cap.release()
    
    def update_ui(self):
        """Update UI elements with current values"""
        try:
            # Update volume text
            self.volume_text.configure(text=f"{self.current_volume}%")
            
            # Update volume bar
            self.volume_bar['value'] = self.current_volume
            
            # Update status
            if self.hand_detected:
                self.status_text.configure(
                    text="● Hand Detected",
                    fg="#00ff00"
                )
            else:
                self.status_text.configure(
                    text="● Waiting for hand...",
                    fg="#ffff00"
                )
            
            # Update distance
            self.distance_text.configure(
                text=f"Distance: {int(self.current_distance)} px"
            )
        except:
            pass
    
    def on_closing(self):
        """Handle window closing"""
        print("Closing application...")
        self.running = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        print("🚀 Starting Hand Gesture Volume Control")
        print("=" * 50)
        self.root.mainloop()

if __name__ == "__main__":
    app = GestureVolumeApp()
    app.run()