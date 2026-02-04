import tkinter as tk
import customtkinter as ctk 
from PIL import Image, ImageTk
from authtoken import auth_token
import torch
from diffusers import AutoPipelineForText2Image
import threading
from datetime import datetime
import os

# Create the app
app = tk.Tk()
app.geometry("1200x750")
app.title("Image Generation App - By Ayushman Banerjee") 
ctk.set_appearance_mode("dark")
app.configure(bg="#0a0a0a")

# Custom colors for bento grid theme
COLORS = {
    'bg_primary': '#0a0a0a',
    'bg_secondary': '#141414',
    'bg_card': '#1a1a1a',
    'accent_1': '#6366f1',  # Indigo
    'accent_2': '#8b5cf6',  # Purple
    'accent_3': '#ec4899',  # Pink
    'text_primary': '#ffffff',
    'text_secondary': '#a1a1aa',
    'border': '#27272a'
}

# Global variables
current_image = None
is_generating = False

# Initialize the model (using SD-Turbo for speed)
modelid = "stabilityai/sd-turbo"  # Much faster than v1-4
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model with optimizations
print("Loading model...")
pipe = AutoPipelineForText2Image.from_pretrained(
    modelid,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    use_auth_token=auth_token
)
pipe = pipe.to(device)

# Enable memory optimizations
if device == "cuda":
    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

print(f"Model loaded on {device}!")

# Main container frame
main_frame = ctk.CTkFrame(app, fg_color=COLORS['bg_primary'], corner_radius=0)
main_frame.pack(fill="both", expand=True, padx=0, pady=0)

# Header section (bento style)
header_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_secondary'], corner_radius=12, height=100)
header_frame.pack(fill="x", padx=20, pady=20)
header_frame.pack_propagate(False)

# Title with gradient effect (simulated with colors)
title_label = ctk.CTkLabel(
    header_frame, 
    text="✨ Image Generation",
    font=("Arial", 32, "bold"),
    text_color=COLORS['text_primary']
)
title_label.pack(pady=8)

subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Lightning-fast AI image generation",
    font=("Arial", 13),
    text_color=COLORS['text_secondary']
)
subtitle_label.pack()

# Content grid (bento layout)
content_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_primary'])
content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Left column - Controls
controls_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['bg_card'], corner_radius=12, width=380)
controls_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
controls_frame.pack_propagate(False)

# Controls title
controls_title = ctk.CTkLabel(
    controls_frame,
    text="Create Your Image",
    font=("Arial", 22, "bold"),
    text_color=COLORS['text_primary']
)
controls_title.pack(pady=(20, 15), padx=20, anchor="w")

# Prompt input section
prompt_label = ctk.CTkLabel(
    controls_frame,
    text="Describe your image",
    font=("Arial", 11, "bold"),
    text_color=COLORS['text_secondary']
)
prompt_label.pack(pady=(5, 5), padx=20, anchor="w")

prompt = ctk.CTkTextbox(
    controls_frame,
    height=100,
    width=340,
    font=("Arial", 13),
    text_color=COLORS['text_primary'],
    fg_color=COLORS['bg_secondary'],
    border_color=COLORS['border'],
    border_width=2,
    corner_radius=8
)
prompt.pack(padx=20, pady=(0, 12))
prompt.insert("1.0", "A serene landscape with mountains at sunset")

# Generation settings
settings_label = ctk.CTkLabel(
    controls_frame,
    text="⚙️ Generation Settings",
    font=("Arial", 11, "bold"),
    text_color=COLORS['text_secondary']
)
settings_label.pack(pady=(8, 8), padx=20, anchor="w")

# Steps slider (SD-Turbo works well with 1-4 steps)
steps_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
steps_frame.pack(padx=20, pady=3, fill="x")

steps_label = ctk.CTkLabel(steps_frame, text="Steps: 1", font=("Arial", 10), text_color=COLORS['text_secondary'])
steps_label.pack(anchor="w")

steps_slider = ctk.CTkSlider(
    steps_frame,
    from_=1,
    to=4,
    number_of_steps=3,
    button_color=COLORS['accent_1'],
    button_hover_color=COLORS['accent_2'],
    progress_color=COLORS['accent_1'],
    width=340
)
steps_slider.set(1)
steps_slider.pack(fill="x", pady=3)

def update_steps_label(value):
    steps_label.configure(text=f"Steps: {int(value)}")
    
steps_slider.configure(command=update_steps_label)

# Guidance scale slider
guidance_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
guidance_frame.pack(padx=20, pady=3, fill="x")

guidance_label = ctk.CTkLabel(guidance_frame, text="Guidance: 0.0", font=("Arial", 10), text_color=COLORS['text_secondary'])
guidance_label.pack(anchor="w")

guidance_slider = ctk.CTkSlider(
    guidance_frame,
    from_=0,
    to=2,
    button_color=COLORS['accent_2'],
    button_hover_color=COLORS['accent_3'],
    progress_color=COLORS['accent_2'],
    width=340
)
guidance_slider.set(0.0)
guidance_slider.pack(fill="x", pady=3)

def update_guidance_label(value):
    guidance_label.configure(text=f"Guidance: {value:.1f}")
    
guidance_slider.configure(command=update_guidance_label)

# Generate button - MOVED UP FOR VISIBILITY
def generate():
    global current_image, is_generating
    
    if is_generating:
        return
    
    is_generating = True
    trigger.configure(state="disabled", text="⏳ Generating...", fg_color=COLORS['text_secondary'])
    status_label.configure(text="🎨 Creating your masterpiece...")
    progress_bar.set(0)
    
    def generate_thread():
        global current_image, is_generating
        try:
            prompt_text = prompt.get("1.0", "end-1c").strip()
            if not prompt_text:
                prompt_text = "A beautiful landscape"
            
            # Update progress
            app.after(0, lambda: progress_bar.set(0.3))
            
            # Generate image with optimized settings for SD-Turbo
            num_steps = int(steps_slider.get())
            guidance_value = guidance_slider.get()
            
            # SD-Turbo works best with low steps and guidance
            image = pipe(
                prompt=prompt_text,
                num_inference_steps=num_steps,
                guidance_scale=guidance_value
            ).images[0]
            
            app.after(0, lambda: progress_bar.set(0.7))
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'generated_{timestamp}.png'
            image.save(filename)
            current_image = image
            
            app.after(0, lambda: progress_bar.set(1.0))
            
            # Display image
            display_img = image.resize((512, 512), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(display_img)
            lmain.configure(image=img_tk, text="")
            lmain.image = img_tk  # Keep a reference
            
            # Update status
            app.after(0, lambda: status_label.configure(text=f"✨ Generated! Saved as {filename}"))
            
        except Exception as e:
            app.after(0, lambda: status_label.configure(text=f"❌ Error: {str(e)}"))
            print(f"Error generating image: {e}")
        finally:
            is_generating = False
            app.after(0, lambda: trigger.configure(
                state="normal",
                text="🚀 Generate Image",
                fg_color=COLORS['accent_1']
            ))
            app.after(0, lambda: progress_bar.set(0))
    
    # Start generation in separate thread
    thread = threading.Thread(target=generate_thread, daemon=True)
    thread.start()

# BIG PROMINENT GENERATE BUTTON
trigger = ctk.CTkButton(
    controls_frame,
    height=55,
    width=340,
    text="🚀 Generate Image",
    font=("Arial", 18, "bold"),
    text_color=COLORS['text_primary'],
    fg_color=COLORS['accent_1'],
    hover_color=COLORS['accent_2'],
    corner_radius=12,
    command=generate,
    border_width=2,
    border_color=COLORS['accent_2']
)
trigger.pack(padx=20, pady=15)

# Progress bar
progress_bar = ctk.CTkProgressBar(
    controls_frame,
    width=340,
    height=6,
    progress_color=COLORS['accent_1'],
    fg_color=COLORS['bg_secondary'],
    corner_radius=3
)
progress_bar.pack(padx=20, pady=(0, 8))
progress_bar.set(0)

# Status label
status_label = ctk.CTkLabel(
    controls_frame,
    text="✨ Ready to generate amazing images!",
    font=("Arial", 10),
    text_color=COLORS['text_secondary'],
    wraplength=320
)
status_label.pack(pady=(5, 15), padx=20)

# Right column - Image display (larger bento card)
display_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['bg_card'], corner_radius=12)
display_frame.pack(side="right", fill="both", expand=True)

# Display title
display_title = ctk.CTkLabel(
    display_frame,
    text="Your Creation",
    font=("Arial", 22, "bold"),
    text_color=COLORS['text_primary']
)
display_title.pack(pady=(20, 10), padx=20, anchor="w")

# Image container with border
image_container = ctk.CTkFrame(
    display_frame,
    fg_color=COLORS['bg_secondary'],
    corner_radius=10,
    border_width=2,
    border_color=COLORS['border']
)
image_container.pack(padx=20, pady=(10, 15), fill="both", expand=True)

lmain = ctk.CTkLabel(
    image_container,
    text="🎨\n\nYour generated image will appear here\n\nEnter a prompt and click 'Generate Image'",
    font=("Arial", 14),
    text_color=COLORS['text_secondary'],
    fg_color="transparent"
)
lmain.pack(expand=True, fill="both", padx=20, pady=20)

# Save button
save_button = ctk.CTkButton(
    display_frame,
    height=45,
    text="💾 Save Image",
    font=("Arial", 14, "bold"),
    text_color=COLORS['text_primary'],
    fg_color=COLORS['bg_secondary'],
    hover_color=COLORS['border'],
    corner_radius=10,
    border_width=2,
    border_color=COLORS['border'],
    command=lambda: current_image.save(f'saved_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png') if current_image else status_label.configure(text="⚠️ No image to save yet!")
)
save_button.pack(padx=20, pady=(0, 20), fill="x")

# Info footer
info_label = ctk.CTkLabel(
    main_frame,
    text=f"⚡ Running on {device.upper()} • SD-Turbo Model • Ultra-fast generation",
    font=("Arial", 9),
    text_color=COLORS['text_secondary']
)
info_label.pack(pady=(0, 10))

# Start the app
print("\n" + "="*60)
print("🚀 APP STARTED SUCCESSFULLY!")
print("="*60)
print(f"✓ Model: SD-Turbo")
print(f"✓ Device: {device.upper()}")
print(f"✓ Window Size: 1200x750")
print("="*60)
print("\n👉 The GENERATE BUTTON is in the left panel (blue button)")
print("👉 Enter your prompt and click 'Generate Image' to start!")
print("\n")

app.mainloop()