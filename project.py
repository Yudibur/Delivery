#Problem set 9
#Final Project

import random
import os

DB_NAME = "route_database_submit.txt"
list_packages = {
    "stop_locate": "XXXX",
    "stop_num":10, #prime key, semacam ID yang unik
    "stop_volume":2.5,
    "stop_weight":1.25, #255 spasi
    "stop_base_pay":3,
    "stop_del_time":5,
    "stop_rating": 5,
    "stop_tips": 3.0 
}

max_capacity = 10

def get_location():
    while(True):
        try:
            location = input ("Choose Your route location (Arabasta/Dressrosa/Wano): ")
            if location in {"Arabasta", "Dressrosa", "Wano"}:
                return location
            else:
                print ("Wrong location. Please input again your route location (Arabasta/Dressrosa/Wano)")
        except KeyboardInterrupt:
            print ("\nExiting due to user interruption")
            raise SystemExit(1)


def create_route():
    # print ("cek route ok")
    print ("\n\nCreate Route")
    print (50*"-")

    ##Choose location
    locate = get_location()
    if locate == "Arabasta":
        base_pay = 3
    elif locate == "Dressrosa":
        base_pay = 4
    elif locate == "Wano":
        base_pay = 5
    

    print (f"You have choose {locate}. All stops that You are input must be in {locate} area")
    max_capacity = 10
    capacity = 0
    del_time = 0
    tips = 0
    rating = 0
    stop_no = 1
    
    data_header = f'lokasi, stop_nomor, volume, weight, pay, deliv_time, tips, rating'
    header = data_header+(70-len(data_header))*" "+":"
    # print (len(header))
    with open(DB_NAME,'w',encoding="utf-8") as file: #pake append ya
        file.write(f"{header}\n")
    while capacity <= max_capacity:
        if capacity < max_capacity:
            print (f"\nYour total Route volume now is {capacity} cu.ft. You can add another packages until maximum {max_capacity} cu.ft")
            volume = float(input(f"Packages volume of Stop no.{stop_no} (in cu.ft): " ))
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

            # f"stop+{str(stop_no)}" == Packages (stop_no,volume,0.5*volume,base_pay,del_time,rating,tips)
            # print (stop)
            create_database(locate,stop_no,volume,weight,base_pay,del_time,rating,tips)
            capacity += volume
            stop_no += 1

        elif capacity == max_capacity:
            print (f"\nYour total Route volume now is reach maximum capacity {capacity} cu.ft")
            break
            #go to database write
        else:
            print (f"\nCapacity over the maximum capacity, add another packages. Your total Route volume now is {capacity} cu.ft") 
            #kasi pilihan stop atau add anothr 
            volume = float(input(f"Packages volume of Stop no.{stop_no} (in cu.ft): " ))
            # f"stop+{str(stop_no)}" == Packages (stop_no,volume,0.5*volume,base_pay,del_time,rating,tips)
            capacity += volume
            stop_no += 1
    return base_pay

def create_database(locate,stop_no,volume,weight,base_pay,del_time,rating,tips):
    list_packages["stop_locate"] = locate
    list_packages["stop_num"] = stop_no
    list_packages["stop_volume"] = volume
    list_packages["stop_weight"] = weight
    list_packages["stop_base_pay"] = base_pay
    list_packages["stop_del_time"] = del_time
    list_packages["stop_rating"] = rating
    list_packages["stop_tips"] = tips
    
    stop_packages = f"{list_packages["stop_locate"]},{list_packages["stop_num"]},{list_packages["stop_volume"]},{list_packages["stop_weight"]},{list_packages["stop_base_pay"]},{list_packages["stop_del_time"]},{list_packages["stop_rating"]},{list_packages["stop_tips"]}\n"
    with open(DB_NAME,'a',encoding="utf-8") as file: #to replace that have same number of real character
        # file.seek(72*nomor)                 
        file.write(stop_packages) #if use len(i), len i is index of i, not count real character number


def driver_delivery():
    try:
        with open(DB_NAME, 'r') as file:
            content = file.read().splitlines()            
#         ##choose stop number frame
            stop_list = list(range(1,len(content)))
            print (f"Your Stop Number are: {stop_list}")
            stop_to_update = int(input("Choose Stop Number to Deliver: ")) 
#     ##window input delivery time
            print ("Please estimated time since Last Stop/Warehouse. Exp:5 minutes 30 seconds You can input '5.5'")
            new_stop_time = float(input("How Much Time You Need To Delivered This Stop? "))
            update_time(stop_to_update,new_stop_time)
            return stop_to_update,new_stop_time
    except:
        print("Error Read Database")
        return False


#             
#     ##update del_time to database
def update_time(stop_to_update,new_stop_time):        
#         ##update database: read database-> split and strip data to make new list ->define new stop list ->update database
#             ##read database
    with open(DB_NAME, 'r') as file:
        content = file.read().splitlines()
#             ##split and strip data to make new list
        split_content = content[stop_to_update].split(",")
        new_stop_update = f"{str(split_content[0])+","+str(split_content[1])+","+str(split_content[2])+","+str(split_content[3])+","+str(split_content[4])+","+str(new_stop_time)+","+str(split_content[6])+","+str(split_content[7])}"
        update_database(stop_to_update,new_stop_update)

#                 
            ##update stop database
def update_database(stop_to_update, new_stop_list):
    # print ("update database ok")
    with open(DB_NAME,'r+',encoding="utf-8") as file: 
        lines = file.readlines() #read all the lines mirip read+splitlines
        old_text = lines[stop_to_update].rstrip("\n")
        lines[stop_to_update] = new_stop_list + "\n"
        file.seek(0)
        file.writelines(lines)
        file.truncate()
        
def costumer_rating():
    # print ("costumer ok")
    with open(DB_NAME, 'r') as file:
            content = file.read().splitlines()            
#         ##choose stop number frame
            stop_list = list(range(1,len(content)))
            print (f"Your Stop Number are: {stop_list}")
            stop_to_update = int(input("Choose Stop Number to rate: ")) 
#     ##window input delivery time
            print ("Please rate our delivery and give tips if you want")
            new_stop_rate = int(input("Rate Us (1 to 5 which 5 is excellent): "))
            new_stop_tips = float(input("Your Tips (type 0 if no tips for us, no worries): "))
            update_rate_tips(stop_to_update,new_stop_rate, new_stop_tips)
            return stop_to_update,new_stop_rate,new_stop_tips
    
def update_rate_tips(stop_to_update,new_stop_rate,new_stop_tips):
    # print ("update tips ok")
    with open(DB_NAME, 'r') as file:
        content = file.read().splitlines()
#             ##split and strip data to make new list
        split_content = content[stop_to_update].split(",")
        new_stop_update = f"{str(split_content[0])+","+str(split_content[1])+","+str(split_content[2])+","+str(split_content[3])+","+str(split_content[4])+","+str(split_content[5])+","+str(new_stop_tips)+","+str(new_stop_rate)}"
        update_database(stop_to_update,new_stop_update)

def driver_payment():  
        ##read database
    try:
        with open(DB_NAME, 'r') as file:
            content = file.readlines()
        ##make new list, split, strip and append list
            count_stop = len(content)
            # print (f"total stop = {count_stop-1}")
            new_packages_list = []
            for i in range(1,count_stop): #not include header
                split_content = content[i].split(",")
                new_stop_list = []
                for i in split_content:
                    strip_i = i.strip(":[] ''\n")
                    new_stop_list.append(strip_i) #strip and split, then append
                new_packages_list.append(new_stop_list)        
        
        # print (f"new_packages_list3 : {new_packages_list}")
        ##find total weight. weight koef and total tips
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
        # print (f"total tips = {sum_tips}")

    ##find total payment with weight koef 
        sum_payment = 0
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
            # print (f"payment stop ke {i} = {stop_payment}")
            sum_payment += stop_payment        
        # print (f"total payment for this route = {sum_payment}")

            
    except:
        print("Error Read Database")
        return False

    ## get total payment (you_got) and show in message box
    you_got = sum_payment + sum_tips
    print (f"Your Payment for this route is ${you_got:.2f}" ) 
    return you_got


print ("cek2")
#bikin main windownya dan opsi pilih2nya
def main():
    system_operation = os.name
    while(True):
        match system_operation:
            case "posix": os.system("clear")
            case "nt": os.system("cls")

        print("WELCOME TO TREASURE DELIVERY")
        print("YOUR FUTURE SHIPPING")
        print(30*"#")

        print(f"1. Create Route")
        print(f"2. Driver Delivery Report")
        print(f"3. Costumer Rating and Tips")
        print(f"4. Driver Payment\n")

        user_option = input("Choose Menu: ")

        match user_option:
            case "1": create_route()
            case "2": driver_delivery()
            case "3": costumer_rating()
            case "4": driver_payment()

        is_done = input("Are You Quit (y/n)? ")
        if is_done == "y" or is_done == "Y":
            break

    print("Program End, Thank You")

if __name__ == "__main__":
    main()
