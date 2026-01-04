# -*- coding: utf-8 -*-
"""
PNG to High-Resolution Smoothed Black & White Converter
Spline-like edge smoothing for minimal jaggies
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps
import os


# ---------------- Load PNG Image ----------------
def load_png_image():
    filename = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=[("PNG Images", ("*.png",))]
    )
    if not filename:
        return None, None

    img = Image.open(filename).convert("L")  # grayscale
    return img, filename


# ---------------- High-Resolution Smooth + Threshold ----------------
def smooth_black_white(img, threshold=140, upscale_factor=4):
    """
    Upscale image, smooth edges with Gaussian blur, 
    then threshold to produce clean black & white.
    """

    w, h = img.size

    # --- Upscale to higher resolution for smoother edges ---
    high_res = img.resize((w * upscale_factor, h * upscale_factor), Image.LANCZOS)

    # --- Remove speckle noise ---
    high_res = high_res.filter(ImageFilter.MedianFilter(size=3))

    # --- Slight Gaussian blur to smooth edges (spline-like) ---
    high_res = high_res.filter(ImageFilter.GaussianBlur(radius=1.5))

    # --- Optional: enhance edges ---
    #high_res = high_res.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # --- Threshold to black & white ---
    bw = high_res.point(lambda x: 255 if x > threshold else 0, mode="L")

    # --- Downscale back to original size with LANCZOS for smoothness ---
    bw_final = bw.resize((w, h), Image.LANCZOS)

    # --- Optional: slight smoothing of final image ---
    bw_final = bw_final.filter(ImageFilter.SMOOTH_MORE)

    return bw_final


# ---------------- Save Image ----------------
def save_bw_image(bw_img, original_path):
    default_name = (
        os.path.splitext(os.path.basename(original_path))[0]
        + "_bw_smooth_highres.png"
    )

    save_path = filedialog.asksaveasfilename(
        title="Save Smoothed Black & White Image",
        defaultextension=".png",
        initialfile=default_name,
        filetypes=[("PNG Images", ("*.png",))]
    )

    if not save_path:
        messagebox.showinfo("Cancelled", "File not saved.")
        return

    bw_img.save(save_path)
    messagebox.showinfo("Success", f"Image saved to:\n{save_path}")


# ---------------- Convert Workflow ----------------
def convert_to_black_and_white():
    img, path = load_png_image()

    if img is None:
        messagebox.showinfo("Cancelled", "No image selected.")
        return

    bw_img = smooth_black_white(img)

    show_preview(img, bw_img)
    save_bw_image(bw_img, path)


# ---------------- Preview Window ----------------
def show_preview(original, bw):
    preview = tk.Toplevel()
    preview.title("Preview")

    original_preview = original.copy()
    bw_preview = bw.copy()

    original_preview.thumbnail((300, 300))
    bw_preview.thumbnail((300, 300))

    tk_original = ImageTk.PhotoImage(original_preview)
    tk_bw = ImageTk.PhotoImage(bw_preview)

    tk.Label(preview, text="Original PNG").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(preview, text="Smoothed Black & White PNG").grid(row=0, column=1, padx=10, pady=5)

    tk.Label(preview, image=tk_original).grid(row=1, column=0, padx=10)
    tk.Label(preview, image=tk_bw).grid(row=1, column=1, padx=10)

    preview.tk_original = tk_original
    preview.tk_bw = tk_bw


# ---------------- Main GUI ----------------
class BWConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("High-Res PNG → Smoothed Black & White Converter")
        self.geometry("460x260")
        self.resizable(False, False)

        tk.Label(
            self,
            text="High-Resolution Smoothed B&W",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            self,
            text="Spline-like smoothing with minimal jaggies",
            font=("Arial", 11),
            fg="gray",
            wraplength=400,
            justify="center"
        ).pack(pady=5)

        tk.Button(
            self,
            text="Load PNG Image",
            font=("Arial", 14),
            width=25,
            command=convert_to_black_and_white
        ).pack(pady=30)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app = BWConverterGUI()
    app.mainloop()
