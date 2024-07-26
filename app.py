import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from ui_backend import generate_images
import webbrowser
import os
import sys


def get_resource_path(relative_path):
    """Get the absolute path to the resource when using pyinstaller"""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GetImagesFromOBJ:
    def __init__(self, root):
        self.docs_file_path = get_resource_path("docs/index.html")
        self.root = root
        self.root.title("Get Images From OBJ File")
        self.root.geometry("")
        self.root.resizable(width=False, height=False)

        # Configure Font
        default_font = ("Helvetica", 16)
        self.root.option_add("*Font", default_font)

        # MENU BAR
        self.setMenuBar()

        # LAYOUT
        self.setLayout()

    def setMenuBar(self):
        self.menu = tk.Menu()
        self.root.config(menu=self.menu)

        # TOGGLE ADVANCE SETTINGS
        self.toggle_advance_settings_menu = tk.Menu(self.menu, tearoff=False)
        self.toggle_advance_settings_menu.add_command(
            label="Toggle Advance Settings",
            command=self.toggle_advance_settings_menu_action,
        )
        self.menu.add_cascade(label="Options", menu=self.toggle_advance_settings_menu)

        # HELP SECTION
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label="Open docs", command=self.open_docs)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

    def open_docs(self):
        webbrowser.open(f"{self.docs_file_path}")

    def toggle_advance_settings_menu_action(self):
        self.is_advance_options_active.set(
            1 if self.is_advance_options_active.get() == 0 else 0
        )
        self.toggle_advance_settings()

    def setLayout(self):
        self.set_basic_frame()
        self.set_config_frame()
        self.set_advance_config_frame()
        self.set_accept_button()

    def set_basic_frame(self):
        # BASIC FRAME
        self.basic_frame = tk.Frame(self.root, padx=10)
        self.basic_frame.pack(side=tk.TOP, pady=10, padx=20)

        # Input file
        tk.Label(self.basic_frame, text="Input:").grid(row=0, column=0, pady=10, padx=2)
        self.input_entry = tk.Entry(self.basic_frame)
        self.input_entry.grid(row=0, column=1, pady=10, padx=5)
        self.browse_input_button = tk.Button(
            self.basic_frame, text="Browse", command=self.browse_input
        )
        self.browse_input_button.grid(row=0, column=2, pady=10, padx=10)

        # Ouput folder
        tk.Label(self.basic_frame, text="Output folder:").grid(
            row=1, column=0, pady=(0, 10), padx=2
        )
        self.output_entry = tk.Entry(self.basic_frame)
        self.output_entry.grid(row=1, column=1, padx=5)
        self.browse_output_button = tk.Button(
            self.basic_frame, text="Browse", command=self.browse_output
        )
        self.browse_output_button.grid(row=1, column=2, padx=10)

    def set_config_frame(self):
        tk.Label(root, text="Configuration").pack(
            side=tk.TOP, pady=(15, 0), padx=20, fill=tk.X
        )

        # CONFIG FRAME
        self.config_frame = tk.Frame(self.root, padx=20)
        self.config_frame.pack(side=tk.TOP, pady=(10, 5), padx=20)

        # Size
        tk.Label(self.config_frame, text="Size:").grid(
            row=0, column=0, pady=(10, 5), padx=10
        )
        self.size = tk.Entry(self.config_frame)
        self.size.insert(0, "600")
        self.size.grid(row=0, column=1, padx=5)

        # Distance
        tk.Label(self.config_frame, text="Distance of camera:").grid(
            row=1, column=0, pady=(0, 5), padx=10
        )
        self.distance = tk.Entry(self.config_frame)
        self.distance.insert(0, "60")
        self.distance.grid(row=1, column=1, padx=5)

        # Rotations
        tk.Label(self.config_frame, text="Quantity of rotations:").grid(
            row=2, column=0, pady=(0, 5), padx=10
        )
        self.number_rotations = tk.Entry(self.config_frame)
        self.number_rotations.insert(0, "3")
        self.number_rotations.grid(row=2, column=1, padx=5)

        # Images per rotations
        tk.Label(self.config_frame, text="Number of images per rotation:").grid(
            row=3, column=0, pady=(0, 5), padx=10
        )
        self.images_per_rotation = tk.Entry(self.config_frame)
        self.images_per_rotation.insert(0, "10")
        self.images_per_rotation.grid(row=3, column=1, padx=5)

        # Angle between rotations
        tk.Label(self.config_frame, text="Angle between rotations:").grid(
            row=4, column=0, pady=(0, 5), padx=10
        )
        self.angle_between_rotations = tk.Entry(self.config_frame)
        self.angle_between_rotations.insert(0, "20")
        self.angle_between_rotations.grid(row=4, column=1, padx=5)

    def set_advance_config_frame(self):
        # CONFIG FRAME FOR ADVANCE SETTINGS AND CHECKBOX
        self.advance_title_frame = tk.Frame(self.root, padx=10)
        self.advance_title_frame.pack(side=tk.TOP, pady=(15, 0), padx=20, expand=False)

        tk.Label(self.advance_title_frame, text="Advance configuration").pack(
            side=tk.LEFT
        )
        self.is_advance_options_active = tk.IntVar()
        self.checkbox_advance_options = tk.Checkbutton(
            self.advance_title_frame,
            variable=self.is_advance_options_active,
            command=self.toggle_advance_settings,
        )
        self.checkbox_advance_options.pack(side=tk.LEFT, padx=10)

        # CONFIG FRAME
        self.advance_config_frame = tk.Frame(self.root, padx=10)
        # set layout in toggle functions

        # Init movement
        tk.Label(self.advance_config_frame, text="Init movement:").grid(
            row=0, column=0, pady=(0, 5), padx=10
        )
        self.init_movement = tk.Entry(self.advance_config_frame)
        self.init_movement.insert(0, "0")
        self.init_movement.grid(row=0, column=1, padx=5)

        # end movement
        tk.Label(self.advance_config_frame, text="End movement").grid(
            row=1, column=0, pady=(0, 5), padx=10
        )
        self.end_movement = tk.Entry(self.advance_config_frame)
        self.end_movement.insert(0, "90")
        self.end_movement.grid(row=1, column=1, padx=5)

        # quantity of steps in movement
        tk.Label(self.advance_config_frame, text="Quantity of steps in movement:").grid(
            row=2, column=0, pady=(0, 5), padx=10
        )
        self.steps_in_movement = tk.Entry(self.advance_config_frame)
        self.steps_in_movement.insert(0, "9")
        self.steps_in_movement.grid(row=2, column=1, padx=5)

    def browse_input(self):
        input_file = filedialog.askopenfilename(
            defaultextension=".obj",
            filetypes=[("OBJ files", "*.obj")],
        )
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)

    def browse_output(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_folder)

    def toggle_advance_settings(self):
        if self.is_advance_options_active.get() == 1:
            self.accept_button.pack_forget()
            self.advance_config_frame.pack(side=tk.TOP, pady=10, padx=20)
            self.accept_button.pack(side=tk.TOP, pady=15, padx=10)
        else:
            self.advance_config_frame.pack_forget()

    def set_accept_button(self):
        self.accept_button = tk.Button(
            self.root, text="Generate images", command=self.action_accept_button
        )
        self.accept_button.pack(side=tk.TOP, pady=15, padx=10)

    def action_accept_button(self):

        # GET AND VALIDATE INPUTS
        input = self.input_entry.get()
        output = self.output_entry.get()

        if not input:
            messagebox.showerror("Error", "Please, enter a valid input file.")
            return
        if not output:
            messagebox.showerror("Error", "Please, enter a valid output folder")
            return

        try:
            size = int(self.size.get())
        except ValueError:
            messagebox.showerror("Error", "Please, enter a valid size.")
            return

        try:
            distance = int(self.distance.get())
            number_rotations = int(self.number_rotations.get())
            images_per_rotation = int(self.images_per_rotation.get())
            angle_between_rotations = int(self.angle_between_rotations.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Please, check for blank or bad syntax in configuration inputs"
            )
            return

        try:
            if self.is_advance_options_active.get() == 1:
                init_movement = int(self.init_movement.get())
                end_movement = int(self.end_movement.get())
                steps_in_movement = int(self.steps_in_movement.get())
            else:
                init_movement = 0
                end_movement = 0
                steps_in_movement = 1
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please, check for blank or bad syntax in advance configuration inputs",
            )
            return

        # GENERATE IMAGES
        # create thread to run subprocess, and main thread run animation
        threading.Thread(
            target=self.execute_backend,
            kwargs={
                "input": input,
                "output": output,
                "size": size,
                "number_rotations": number_rotations,
                "images_per_rotation": images_per_rotation,
                "angle_between_rotations": angle_between_rotations,
                "distance": distance,
                "init_movement": init_movement,
                "end_movement": end_movement,
                "steps_in_movement": steps_in_movement,
            },
        ).start()
        self.set_loading_pop_up()

    def execute_backend(
        self,
        input,
        output,
        size,
        number_rotations,
        images_per_rotation,
        angle_between_rotations,
        distance,
        init_movement,
        end_movement,
        steps_in_movement,
    ):
        try:
            result = generate_images(
                input=input,
                output=output,
                size=size,
                numberRotations=number_rotations,
                numberImages=images_per_rotation,
                anglePerRotation=angle_between_rotations,
                distanceOrRadio=distance,
                initMovement=init_movement,
                endMovement=end_movement,
                cantStepMovement=steps_in_movement,
            )
        finally:
            self.root.after(0, self.unset_loading_pop_up)
            if result != 0:
                messagebox.showerror("Error", "The process to generate images failed")

    def set_loading_pop_up(self):
        self.loading_popup = tk.Toplevel(self.root)
        self.loading_popup.geometry("220x70")
        self.loading_popup.title("Generating images...")

        self.label = tk.Label(self.loading_popup, text="Generating images...")
        self.label.pack(pady=10)

        self.loading_label = tk.Label(self.loading_popup, text="")
        self.loading_label.pack()
        self.loading = True
        i = 0
        chars = ["|", "/", "-", "\\"]
        while self.loading:
            c = chars[i]
            self.loading_label.config(text=c)
            self.loading_label.update()

            # wait 100ms but avoiding sleep of python to keet ui executing
            self.loading_popup.after(100)
            i += 1
            if i == 4:
                i = 0
        if self.loading_popup is not None:
            self.loading_popup.destroy()
            self.loading_popup = None

    def unset_loading_pop_up(self):
        self.loading = False


if __name__ == "__main__":
    root = tk.Tk()
    app = GetImagesFromOBJ(root)
    root.mainloop()
