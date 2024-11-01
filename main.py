import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk

# Database setup
conn = sqlite3.connect('job_applications.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    company_name TEXT,
    position TEXT,
    country TEXT,
    city TEXT,
    date_applied TEXT,
    status TEXT CHECK(status IN ('applied', 'rejected', 'invited to interview')) DEFAULT 'applied',
    interview_date TEXT,
    notes TEXT,
    job_description TEXT
)
''')
conn.commit()

# Theme configuration
light_theme = {
    "bg": "white", "fg": "black", "button_bg": "#0078d4", "button_fg": "white",
    "entry_bg": "#f3f4f6", "tree_bg": "white", "tree_fg": "black",
    "header_bg": "#f3f4f6", "header_fg": "black", "icon_bg": "white"
}
dark_theme = {
    "bg": "#2e2e2e", "fg": "white", "button_bg": "#444444", "button_fg": "white",
    "entry_bg": "#3e3e3e", "tree_bg": "#2e2e2e", "tree_fg": "black",
    "header_bg": "#444444", "header_fg": "white", "icon_bg": "#2e2e2e"
}
current_theme, current_icon = light_theme, "icons/light_icon.png"

def toggle_theme():
    global current_theme, current_icon
    current_theme, current_icon = (dark_theme, "icons/dark_icon.png") if current_theme == light_theme else (light_theme, "icons/light_icon.png")
    apply_theme()

def apply_theme():
    root.configure(bg=current_theme["bg"])
    left_btn_frame.configure(bg=current_theme["bg"])
    right_btn_frame.configure(bg=current_theme["bg"])
    add_button.configure(bg=current_theme["icon_bg"], activebackground=current_theme["icon_bg"])
    delete_button.configure(bg=current_theme["icon_bg"], activebackground=current_theme["icon_bg"])
    toggle_icon_button.configure(bg=current_theme["icon_bg"], activebackground=current_theme["icon_bg"])

    theme_icon = Image.open(current_icon).convert("RGBA").resize((24, 24), Image.ANTIALIAS)
    theme_icon = ImageTk.PhotoImage(theme_icon)
    toggle_icon_button.config(image=theme_icon)
    toggle_icon_button.image = theme_icon

    style.theme_use("clam" if current_theme == dark_theme else "default")
    style.configure("Treeview", background=current_theme["tree_bg"], foreground=current_theme["tree_fg"],
                    fieldbackground=current_theme["tree_bg"], highlightthickness=0)
    style.configure("Treeview.Heading", background=current_theme["header_bg"], foreground=current_theme["header_fg"], font=("Segoe UI", 11, "bold"))
    refresh_table()

def load_applications():
    cursor.execute('SELECT * FROM applications')
    return cursor.fetchall()

def add_application(company_name, position, country, city, notes="", job_description=""):
    try:
        date_applied = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO applications (company_name, position, country, city, date_applied, status, notes, job_description)
            VALUES (?, ?, ?, ?, ?, 'applied', ?, ?)
        ''', (company_name, position, country, city, date_applied, notes or "", job_description or ""))
        conn.commit()
        return True
    except Exception as e:
        print("Error adding application:", e)
        return False

def delete_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("No selection", "Please select an application to delete.")
        return
    if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected application(s)?"):
        for item in selected_items:
            app_id = tree.item(item)["values"][0]
            cursor.execute('DELETE FROM applications WHERE id = ?', (app_id,))
        conn.commit()
        refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for app in load_applications():
        status_color = {"applied": "#FFD700", "rejected": "#FF6347", "invited to interview": "#90EE90"}.get(app[6], "white")
        tree.insert("", "end", values=app, tags=(app[6],))
        tree.tag_configure(app[6], background=status_color)
    adjust_column_widths()

def adjust_column_widths():
    if not tree.get_children():
        return
    for col in tree["columns"]:
        widths = [tree.bbox(item, column=col)[2] for item in tree.get_children() if tree.bbox(item, column=col)]
        if widths:
            tree.column(col, width=max(widths))

def new_application_popup():
    popup = tk.Toplevel(root)
    popup.title("New Application")
    popup.geometry("400x400")
    popup.configure(bg=current_theme["bg"])

    fields = ["Company Name", "Position", "Country", "City", "Application Date", "Notes", "Job Description"]
    entries = {}
    for i, field in enumerate(fields):
        tk.Label(popup, text=field, bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", padx=10, pady=(10, 5))
        entry = tk.Text(popup, width=30, height=5, bg=current_theme["entry_bg"], fg=current_theme["fg"], bd=0, relief="solid") if field == "Job Description" else tk.Entry(popup, bg=current_theme["entry_bg"], fg=current_theme["fg"], bd=0, relief="solid", font=("Segoe UI", 10))
        if field == "Application Date":
            entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
            entry.config(state="disabled")
        entry.grid(row=i, column=1, pady=(10, 5), padx=10)
        entries[field] = entry

    def submit():
        company_name = entries["Company Name"].get()
        position = entries["Position"].get()
        country = entries["Country"].get()
        city = entries["City"].get()
        notes = entries["Notes"].get("1.0", "end-1c").strip() if isinstance(entries["Notes"], tk.Text) else ""
        job_description = entries["Job Description"].get("1.0", "end-1c").strip() if isinstance(entries["Job Description"], tk.Text) else ""
        
        if add_application(company_name, position, country, city, notes, job_description):
            popup.destroy()
            refresh_table()
        else:
            messagebox.showerror("Error", "Failed to add application.")


    tk.Button(popup, text="Add Application", command=submit, bg=current_theme["button_bg"], fg=current_theme["button_fg"], font=("Segoe UI", 10), bd=0, relief="flat", cursor="hand2").grid(row=len(fields), column=0, columnspan=2, pady=20)

def show_job_details(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    app_id = tree.item(selected_item)["values"][0]
    cursor.execute('SELECT * FROM applications WHERE id = ?', (app_id,))
    job = cursor.fetchone()
    if not job:
        messagebox.showerror("Error", "Could not retrieve job details.")
        return

    details_popup = tk.Toplevel(root)
    details_popup.title("Job Details")
    details_popup.geometry("400x550")
    details_popup.configure(bg=current_theme["bg"])
    fields = ["Company Name", "Position", "Country", "City", "Date Applied", "Status", "Notes"]
    for i, field in enumerate(fields):
        tk.Label(details_popup, text=f"{field}:", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=(10, 5))
        tk.Label(details_popup, text=job[i + 1] or "N/A", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10)).grid(row=i, column=1, sticky="w", padx=10, pady=(10, 5))

    tk.Label(details_popup, text="Job Description:", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10, "bold")).grid(row=len(fields), column=0, sticky="nw", padx=10, pady=(10, 5))
    description_text = tk.Text(details_popup, width=40, height=6, wrap="word", font=("Segoe UI", 10), bg=current_theme["entry_bg"], fg=current_theme["fg"], bd=0)
    description_text.insert("1.0", job[9] or "N/A")
    description_text.config(state="disabled")
    description_text.grid(row=len(fields), column=1, sticky="w", padx=10, pady=(10, 5))

    status_combobox = ttk.Combobox(details_popup, values=["applied", "rejected", "invited to interview"], font=("Segoe UI", 10))
    status_combobox.set(job[6])
    status_combobox.grid(row=9, column=1, sticky="w", padx=10, pady=(10, 5))

    tk.Label(details_popup, text="Change Status:", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10)).grid(row=9, column=0, sticky="w", padx=10, pady=(10, 5))
    interview_date_entry = tk.Entry(details_popup, bg=current_theme["entry_bg"], fg=current_theme["fg"], bd=0, relief="solid", font=("Segoe UI", 10))
    if job[6] == "invited to interview":
        interview_date_entry.insert(0, job[7])
        interview_date_entry.grid(row=10, column=1, padx=10, pady=(10, 5))
    interview_date_label = tk.Label(details_popup, text="Interview Date:", bg=current_theme["bg"], fg=current_theme["fg"], font=("Segoe UI", 10))
    interview_date_label.grid(row=10, column=0, sticky="w", padx=10, pady=(10, 5))

    def update_status():
        new_status = status_combobox.get()
        interview_date = interview_date_entry.get() if new_status == "invited to interview" else None
        try:
            cursor.execute('UPDATE applications SET status = ?, interview_date = ? WHERE id = ?', (new_status, interview_date, app_id))
            conn.commit()
            refresh_table()
            details_popup.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Database Error", "Status value is invalid.")

    tk.Button(details_popup, text="Update Status", command=update_status, bg=current_theme["button_bg"], fg=current_theme["button_fg"], font=("Segoe UI", 10), bd=0, relief="flat", cursor="hand2").grid(row=11, column=0, columnspan=2, pady=20)

# GUI setup
root = tk.Tk()
root.title("Job Application Tracker")
root.geometry("800x600")

style = ttk.Style()
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

tree = ttk.Treeview(root, columns=("ID", "Company", "Position", "Country", "City", "Date Applied", "Status", "Notes"), show="headings")
for col in ["ID", "Company", "Position", "Country", "City", "Date Applied", "Status", "Notes"]:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=20, pady=20)
refresh_table()
tree.bind("<Double-1>", show_job_details)

left_btn_frame = tk.Frame(root, bg=current_theme["bg"])
right_btn_frame = tk.Frame(root, bg=current_theme["bg"])

delete_icon = ImageTk.PhotoImage(Image.open("icons/Delete.png").resize((24, 24), Image.ANTIALIAS))
new_icon = ImageTk.PhotoImage(Image.open("icons/New.png").resize((24, 24), Image.ANTIALIAS))
add_button = tk.Button(left_btn_frame, image=new_icon, command=new_application_popup, bg=current_theme["icon_bg"], bd=0, relief="flat", cursor="hand2")
delete_button = tk.Button(left_btn_frame, image=delete_icon, command=delete_selected, bg=current_theme["icon_bg"], bd=0, relief="flat", cursor="hand2")
add_button.image, delete_button.image = new_icon, delete_icon
add_button.pack(side="left", padx=5, pady=10)
delete_button.pack(side="left", padx=5, pady=10)

theme_icon = ImageTk.PhotoImage(Image.open(current_icon).resize((24, 24), Image.ANTIALIAS))
toggle_icon_button = tk.Button(right_btn_frame, image=theme_icon, command=toggle_theme, bg=current_theme["icon_bg"], bd=0, relief="flat", cursor="hand2")
toggle_icon_button.image = theme_icon
toggle_icon_button.pack(side="right", padx=5, pady=10)

left_btn_frame.pack(side="left", anchor="w", padx=10, pady=10)
right_btn_frame.pack(side="right", anchor="e", padx=10, pady=10)

apply_theme()
root.mainloop()
