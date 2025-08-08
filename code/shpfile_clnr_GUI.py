import geopandas as gpd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def clean_shapefile(input_path, output_path, target_crs=None):
    try:
        print(f"Loading {input_path}...")
        gdf = gpd.read_file(input_path)

        # Remove empty or null geometries
        gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()]

        # Fix invalid geometries
        gdf["geometry"] = gdf["geometry"].buffer(0)

        # Remove duplicates
        gdf = gdf.drop_duplicates(subset="geometry")

        # Optional reprojection
        if target_crs:
            print(f"Reprojecting to {target_crs}...")
            gdf = gdf.to_crs(target_crs)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gdf.to_file(output_path)
        print(f"Cleaned shapefile saved to {output_path}")
        messagebox.showinfo("Success", f"Cleaned shapefile saved:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Select Shapefile",
        filetypes=[("Shapefiles", "*.shp")]
    )
    if file_path:
        input_var.set(file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Cleaned Shapefile",
        defaultextension=".shp",
        filetypes=[("Shapefiles", "*.shp")]
    )
    if file_path:
        output_var.set(file_path)

def run_cleaning():
    input_path = input_var.get()
    output_path = output_var.get()
    target_crs = crs_var.get().strip() or None

    if not input_path or not output_path:
        messagebox.showwarning("Missing Information", "Please select input and output files.")
        return

    clean_shapefile(input_path, output_path, target_crs)

def drop(event):
    # Extract file path from drop event
    file_path = event.data.strip("{}")  # Remove curly braces from Windows paths
    if file_path.lower().endswith(".shp"):
        input_var.set(file_path)
    else:
        messagebox.showerror("Invalid File", "Please drop a .shp file.")

# --- GUI Setup ---
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    root = TkinterDnD.Tk()
except ImportError:
    messagebox.showerror("Missing Package",
                         "Please install tkinterdnd2 to enable drag-and-drop:\n\npip install tkinterdnd2")
    raise SystemExit

root.title("Shapefile Cleaner (Drag & Drop)")
root.geometry("500x250")
root.resizable(False, False)

input_var = tk.StringVar()
output_var = tk.StringVar()
crs_var = tk.StringVar()

# Input field with drag-and-drop
tk.Label(root, text="Input Shapefile (drag .shp here):").pack(anchor="w", padx=10, pady=(10, 0))
input_entry = tk.Entry(root, textvariable=input_var, width=50)
input_entry.pack(side="left", padx=10)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind("<<Drop>>", drop)
tk.Button(root, text="Browse", command=select_input_file).pack(side="left", padx=5)

# Output file
tk.Label(root, text="Output Shapefile:").pack(anchor="w", padx=10, pady=(10, 0))
tk.Entry(root, textvariable=output_var, width=50).pack(side="left", padx=10)
tk.Button(root, text="Save As", command=select_output_file).pack(side="left", padx=5)

# CRS input
tk.Label(root, text="Target CRS (EPSG code, optional):").pack(anchor="w", padx=10, pady=(10, 0))
tk.Entry(root, textvariable=crs_var, width=20).pack(anchor="w", padx=10)

# Clean button
tk.Button(root, text="Clean Shapefile", command=run_cleaning,
          bg="#4CAF50", fg="white", height=2).pack(pady=20)

root.mainloop()
