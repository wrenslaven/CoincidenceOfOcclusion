import assetloader
import json
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime

class EmailView:
    def __init__(self, root, controller, canvas):

        self.root = root
        self.controller = controller
        self.canvas = canvas

        self.font = tkfont.Font(family="W95FA", size=12)

        self.emails_to_load_list = []
        self.email_buttons_list = []

        self.PAGE_SIZE = 4
        self.current_page_num = 0

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

        self.current_page_num = 0

        self.email_frame = tk.Frame(self.root, width=500, height=430)
        self.email_frame.grid_propagate(0)

        self.current_email_window = tk.Text(self.email_frame, width=40, height=21, wrap="word", state="disabled", font=self.font)

        self.email_icon_window = tk.Frame(self.email_frame)

        self.email_pagination_frame = tk.Frame(self.email_frame, width=165, height=45)
        self.email_pagination_frame.grid_propagate(0)

        self.prev_button = tk.Button(self.email_pagination_frame, text="<", command=self.load_prev_page,
                                     state="disabled")
        self.next_button = tk.Button(self.email_pagination_frame, text=">", command=self.load_next_page,
                                     state="disabled")
        self.current_emails_label = tk.Label(self.email_pagination_frame, text=f"1 - 4 of 4", width=11)



    def load_email_view(self, event):
        currently_loaded = 0

        self.controller.gamestate = "email"

        desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="teal")
        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)

        icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)
        self.canvas.tag_bind(icon_photos_id, "<Button-1>", self.controller.to_photos_view)

        icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        # Remember not to tag_bind widgets when their window is already up, so they don't stack on top of themselves

        self.canvas.create_window(420, 302, window=self.email_frame)
        self.current_email_window.grid(row=0, column=1)
        self.email_icon_window.grid(row=0, column=0, sticky="nw")
        self.email_pagination_frame.grid(row=1, column=0, sticky="sw")
        self.prev_button.grid(row=0, column=0, padx=10, pady=5, sticky="sw")
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="se")
        self.current_emails_label.grid(row=0, column=1, pady=10)


        self.emails_to_load_list = []
        for email in self.email_dict:
            if self.email_dict[email]["sent"] :
                self.emails_to_load_list.insert(0, email)

        self.load_email_icons(add_new_email=False)

        self.current_emails_label.config(text=f"1 - 4 of {len(self.emails_to_load_list)}")

        self.title_bar_id = self.create_title_bar()

    def create_title_bar(self):
        self.canvas.delete("titlebar", "close_window", "close_window_x")
        self.root.update_idletasks()
        frame_width = self.email_frame.winfo_width()
        frame_x = self.email_frame.winfo_x()
        frame_y = self.email_frame.winfo_y()

        x1 = frame_x
        y1 = frame_y - 30
        x2 = frame_x + frame_width
        y2 = frame_y

        titlebar_id = self.canvas.create_rectangle(x1 - 5, y1, x2 - 5, y2, fill="blue", tags="titlebar")
        self.canvas.tag_raise("close_window")
        self.canvas.tag_raise("close_window_x")

        close_window_id = self.canvas.create_rectangle(x2 - 30, y1 + 5, x2 - 10, y1 + 25, fill="red", tags="close_window")
        self.canvas.tag_bind(close_window_id, "<Button-1>", self.controller.to_computer_view)
        close_window_x = self.canvas.create_text(x2 - 20, y1 + 15, text="X", fill="white", tags="close_window_x")
        self.canvas.tag_bind(close_window_x, "<Button-1>", self.controller.to_computer_view)

        return titlebar_id

    def load_email_icons(self, add_new_email):
        idx_list = []

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

                if i <4:
                    email_button.page_num = 0
                elif 4 <= i < 8:
                    email_button.page_num = 1
                elif 8 <= i < 11:
                    email_button.page_num = 2
                if email_button.page_num == self.current_page_num:
                    email_button.grid(row=i, column=0, pady=(0, 10))
                    idx_list.append(i)

        if len(self.emails_to_load_list) > 4:
            self.prev_button.config(state="normal")
            self.next_button.config(state="normal")
        self.current_emails_label.config(text=f"{min(idx_list) + 1} - {max(idx_list) + 1} of {len(self.emails_to_load_list)}")

    def load_email(self, email_i):
        self.current_email_window.config(state="normal")
        self.current_email_window.delete(1.0, tk.END)

        # Before adding body, add header information
        self.current_email_window.insert(tk.END,"From: ")
        self.current_email_window.insert(tk.END,f"{email_i["sender"]}\n")
        self.current_email_window.insert(tk.END,f"To: ")
        self.current_email_window.insert(tk.END,f"{email_i["recipient"]}\n")
        self.current_email_window.insert(tk.END,f"Sent: ")
        self.current_email_window.insert(tk.END,f"{email_i["timestamp"]}\n")
        self.current_email_window.insert(tk.END,f"Subject: ")
        self.current_email_window.insert(tk.END,f"{email_i["subject"]}\n\n")

        self.current_email_window.insert(tk.END, email_i["body"])

        self.current_email_window.config(state="disabled")

    def send_new_email(self):
        print("This ran")
        self.load_email_icons(add_new_email=True)

        self.controller.mail_sfx.play()

    def update_page_display(self):
        for widget in self.email_icon_window.grid_slaves():
            widget.grid_forget()
        start = self.current_page_num * self.PAGE_SIZE

        end = start + self.PAGE_SIZE
        page_items = self.email_buttons_list[start:end]

        for i, btn in enumerate(page_items):
            btn.grid(row=i, column=0, pady=(0, 10), sticky="w")

        max_page = max(0, (len(self.email_buttons_list) - 1) // self.PAGE_SIZE)

        self.prev_button.config(state="normal" if self.current_page_num > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_page_num < max_page else "disabled")

        total = len(self.email_buttons_list)
        if total > 0:
            self.current_emails_label.config(text=f"{start + 1} - {min(end, total)} of {total}")
        else:
            self.current_emails_label.config(text="0 - 0 of 0")

        self.create_title_bar()

    def load_next_page(self):
        max_page = max(0, (len(self.email_buttons_list) - 1) // self.PAGE_SIZE)
        if self.current_page_num < max_page:
            self.current_page_num += 1
            self.update_page_display()

    def load_prev_page(self):
        if self.current_page_num > 0:
            self.current_page_num -= 1
            self.update_page_display()