import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

def main():
    MainWindow()

DB_NAME = "route_database2.txt"

##window for input driver delivery report: window choose stop number-> window input delivery time -> update del_time to database
def driver_delivery():
    ##window choose stop number
        ##open database
    try:
        with open(DB_NAME, 'r') as file:
            content = file.readlines()
        ##choose stop number frame
            input_costumer = tk.Toplevel()
            input_costumer.title = ("Driver Delivery Report")
            input_costumer.geometry = ("200x200")
        ##make widget: list for stop number combobox/dropdown (input_stop_combobox)
            total_stop = len(content)-1
            # print (total_stop)
            stop_list = []
            for i in range (0,total_stop):
                stop_list.append(i+1)
            input_stop_label = tk.Label (input_costumer, text = "Choose Your Packages Stop")
            input_stop_label.grid (row = 0 ,column = 0,padx = 5, pady = 5, sticky= "w") 
            input_stop_combobox = ttk.Combobox(input_costumer, values= stop_list)
            input_stop_combobox.grid(row=1, column=0, padx = 20, pady = 5)

    ##window input delivery time
            def input_deliv_time():
        ##frame and widget
                input_driver = tk.Toplevel()
                input_driver.title = ("Driver Input")
                input_driver.geometry = ("200x200")

                input_time_label = tk.Label (input_driver, text = "How Much Time You Need To Delivered This Stop? \nCalculate Time Since Last Stop/Warehouse \nExp:5 minutes 30 seconds You can input '5.5'")
                input_time_label.grid (row = 0 ,column = 0,padx = 5, pady = 5, sticky= "w")
                input_time_entry = tk.Entry(input_driver)
                input_time_entry.grid (row = 1 ,column = 0, padx = 5, pady = 5)
    ##update del_time to database
                def update_time():
                    # print ("update rating tips")
        ##messagebox for driver to confirm input_data and update to database                        
                    stop_to_update = int(input_stop_combobox.get())
                    new_stop_time = float(input_time_entry.get())
                    ask_rating = tk.messagebox.askquestion (title = None, message = f"Confirm {new_stop_time} minutes for this Stop delivery time?")
                    # print (ask_rating)
                    if ask_rating == "yes":
                        # print ("Choose Yes")
        ##update database: read database-> split and strip data to make new list ->define new stop list ->update database
            ##read database
                        with open(DB_NAME, 'r') as file:
                            content = file.readlines()
            ##split and strip data to make new list
                            split_content = content[stop_to_update].split(",")
                            new_stop_list = []
                            for i in split_content:
                                strip_i = i.strip(":[] ''\n")
                                new_stop_list.append(strip_i) #strip dan split, terus append
                            #     print(new_stop_list)
                            # print (new_stop_list[7])
            ##define new stop list (same format as database from create) with new_del_time
                            new_stop_volume = float(new_stop_list[2])
                            new_stop_weight = float(new_stop_list[3])
                            new_stop_pay = float(new_stop_list[4])
                            new_stop_tips = float(new_stop_list[6])
                            new_stop_rating = int(new_stop_list[7])
                            new_stop_list[1] = stop_to_update
                            new_stop_list[2] = new_stop_volume
                            new_stop_list[3] = new_stop_weight
                            new_stop_list[4] = new_stop_pay
                            new_stop_list[5] = new_stop_time                            
                            new_stop_list[6] = new_stop_tips
                            new_stop_list[7] = new_stop_rating

                ##trick for get same karakter as format in create
                    ##count all index len
                            length_new_stop_entry = 0
                            for i in new_stop_list:
                                # print (i)
                                str_i = str(i)
                                length_new_stop_entry += len(str_i)
                            # print (new_stop_list)
                            # print (new_stop_tips)
                            # print (new_stop_rating)
                            # print (len(new_stop_list))
                            # print (length_new_stop_entry)
                ##new stop entry with same total character
                            new_stop_entry = f"{new_stop_list}{" "*(70-length_new_stop_entry-19)}:\n" #18 = 1+kurung siku, koma atas, koma bawah white space
            ##update database
                            try:
                                with open(DB_NAME,'r+',encoding="utf-8") as file: #r+ to replace data
                                    file.seek(72*stop_to_update)   
                                    file.write(new_stop_entry) 
                            except:
                                print("error updating data")
                        input_driver.destroy()
                        input_costumer.destroy()   
                    
                    elif ask_rating == "no":
                        input_driver.destroy()
                        input_costumer.destroy()
                        # print ("Choose No") #you can pass another task/function

                ##button window input del_time
                button_input = tk.Button(input_driver, text="Save", command= update_time)
                button_input.grid(row=3, column=0, sticky="news", padx=5, pady=5)
            ##button window choose stop
            button = tk.Button(input_costumer, text="Next", command= input_deliv_time)
            button.grid(row=2, column=0, sticky="news", padx=5, pady=5)
    except:
        print("Error Read Database")
        return False

##driver payment: sum weight to get weight koef ->find total payment with weight koef -> get total payment (you_got) and show in message box 
##total payment = sum(base pay*weight koef*rating koef*time koef)+sum tips
def driver_payment():
    ##sum weight to get weight koef
    print ("Your Payment for route number: is  ")
        ##read database
    try:
        with open(DB_NAME, 'r') as file:
            content = file.readlines()
        ##make new list, split, strip and append list
            
            print ("disini ok1")
            count_stop = len(content)
            print (count_stop)
            new_packages_list = []
            for i in range(1,count_stop): #not include header
                print(f"this is index i form database: {content[i]}")
                split_content = content[i].split(",")
                new_stop_list = []
                for i in split_content:
                    strip_i = i.strip(":[] ''\n")
                    new_stop_list.append(strip_i) #strip and split, then append
                    print(f"new list with split and split from index i of database: {new_stop_list}")
                new_packages_list.append(new_stop_list)        
        
        # print (f"new_packages_list3 : {new_packages_list}")
        ##find total weight. weight koef and total tips
        print ("disini ok2")
        sum_weight = 0
        sum_tips = 0
        for i in new_packages_list:
            # for a in b:
            new_stop_weight = float(i[3])
            new_stop_tips = float(i[6])
            sum_weight += new_stop_weight
            sum_tips += new_stop_tips 

        # print (sum_weight)
        if sum_weight > 500:
            weight_koef = 1
        elif sum_weight> 400 and sum_weight<=500:
            weight_koef = 0.85
        elif sum_weight> 300 and sum_weight<=400:
            weight_koef = 0.7
        elif sum_weight> 200 and sum_weight<=300:
            weight_koef = 0.55
        elif sum_weight <=200:
            weight_koef = 0.4
        # weight_koef = 0.85
        # print (sum_tips)

    ##find total payment with weight koef 
        sum_payment = 0
        print ("disini ok3")
        for i in new_packages_list:
            new_base_pay = float(i[4])
            new_stop_time = float(i[5])
            if new_stop_time >= 0:
                time_koef = 1
            else:
                time_koef = 0
            new_stop_rating = int(i[7])
            if new_stop_rating == 5:
                rating_koef = 1
            elif new_stop_rating == 4:
                rating_koef = 0.9
            elif new_stop_rating == 3:
                rating_koef = 0.8
            elif new_stop_rating == 2:
                rating_koef = 0.7
            elif new_stop_rating == 1:
                rating_koef = 0.6
            else:
                print ("Wrong Rating Customer")
            stop_payment = new_base_pay*weight_koef*rating_koef*time_koef
            print (f"payment stop ke {i} = {stop_payment}")
            sum_payment += stop_payment        
        # print (f"total payment for this route = {sum_payment}")

            
    except:
        print("Error Read Database")
        return False

    ## get total payment (you_got) and show in message box
    you_got = sum_payment + sum_tips
    tk.messagebox.showinfo(title = "Driver Payment", message = f"Your Payment for this route is ${you_got:.2f}" )                   

##window for Costumer input tips and rating: window for choose stop number ->
def costumer():
    # print ("input costumer rating")  
    ##window and widget for choose stop number
        ##read database 
    try:
        with open(DB_NAME, 'r') as file:
            content = file.readlines()
        ##make list for combobox stop number
            number_stop = len(content) #coz start from 1, content include header
            print (number_stop)
            stop_list = []
            for i in range (1,number_stop):
                stop_list.append(i)
    ##make window and widget for choose stop number
            input_costumer = tk.Toplevel()
            input_costumer.title = ("Costumer Input")
            input_costumer.geometry = ("200x200")

            input_stop_label = tk.Label (input_costumer, text = "Choose Your Packages Stop")
            input_stop_label.grid (row = 0 ,column = 0,padx = 5, pady = 5, sticky= "w") 
            input_stop_combobox = ttk.Combobox(input_costumer, values= stop_list)
            input_stop_combobox.grid(row=1, column=0, padx = 20, pady = 5)
            #window for input rating and tips
            def input_rating_tips():
                input_costumer_rating = tk.Toplevel()
                input_costumer_rating.title = ("Costumer Input")
                input_costumer_rating.geometry = ("200x200")

                input_rating_label = tk.Label (input_costumer_rating, text = "Rating Your Packages Delivery ")
                input_rating_label.grid (row = 0 ,column = 0,padx = 5, pady = 5, sticky= "w")
                input_rating_combobox = ttk.Combobox(input_costumer_rating, values= [1,2,3,4,5])
                input_rating_combobox.grid(row=1, column=0, padx = 5, pady = 5)

                input_tips_label = tk.Label (input_costumer_rating, text = "Tips for Driver")
                input_tips_label.grid (row = 2 ,column = 0,padx = 5, pady = 5, sticky= "w")
                input_tips_entry = tk.Entry(input_costumer_rating)
                input_tips_entry.grid (row = 3 ,column = 0, padx = 5, pady = 5)

                ##update rating n tips to database
                def update_rating_tips(): 
                    # print ("update rating tips")
                    ##get value
                    stop_to_update = int(input_stop_combobox.get()) 
                    new_stop_rating = int(input_rating_combobox.get()) 
                    new_stop_tips = float(input_tips_entry.get())
                    print (f"stop to update : {stop_to_update} with new rating = {new_stop_rating} and tips = {new_stop_tips}")
                    ##messagebox to confirm and update database
                    ask_rating = tk.messagebox.askquestion (title = None, message = f"Confirm for stop number {stop_to_update}: rate {new_stop_rating} and tip ${new_stop_tips}" )
                    print (ask_rating)
                    if ask_rating == "yes":
                        print ("Choose Yes")
                        ##update database: read database-> split and strip data to make new list ->define new stop list ->update to database
                            ##read database
                        with open(DB_NAME, 'r') as file:
                            content = file.readlines()
                            # print (f"length database = {len(DB_NAME)}")
                            # print (f"length content = {len(content)}")
                            # print (content[stop_to_update])
                            ##split and strip data to make new list
                            split_content = content[stop_to_update].split(",")
                            new_stop_list = []
                            for i in split_content:
                                strip_i = i.strip(":[] ''\n")
                                new_stop_list.append(strip_i) #strip and split, then append
                                print(new_stop_list)                            
                            ##define new stop list
                            new_stop_volume = float(new_stop_list[2])
                            new_stop_weight = float(new_stop_list[3])
                            new_stop_pay = float(new_stop_list[4])
                            new_stop_time = float(new_stop_list[5])

                            new_stop_list[1] = stop_to_update
                            new_stop_list[2] = new_stop_volume
                            new_stop_list[3] = new_stop_weight
                            new_stop_list[4] = new_stop_pay
                            new_stop_list[5] = new_stop_time                            
                            new_stop_list[6] = new_stop_tips
                            new_stop_list[7] = new_stop_rating
                            # new_stop_entry = f"{new_stop_list}{" "*(70-len(new_stop_list))}a\n"
                            ##trick
                            length_new_stop_entry = 0
                            for i in new_stop_list:
                                # print (i)
                                str_i = str(i)
                                length_new_stop_entry += len(str_i)
                            # print (new_stop_list)
                            # print (new_stop_tips)
                            # print (new_stop_rating)
                            # print (len(new_stop_list))
                            # print (length_new_stop_entry)
                            new_stop_entry = f"{new_stop_list}{" "*(70-length_new_stop_entry-19)}:\n" #18 = 1+kurung siku, koma atas, koma bawah white space
                            ##update to database
                            try:
                                with open(DB_NAME,'r+',encoding="utf-8") as file: # r+ to replace
                                    file.seek(72*stop_to_update)
                                    file.write(new_stop_entry) 
                            except:
                                print("error updating data")
                            
                        input_costumer.destroy()
                        input_costumer_rating.destroy()
                    elif ask_rating == "no":
                        print ("Choose No")
        ##button for input rating n tips
                button_input = tk.Button(input_costumer_rating, text="Save", command= update_rating_tips)
                button_input.grid(row=4, column=0, sticky="news", padx=5, pady=5)
    ##button for choose stop 
            button = tk.Button(input_costumer, text="Next", command= input_rating_tips)
            button.grid(row=2, column=0, sticky="news", padx=5, pady=5)
    except:
        print("Error Read Database")
        return False

##class to make main window with tkinter      
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Treasure Delivery")
        self.geometry("250x300")

        self.create_widgets()

        self.mainloop()

    ##create widget for main window, menu input     
    def create_widgets(self):
        welcome = tk.LabelFrame (self, text = "WELCOME")
        welcome.grid(row = 0 ,column = 0, sticky= "w")
        welcoming = tk.Label (welcome, text = "WELCOME TO TREASURE DELIVERY,\nTHE FUTURE DELIVERY")
        welcoming.grid(row = 0 ,column = 0,padx = 5, pady = 20, sticky= "w")
        info = tk.Label (welcome, text = "Please choose these option below: ")
        info.grid(row = 1 ,column = 0, padx = 5, pady = 5, sticky= "w")
        global create_var #global so it can called outside the function but still inside class
        global delivery_var 
        global rating_var 
        global payment_var 
        create_var = tk.StringVar(value="Not Choose")
        delivery_var = tk.StringVar(value="Not Choose")
        rating_var = tk.StringVar(value="Not Choose")
        payment_var = tk.StringVar(value="Not Choose")
        create_check = tk.Checkbutton (self, text= "Create Route", variable=create_var, onvalue="Choose", offvalue="Not Choose")
        delivery_check = tk.Checkbutton (self, text= "Driver Delivery", variable=delivery_var, onvalue="Choose", offvalue="Not Choose")
        rating_check = tk.Checkbutton (self, text= "Costumer Rating", variable=rating_var, onvalue="Choose", offvalue="Not Choose")
        payment_check = tk.Checkbutton (self, text= "Driver Payment", variable=payment_var, onvalue="Choose", offvalue="Not Choose")
        create_check.grid(row=2, column=0, padx = 5, pady = 5, sticky= "w")
        delivery_check.grid(row=3, column=0, padx = 5, pady = 5, sticky= "w")
        rating_check.grid(row=4, column=0, padx = 5, pady = 5, sticky= "w")
        payment_check.grid(row=5, column=0, padx = 5, pady = 5, sticky= "w")

        button_frame = tk.Frame (self)
        button_frame.grid (row = 6, column=0)
        button = tk.Button(button_frame, text="Next", command= self.menu_option)
        button.grid(row=1, column=0, sticky="news", padx=5, pady=5)
        button_close = tk.Button(button_frame, text="Close", command= self.close_mainwindow)
        button_close.grid(row=1, column=1, sticky="news", padx=5, pady=5)

        ##opti 1/button execution for create widget: close mainwindow
    def close_mainwindow(self):
        self.destroy()

        ##opti 2/button execution for create widget: get value button and go to choosen menu
    def menu_option(self):
        create = create_var.get()
        delivery = delivery_var.get()
        rating = rating_var.get()
        payment = payment_var.get()
            #go to choosen menu
        if create == "Choose":
            location()
        elif delivery == "Choose":
            # print ("You Chooose Delivery")
            driver_delivery()
        elif rating == "Choose":
            # print ("You Chooose Rating")
            costumer()
        elif payment == "Choose":
            # print ("You Chooose Payment") 
            driver_payment()

list_packages = []
##class to make window for input stop attribute with tkinter
##Location Class: 1) Window for choose location (get location attribute)-> 2)define pay,and other attribute->
##3)window input volume(get volume and weight) ->4)cek capacity limit and define package list ->5)create database

## The Step: window for choose location -> get value location-> define self.pay (base pay for any location) and another attribute for class location
##-> window for input volume-> for check max capacity, limit of packages (include define package list to input database) 
##->create database from stop attribute/list

###FROM HERE OK
max_capacity = 10           
# capacity = 0
def location():
    ##window for choose location   
        ##Frame
    input_location = tk.Toplevel()
    input_location.title = ("Treasure Delivery: Select Route")
    input_location.geometry = ("180x100")    

        ##widget for choose location    
    create_loct_label = tk.Label(input_location, text="Choose Route Location") 
    create_loct_label.grid(row = 0, column = 0, sticky="news", padx = 20, pady = 5) 
    route_loct_combobox = ttk.Combobox(input_location, values=["Arabasta", "Dressrosa", "Wano"])
    route_loct_combobox.grid(row=1, column=0, padx = 20, pady = 5)

    
        
    ##get value location
    def input_volume(locate,pay,del_time,tips,rating,xy): #input pair row 514
        window_input_stop = tk.Tk()
        window_input_stop.title ("Treasure Delivery Costumer: input stop")
        input_stop_frame = tk.Frame(window_input_stop) 
        input_stop_frame.pack() 
        stop_info_frame = tk.LabelFrame(input_stop_frame, text = "Current Capacity")
        # stop_info_frame = tk.LabelFrame(input_stop_frame, text = "Stop Location")
        stop_info_frame.grid(row = 0 ,column = 0, padx = 20, pady = 20)
        stop_loct_label = tk.Label (stop_info_frame, text = f"Your total Route volume now is {xy} cu.ft. You can add another packages until maximum 10 cu.ft")
        # stop_loct_label = tk.Label (stop_info_frame, text = f"Your Route Location is location. Make sure all stop that You input is in location area")
        stop_loct_label.grid(row = 0 ,column = 0, padx = 20, pady = 20)        
        stop_frame = tk.LabelFrame(input_stop_frame,text = "Input Stop") 
        stop_frame.grid(row = 1 ,column = 0, padx = 20, pady = 20)
        stop_number_frame = tk.Label(stop_frame,text = "Stop Number") 
        stop_number_frame.grid(row = 0 ,column = 0, padx = 20, pady = 20) 
        stop_number_spinbox = tk.Spinbox(stop_frame, from_=1, to=100)
        stop_number_spinbox.grid(row=1, column=0)
        stop_volume_label = tk.Label(stop_frame, text = "Packages Volume (in cu.ft)")
        stop_volume_label.grid (row = 0 ,column = 1, padx = 20, pady = 5)
        stop_volume_entry = tk.Entry(stop_frame)
        stop_volume_entry.grid (row = 1 ,column = 1, padx = 20, pady = 5)

    ##for check max capacity, limit of packages
        def check_capacity():
            # input_stop_frame.destroy()
            # window_input_stop.destroy()
            # self.destroy()
            ##defined self.volume
            # print(f"stop location = {self.locate}")
            stop = int(stop_number_spinbox.get())
            # print(f"stop number = {self.stop}")
            volume = float(stop_volume_entry.get())
            print (volume)
            ##defined self.weight
            if volume >= 1:
                x = random.uniform(7.5,15)
                weight_koef = round(x,2)
                weight = round(weight_koef*volume,2)
            elif volume >= 0.5 and volume < 1 :
                x = random.uniform(6,12)
                weight_koef = round(x,2)
                weight = round(weight_koef*volume,2)
            else:
                x = random.uniform(1,5)
                weight_koef = round(x,2)
                weight = round(weight_koef*volume,2)
            # print(f"stop volume = {self.volume}")
            # print (f"{self.stop} with volume {self.volume} cu.ft")
            # print(f"Berat: {self.weight} kg")
            # print(f"Payment: {self.pay} kg")
            # print(f"deliv_time: {self.del_time} kg")
            # print(f"rating: {self.rating} kg")
            # print(f"tips: {self.tips} kg")            
            # capacity += volume 

            # return stop,volume,weight
            
            
            
            ## define package list to input database
            packages = [locate,stop,volume,weight,pay,del_time,tips,rating]
            list_packages.append(packages) #no need to looping coz the window is always open, just input
            print (f"list_packages: {list_packages}")
            print (f"list_packages: {list_packages[0]}")
            print (f"list_packages: {list_packages[0][2]}")
            window_input_stop.destroy()
            xy = 0
            for i in list_packages:
                xy += float(i[2])
                # print (f"now = {self.capacity}")

            print (f"Kapasitas sekarang = {xy}")
            if xy < max_capacity: 
                input_volume(locate,pay,del_time,tips,rating,xy)
                print ("kasi pilihan supaya window destroy") #no need
            elif xy == max_capacity:
                xy += 0.1
                # print ("maximum capacity")
                # print (f"Total packages : {len(list_packages)} packages")
                #kasi messagebox kalau sudah reach max capacity, trus harus bisa close sampe mainwindow
            ## go to next if capacity reach max
                create_database()
            else:                
                print ("Your total route volume has reach maximum capacity (10 cu.ft)")       
                reach_limit = tk.messagebox.showwarning(title= "Reach Capacity Limit", message="input another packages so didn't over max capacity")
                list_packages.pop()
                print (f"list_packages: {list_packages}")                
                input_volume(locate,pay,del_time,tips,rating,xy)
                #muncul messagebox over max capacity, trus balik ke menu add package         
                
                return xy
            
        button_create = tk.Button(input_stop_frame, text="Add Package", command= check_capacity)
        button_create.grid(row=2, column=0, sticky="news", padx=20, pady=5)
        button_stop = tk.Button(input_stop_frame, text="Stop", command= create_database)
        button_stop.grid(row=2, column=1, sticky="news", padx=20, pady=5)

    def get_selected_loct():        
        locate = route_loct_combobox.get()
        print(f"locate= {locate}")
            ##messagebox for confirm choosen location and go to next step: input_stop
        ask_location = tk.messagebox.askokcancel (title = "Route Location", message = f"You have choose {locate}. All stops that You are input must be in {locate} area")
        if ask_location == True:
            # print ("location chosen ok")
            ##define self.pay (base pay for any location) and another attribute for class location. Also to next step        
            print ("input stop ok")     
            if locate == "Arabasta":
                pay = 3
            elif locate == "Dressrosa":
                pay = 4
            elif locate == "Wano":
                pay = 5
            else:
                pay = 3        
            del_time = 0 
            tips = 0
            rating = 0
            xy = 0 #(initial capacity)
            print (pay)
            input_volume(locate,pay,del_time,tips,rating,xy)
            
    ##window for input volume        
            


        else:
            # print ("location chosen not ok")
            location() 
        
        ##button to choose location
    button_create = tk.Button(input_location, text="Next", command= get_selected_loct)
    button_create.grid(row=2, column=0, sticky="news", padx=20, pady=5)
    
    

    

    ##create database from stop attribute/list
    def create_database():
        # self.destroy()
        # print ("create database ready")
        ##define header and write to database
        data_header = f'lokasi, stop_nomor, volume, berat, pay, deliv_time, tips, rating'
        header = data_header+(70-len(data_header))*" "+":"
        # print (len(header))
        with open(DB_NAME,'w',encoding="utf-8") as file: #pake append ya
            file.write(f"{header}\n")
        ##write packages list to database
        nomor = 1 #to adjust the seek, cursor should start from line 2 start (count 72)
        for i in list_packages:
            with open(DB_NAME,'a',encoding="utf-8") as file: #cannot count the real character, because len count index
                panjang = file.write(f"{i}\n") #this count real character
                print (i)
                print (len(i))
                print (panjang)
            ##trick to make same format 
            with open(DB_NAME,'r+',encoding="utf-8") as file: #to replace that have same number of real character
                file.seek(72*nomor)                 
                file.write(f"{i}{" "*(70-panjang)}:\n") #if use len(i), len i is index of i, not count real character number
            nomor += 1

if __name__ == "__main__":
    main()
