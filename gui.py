"""
Copyright 2025 github.com/A-Temur, Abdullah Temur. All rights reserved.
"""

import importlib
import json
import os
import runpy
import sys
import gui_context
from webbrowser import open as webbrowser_open
from tkinter import filedialog

import customtkinter
from PIL import Image
# noinspection PyPackageRequirements
from tktooltip import ToolTip

import main

def center_window(window, width, height):
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set window geometry
    window.geometry(f"{width}x{height}+{x}+{y}")



class MainWindow(customtkinter.CTk):

    @property
    def required_conditions_met(self):
        all_bool = [x.required_condition_met for x in self._required_widgets]
        return all(all_bool)

    def __init__(self):
        super().__init__()

        self.conf_module = importlib.import_module("schema")

        self.title("Metabooster")
        # Increased height to make space for the logo
        # self.geometry("1000x670")
        center_window(self, 844, 677)

        # list of supported media files with custom descriptions
        self.supported_files = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".heic", ".pdf"]
        # filtered all files for only custom description supported files
        self.filtered_files = []

        # used for determining whether the target dir has changed
        self.last_target_dir = ""

        # used to store a list of all string inputs for convenient access
        self.str_inputs = []

        # holds the conf
        self.conf = None

        # holds original conf
        self.original_conf = None

        # save when closing main window
        self.save_jsonld = False
        self.save_custom_desc = False


        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.grid_rowconfigure(0, weight=1)
        # # Configure column 0 to have equal weight for centering the logo
        # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = customtkinter.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


        logo_frame = customtkinter.CTkFrame(main_frame)
        logo_frame.grid_rowconfigure(0, weight=1)
        logo_frame.grid_columnconfigure(0, weight=1)
        logo_frame.grid_columnconfigure(1, weight=1)
        logo_frame.grid_columnconfigure(2, weight=1)
        logo_frame.pack(fill="both", pady=(0, 10))

        directory_frame = customtkinter.CTkFrame(main_frame)
        directory_frame.grid_columnconfigure(1, weight=1)
        directory_frame.pack(fill="both")

        fields_frame = customtkinter.CTkFrame(main_frame)
        fields_frame.grid_columnconfigure(1, weight=1)
        fields_frame.pack(fill="both")

        buttons_frame = customtkinter.CTkFrame(main_frame)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.pack(fill="both")


        self.GITHUB_URL = "https://github.com/A-Temur"
        self.KOFI_URL = "https://ko-fi.com/your-username"

        # --- 2. Load and Add Logo ---
        try:
            gh_image_data = Image.open("media/github-mark-white.png")
            gh_image = customtkinter.CTkImage(gh_image_data, gh_image_data, (50, 50))

            gh_label = customtkinter.CTkLabel(logo_frame, image=gh_image, text="")
            gh_label.grid(row=0, column=0, sticky="e", padx=15)

            # Make the label clickable
            gh_label.bind("<Button-1>", lambda e: self.open_link(self.GITHUB_URL))
            # Change cursor to a hand when hovering over the icon
            gh_label.configure(cursor="hand2")

            # Open the image using Pillow
            logo_image_data = Image.open("media/metabooster_logo_rounded.png")
            # Create a CTkImage object
            logo_image = customtkinter.CTkImage(
                dark_image=logo_image_data,
                light_image=logo_image_data,
                size=(112, 112)  # Adjust size as needed
            )
            # Create a label to display the image. 
            # columnspan=3 makes it span all columns, allowing it to be centered.
            logo_label = customtkinter.CTkLabel(logo_frame, image=logo_image, text="")
            logo_label.grid(row=0, column=1)

            kofi_image_data = Image.open("media/support_me_on_kofi_badge_blue.png")
            kofi_image = customtkinter.CTkImage(kofi_image_data, kofi_image_data, (80, 50))

            kofi_label = customtkinter.CTkLabel(logo_frame, image=kofi_image, text="")
            kofi_label.grid(row=0, column=2, sticky="w")

            # Make the label clickable
            kofi_label.bind("<Button-1>", lambda e: self.open_link(self.KOFI_URL))
            # Change cursor to a hand when hovering over the icon
            kofi_label.configure(cursor="hand2")


        except FileNotFoundError:
            # Fallback if logo.png is not found
            logo_label = customtkinter.CTkLabel(self, text="My Application", font=("Arial", 24))
            logo_label.grid(row=0, column=1, columnspan=3, pady=(20, 10))

        # def reset_border_color(target_widget):
        #     if not target_widget.already_changed:
        #
        #         target_widget.configure(border_color='#565B5E')
        #         target_widget.already_changed = True

        # 3. Select your Projects directory:

        def reset_border_color(new_value, target_widget):
            """
            Resets border color once, when input received
            :param new_value:
            :param target_widget:
            :return:
            """
            if not target_widget.required_condition_met:
                new_value = new_value[0]
                # check whether the new value isn't only the placeholder text and not empty str
                # noinspection PyProtectedMember
                if new_value != '' and new_value != target_widget._placeholder_text:
                    target_widget.configure(border_color="#565B5E")
                    target_widget.required_condition_met = True

            if self.required_conditions_met:
                self.submit_button.configure(fg_color="green")

            return True  # Always allow the input

        self._required_widgets = []

        self.dir1_label = customtkinter.CTkLabel(directory_frame, text="Select the Target directory:")
        self.dir1_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.target_dir = customtkinter.CTkEntry(directory_frame, placeholder_text="Select directory...",
                                                 border_color="green")
        self.target_dir.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.dir1_button = customtkinter.CTkButton(directory_frame, text="Browse...",
                                                   command=lambda: self.select_dir(self.target_dir))
        self.dir1_button.grid(row=0, column=2, padx=10, pady=(10, 5), sticky="e")

        self.target_dir.required_condition_met = False
        self._required_widgets.append(self.target_dir)

        CustomTooltip(self.target_dir, "Select the directory in which your files are")


        # vcmd = (self.register(validate_input), '%P')
        # noinspection PyTypeChecker
        self.target_dir.configure(validate='key',
                                  validatecommand=(self.register(lambda *args: reset_border_color(args,
                                                                                                  self.target_dir)),
                                                   '%P'))

        # 4. Select output directory location
        self.dir2_label = customtkinter.CTkLabel(directory_frame, text="Select output location:")
        self.dir2_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.out_dir = customtkinter.CTkEntry(directory_frame,
                                              placeholder_text="Select the location of the output...",
                                              border_color='green')
        self.out_dir.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.dir2_button = customtkinter.CTkButton(directory_frame, text="Browse...",
                                                   command=lambda: self.select_dir(self.out_dir, False))
        self.dir2_button.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        self.out_dir.required_condition_met = False
        self._required_widgets.append(self.out_dir)

        self.create_new_dir = False


        # noinspection PyTypeChecker
        self.out_dir.configure(validate='key',
                                  validatecommand=(self.register(lambda *args: reset_border_color(args,
                                                                                                  self.out_dir)),
                                                   '%P'))

        CustomTooltip(self.out_dir, "A new directory will be created by default, except when you specifically select an already existing directory")

        # String Inputs
        # Author
        self.author_label = customtkinter.CTkLabel(fields_frame, text="Author:")
        self.author_label.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")
        self.author_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="Enter author name")
        self.author_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=(20, 5), sticky="ew")
        self.str_inputs.append(self.author_entry)

        # Copyright
        self.copyright_label = customtkinter.CTkLabel(fields_frame, text="Copyright:")
        self.copyright_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.copyright_entry = customtkinter.CTkEntry(fields_frame,
                                                      placeholder_text="e.g. Copyright 2025 OG-Brain.com, Abdullah Temur. All rights reserved.")
        self.copyright_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.copyright_entry)

        # Media Description
        self.media_desc_label = customtkinter.CTkLabel(fields_frame, text="Default Description:")
        self.media_desc_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.media_desc_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g. Media for OG-Brain.com")
        self.media_desc_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.media_desc_entry)

        CustomTooltip(self.media_desc_entry, "This description will be inserted to all supported files")

        # Keywords
        self.keywords_label = customtkinter.CTkLabel(fields_frame, text="Keywords (Comma separated):")
        self.keywords_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.keywords_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g.: OG-Brain, Abdullah Temur, Bio-inspired AI")
        self.keywords_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.keywords_entry)

        # Media Title Prefix
        self.title_prefix_label = customtkinter.CTkLabel(fields_frame, text="Media Title Prefix:")
        self.title_prefix_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.title_prefix_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g. Website.com ")
        self.title_prefix_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.title_prefix_entry)

        CustomTooltip(self.title_prefix_entry, "This will be used as the title for your files. "
                                               "E.g. when your prefix is 'Website.com', "
                                               "the resulting Title will be: 'Website.com filename'")

        # Directory Title Prefix
        self.dir_prefix_label = customtkinter.CTkLabel(fields_frame, text="Directory Title Prefix:")
        self.dir_prefix_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.dir_prefix_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g. OG-Brain.com directory ")
        self.dir_prefix_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.dir_prefix_entry)

        CustomTooltip(self.dir_prefix_entry, "Since directories by themselves doesn't support metadata, "
                                             "Metabooster automatically creates a new json file for each directory."
                                             "This prefix is used for such json files 'Title'. "
                                             "E.g. when your prefix is 'Website.com', "
                                             "the resulting Title will be: 'Website.com directoryname'")

        # Default directory metadata file description
        self.dir_file_desc_label = customtkinter.CTkLabel(fields_frame, text="Default directory file description:")
        self.dir_file_desc_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.dir_file_desc_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g.: Directory metadata file")
        self.dir_file_desc_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.dir_file_desc_entry)

        CustomTooltip(self.dir_file_desc_entry, "Used for directory metadata files")

        # HTML File for JSON-LD
        self.jsonld_html_label = customtkinter.CTkLabel(fields_frame, text="HTML File for JSON-LD:")
        self.jsonld_html_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.jsonld_html_entry = customtkinter.CTkEntry(fields_frame,
                                                        placeholder_text="Enter your HTML filename (leave empty if not needed), e.g.: index.html")
        self.jsonld_html_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.jsonld_html_entry)

        # Default name jsonld file
        self.jsonld_filename_label = customtkinter.CTkLabel(fields_frame, text="Default name of jsonld file:")
        self.jsonld_filename_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.jsonld_filename_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g.: media_jsonld.json")
        self.jsonld_filename_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.jsonld_filename_entry)

        # Website URL
        self.website_label = customtkinter.CTkLabel(fields_frame, text="Website URL:")
        self.website_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.website_entry = customtkinter.CTkEntry(fields_frame, placeholder_text="e.g.: https://www.og-brain.com")
        self.website_entry.grid(row=9, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.str_inputs.append(self.website_entry)

        # custom descriptions
        self.custom_desc_button = customtkinter.CTkButton(buttons_frame, text="Create Custom Descriptions",
                                                          command=self.create_custom_descriptions, width=200)
        self.custom_desc_button.grid(row=0, column=0, pady=5, padx=30)

        # Run metabooster button
        self.submit_button = customtkinter.CTkButton(buttons_frame, text="Run Metabooster", command=self.submit, width=200)
        self.submit_button.grid(row=0, column=1, pady=5, padx=30)

        # JSON-LD HEAD edit button
        self.jsonld_edit_button = customtkinter.CTkButton(buttons_frame, text="Edit JSON-LD HEAD", command=self.open_jsonld_editor, width=200)
        self.jsonld_edit_button.grid(row=0, column=2, pady=5, padx=30)


        self.load_conf()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_dir(self, target_entry_widget, target_dir_selected=True):
        path = filedialog.askdirectory()
        if path:
            target_entry_widget.delete(0, "end")
            target_entry_widget.insert(0, path)

            if target_dir_selected:
                original_dir_name = os.path.basename(path)
                final_dir = path.replace(original_dir_name, f"Metaboosted_{original_dir_name}")
                self.out_dir.delete(0, "end")
                self.out_dir.insert(0, final_dir)
            else:
                self.create_new_dir = True

    def on_close(self):
        if self.save_jsonld:
            self.original_conf["json_ld"] = self.conf["json_ld"]
        elif self.save_custom_desc:
            self.original_conf["custom_descriptions"] = self.conf["custom_descriptions"]

        if self.save_jsonld or self.save_custom_desc:
            with open("conf.json", "w", encoding="utf-8") as f:
                json.dump(self.original_conf, f, indent=4)

        self.destroy()


    def load_conf(self):
        popup_progressbar = PopupProgressBar(self, "Loading Configuration", "Loading files...")

        with open("conf.json", "r", encoding="utf-8") as f:
            custom_conf = json.load(f)

        self.original_conf = custom_conf
        self.conf = custom_conf
        popup_progressbar.progress_bar.update()

        self.author_entry.delete(0, "end")
        self.author_entry.insert(0, custom_conf["autor"])
        popup_progressbar.progress_bar.update()

        self.copyright_entry.delete(0, "end")
        self.copyright_entry.insert(0, custom_conf["copyright_"])
        popup_progressbar.progress_bar.update()

        self.media_desc_entry.delete(0, "end")
        self.media_desc_entry.insert(0, custom_conf["default_media_description"])
        popup_progressbar.progress_bar.update()

        self.keywords_entry.delete(0, "end")
        self.keywords_entry.insert(0, ", ".join(custom_conf["keywords"]))
        popup_progressbar.progress_bar.update()

        self.title_prefix_entry.delete(0, "end")
        self.title_prefix_entry.insert(0, custom_conf["media_title_prefix"])
        popup_progressbar.progress_bar.update()

        self.dir_prefix_entry.delete(0, "end")
        self.dir_prefix_entry.insert(0, custom_conf["directory_title_prefix"])
        popup_progressbar.progress_bar.update()

        self.dir_file_desc_entry.delete(0, "end")
        self.dir_file_desc_entry.insert(0, custom_conf["default_directory_description"])
        popup_progressbar.progress_bar.update()

        self.jsonld_html_entry.delete(0, "end")
        self.jsonld_html_entry.insert(0, custom_conf["add_metadata_json_to_html_file"])
        popup_progressbar.progress_bar.update()

        self.jsonld_filename_entry.delete(0, "end")
        self.jsonld_filename_entry.insert(0, custom_conf["default_name_jsonld_file"])
        popup_progressbar.progress_bar.update()

        self.website_entry.delete(0, "end")
        self.website_entry.insert(0, custom_conf["website"])
        popup_progressbar.progress_bar.update()

        self.after(1500, popup_progressbar.destroy)

    def submit(self):
        popup = PopupProgressBar(self, "Loading", "Metaboosting your data...")
        # write all widget entrys into custom conf json
        # with open("conf_overwrite/conf.json", "r", encoding="utf-8") as f:
        #     popup.update()
        #     custom_conf = json.load(f)

        popup.update()
        self.conf["autor"] = self.author_entry.get()
        self.conf["copyright_"] = self.copyright_entry.get()
        self.conf["default_media_description"] = self.media_desc_entry.get()
        self.conf["keywords"] = [keyword.lstrip() for keyword in self.keywords_entry.get().strip().split(',') if keyword != ""]
        self.conf["media_title_prefix"] = self.title_prefix_entry.get().rstrip() + " "
        self.conf["directory_title_prefix"] = self.dir_prefix_entry.get()
        self.conf["default_directory_description"] = self.dir_file_desc_entry.get()
        self.conf["add_metadata_json_to_html_file"] = self.jsonld_html_entry.get()
        self.conf["default_name_jsonld_file"] = self.jsonld_filename_entry.get()
        self.conf["website"] = self.website_entry.get().rstrip("/") + "/"

        popup.update()
        with open("conf.json", "w", encoding="utf-8") as f:
            popup.update()
            json.dump(self.conf, f, indent=4)

        # entry point for backend.

        """
        Abstract:
        1. Create list of arguments/flags
            - indicate that the the script is running in gui-mode (e.g. --gui-mode)
            - pass the progress bar reference
        2. backend determines that it is running in gui mode, behaves accordingly
        """

        # custom_globals = {
        #     # '__name__': '__main__',
        #     'progress_bar': popup,
        #     # 'sys': type('MockSys', (), {'argv': ['main.py', f'{self.target_dir.get()}', f'{self.out_dir.get()}','--gui-mode']})()
        # }

        gui_context.GuiContext.set_gui_ref(popup.update)

        # Save original argv
        original_argv = sys.argv.copy()

        # Set custom arguments
        sys.argv = ['main.py', f'{self.target_dir.get()}', f'{self.out_dir.get()}', "gui"]

        runpy.run_module('main', run_name="__main__", alter_sys=True)

        # Restore original sys.argv
        sys.argv = original_argv

        popup.destroy()
        self.create_popup_dialog("Finished!", "Metaboosted your files, have fun!")

    def create_popup_dialog(self, title_, text_):
        dialog_ = customtkinter.CTkToplevel(self)
        dialog_.title(title_)
        center_window(dialog_, 300, 100)

        dialog_label_ = customtkinter.CTkLabel(dialog_, text=text_)
        dialog_label_.pack(pady=20)

        ok_button = customtkinter.CTkButton(dialog_, text="OK", command=dialog_.destroy)
        ok_button.pack()

        dialog_.transient(self)
        dialog_.wait_visibility()
        dialog_.grab_set()
        self.wait_window(dialog_)

    def create_custom_descriptions(self):
        if not bool(self.target_dir.get()):
            # create popup informing user that he must select target directory first
            self.create_popup_dialog("Error", "You must select a target directory first!")
            return

        def fill_frame():
            # with open("conf_overwrite/conf.json", "r", encoding="utf-8") as f:
            #     custom_conf = json.load(f)

            conf_keys = self.conf["custom_descriptions"].keys()

            for supported_file in self.filtered_files:
                file_txt = os.path.basename(supported_file)
                scrollable_frame_label = customtkinter.CTkLabel(scrollable_frame,
                                                                text=f"{file_txt}")
                scrollable_frame_label.pack(padx=10, pady=5, anchor="w")
                scrollable_frame_input = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Leave empty, if there's no need")
                scrollable_frame_input.pack(padx=10, pady=5, anchor="w", fill="x")

                if file_txt in conf_keys:
                    scrollable_frame_input.insert(0, self.conf["custom_descriptions"][file_txt])

                scrollable_frame.labels.append((scrollable_frame_label, scrollable_frame_input))

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
                    # noinspection PyProtectedMember
                    filename = lis_item_[0]._text
                    json_dict_[filename] = custom_descript

            if len(json_dict_) >= 1:
                # read custom_conf
                # with open("conf_overwrite/conf.json", "r", encoding="utf-8") as f:
                #     custom_conf = json.load(f)
                self.conf["custom_descriptions"] = json_dict_
                # write to custom_conf
                # with open("conf_overwrite/conf.json", "w", encoding="utf-8") as f:
                #     json.dump(custom_conf, f, indent=4)
                self.save_custom_desc = True

            new_window.destroy()
            popup_ = PopupProgressBar(self, "Save", "Saving custom descriptions...")
            self.after(1500, popup_.destroy)

        target_dir_changed = True

        # check whether target dir has changed
        if self.target_dir.get() == self.last_target_dir:
            target_dir_changed = False

        # create new window (scrollable)
        new_window = customtkinter.CTkToplevel(self)
        # make window invisible by default
        new_window.attributes("-alpha", 0)
        new_window.title("Create Custom Descriptions")
        center_window(new_window, 430, 566)
        new_window.wait_visibility()

        # add widgets
        scrollable_frame = customtkinter.CTkScrollableFrame(new_window)
        # scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_columnconfigure(1, weight=1)
        scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        scrollable_frame.labels = []

        save_button = customtkinter.CTkButton(new_window, text="Save", command=save_custom_descriptions)
        save_button.grid(row=1, column=0, pady=20)

        cancel_button = customtkinter.CTkButton(new_window, text="Cancel", command=new_window.destroy)
        cancel_button.grid(row=1, column=1, pady=20)

        popup_bar = PopupProgressBar(self, "...", "Loading files ...")

        if target_dir_changed:
            self.filtered_files = []
            self.last_target_dir = self.target_dir.get()
            popup_bar.update("Iterating over files...")
            fill_files_list()
            # self.after(0, update_progress, "filling frame...")

        if len(self.filtered_files) >= 1:
            popup_bar.update("filling frame...")
            fill_frame()
            # destroy progress bar
            popup_bar.destroy()
            # make window visible
            new_window.attributes('-alpha', 1)
            new_window.grab_set()
        else:
            popup_bar.destroy()
            new_window.destroy()
            self.create_popup_dialog("Error", "No supported files found in target directory")

    def open_jsonld_editor(self):
        def get_conf():
            # # get schema variable via str
            # schema_var = getattr(self.conf_module, key_)

            # # get default schema conf
            # conf = json.dumps(schema_var, indent=4)

            # with open("conf_overwrite/conf.json", "r", encoding="utf-8") as f:
            #     custom_conf = json.load(f)

            custom_conf = self.conf

            # check whether it is the first time loading json_ld
            # if yes, create license, description, 'name' dynamically via existing fields (if there are any)
            if self.conf["load_dynamic_jsonld"]:
                # schema:
                # "@type": "CreativeWork",
                # "license": f"{website}license.txt",
                # "description": default_media_description,
                # "author": {
                #     "@type": "Person",
                #     "name": autor
                # }
                custom_conf["json_ld"]["@graph"][0]["license"] = f"{custom_conf["website"]}/license.txt"
                custom_conf["json_ld"]["@graph"][0]["description"] = f"{custom_conf["default_media_description"]}"
                custom_conf["json_ld"]["@graph"][0]["author"]["name"] = f"{custom_conf["autor"]}"

                # change flag
                custom_conf["load_dynamic_jsonld"] = False

            return custom_conf

        def hide_stop_progress_bar(reset_status_=False):
            progress_bar.stop()
            progress_bar.pack_forget()
            if reset_status_:
                text_status.configure(text="Ready")

        def show_start_progress_bar(text_status_):
            progress_bar.pack(pady=10)
            progress_bar.start()
            text_status.configure(text=text_status_)

            # Create save button

        def save_changes():
            try:
                show_start_progress_bar("Saving new JSON-LD Head, please wait...")
                # Get content from text widget
                new_json = json.loads(text_widget.get("1.0", "end"))

                self.conf["json_ld"] = new_json

                # save conf
                # with open("conf_overwrite/conf.json", "w", encoding="utf-8") as f:
                #     json.dump(conf, f, indent=4)

                self.save_jsonld = True

                hide_stop_progress_bar()
                editor_window.destroy()
                popup = PopupProgressBar(self, "..", "Saving new JSON Head...")
                self.after(1000, popup.destroy)

            except json.JSONDecodeError:
                print("Invalid JSON format")
                text_status.configure(text="Invalid JSON format")
                hide_stop_progress_bar()

        def cancel_button_clicked():
            editor_window.destroy()


        def generate_from_mainwindow():
            conf["json_ld"]["@graph"][0]["license"] = f"{self.website_entry.get().rstrip("/")}/license.txt"
            conf["json_ld"]["@graph"][0]["description"] = f"{self.media_desc_entry.get()}"
            conf["json_ld"]["@graph"][0]["author"]["name"] = f"{self.author_entry.get()}"
            insert_text_ = json.dumps(conf["json_ld"], indent=4)
            # delete contents from text_widget
            text_widget.delete(0.0, 'end')
            # insert new content
            text_widget.insert(1.0, insert_text_)

        editor_window = customtkinter.CTkToplevel(self)
        editor_window.title("JSON-LD HEAD Editor")
        center_window(editor_window, 490, 400)
        # editor_window.transient(self)
        editor_window.wait_visibility()
        editor_window.grab_set()

        editor_window.grid_rowconfigure(0, weight=1)
        editor_window.grid_columnconfigure(0, weight=1)
        # editor_window.grid_columnconfigure(1, weight=1)

        # create separate frame to use pack for one frame

        # frame for everything except save and cancel buttons
        main_frame = customtkinter.CTkFrame(editor_window)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        # frame for save and cancel button
        save_cancel_frame = customtkinter.CTkFrame(editor_window, fg_color='gray10')
        save_cancel_frame.grid(row=1, column=0, sticky="ew", columnspan=2, padx=20)
        save_cancel_frame.grid_columnconfigure(1, weight=1)

        progress_bar = customtkinter.CTkProgressBar(main_frame, mode="indeterminate", width=300)
        # make invisible by default
        progress_bar.pack_forget()

        # create text status field
        text_status = customtkinter.CTkLabel(main_frame, text="Ready", font=("Arial", 12))
        text_status.pack(pady=10)

        # Create text widget for editing
        text_widget = customtkinter.CTkTextbox(main_frame)
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        button_width = 120

        # Save and cancel buttons
        save_button = customtkinter.CTkButton(save_cancel_frame, text="Save", command=save_changes, width=button_width)
        save_button.grid(row=0, column=0, pady=20)

        cancel_button = customtkinter.CTkButton(save_cancel_frame, text="Cancel", command=cancel_button_clicked, width=button_width)
        cancel_button.grid(row=0, column=2, pady=20)

        # generate from new conf button
        generate_button = customtkinter.CTkButton(save_cancel_frame, text="Generate", command=generate_from_mainwindow, width=button_width)
        generate_button.grid(row=0, column=1, pady=20)


        show_start_progress_bar("Retrieving JSON-LD content, please wait...")

        conf = get_conf()
        insert_text = json.dumps(conf["json_ld"], indent=4)

        text_widget.insert("1.0", insert_text)

        hide_stop_progress_bar(True)


    # --- 4. Add a method to open links ---
    # noinspection PyMethodMayBeStatic
    def open_link(self, url):
        """Opens the given URL in a new browser tab."""
        webbrowser_open(url)
        print(f"Opening {url}...")


class PopupProgressBar:
    def __init__(self, parent:MainWindow, title, text):
        self.window = customtkinter.CTkToplevel(parent)
        # remove default title bar
        self.window.overrideredirect(True)
        # parent.attributes('-topmost', False)


        self.window.title(title)
        center_window(self.window, 500, 70)

        self.progress_bar = customtkinter.CTkProgressBar(self.window, mode="indeterminate", width=300)
        self.progress_bar.pack(pady=10)
        self.progress_label = customtkinter.CTkLabel(self.window, text=text, font=("Arial", 12))
        self.progress_label.pack()

        self.progress_bar.start()
        # transient doesn't bring this window to the foreground when using overrideredirect(True)
        # self.window.transient(parent)

        self.window.wait_visibility()
        self.window.focus_force()
        self.window.grab_set()

    def update(self, text=""):
        if bool(text):
            self.progress_label.configure(text=text)
        self.progress_bar.update()

    def destroy(self):
        self.progress_bar.stop()
        self.window.destroy()



class CustomTooltip(ToolTip):
    def __init__(self, *args):
        super().__init__(*args)



if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
