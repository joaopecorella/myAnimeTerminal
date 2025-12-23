import pandas as pd
import tkinter as tk
import os
import re
import yaml
import requests
import numpy as np
import threading
import time
import queue
import csv
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence, UnidentifiedImageError
from tk_config import style
from fuzzywuzzy import process
from jikanpy import Jikan
from messages import messages, authors, casey_computer_sequence, casey_computer_name, fugitive, rolling_type_message


class AnimeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("myAnimeTerminal")
        self.geometry(f"1284x820+200+0")
        self.resizable(False, False)
        self.configure(background= "#000000", borderwidth = 0.0)
        
        style(self) # still insecure about this line!
        
        # Shared state
        self.state = {
            "genres": self.load_config("config.yaml", "genres"),
            "studios": self.load_config("config.yaml", "studios"),
            "anime_info": self.load_data(r"data\anime_info_processed.csv"),
            "users_recomendations": self.load_data(r"data\anime_rec_processed.csv"),
            "authors": authors,
            "casey_computer_sequence": casey_computer_sequence,
            "casey_computer_name": casey_computer_name, 
            "fugitive": fugitive}
        
        self.image_loader(filepath = r"misc\actual_design_recent.png", x_loc = 0, y_loc = 0)
        
        self.animation_sequence()

        self.cbox(self.state["genres"], row = 1, exploration = self.threeview_window)
        self.cbox(self.state["studios"], row = 2, exploration = self.threeview_window)
        
        self.search_box()
        
        self.favorites_button()
        self.return_to_home()
        self.delete_favorites_button()
        
        self.update_idletasks()
        
    def image_loader(self, filepath:str, x_loc:int, y_loc:int):

        """

        Loads the image into the main application window. Updates the GUI directly. GIF, PGM, PPM, PNG supported.

        Args:
            filepath (str | filepath): Path to the dataset.
            x_loc (int | tk.Label.place): Represents X location axis of the image.
            y_loc (int | tk.Label.place): Represents Y location axis of the image.

        Returns:
            tk.PhotoImage(): The loaded image.
        """

        try:
            pil_image = Image.open(filepath)
        except Exception as e:
            bg_image = tk.PhotoImage()
            bg_label = tk.Label(self, text = "Image not found. ", borderwidth= 0.0)
            bg_label.place(x = x_loc, y = y_loc)
            return bg_image
        else:
            frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(pil_image)]
            bg_label = tk.Label(self, image=frames[0], background = "#39FF14", borderwidth= 0.0)
            bg_label.image = frames[0]
            bg_label.place(x = x_loc, y = y_loc)
            if len(frames) > 1:
                def animate(index=0):
                    frame = frames[index]
                    bg_label.configure(image=frame)
                    self.after(85, animate, (index + 1) % len(frames))
                animate()

    def load_config(self, filepath:str, index:str):

        '''
        Loads YAML configuration.
        
        Args:
            filepath (str): Path to the YAML config.
            index (str): The string index of the data.

        Raises:
            FileNotFoundError: If the file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
            pd.errors.ParserError: If parsing fails.
        '''
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found {filepath}")                            
        try:                
            with open(filepath) as file:
                config = yaml.safe_load(file)
                return config[index]
        except Exception as e:
            raise RecursionError(f"Failed to load data. {filepath}")
        
    def load_data(self, filepath:str, sep=None):

        '''
        Loads CSV data with optional parameters.
            
        Args:
            filepath (str): Path to the dataset.
            sep (str, optional): Type of column separator.

        Returns:
            pd.DataFrame: Loaded DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
            pd.errors.ParserError: If parsing fails.
        '''
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found {filepath}")
        try:
            if sep is not None:
                return pd.read_csv(filepath, sep = sep)
            return pd.read_csv(filepath)
        except Exception as e:
            raise RecursionError(f"Failed to load data. {filepath}")

    def typewritter_effect(self, text:str, font_size:int, break_line:int, speed:str, width_int:int, height_int:int, x_loc:int, y_loc:int, home_screen_return:bool):
    
        """
        Creates a container and creates a text on the main aplication window, utilizing a typewritter effect. Updates GUI directly or based on a event.
        
        Args:
            text (str): The string to displayed and effected.
            font_size (int): The size of the font.
            break_line (int): breaks a long string with \n. Used to be fitted with the width of the container.
            speed (str | "slow", "fast"): speed of typewritter effect.
            width_int (int): The width of the container. 
            height_int (int): The height of the container.
            x_loc (int): The x location in perspective of the main aplication window.
            y_loc (int): The y location in perspective of the main aplication window.
            home_screen_return (bool): Tags widget for deletion.
        Raises:
            ValueError: if the argument is improperly determined.
        """
        # variables.
        string_var = tk.StringVar()
        
        label = tk.Text(self,
            background="#000000",
            foreground="#39FF14",
            borderwidth= 0.0,
            font=("Flexi IBM VGA True", font_size),
            width = width_int,
            height = height_int)
        label.place(x = x_loc, y = y_loc)
        
        wrapped = re.sub(r"(.{1,%d})(?:\s+|$)" % break_line, r"\1\n", text)

        if speed == "fast":
            for i in wrapped.split(" "):
                j = string_var.get()
                label.insert("end", i + " " + j)
                self.update()
                
        elif speed == "slow":
            for i in wrapped:
                j = string_var.get()
                label.insert("end", i + j)
                self.update()
        else:
            raise ValueError(f"Speed argument is improperly determined.\nUse: 'fast' or 'slow'.\nUsed: {speed}")
        
        if home_screen_return == True:
            label._tag = "delete_me"
        
        return label
    
    def rolling_effect(self, text:str, font_size:int, width_int:int, height_int:int, x_loc:int, y_loc:int):
            """ 
            Creates a container and creates a text on the main aplication window, utilizing a rolling effect. Updates GUI directly or based on a event.
            
            Args:
                text (str): The string to displayed and effected.
                font_size (int): The size of the font.
                width_int (int): The width of the container. 
                height_int: The height of the container.
                x_loc (int): The x location in perspective of the main aplication window.
                y_loc (int): The y location in perspective of the main aplication window.
            Raises:
                ValueError: if the argument is improperly determined.
            """
                
            label = tk.Text(self,
            background="#000000",
            foreground="#39FF14",
            borderwidth= 0.0,
            font=("Flexi IBM VGA True", font_size),
            width = width_int,
            height = height_int)
            label.place(x = x_loc, y = y_loc)

            def animate(i=0):
                if i >= len(text):
                    return
                
                calc = len(text) - i
                string = " " * calc + text[:i + 1]

                label.delete("1.0", "end")
                label.insert("end", "".join(string))

                label.after(300, animate, i + 1)

            animate()

    def animation_sequence(self):
        """
        Displays a set of effects and images to fill the main window. Uses random messages.
        
        """
        
        #variables.
        random_int = np.random.randint(1,3)

        title_animation = self.typewritter_effect(text = casey_computer_name["1"], font_size= 28, speed= "slow", break_line = 38, width_int = 25, height_int = 1, x_loc = 27, y_loc = 29, home_screen_return = False) 
        poem_animation = self.typewritter_effect(text = casey_computer_sequence["1"], font_size= 17, speed= "slow", break_line = 38, width_int = 40, height_int = 14, x_loc = 27, y_loc = 102, home_screen_return = False) 
        
        title_animation.after(120, title_animation.destroy)
        poem_animation.after(120, poem_animation.destroy)

        authors_name = self.typewritter_effect(text= authors[f"{random_int}"], font_size= 28, speed= "slow", break_line = 38, width_int = 25, height_int = 1, x_loc = 27, y_loc = 29, home_screen_return= False)
        authors_message = self.typewritter_effect(text = messages[f"{random_int}"],font_size= 17, speed= "slow", break_line = 38, width_int = 40, height_int = 14, x_loc = 27, y_loc = 102, home_screen_return = False)
        human_incomplete_image = self.image_loader(filepath = r"misc\incomplete_resized.gif", x_loc= 26, y_loc = 459)
        neon_city_image = self.image_loader(filepath = r"misc\contender_resized.gif", x_loc= 456, y_loc = 24)
        map_city_image = self.image_loader(filepath=  r"misc\map_with_effect_resized.png", x_loc= 457, y_loc= 460)  
        fugitive_image = self.image_loader(filepath = r"misc\kav_effect_resized.png", x_loc = 846, y_loc = 26)
        fugitive_status = self.typewritter_effect(text = fugitive["1"], font_size= 15, break_line= 30, speed = "slow", height_int= 7, width_int= 32, x_loc= 997, y_loc= 28, home_screen_return = False)
        ghost_gif = self.image_loader(filepath = r"misc\ghost_image_resized.gif", x_loc = 845, y_loc = 200)
        rolling_message = self.rolling_effect(text = rolling_type_message[f"{random_int}"], font_size = 38, width_int= 55, height_int = 1, x_loc= 27, y_loc= 724)

    def cbox(self, text:str, row:int, exploration:callable):
        """
        Creates a combobox for a given string in the main aplication window. Updates the 
        GUI directly. Binds the returned value to a callback event

        Args:
            text (tk.StringVar | str): The text to be displayed.
            row (int): The row of which the combobox will be displayed.
            exploration (function): Callback event.
        
        """

        # variables.
        y = row * 28
        n = tk.StringVar()
        font_and_size = ("Flexi IBM VGA True", 13)

        # purposly conflicted with the style class to enforce matching width with other widgets.
        label_choosen = ttk.Combobox(self, width = 13, textvariable = n, font = font_and_size)
        label_choosen.place(x = 1140, y = y + 52)
        label_choosen['values'] = text
        label_choosen.current(0)

        # The popdown string values cannot be configured using the style class.

        self.option_add("*TCombobox*Listbox*Background", "#000000")
        self.option_add('*TCombobox*Listbox.foreground', '#39FF14')
        label_choosen.option_add('*TCombobox*Listbox.font', font_and_size)

        label_choosen.bind("<<ComboboxSelected>>", lambda _ : exploration(label_choosen.get()))

    def threeview_window(self, value:tk.StringVar):

        """
        Callback event binded to cbox. Uses the user returned string to create a ttk.Treeview displaying a sorted DataFrame based on the inputted value and diplays API widgets feature.
        Binds the new returned user value of this widget to a recursive_event.

        Args:
            value (ttk.Combobox.get| tk.StringVar): The string selected from combobox.
        """
        # variables
        selected = value
        data = self.state["anime_info"]

        # container
        window = tk.Frame(master = self, borderwidth= 0.0)
        window.place(x = 456, y = 460)
        window._tag = "delete_me"

        if selected in self.state["genres"]:

            filtered_data = data[data["Genres"].str.contains(selected, na=False)]
            sorted_data = filtered_data.sort_values("Completed_count", ascending = False)
            sorted_data.drop(["Unnamed: 0", "Anime_id", "Completed_count", "Genres"], axis = 1, inplace = True)

            sorted_by_status = self.typewritter_effect(text = f"Sorted by: {selected}", font_size = 28, break_line= 38, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return= True)
            
            tree = ttk.Treeview(window, columns=list(sorted_data.columns), show="headings")
            tree._tag = "delete_me"
                
            for column in sorted_data.columns:
                tree.heading(column, text=column)
            for _, row in sorted_data.iterrows():
                tree.insert("", "end", values=list(row))
                
            tree.pack(expand=True, fill='both')
            
            tree.bind("<Double-1>", lambda event: self.recursive_event(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
            tree.bind("<Double-1>", lambda event: self.jikan_api(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
            tree.bind("<Button-3>", lambda event: self.file_favorite_treatment(tree.item(tree.identify_row(event.y))["values"][0]), add='+') # New.

        elif selected in self.state["studios"]:
            
            filtered_data = data[data["Studios"].str.contains(selected, na=False)]
            sorted_data = filtered_data.sort_values("Completed_count", ascending = False)
            sorted_data.drop(["Unnamed: 0", "Anime_id", "Completed_count", "Genres"], axis = 1, inplace = True)

            sorted_by_status = self.typewritter_effect(text = f"From: {selected}", font_size = 28, break_line= 38, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return = True)

            tree = ttk.Treeview(window, columns=list(sorted_data.columns), show="headings")
            tree._tag = "delete_me"

            for column in sorted_data.columns:
                tree.heading(column, text=column)
            for _, row in sorted_data.iterrows():
                tree.insert("", "end", values=list(row))
                
            tree.pack(expand=True, fill='both')

            tree.bind("<Double-1>", lambda event: self.recursive_event(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
            tree.bind("<Double-1>", lambda event: self.jikan_api(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
            tree.bind("<Button-3>", lambda event: self.file_favorite_treatment(tree.item(tree.identify_row(event.y))["values"][0]), add='+') # New.

    def recursive_event(self, event:tk.StringVar):
        """
        Callback event binded to threeview_window. Uses the user returned value to diplay a ttk.Treeview recomendation three. Binds the inputted value and diplays API widgets feature.

        Args:
            value (ttk.Combobox.get| tk.StringVar): The string selected from threeview_window.
        
        """
        
        # variables.
        selected = event
        data = self.state["anime_info"]
        data = self.state["anime_info"]
        user_recomendations = self.state["users_recomendations"]


        if (data["Title"] == selected).any():

            filtered_data = data[data['Title'] == selected]['Anime_id'].iloc[0]
            grouped_data = user_recomendations[user_recomendations['Animea'] == filtered_data].groupby('Num_recommenders').first()
            index_data_sorted = grouped_data.sort_values(by = ['Num_recommenders'], ascending = False)
            recomendation_data = data[data['Anime_id'].isin(index_data_sorted['Animeb'].values)]  
            
            user_data = recomendation_data.copy()
            user_data.drop(["Unnamed: 0", "Anime_id", "Completed_count", "Genres"], axis = 1, inplace = True)

            similar_to_statues = self.typewritter_effect(text = f"Similar to: {selected}", font_size = 28, break_line= 38, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return = True)


            window = tk.Frame(master = self, borderwidth= 0.0)
            window.place(x = 456, y = 460)
            window._tag = "delete_me"

            tree = ttk.Treeview(window, columns=list(user_data.columns), show="headings")
            tree._tag = "delete_me"

            for column in user_data.columns:
                tree.heading(column, text=column)
            for _, row in user_data.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack( expand=True, fill='both')

            tree.bind("<Double-1>", lambda event: self.jikan_api(tree.item(tree.identify_row(event.y))["values"][0]))
            tree.bind("<Button-3>", lambda event: self.file_favorite_treatment(tree.item(tree.identify_row(event.y))["values"][0]), add='+') # New.

        else: # Always if the search bar has found nothing.
            
            # variables.
            user_query = selected
            choices = data["Title"]

            what_did_you_mean_status = self.typewritter_effect(text = f"What did you mean? ", font_size = 28, break_line= 38, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return= True)
            
            best_match = process.extract(user_query, choices)
            temp_names = []

            if best_match:
                for i in best_match:
                    temp_names.append(*i[0:1])

            user_data_did_you_mean = pd.DataFrame({"Title": temp_names})

            window = tk.Frame(master = self, borderwidth= 0.0)
            window.place(x = 456, y = 460)
            window._tag = "delete_me"

            tree = ttk.Treeview(window, columns=list(user_data_did_you_mean.columns), show="headings")
            tree._tag = "delete_me"
            
            tree.column("Title", width=800, stretch=False) # This makes sure that the spanwed tree fits the aplication. 

            for column in user_data_did_you_mean.columns:
                tree.heading(column, text=column)
            for _, row in user_data_did_you_mean.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack( expand=True, fill='both' )
            
            tree.bind("<Button-3>", lambda event: self.file_favorite_treatment(tree.item(tree.identify_row(event.y))["values"][0]), add='+')

            """
            NOTE:

            If the first condition is False, a tree will be spawn to display alternatives using the levenshtein distance in reference to the inputted value.
            
            Also, this tree will also be binded to recursive_event, which will call upon itself, and then, the first condition will be True. Given the is drawn uppon the very same Database, won't be a dismatch.
            
            More on Levenshtein distance: https://en.wikipedia.org/wiki/Levenshtein_distance
            """

            tree.bind("<Double-1>", lambda event: self.recursive_event(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
            tree.bind("<Double-1>", lambda event: self.jikan_api(tree.item(tree.identify_row(event.y))["values"][0]), add='+')

    def jikan_api(self, event:tk.StringVar):
        """
        Callback event binded to threeview_window and recursive_event. Uses Jikanpy-V4 API to request two JSON files about the user inputted value.

        Args:
            value (ttk.Combobox.get| tk.StringVar): The string selected from threeview_window and recursive_event.

        See more on: https://jikanpy.readthedocs.io/en/latest/
        """
        # Variables

        value = event
        raw_data = self.state["anime_info"]
        anime_id = int(raw_data[raw_data["Title"] == value]["Anime_id"].values[0])
        
        # Queue for thread results
        result_queue = queue.Queue()

        def worker():
            try:
                j = Jikan()
                data_info = j.anime(anime_id)
                data_reviews = j.anime(anime_id, extension="reviews")
                time.sleep(1)
                result_queue.put(("ok", data_info, data_reviews))
            except Exception as e:
                result_queue.put(("error", str(e)))

        # Launch thread
        threading.Thread(target=worker, daemon=True).start()

        # Poll the queue without blocking UI
        def check_queue():
            try:
                status, *payload = result_queue.get_nowait()
            except queue.Empty:
                self.after(20, check_queue)
                return
            
            if status == "ok":
                data_info, data_reviews = payload
                self.load_api_widgets(data_info)
                self.load_api_reviews(data_reviews)
            else:
                error_message = payload[0]
                self.typewritter_effect(
                    text=f"Error: {error_message}",
                    font_size=28,
                    break_line=38,
                    speed="slow",
                    width_int=49,
                    height_int=1,
                    x_loc=462,
                    y_loc=388,
                    home_screen_return=True
                )

        # Start polling
        self.after(100, check_queue)

    def image_loader_url(self, url:str, x_resize:int, y_resize:int):
        
        """
        Loads the image from a URL.  

        Args:
            x_resize (int| Image.open.resize): To resize the image based on a given x axis.  
            y_resize (int| Image.open.resize): To resize the image based on a given y axis.  
        Raises: 
            requests.exceptions.RequestException: if an ambiguous exception happens while handling the request.
            UnidentifiedImageError: if an image cannot be opened and identified.
            OSError: for I/O related errors.

        """
        try: 
            
            pil_image = Image.open(requests.get(url, stream=True).raw).resize(size = (x_resize, y_resize))# A little to crypt for my taste.
            tk_image = ImageTk.PhotoImage(pil_image)
            image_label = tk.Label(self, image=tk_image, background= "#000000", borderwidth= 0.0)
            image_label._tag = "delete_me"
            image_label.image = tk_image # avoids tkinter garbage collector.
            image_label.place(x = 455, y = 24)
        
        except (requests.exceptions.RequestException, UnidentifiedImageError, OSError) as e:
            
            print(f"Error loading image: {e}")

    def load_api_widgets(self, value:tk.StringVar):

        """
        Callback event binded to jikan_api. Assembles API widgets feature and displays onto the screen. Updates GUI directly.
        
        Args:
            value (ttk.Combobox.get| tk.StringVar): The string selected from threeview_window and recursive_event.
        """
        request = value
        
        response_synopsis = request["data"]["synopsis"]
        response_name = request["data"]["title"]
        response_image = request["data"]["images"]["jpg"]["large_image_url"]

        title_widget = self.typewritter_effect(text = response_name, font_size= 28, speed= "slow", break_line = 38, width_int = 25, height_int = 1, x_loc = 27, y_loc = 29, home_screen_return= True)
        image_widget = self.image_loader_url(url = response_image, x_resize = 364, y_resize = 325)
        synopsis_widget = self.typewritter_effect(text = response_synopsis, font_size= 17, speed= "slow", break_line = 38, width_int = 40, height_int = 14, x_loc = 27, y_loc = 102, home_screen_return= True)

    def load_api_reviews(self, value:tk.StringVar):
        """
        Callback event binded to jikan_api. Assembles reviews and displays onto the screen. Updates GUI directly.

         Args:
            value (ttk.Combobox.get| tk.StringVar): The string selected from threeview_window and recursive_event.

        """
        # variables.    
        request = value
        text = []

        for review in request.get('data', []):
            text.append(f"User: {review['user']['username'][:3] + '█' * 10}")
            text.append(f"Score: {review['score']}")
            text.append(f"Content: {review['review']}")
            text.append("__" * 30)
        reviews_widget = self.typewritter_effect(text = "\n".join(text), font_size = 14, break_line= 152, speed= "fast", width_int= 152, height_int= 3, x_loc= 27, y_loc= 724, home_screen_return= True) # x_loc, y_loc done.

    def search_box(self):

        """
        Creates a search box for a given string in the main aplication window. Capitalizes the returned string for a better matching. Updates the GUI directly. Binds the returned inputted value to recursive_event.
        
        """
        # variable.
        _ = tk.StringVar()
        font_and_size = ("Flexi IBM VGA True", 13)
        
        search_entry = tk.Entry(self, textvariable = _ , background="#39FF14", foreground="#080B08", font= font_and_size, width= 15)
        search_entry.place(x = 1140, y = 146)
            
        def capitalize_after_space(text:str):
            """
            Capitalizes strings after space (internally).

            Args:
                text (str) = A string to be processed.
            """
            words = text.split(' ')  
            capitalized_words = [word.capitalize() for word in words]
            return ' '.join(capitalized_words)


        search_entry.bind("<Return>", lambda event: (self.recursive_event(capitalize_after_space((search_entry.get()))), 
                                                    search_entry.delete(0, "end")))

    def return_to_home(self):

        """
        Creates button to return to home screen. Widgets to be deleted maped previosly. Updates GUI directly.

        """
            
        close_window_frame = tk.Label(self, borderwidth= 0 )
        close_window_frame.place(x = 1220, y = 28)


        def delete_widgets():
            for w in self.winfo_children():
                if getattr(w, "_tag", "") == "delete_me":
                    w.destroy()




        button = tk.Button(close_window_frame, text = "HOME", command = lambda: delete_widgets(),
                        background="#39FF14",
                        foreground="#000000",
                        font=("Flexi IBM VGA True", 11)
                        )
        
        button.pack()

    def file_favorite_treatment(self, value:tk.StringVar):
        """
        Callback event. Informs the user if a title have been added into the favorites. Creates a CSV file with the user favorite animes. Updates the GUI directly.
        """
        # variables.
        selected = value
        filepath = "saved_titles.csv"
        saved_files = []
        
        if selected:

            favorite_status = self.typewritter_effect(text = f"{selected} has been favorited.", font_size = 28, break_line= 38, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return= True)
            favorite_status.after(600, favorite_status.destroy)

            if not os.path.isfile(filepath):
                with open(file = filepath, mode = "w", newline = "") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Title"])
                    writer.writerow([selected])
            else:
                with open(filepath, "r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            saved_files.append(row[0])

                if selected not in saved_files:
                    with open(filepath, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([selected])

    def favorites_button(self):

            """
            Callback event. Creates a button and commands a ttk.three to spawn containing the user favorite titles. Updates GUI directly.
            """

            # variables. 
            filepath = "saved_titles.csv"

            def favorite_tree():

                if os.path.isfile(filepath):

                    window = tk.Frame(master = self, borderwidth= 0.0)
                    window.place(x = 456, y = 460)
                    window._tag = "delete_me"

                    sorted = pd.read_csv(filepath)
                    
                    tree = ttk.Treeview(window, columns=list(sorted.columns))
                    tree.column("Title", width=600, stretch=False)
                    tree._tag = "delete_me"
                        
                    for column in sorted.columns:
                        tree.heading(column, text=column)
                    for _, row in sorted.iterrows():
                        tree.insert("", "end", values=list(row))
                        
                    tree.pack(expand=True, fill='both')

                    tree.bind("<Double-1>", lambda event: self.recursive_event(tree.item(tree.identify_row(event.y))["values"][0]), add='+')
                    tree.bind("<Double-1>", lambda event: self.jikan_api(tree.item(tree.identify_row(event.y))["values"][0]), add='+')

                else:
                    favorite_status = self.typewritter_effect(text = f"No favorites yet.", font_size = 28, break_line= 50, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return= True)
                    favorite_status.after(550, favorite_status.destroy)
                
            
            close_window_frame = tk.Label(self, borderwidth= 0 )
            close_window_frame.place(x = 1178, y = 28)

            
            button = tk.Button(close_window_frame,
                               text = "SAVED",
                               command = lambda: favorite_tree(),
                               background="#39FF14",
                               foreground="#000000",
                               font=("Flexi IBM VGA True", 11)
                            )
            
            button.pack()

    def delete_favorites_button(self):

        """
        Deletes file containing user favorites. Informs the user about the operation.
        """
        # variables.
        filepath = "saved_titles.csv"

        def favorite_deletion():
            if os.path.isfile(filepath):
                os.remove(filepath)
            else:
                favorite_status = self.typewritter_effect(text = f"No favorites to delete.", font_size = 28, break_line= 50, speed = "slow", width_int= 49, height_int= 1, x_loc= 462, y_loc= 388, home_screen_return= True)
                favorite_status.after(550, favorite_status.destroy)

        close_window_frame = tk.Label(self, borderwidth= 0 )
        close_window_frame.place(x = 1148, y = 28)


            
        button = tk.Button(close_window_frame,
                               text = "DEL",
                               command = lambda: favorite_deletion(),
                               background="#39FF14",
                               foreground="#000000",
                               font=("Flexi IBM VGA True", 11)
                            )
            
        button.pack()


if __name__ == "__main__":
    app = AnimeApp()
    app.mainloop()

# Needs to make sure the font is present in the system.
# And also, fix the comment section, it's terrible. It may be an overhull needed.
# Makes sure anime_processing runs begore launch. 



