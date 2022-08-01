import tkinter as tk
import tempfile
import os
from tkinter import ttk, BooleanVar, TclError
from tkinter.filedialog import askdirectory, askopenfiles
from . import thumbnail
from . import collect_images
from . import save_images
from . import filter
from . import rotate
from PIL import Image, ImageTk

button_width = 20
button_pady = 2.5


class Application(tk.Frame):
    def __init__(self, master=None):
        """Instantiation function"""
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """Creates and places all GUI elements"""
        self.frame = tk.Frame(self.master)
        self.frame.pack(anchor="nw", side="left")
        self.frame2 = tk.Frame(self.master)
        self.frame2.pack(anchor="nw", side="left")
        self.image_folder = "../resources/img/spec2-images"
        try:
            os.listdir(self.image_folder)
        except FileNotFoundError:
            self.image_folder = "resources/img/spec2-images"


        self.image_dictionary = collect_images.get_images(self.image_folder)
        self.save_location = None
        self.history = []
        self.times_undone = 0
        self.first_undo = True
        self.can_history = BooleanVar()
        self.apply_to_all = BooleanVar()
        self.memory_error_message = "Error: Memory Error"
        self.image_index = 0

        self.get_preview()

        def create_buttons():
            """Defines all of the GUI elements"""
            self.greyscale_button = tk.Button(self.frame, text="Convert to greyscale",
                                              command=self.fast_convert_grayscale,
                                              width=button_width)

            self.slow_grayscale_button = tk.Button(self.frame, text="Slow grayscale", command=self.convert_grayscale,
                                                   width=button_width)

            self.thumbnail_button = tk.Button(self.frame, text="Convert to thumbnail",
                                              command=self.convert_to_thumbnail,
                                              width=button_width)

            self.colour_button = tk.Button(self.frame, text="Apply colour change", command=self.change_colours,
                                           width=button_width)
            self.red_entry = tk.Entry(self.frame, width=5)
            self.green_entry = tk.Entry(self.frame, width=5)
            self.blue_entry = tk.Entry(self.frame, width=5)
            self.red_label = tk.Label(self.frame, text="R:")
            self.green_label = tk.Label(self.frame, text="G:")
            self.blue_label = tk.Label(self.frame, text="B:")

            self.brightness_button = tk.Button(self.frame, text="Apply brightness change",
                                               command=self.change_brightness, width=button_width)
            self.brightness_entry = tk.Scale(self.frame, width=4, length=80, from_=0.1, to=2, orient="horizontal", resolution=0.1, sliderlength=20)

            self.brighness_label = tk.Label(self.frame, text="Brightness:")

            self.filter_button = tk.Button(self.frame, text="Apply filter", command=self.apply_filter,
                                           width=button_width)
            self.filter_menu = ttk.Combobox(self.frame,
                                            values=["emboss", "blur", "smooth", "smooth_more", "sharpen", "contour",
                                                    "detail", "edge_enhance", "edge_enhance_more", "find_edges"],
                                            state="readonly")

            self.rotate_button = tk.Button(self.frame, text="Rotate 90°", command=self.rotate, width=button_width)

            self.reset_button = tk.Button(self.frame, text="Reset images", command=self.reset_images,
                                          width=button_width)
            self.reset_label = tk.Label(self.frame, text="<--- Deletes history", width=button_width)

            self.undo_button = tk.Button(self.frame, text="Undo", command=self.undo, width=button_width)
            self.redo_button = tk.Button(self.frame, text="Redo", command=self.redo, width=button_width)

            self.choose_folder = tk.Button(self.frame, text="Choose input folder", width=button_width,
                                           command=self.select_folder_input)
            self.choose_files = tk.Button(self.frame, text="Choose input files", width=button_width,
                                          command=self.select_files_input)
            self.choose_output = tk.Button(self.frame, text="Choose output folder", width=button_width,
                                           command=self.choose_save_loaction)
            self.history_check = tk.Checkbutton(self.frame, text="Enable undo and redo?", var=self.can_history)
            self.apply_to_all_check = tk.Checkbutton(self.frame, text="Apply to all images?", var=self.apply_to_all)

            self.save_button = tk.Button(self.frame, text="Save", command=self.save, width=button_width)
            self.quit_button = tk.Button(self.frame, text="Quit", command=self.master.destroy, width=button_width)

            self.empty_1 = tk.Label(self.frame, text="")
            self.empty_2 = tk.Label(self.frame, text="")
            self.empty_3 = tk.Label(self.frame, text="")
            self.empty_4 = tk.Label(self.frame, text="")
            self.empty_5 = tk.Label(self.frame, text="")

            self.preview_image_label = tk.Label(self.frame2, image=self.preview_image)
            self.previous_image_button = tk.Button(self.frame2, text="<<", command=self.previous_image)
            self.image_text_label = tk.Label(self.frame2, text="Preview Image (0)")
            self.next_image_button = tk.Button(self.frame2, text=">>", command=self.next_image)
            self.fullscreen_preview_button = tk.Button(self.frame2, text="Preview in fullscreen",
                                                       command=self.fullscreen_preview)
            self.empty_label = tk.Label(self.frame2,
                                        text="                                                                                                                                                                                     ")

            self.warning_label = tk.Label(self.frame, text="")
        create_buttons()

        def grid_images():
            """Places all GUI elements on screen"""
            self.greyscale_button.grid(row=0, sticky="W", pady=button_pady)
            self.slow_grayscale_button.grid(row=0, column=1, columnspan=6, sticky="W", pady=button_pady)
            self.thumbnail_button.grid(row=2, sticky="W", pady=button_pady)
            self.rotate_button.grid(row=3, sticky="w", pady=button_pady)

            self.empty_1.grid(row=4, sticky="w", pady=button_pady)

            self.colour_button.grid(row=5, sticky="w", pady=button_pady)
            self.red_entry.grid(row=5, column=2, sticky="w", pady=1)
            self.green_entry.grid(row=5, column=4, sticky="w", pady=1)
            self.blue_entry.grid(row=5, column=6, sticky="w", pady=1)
            self.red_label.grid(row=5, column=1, sticky="w", pady=1)
            self.green_label.grid(row=5, column=3, sticky="w", pady=1)
            self.blue_label.grid(row=5, column=5, sticky="w", pady=1)

            self.brightness_button.grid(row=6, sticky="w", pady=button_pady)
            self.brightness_entry.set(1)
            self.brightness_entry.grid(row=6, column=4, sticky="w", columnspan=3)
            self.brighness_label.grid(row=6, column=1, columnspan=3, sticky="w")

            self.filter_button.grid(row=7, sticky="w", pady=button_pady)
            self.filter_menu.grid(row=7, column=1, columnspan=6)
            self.empty_2.grid(row=8, sticky="w", pady=button_pady)

            self.undo_button.grid(row=9, sticky="w", pady=button_pady)
            self.redo_button.grid(row=9, column=1, sticky="w", pady=button_pady, columnspan=6)
            self.reset_button.grid(row=10, sticky="w", pady=button_pady)
            self.reset_label.grid(row=10, column=1, sticky="w", pady=button_pady, columnspan=6)
            self.empty_3.grid(row=11, sticky="w", pady=button_pady)

            self.choose_folder.grid(row=12, sticky="w", pady=button_pady)
            self.choose_files.grid(row=12, column=1, sticky="w", pady=button_pady, columnspan=6)
            self.choose_output.grid(row=13, sticky="w", pady=button_pady)
            self.empty_4.grid(row=14, sticky="w", pady=button_pady)

            self.can_history.set(True)
            self.history_check.grid(row=15, sticky="w", pady=button_pady)
            self.apply_to_all.set(True)
            self.apply_to_all_check.grid(row=16, sticky="w", pady=button_pady)
            self.warning_label.grid(row=17, sticky="w")

            self.save_button.grid(row=19, sticky="W", pady=25)
            self.quit_button.grid(row=19, column=1, sticky="W", pady=25, columnspan=6)

            self.preview_image_label.grid(row=0, column=0, sticky="W", columnspan=4)
            self.previous_image_button.grid(row=1, column=0, padx=0)
            self.image_text_label.grid(row=1, column=1, padx=20)
            self.next_image_button.grid(row=1, column=2, padx=0)
            self.fullscreen_preview_button.grid(row=2, column=1, padx=5, pady=5)
            self.empty_label.grid(row=1, column=3)
        grid_images()

    def get_images(self):
        """Gets images from the designated folder."""
        self.image_dictionary = collect_images.get_images(self.image_folder)
        self.delete_history()
        self.update_image()

    def reset_images(self):
        """Resets the images to the original version before modification and deletes the modification history."""
        self.reset_error_label()
        self.delete_history()
        self.get_images()

    def change_colours(self):
        """Changes the rgb values of the images."""
        self.reset_error_label()
        try:
            self.save_history()
            red, green, blue = 1, 1, 1
            try:
                red = float(self.red_entry.get())
            except ValueError:
                None
            try:
                green = float(self.green_entry.get())
            except ValueError:
                None
            try:
                blue = float(self.blue_entry.get())
            except ValueError:
                None
            self.red_entry.delete(0, 'end')
            self.green_entry.delete(0, 'end')
            self.blue_entry.delete(0, 'end')
            self.update_image_dictionary(filter.change_colours(self.image_dictionary, red, green, blue))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def convert_grayscale(self):
        """Converts the images to grayscale by changing each pixel to grayscale."""
        self.reset_error_label()
        try:
            self.save_history()
            self.update_image_dictionary(filter.grayscale(self.image_dictionary))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def fast_convert_grayscale(self):
        """Converts the images to grayscale."""
        self.reset_error_label()
        try:
            self.save_history()
            self.update_image_dictionary(filter.fast_grayscale(self.image_dictionary))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def change_brightness(self):
        """Changes the brightness value of the images."""
        self.reset_error_label()
        try:
            self.save_history()
            brightness = float(self.brightness_entry.get())
            self.update_image_dictionary(filter.change_brightness(self.image_dictionary, brightness))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def apply_filter(self):
        """Applies a pre-defined filter to the images."""
        self.reset_error_label()
        try:
            self.save_history()
            filter_name = self.filter_menu.get()
            self.update_image_dictionary(filter.apply_filter(self.image_dictionary, filter_name))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def convert_to_thumbnail(self):
        """Converts all images to thumbnails."""
        self.reset_error_label()
        try:
            self.save_history()
            self.update_image_dictionary(thumbnail.convert_to_thumbnail(self.image_dictionary))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def save(self, location=None):
        """Saves images to the defined location."""
        self.reset_error_label()
        if location is None and self.save_location is None:
            try:
                save_images.save(self.image_dictionary)
            except FileNotFoundError:
                save_images.save(self.image_dictionary, "specification-2/output")
        elif self.save_location is not None:
            save_images.save(self.image_dictionary, self.save_location)
        else:
            save_images.save(self.image_dictionary, location)

    def get_preview(self):
        """This finds and resizes (preserving aspect ratio) the image to be previewed on the GUI. """
        temp_image = self.image_dictionary[list(self.image_dictionary.keys())[self.image_index]]
        temp_w, temp_h = temp_image.size
        new_h = 396
        percent_change = temp_h / new_h
        new_w = round(temp_w / percent_change)
        temp_image = temp_image.resize((round(new_w), round(new_h)), Image.ANTIALIAS)
        self.preview_image = ImageTk.PhotoImage(temp_image)

    def update_image(self):
        """Calls function to update the image for preview image and displays this, and updates label underneath."""
        self.reset_error_label()
        self.get_preview()
        self.preview_image_label.configure(image=self.preview_image)

    def next_image(self):
        """Updates the preview image to the next one."""
        self.reset_error_label()
        if self.image_index < len(self.image_dictionary) - 1:
            self.image_index += 1
            self.image_text_label.configure(text=f"Preview Image ({self.image_index})")
            self.update_image()

    def previous_image(self):
        """Updates the preview image to the previous one."""
        self.reset_error_label()
        if self.image_index > 0:
            self.image_index -= 1
            self.image_text_label.configure(text=f"Preview Image ({self.image_index})")
            self.update_image()

    def fullscreen_preview(self):
        """Displays the current preview image as a fullscreen image."""
        self.reset_error_label()
        temp_image = self.image_dictionary[list(self.image_dictionary.keys())[self.image_index]]
        temp_image.show()

    def undo(self):
        """Will undo the last action done to the image by the user."""
        try:
            self.reset_error_label()
            if self.can_history.get():
                if self.first_undo:
                    self.save_history()
                if (len(self.history) > 1) and (self.times_undone < len(self.history) - 1):
                    self.first_undo = False
                    self.times_undone += 1
                    self.image_dictionary = self.history[len(self.history) - (self.times_undone + 1)]
                    self.update_image()
            else:
                self.delete_history()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def redo(self):
        """Will redo the last action undone by the user."""
        self.reset_error_label()
        if self.can_history.get():
            if self.times_undone > 0:
                self.image_dictionary = self.history[len(self.history) - self.times_undone]
                self.times_undone -= 1
                self.update_image()
        else:
            self.delete_history()

    def save_history(self):
        """Adds the latest change to the history dictionary. Will delete any history not needed."""
        self.reset_error_label()
        if self.can_history.get():
            self.delete_junk_history()
            if self.image_dictionary not in self.history:
                self.history.append(self.image_dictionary)
        else:
            self.delete_history()

    def delete_junk_history(self):
        """Deletes history which is not needed after an action has been undone and new changes have been made."""
        self.reset_error_label()
        self.first_undo = True
        del self.history[(len(self.history) - (self.times_undone)):]
        self.times_undone = 0

    def select_folder_input(self):
        """Allows user to choose what file images will loaded from"""
        self.reset_error_label()
        try:
            self.delete_history()
            input_name = askdirectory()
            self.image_folder = input_name
            self.image_index = 0
            self.get_images()
            self.image_text_label.configure(text=f"Preview Image ({self.image_index})")
        except FileNotFoundError:
            None
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def select_files_input(self):
        """Lets user choose a selection of files to be used as input. These will be stored in a temporary directory."""
        self.reset_error_label()
        try:
            self.delete_history()
            image_names = askopenfiles()
            image_names = [name.name for name in image_names]
            self.image_index = 0
            self.image_dictionary = collect_images.get_images_from_files(image_names)
            self.delete_history()
            self.update_image()
            self.image_text_label.configure(text=f"Preview Image ({self.image_index})")
            self.temp_dir = tempfile.TemporaryDirectory()
            self.image_folder = self.temp_dir.name
            self.save(self.image_folder)
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)

    def delete_history(self):
        """Deletes all the change history used by undo and redo."""
        self.reset_error_label()
        del self.history[:]
        self.first_undo = True
        self.times_undone = 0

    def reset_error_label(self):
        """Makes the error label blank"""
        self.warning_label.configure(text="")

    def update_image_dictionary(self, new_dictionary):
        """Applies changes to the image dictionary, either to the whole dictionary or a single image."""
        if self.apply_to_all.get():
            self.image_dictionary = new_dictionary
        else:
            temp_image = new_dictionary[list(new_dictionary.keys())[self.image_index]]
            temp_image_dictionary = (self.image_dictionary).copy()
            temp_image_dictionary[list(temp_image_dictionary.keys())[self.image_index]] = temp_image
            self.image_dictionary = temp_image_dictionary

    def choose_save_loaction(self):
        """Allows user to choose where to save the images to."""
        get_save_location = askdirectory()
        self.save_location = get_save_location

    def rotate(self):
        """Rotates the images"""
        try:
            self.reset_error_label()
            self.save_history()
            self.update_image_dictionary(rotate.rotate(self.image_dictionary))
            self.update_image()
        except MemoryError:
            self.warning_label.configure(text=self.memory_error_message)


def main():
    """Creates and displays the tkinter window"""
    root = tk.Tk()
    root.geometry("1008x567")  # 16:9 aspect ratio
    root.title("Specification-2")
    try:
        root.wm_iconbitmap(r'./program/tkinter_icon.ico')
    except TclError:
        root.wm_iconbitmap(r'specification-2/program/tkinter_icon.ico')
    app = Application(master=root)
    app.mainloop()
