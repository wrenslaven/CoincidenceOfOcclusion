import assetloader
import json
import tkinter as tk
from datetime import datetime

class EmailView:
    def __init__(self, root, controller, canvas):

        self.root = root
        self.controller = controller
        self.canvas = canvas

        self.emails_to_load_list = []
        self.email_buttons_list = []

        email_filepath = "emails/emails.json"
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

        self.current_page_num = 0

        self.email_frame = tk.Frame(self.root, width=600, height=375)

        self.current_email_window = tk.Text(self.email_frame, width=50, height=25, wrap="word", state="disabled")
        self.current_email_window.tag_configure('bold_tag', font=('Courier', 11, 'bold'))
        self.current_email_window.tag_configure('normal_tag', font=('Courier', 11))

        self.email_icon_window = tk.Frame(self.email_frame)
        self.email_pagination_frame = tk.Frame(self.email_frame)
        self.prev_button = tk.Button(self.email_pagination_frame, text="<", command=self.load_prev_page,
                                     state="disabled")
        self.next_button = tk.Button(self.email_pagination_frame, text=">", command=self.load_next_page,
                                     state="disabled")
        self.current_emails_label = tk.Label(self.email_pagination_frame, text="4 of 4")

    def load_email_view(self, event):
        currently_loaded = 0

        self.controller.gamestate = "email"

        desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="dark gray")
        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)

        icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)

        icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        # Remember not to tag_bind widgets when their window is already up, so they don't stack on top of themselves


        back_button_id = self.canvas.create_image(110, 475, image=self.back_button)
        self.canvas.tag_bind(back_button_id, "<Button-1>", self.controller.to_parent_gamestate)

        self.canvas.create_window(420, 290, window=self.email_frame)
        self.current_email_window.grid(row=0, column=1)
        self.email_icon_window.grid(row=0, column=0, sticky="nw")
        self.email_pagination_frame.grid(row=1, column=0, sticky="sw")
        self.prev_button.grid(row=0, column=0, padx=10, pady=10)
        self.next_button.grid(row=0, column=2, padx=5, pady=10)
        self.current_emails_label.grid(row=0, column=1, padx=10, pady=10)


        self.emails_to_load_list = []
        for email in self.email_dict:
            if self.email_dict[email]["sent"] :
                self.emails_to_load_list.insert(0, email)

        self.load_email_icons(add_new_email=False)

        self.current_emails_label.config(text=f"{len(self.emails_to_load_list)} of {len(self.emails_to_load_list)}")


        if len(self.emails_to_load_list) > 4:
            self.prev_button.config(state="normal")
            self.next_button.config(state="normal")
            self.current_emails_label.config(text=f"5 of {len(self.emails_to_load_list)}")

    def load_email_icons(self, add_new_email):
        for widget in self.email_icon_window.grid_slaves():
            widget.grid_remove()
        self.email_buttons_list = []
        self.emails_to_load_list = []
        for email in self.email_dict:
            if self.email_dict[email]["sent"]:
                self.emails_to_load_list.insert(0, email)
            elif not self.email_dict[email]["sent"] and add_new_email:
                self.emails_to_load_list.insert(0, email)
                self.email_dict[email]["sent"] = True
                break

        for i, email in enumerate(self.emails_to_load_list):
            email_by_idx = self.emails_to_load_list[i]
            if self.email_dict[email_by_idx]["sent"]:
                if self.email_dict[email_by_idx]["timestamp"] == 0:
                    now = datetime.now()
                    formatted_time = now.strftime("%I:%M %p")
                    formatted_date = now.strftime("%d/%m")
                    self.email_dict[email_by_idx]["timestamp"] = f"{formatted_time}, {formatted_date}/1993"

                email_button = tk.Button(self.email_icon_window,
                                         text=f"{self.email_dict[email_by_idx]["timestamp"]}\nFrom: "
                                              f"{self.email_dict[email_by_idx]["sender"]}\nTo: "
                                              f"{self.email_dict[email_by_idx]["recipient"]}\nSubject: "
                                              f"{self.email_dict[email_by_idx]["subject"][:10]}"
                                              f"{"..." if len(self.email_dict[email_by_idx]["subject"]) > 10 else ""}",
                                         border=0, highlightthickness=0, justify=tk.LEFT,
                                         command=lambda email_i=self.email_dict[email_by_idx]: self.load_email(email_i))
                self.email_buttons_list.append(email_button)
                if i <= 4:
                    email_button.page_num = 0
                else:
                    email_button.page_num = 1
                if email_button.page_num == self.current_page_num:
                    email_button.grid(row=i, column=0, pady=(0, 10))

    def load_email(self, email_i):
        self.current_email_window.config(state="normal")
        self.current_email_window.delete(1.0, tk.END)

        # Before adding body, add header information
        self.current_email_window.insert(tk.END,"From: ", "bold_tag")
        self.current_email_window.insert(tk.END,f"{email_i["sender"]}\n")
        self.current_email_window.insert(tk.END,f"To: ", "bold_tag")
        self.current_email_window.insert(tk.END,f"{email_i["recipient"]}\n")
        self.current_email_window.insert(tk.END,f"Sent: ", "bold_tag")
        self.current_email_window.insert(tk.END,f"{email_i["timestamp"]}\n")
        self.current_email_window.insert(tk.END,f"Subject: ", "bold_tag")
        self.current_email_window.insert(tk.END,f"{email_i["subject"]}\n\n")

        self.current_email_window.insert(tk.END, email_i["body"], "normal_tag")

        self.current_email_window.config(state="disabled")

    def send_new_email(self):
        print("This ran")
        self.load_email_icons(add_new_email=True)

        if len(self.emails_to_load_list) > 5:
            self.current_emails_label.config(text=f"5 of {len(self.emails_to_load_list)}")
        else:
            self.current_emails_label.config(text=f"{len(self.emails_to_load_list)} of {len(self.emails_to_load_list)}")

        self.controller.mail_sfx.play()

    def load_next_page(self):
        currently_loaded = 0
        for widget in self.email_icon_window.grid_slaves():
            widget.grid_remove()

        self.current_page_num = min(self.current_page_num + 1, 1)
        for i, email_button in enumerate(self.email_buttons_list):
            if email_button.page_num == self.current_page_num:
                email_button.grid(row=i, column=0, pady=(0, 10))
                currently_loaded += 1

        self.current_emails_label.config(
            text=f"{currently_loaded} of {len(self.emails_to_load_list)}")

    def load_prev_page(self):
        currently_loaded = 0
        for widget in self.email_icon_window.grid_slaves():
            widget.grid_remove()

        self.current_page_num = max(self.current_page_num - 1, 0)
        for i, email_button in enumerate(self.email_buttons_list):
            if email_button.page_num == self.current_page_num:
                email_button.grid(row=i, column=0, pady=(0, 10))
                currently_loaded += 1

        self.current_emails_label.config(
            text=f"{currently_loaded} of {len(self.emails_to_load_list)}")