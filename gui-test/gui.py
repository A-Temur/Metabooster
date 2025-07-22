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


class MainWindow(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.conf_module = importlib.import_module("schema")

        self.title("MetaBooster")
        # Increased height to make space for the logo
        self.geometry("800x600")

        # list of supported media files with custom descriptions
        self.supported_files = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".heic", ".pdf"]
        # filtered all files for only custom description supported files
        self.filtered_files = []

        # used for determining whether the target dir has changed
        self.last_target_dir = ""


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
            gh_image_data = Image.open("../media/github-mark-white.png")
            gh_image = customtkinter.CTkImage(gh_image_data, gh_image_data, (50, 50))

            gh_label = customtkinter.CTkLabel(self, image=gh_image, text="")
            gh_label.grid(row=0, column=0, pady=(20, 10), sticky="e")

            # Make the label clickable
            gh_label.bind("<Button-1>", lambda e: self.open_link(self.GITHUB_URL))
            # Change cursor to a hand when hovering over the icon
            gh_label.configure(cursor="hand2")

            # Open the image using Pillow
            logo_image_data = Image.open("../media/PyPortableLogo.png")
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

            kofi_image_data = Image.open("../media/support_me_on_kofi_badge_blue.png")
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

        # Website URL
        self.website_label = customtkinter.CTkLabel(self, text="Website URL:")
        self.website_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.website_entry = customtkinter.CTkEntry(self, placeholder_text="Enter website URL")
        self.website_entry.grid(row=9, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        # JSON-LD Filename
        self.jsonld_edit_button = customtkinter.CTkButton(self, text="Edit JSON-LD", command=self.open_jsonld_editor)
        self.jsonld_edit_button.grid(row=10, column=2, padx=10, pady=5, sticky="e")

        # custom descriptions
        self.custom_desc_button = customtkinter.CTkButton(self, text="Create Custom Descriptions", command=self.create_custom_descriptions)
        self.custom_desc_button.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        # Submit Button
        self.submit_button = customtkinter.CTkButton(self, text="Run Metabooster", command=self.submit)
        self.submit_button.grid(row=10, column=1, padx=10, pady=5, sticky="e")

    def select_dir(self, target_entry_widget):
        path = filedialog.askdirectory()
        if path:
            target_entry_widget.delete(0, "end")
            target_entry_widget.insert(0, path)

    def submit(self):
        # write all entrys into custom conf json
        pass


    def create_popup_dialog(self, title_, text_):
        dialog_ = customtkinter.CTkToplevel(self)
        dialog_.title(title_)
        dialog_.geometry("300x100")

        dialog_label_ = customtkinter.CTkLabel(dialog_, text=text_)
        dialog_label_.pack(pady=20)

        ok_button = customtkinter.CTkButton(dialog_, text="OK", command=dialog_.destroy)
        ok_button.pack()

        dialog_.transient(self)
        dialog_.grab_set()
        self.wait_window(dialog_)

    def create_custom_descriptions(self):
        if not bool(self.target_dir.get()):
            # create popup informing user that he must select target directory first
            self.create_popup_dialog("Error", "You must select a target directory first!")
            return


        def fill_frame():
            if len(self.filtered_files) >= 1:
                for supported_file in self.filtered_files:
                    scrollable_frame_label = customtkinter.CTkLabel(scrollable_frame,
                                                                    text=f"{os.path.basename(supported_file)}")
                    scrollable_frame_label.pack(padx=10, pady=5, anchor="w")
                    scrollable_frame_input = customtkinter.CTkEntry(scrollable_frame, placeholder_text="")
                    scrollable_frame_input.pack(padx=10, pady=5, anchor="w")
                    scrollable_frame.labels.append((scrollable_frame_label, scrollable_frame_input))

                progress_bar.stop()
                progress_window.grab_release()
                progress_window.destroy()

            else:
                progress_bar.stop()
                progress_window.grab_release()
                # make windows invisible
                progress_window.attributes("-alpha", 0)
                new_window.attributes("-alpha", 0)

                self.create_popup_dialog("Error", "No supported files found in target directory")
                progress_window.destroy()
                new_window.grab_release()
                new_window.destroy()

        def fill_files_list():
            # create a list of all files inside the target directory (recursive)
            for root, dirs, files in os.walk(self.target_dir.get()):
                for file in files:
                    if "." + file.split('.')[-1] in self.supported_files:
                        self.filtered_files.append(os.path.join(root, file))


        def save_custom_descriptions():
            lis_item_: tuple[customtkinter.CTkLabel, customtkinter.CTkEntry]

            json_dict_ = {}
            for lis_item_ in scrollable_frame.labels:
                custom_descript = lis_item_[1].get()
                if len(custom_descript) >= 1:
                    filename = lis_item_[0]._text
                    json_dict_[filename] = custom_descript

            if len(json_dict_) >= 1:
                # read custom_conf
                with open("conf_overwrite/custom_conf.json", "r", encoding="utf-8") as f:
                    custom_conf = json.load(f)
                custom_conf["custom_descriptions"] = json_dict_
                # write to custom_conf
                with open("conf_overwrite/custom_conf.json", "w", encoding="utf-8") as f:
                    json.dump(custom_conf, f, indent=4)





        target_dir_changed = True

        # check whether target dir has changed
        if self.target_dir.get() == self.last_target_dir:
            target_dir_changed = False


        # create new window (scrollable)
        new_window = customtkinter.CTkToplevel(self)
        new_window.title("Create Custom Descriptions")
        new_window.geometry("800x600")
        new_window.transient(self)
        new_window.grab_set()

        # add widgets
        scrollable_frame = customtkinter.CTkScrollableFrame(new_window)
        scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)
        scrollable_frame.labels = []

        save_button = customtkinter.CTkButton(new_window, text="Save", command=save_custom_descriptions)
        save_button.pack(pady=10)

        cancel_button = customtkinter.CTkButton(new_window, text="Cancel", command=new_window.destroy)
        cancel_button.pack(pady=10)

        # create progress bar window

        progress_window = customtkinter.CTkToplevel(self)
        progress_window.title("...")
        progress_window.geometry("500x100")
        progress_bar = customtkinter.CTkProgressBar(progress_window, mode="indeterminate", width=300)
        progress_bar.pack(pady=10)
        progress_label = customtkinter.CTkLabel(progress_window, text="Loading files...", font=("Arial", 12))
        progress_label.pack(pady=10)
        progress_bar.start()

        progress_window.transient(self)
        progress_window.grab_set()

        new_window.grab_release()

        if target_dir_changed:
            self.filtered_files = []
            self.last_target_dir = self.target_dir.get()
            progress_label.configure(text="iterating over files...")
            self.after(0, fill_files_list)
            # self.after(0, update_progress, "filling frame...")
            progress_label.configure(text="filling frame...")
            self.after(0, fill_frame)
        else:
            progress_label.configure(text="filling frame...")
            self.after(0, fill_frame)


    def open_jsonld_editor(self):
        def get_conf(key_: str) -> str:
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

        def write_conf(key_: str, value_: dict):
            # read custom_conf
            with open("conf_overwrite/custom_conf.json", "r", encoding="utf-8") as f:
                custom_conf = json.load(f)
            custom_conf[key_] = value_
            # write to custom_conf
            with open("conf_overwrite/custom_conf.json", "w", encoding="utf-8") as f:
                json.dump(custom_conf, f, indent=4)


        def hide_stop_progress_bar(reset_status_=False):
            progress_bar.stop()
            progress_bar.pack_forget()
            if reset_status_:
                text_status.configure(text="Ready")

        def show_start_progress_bar(text_status_):
            progress_bar.pack(pady=10)
            progress_bar.start()
            text_status.configure(text=text_status_)


        editor_window = customtkinter.CTkToplevel(self)
        editor_window.title("JSON-LD Editor")
        editor_window.geometry("600x400")
        editor_window.transient(self)
        editor_window.grab_set()

        progress_bar = customtkinter.CTkProgressBar(editor_window, mode="indeterminate", width=300)
        # make invisible by default
        progress_bar.pack_forget()

        # create text status field
        text_status = customtkinter.CTkLabel(editor_window, text="Ready", font=("Arial", 12))
        text_status.pack(pady=10)

        # Create text widget for editing
        text_widget = customtkinter.CTkTextbox(editor_window)
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        show_start_progress_bar("Retrieving JSON-LD content, please wait...")

        insert_text = get_conf("json_ld")

        text_widget.insert("1.0", insert_text)

        hide_stop_progress_bar(True)

        # Create save button
        def save_changes():
            try:
                show_start_progress_bar("Saving JSON-LD content, please wait...")
                # Get content from text widget
                new_json = json.loads(text_widget.get("1.0", "end"))

                write_conf("json_ld", new_json)

                hide_stop_progress_bar()
                editor_window.destroy()

            except json.JSONDecodeError:
                print("Invalid JSON format")
                text_status.configure(text="Invalid JSON format")
                hide_stop_progress_bar()
            except IOError as e:
                print(f"Error handling files: {e}")
                text_status.configure(text=f"Error handling files {e.__str__()}")
                hide_stop_progress_bar()
            except Exception as e:
                print(f"Unexpected error: {e}")
                text_status.configure(text=f"Unexpected error {e.__str__()}")
                hide_stop_progress_bar()

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
    app = MainWindow()
    app.mainloop()
