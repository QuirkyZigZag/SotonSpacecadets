import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO



# Who is that member of staff????
# made by Toby tragen

#Credit to Ash Roberts for helping me realise I was using the wrong url

#demo codes # 5xswt6 - Dr Singh # 629j6x - Dr Kaplan # 5yls65 - Miss Colmenarejo # 5z6q8w - Dr Yu

class EmailSearchProgram:
    def __init__(self):
        #setting up the tkinter window
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.root.title("EmailSearch")
        self.root.geometry("1200x720")
        self.root.config(bg="red")

        #setting a default url

        self.url = f"https://www.southampton.ac.uk/people/5xswt6"

        #making all of the PIL images

        bg_img = Image.open("whodat2.jpg_large").convert("RGBA")
        title_img = Image.open("whodatmemberofstaff.png").resize((800,100)).convert("RGBA")
        self.default_img = ImageTk.PhotoImage(Image.open("pikachu.jpg").resize((200,200)).convert("RGBA"))
        questionmark = Image.open("questionmark.png").convert("RGBA")

        #this is why I have not used tkinter since y10...
        #no way to make label backgrounds transparent so I found this paste and masking solution

        bg_img.paste(title_img, (200, 10), mask=title_img)
        bg_img.paste(questionmark,( 1050, 250), mask=questionmark)

        #mind numbing UI placement

        self.poke_img = ImageTk.PhotoImage(bg_img)
        self.bg_label = tk.Label(self.root, image=self.poke_img)
        self.bg_label.place(x=0, y=0)

        self.text_box = tk.Entry(self.root, font=('Helvetica', 16))
        self.info_text = tk.Label(self.root, text="It's...", font=('Helvetica', 12))
        self.enter_button = tk.Button(self.root, text="Find", command=self.submit, bg="yellow", font=('Helvetica', 12))

        self.character_img = tk.Label(self.root, image=self.default_img)

        self.text_box.place(x=800, y=300, width=100, height=50)
        self.enter_button.place(x=925,y=310)
        self.info_text.place(x=200,y=450)
        self.character_img.place(x=200, y=200)

        self.root.mainloop()

    #also my first time using Beautiful soup

    def getInfo(self, user_id: str):
        self.url = f"https://www.southampton.ac.uk/people/{user_id}"
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        image = soup.find_all("img")
        name_tag = soup.find("meta", property="og:title")
        if name_tag and "content" in name_tag.attrs:
            full_title = name_tag["content"]
            name = full_title.split("|")[0].strip()
            self.info_text.config(text=f"It's... {name}!")
            self.info_text.update()
        prof_img = self.get_image(image)
        self.character_img.config(image=prof_img)
        self.character_img.image = prof_img

    def submit(self):
        uid = self.text_box.get()
        
        print("submitted")
        if uid !="":
            self. getInfo(uid)
        else:
            self.info_text.config(text=f"It's... you didn't even try...!")
            self.character_img.config(image=self.default_img)
            self.character_img.image = self.default_img
            self.info_text.update()

    # never had to use BytesIO before, was a cool find

    def get_image(self, image)->ImageTk:
        src = image[0]["src"]
        image_url = urljoin(self.url, src)
       # print("Image URL:", image_url)
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)
    
#probably did not need to be a class but made it so anyway
    
Space1 = EmailSearchProgram()
