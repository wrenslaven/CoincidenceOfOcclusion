import assetloader
import json
import tkinter as tk
from datetime import datetime

#TODO: Add ability to receive more emails over time

class EmailView:
    def __init__(self, root, controller, canvas):

        self.root = root
        self.controller = controller
        self.canvas = canvas

        email_filepath = "emails.json"
        try:
            with open(email_filepath, "r", encoding="utf-8") as file:
                self.email_dict = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{email_filepath}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from the file '{email_filepath}'. Check file format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        self.canvas.delete("all")


        self.image_dict = assetloader.load_images()
        self.screen_bezel = self.image_dict["screen-bezel.png"]
        self.icon_trash = self.image_dict["icon-trash.png"]
        self.icon_telescope = self.image_dict["icon-telescope.png"]
        self.icon_photos = self.image_dict["icon-photos.png"]
        self.icon_email = self.image_dict["icon-email.png"]
        self.back_button = self.image_dict["back-button.png"]

    def load_email_view(self, event):
        self.controller.gamestate = "email"

        self.desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="dark gray")
        self.screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        self.icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)

        self.icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(self.icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        self.icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)

        self.icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        # Remember not to tag_bind widgets when their window is already up, so they don't stack on top of themselves?

        self.back_button_id = self.canvas.create_image(110, 475, image=self.back_button)
        self.canvas.tag_bind(self.back_button_id, "<Button-1>", self.controller.to_parent_gamestate)

        self.email_frame = tk.Frame(self.root, width=600, height=375)
        self.canvas.create_window(400, 290, window=self.email_frame)

        self.context_window = tk.Text(self.email_frame, width=45, height=28, wrap="word", state="disabled")
        self.context_window.tag_configure('bold_tag', font=('Courier', 11, 'bold'))
        self.context_window.tag_configure('normal_tag', font=('Courier', 11))

        self.context_window.grid(row=0, column=1)

        self.email_icon_window = tk.Frame(self.email_frame)
        self.email_icon_window.grid(row=0, column=0, sticky="nw")

        self.emails_to_load_list = []
        for email in self.email_dict:
            if self.email_dict[email]["sent"]:
                self.emails_to_load_list.insert(0, email)

        for i, email in enumerate(self.emails_to_load_list):
            email_by_idx = self.emails_to_load_list[i]
            if self.email_dict[email_by_idx]["sent"]:
                email_button = tk.Button(self.email_icon_window,
                                         text=f"{self.email_dict[email_by_idx]["timestamp"]}\nFrom: {self.email_dict[email_by_idx]["sender"]}\nTo: {self.email_dict[email_by_idx]["recipient"]}",
                                         border=0, highlightthickness=0, justify=tk.LEFT,
                                         command=lambda email_i=self.email_dict[email_by_idx]: self.load_email(email_i))
                email_button.grid(row=i, column=0, pady=(0, 10))


        self.root.after(1000, self.send_new_email)

    def load_email(self, email_i):
        self.context_window.config(state="normal")
        self.context_window.delete(1.0, tk.END)

        # Before adding body, add header information
        self.context_window.insert(tk.END,"From: ", "bold_tag")
        self.context_window.insert(tk.END,f"{email_i["sender"]}\n")
        self.context_window.insert(tk.END,f"To: ", "bold_tag")
        self.context_window.insert(tk.END,f"{email_i["recipient"]}\n")
        self.context_window.insert(tk.END,f"Sent: ", "bold_tag")
        self.context_window.insert(tk.END,f"{email_i["timestamp"]}\n")
        self.context_window.insert(tk.END,f"Subject: ", "bold_tag")
        self.context_window.insert(tk.END,f"{email_i["subject"]}\n\n")

        self.context_window.insert(tk.END, email_i["body"], "normal_tag")

        self.context_window.config(state="disabled")

    def send_new_email(self):
        # First, figure out which email is next in queue.
        self.new_emails_to_load_list = []
        found_unsent_email = False

        for email in self.email_dict:
            if self.email_dict[email]["sent"]:
                self.new_emails_to_load_list.insert(0, email)
            elif not self.email_dict[email]["sent"]:
                self.new_emails_to_load_list.insert(0, email)
                break

        print(self.emails_to_load_list)

        # Then rebuild inbox (remove all email icons so they can be replaced)

        #Get current datetime for the new email
        #TODO: Have this updated in the JSON so when a second new email loads both don't get the new datetime

        for widget in self.email_icon_window.grid_slaves():
            widget.grid_remove()

        for i, email in enumerate(self.new_emails_to_load_list):
            print(self.emails_to_load_list)
            email_by_idx = self.new_emails_to_load_list[i]

            if self.email_dict[email_by_idx]["timestamp"] == 0:
                now = datetime.now()
                formatted_time = now.strftime("%I:%M %p")
                formatted_date = now.strftime("%d/%m/%y")
                self.email_dict[email_by_idx]["timestamp"] = f"{formatted_time}, {formatted_date}"

            email_button = tk.Button(self.email_icon_window,
                                     text=f"{self.email_dict[email_by_idx]["timestamp"]}\nFrom: {self.email_dict[email_by_idx]["sender"]}\nTo: {self.email_dict[email_by_idx]["recipient"]}",
                                     border=0, highlightthickness=0, justify=tk.LEFT,
                                     command=lambda email_i=self.email_dict[email_by_idx]: self.load_email(email_i))
            email_button.grid(row=i, column=0, pady=(0, 10))


            self.controller.mail_sfx.play()