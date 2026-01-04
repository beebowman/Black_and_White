# -*- coding: utf-8 -*-
"""
PNG to Smoothed Black & White Converter
Inspired by Pygear GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import os


# ---------------- Load PNG Image ----------------
def load_png_image():
    filename = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=[("PNG Images", ("*.png",))]  # PNG only
    )
    if not filename:
        return None, None

    img = Image.open(filename).convert("L")  # grayscale
    return img, filename


# ---------------- Smooth + Threshold ----------------
def smooth_black_white(img, threshold=128):
    """
    Smooths edges while preserving a true black & white output
    """

    # Remove speckle noise
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Slight blur to soften jagged edges
    img = img.filter(ImageFilter.GaussianBlur(radius=1))

    # Re-apply threshold to return to pure black & white
    bw_img = img.point(lambda x: 255 if x > threshold else 0, "1")

    return bw_img


# ---------------- Save Image ----------------
def save_bw_image(bw_img, original_path):
    default_name = (
        os.path.splitext(os.path.basename(original_path))[0]
        + "_black_white_smooth.png"
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

    original.thumbnail((300, 300))
    bw.thumbnail((300, 300))

    tk_original = ImageTk.PhotoImage(original)
    tk_bw = ImageTk.PhotoImage(bw)

    tk.Label(preview, text="Original PNG").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(preview, text="Smoothed Black & White PNG").grid(row=0, column=1, padx=10, pady=5)

    tk.Label(preview, image=tk_original).grid(row=1, column=0, padx=10)
    tk.Label(preview, image=tk_bw).grid(row=1, column=1, padx=10)

    # Keep references
    preview.tk_original = tk_original
    preview.tk_bw = tk_bw


# ---------------- Main GUI ----------------
class BWConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PNG → Smoothed Black & White Converter")
        self.geometry("420x240")
        self.resizable(False, False)

        tk.Label(
            self,
            text="PNG to Smoothed Black & White",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            self,
            text="Loads a PNG, smooths edges, and exports a clean black & white image",
            font=("Arial", 11),
            fg="gray",
            wraplength=380,
            justify="center"
        ).pack(pady=5)

        tk.Button(
            self,
            text="Load PNG Image",
            font=("Arial", 14),
            width=22,
            command=convert_to_black_and_white
        ).pack(pady=30)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app = BWConverterGUI()
    app.mainloop()
