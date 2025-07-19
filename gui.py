"""
Copyright 2025 github.com/A-Temur, Abdullah Temur. All rights reserved.
"""

import os
import webbrowser
from tkinter import filedialog

import customtkinter
import json
import importlib

from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.conf_module = importlib.import_module("schema")

        self.title("MetaBooster")
        # Increased height to make space for the logo
        self.geometry("757x474")

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(1, weight=1)
        # # Configure column 0 to have equal weight for centering the logo
        # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.GITHUB_URL = "https://github.com/A-Temur"
        self.KOFI_URL = "https://ko-fi.com/your-username"

        # --- 2. Load and Add Logo ---
        try:
            gh_image_data = Image.open("media/github-mark-white.png")
            gh_image = customtkinter.CTkImage(gh_image_data, gh_image_data, (50, 50))

            gh_label = customtkinter.CTkLabel(self, image=gh_image, text="")
            gh_label.grid(row=0, column=0, pady=(20, 10), sticky="e")

            # Make the label clickable
            gh_label.bind("<Button-1>", lambda e: self.open_link(self.GITHUB_URL))
            # Change cursor to a hand when hovering over the icon
            gh_label.configure(cursor="hand2")

            # Open the image using Pillow
            logo_image_data = Image.open("media/PyPortableLogo.png")
            # Create a CTkImage object
            logo_image = customtkinter.CTkImage(
                dark_image=logo_image_data,
                light_image=logo_image_data,
                size=(112, 112)  # Adjust size as needed
            )
            # Create a label to display the image. 
            # columnspan=3 makes it span all columns, allowing it to be centered.
            logo_label = customtkinter.CTkLabel(self, image=logo_image, text="")
            logo_label.grid(row=0, column=1, pady=(20, 10))

            kofi_image_data = Image.open("media/support_me_on_kofi_badge_blue.png")
            kofi_image = customtkinter.CTkImage(kofi_image_data, kofi_image_data, (80, 50))

            kofi_label = customtkinter.CTkLabel(self, image=kofi_image, text="")
            kofi_label.grid(row=0, column=2, pady=(20, 10), sticky="w")

            # Make the label clickable
            kofi_label.bind("<Button-1>", lambda e: self.open_link(self.KOFI_URL))
            # Change cursor to a hand when hovering over the icon
            kofi_label.configure(cursor="hand2")


        except FileNotFoundError:
            # Fallback if logo.png is not found
            logo_label = customtkinter.CTkLabel(self, text="My Application", font=("Arial", 24))
            logo_label.grid(row=0, column=1, olumnspan=3, pady=(20, 10))


        # 3. Select your Projects directory:
        self.dir1_label = customtkinter.CTkLabel(self, text="Select the Target directory:")
        self.dir1_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="w")
        # ... (rest of the widgets)
        self.target_dir = customtkinter.CTkEntry(self, placeholder_text="Select directory...")
        self.target_dir.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.dir1_button = customtkinter.CTkButton(self, text="Browse...", command=lambda: self.select_dir(self.target_dir))
        self.dir1_button.grid(row=1, column=2, padx=10, pady=(10, 5))

        # 4. Select output directory location
        self.dir2_label = customtkinter.CTkLabel(self, text="Select output directory location:")
        self.dir2_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.out_dir = customtkinter.CTkEntry(self,
                                              placeholder_text="Select the location of the resulting PyPortable output...")
        self.out_dir.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.dir2_button = customtkinter.CTkButton(self, text="Browse...", command=lambda: self.select_dir(self.out_dir))
        self.dir2_button.grid(row=2, column=2, padx=10, pady=5)

        # String Inputs
        # Author
        self.author_label = customtkinter.CTkLabel(self, text="Author:")
        self.author_label.grid(row=3, column=0, padx=10, pady=(20, 5), sticky="w")
        self.author_entry = customtkinter.CTkEntry(self, placeholder_text="Enter author name")
        self.author_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=(20, 5), sticky="ew")

        # Copyright
        self.copyright_label = customtkinter.CTkLabel(self, text="Copyright:")
        self.copyright_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.copyright_entry = customtkinter.CTkEntry(self, placeholder_text="e.g. Copyright 2025 OG-Brain.com, Abdullah Temur. All rights reserved.")
        self.copyright_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Media Description
        self.media_desc_label = customtkinter.CTkLabel(self, text="Default Media Description:")
        self.media_desc_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.media_desc_entry = customtkinter.CTkEntry(self, placeholder_text="e.g. Media for OG-Brain.com")
        self.media_desc_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Media Title Prefix
        self.title_prefix_label = customtkinter.CTkLabel(self, text="Media Title Prefix:")
        self.title_prefix_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.title_prefix_entry = customtkinter.CTkEntry(self, placeholder_text="Enter media title prefix")
        self.title_prefix_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Directory Title Prefix
        self.dir_prefix_label = customtkinter.CTkLabel(self, text="Directory Title Prefix:")
        self.dir_prefix_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.dir_prefix_entry = customtkinter.CTkEntry(self, placeholder_text="Enter directory title prefix")
        self.dir_prefix_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # HTML File for JSON-LD
        self.jsonld_html_label = customtkinter.CTkLabel(self, text="HTML File for JSON-LD:")
        self.jsonld_html_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.jsonld_html_entry = customtkinter.CTkEntry(self,
                                                        placeholder_text="Enter HTML filename (leave empty if not needed)")
        self.jsonld_html_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # JSON-LD Filename
        self.jsonld_edit_button = customtkinter.CTkButton(self, text="Edit JSON-LD", command=self.open_jsonld_editor)
        self.jsonld_edit_button.grid(row=9, column=2, padx=10, pady=5)

        # Website URL
        self.website_label = customtkinter.CTkLabel(self, text="Website URL:")
        self.website_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.website_entry = customtkinter.CTkEntry(self, placeholder_text="Enter website URL")
        self.website_entry.grid(row=10, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        

        # Submit Button
        self.submit_button = customtkinter.CTkButton(self, text="Create PyPortable Application", command=self.submit)
        self.submit_button.grid(row=11, column=1, columnspan=2, padx=10, pady=(20, 10), sticky="e")

    def select_dir(self, target_entry_widget):
        path = filedialog.askdirectory()
        if path:
            target_entry_widget.delete(0, "end")
            target_entry_widget.insert(0, path)

    def submit(self):
        print("Submit button clicked")


    def get_conf(self, key_:str) -> str:
        # get schema variable via str
        schema_var = getattr(self.conf_module, key_)

        # get default schema conf
        conf = json.dumps(schema_var, indent=4)

        # get custom conf instead if it exists
        if os.path.exists("conf_overwrite/custom_conf.json"):
            with open("conf_overwrite/custom_conf.json", "r", encoding="utf-8") as f:
                try:
                    custom_conf = json.load(f)
                except json.JSONDecodeError:
                    print("Invalid JSON format")
                # check whether the key exists in custom_conf
                if key_ in custom_conf:
                    conf = json.dumps(custom_conf["json_ld"], indent=4)

        return conf


    def write_conf(self, key_:str, value_:dict):
        # read custom_conf
        with open("conf_overwrite/custom_conf.json", "r", encoding="utf-8") as f:
            custom_conf = json.load(f)
        custom_conf[key_] = value_
        # write to custom_conf
        with open("conf_overwrite/custom_conf.json", "w", encoding="utf-8") as f:
            json.dump(custom_conf, f, indent=4)


    def open_jsonld_editor(self):
        editor_window = customtkinter.CTkToplevel(self)
        editor_window.title("JSON-LD Editor")
        editor_window.geometry("600x400")
        editor_window.focus_force()

        # Create text widget for editing
        text_widget = customtkinter.CTkTextbox(editor_window)
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        insert_text = self.get_conf("json_ld")

        text_widget.insert("1.0", insert_text)

        # Create save button
        def save_changes():
            try:
                # Get content from text widget
                new_json = json.loads(text_widget.get("1.0", "end"))

                self.write_conf("json_ld", new_json)

                editor_window.destroy()

            except json.JSONDecodeError:
                print("Invalid JSON format")
            except IOError as e:
                print(f"Error handling files: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        save_button = customtkinter.CTkButton(editor_window, text="Save", command=save_changes)
        save_button.pack(pady=10)

        def cancel_button_clicked():
            editor_window.destroy()

        cancel_button = customtkinter.CTkButton(editor_window, text="Cancel", command=cancel_button_clicked)
        cancel_button.pack(pady=10)
        
        
    # --- 4. Add a method to open links ---
    def open_link(self, url):
        """Opens the given URL in a new browser tab."""
        webbrowser.open_new_tab(url)
        print(f"Opening {url}...")


if __name__ == '__main__':
    app = App()
    app.mainloop()
