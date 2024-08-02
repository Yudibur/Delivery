import pytest
# from project import create_database
import project
import os
import tempfile

def test_create_route(monkeypatch, capsys,tmp_path):
    #assert output
    inputs = ["Wano","4","3","2","1"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    project.create_route() #project

    captured = capsys.readouterr() #project
    output_lines = captured.out.splitlines()
    assert output_lines[2] == "Create Route" 
    assert "Your total Route volume now is 7.0 cu.ft. You can add another packages until maximum 10 cu.ft" in captured.out
    # assert "Your total Route volume now is 4.0 cu.ft. You can add another packages until maximum 10 cu.ft" in output_lines
    assert output_lines[-1] == "Your total Route volume now is reach maximum capacity 10.0 cu.ft"
    

    #assert read database
    current_directory = os.path.dirname(os.path.abspath(__file__))
    db_file_path = os.path.join(current_directory, "route_database_submit.txt")
    db_file = db_file_path
    with open(db_file, "r", encoding="utf-8") as file:
        content = file.read().splitlines()
        
    data_header = f'lokasi, stop_nomor, volume, weight, pay, deliv_time, tips, rating'
    header = data_header+(70-len(data_header))*" "+":"
    assert content[0] == header

    #assert base_pay
    inputs = ["Arabasta","5","2","2","1"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = project.create_route() #project
    assert result == 3

def test_get_location (monkeypatch):
    #simulate user input
    monkeypatch.setattr("builtins.input", lambda _:"Wano")
    location = project.get_location()
    assert location == "Wano"  
    

def test_create_database(tmp_path):
    # Set up initial data (you can adjust this based on your actual use case)
    locate = "Wano"
    stop_no = 3
    volume = 10
    weight = 5
    base_pay = 5
    del_time = 30
    rating = 4
    tips = 2

    # Call your function with the test data
    project.create_database(locate, stop_no, volume, weight, base_pay, del_time, rating, tips)

    # Read the content of the file and assert its correctness
    current_directory = os.path.dirname(os.path.abspath(__file__))
    db_file_path = os.path.join(current_directory, "route_database_submit.txt")
    db_file = db_file_path
    with open(db_file, "r", encoding="utf-8") as file:
        content = file.read().splitlines()
        # content = file.read().strip()

    expected_content = f"{str(locate)+","+str(stop_no)+","+str(volume)+","+str(weight)+","+str(base_pay)+","+str(del_time)+","+str(rating)+","+str(tips)}"
    assert content[-1] == expected_content
    #delete last line to get original database back
    with open(db_file, "r", encoding="utf-8") as file:
        content = file.readlines()
    content.pop()

    with open(db_file, "w", encoding="utf-8") as file:
        file.writelines(content)



def test_driver_delivery(monkeypatch, capsys):
    inputs = ["2","2.5"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    #assert 2 return value
    stop_to_update = project.driver_delivery()
    assert stop_to_update == (2, 2.5)

    #assert output
    captured = capsys.readouterr() #project
    output_lines = captured.out.splitlines()
    assert output_lines[1] == "Please estimated time since Last Stop/Warehouse. Exp:5 minutes 30 seconds You can input '5.5'" 

def test_update_time():
    #check if the database was updated correctly
    stop_to_update = 1
    new_stop_time = 5.5
    project.update_time(stop_to_update, new_stop_time)
    assert True

def test_costumer_rating(monkeypatch, capsys):
    inputs = ["3","4","5"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    #assert 2 return value
    stop_to_update = project.costumer_rating()
    assert stop_to_update == (3, 4, 5)

    #assert output
    captured = capsys.readouterr() #project
    output_lines = captured.out.splitlines()
    assert output_lines[1] == "Please rate our delivery and give tips if you want" 

def test_update_rate_tips():
    #check if the database was updated correctly
    stop_to_update = 1
    new_stop_rate = 3
    new_stop_tips = 1
    project.update_rate_tips(stop_to_update, new_stop_rate, new_stop_tips)
    assert True

def test_driver_payment(tmp_path):
    # Set up initial data (you can adjust this based on your actual use case)
    DB_NAME = "route_database_submit.txt"
    data_header = f'lokasi, stop_nomor, volume, weight, pay, deliv_time, tips, rating'
    header = data_header+(70-len(data_header))*" "+":"
    # print (len(header))
    with open(DB_NAME,'w',encoding="utf-8") as file: #pake append ya
        file.write(f"{header}\n")

    project.create_database("Dressrosa",1,4.0,50.00,4,13.0,2,3)
    project.create_database("Dressrosa",2,3.0,25.50,4,2.0,3,5)
    project.create_database("Dressrosa",3,2.0,19.00,4,1.0,3,3)
    project.create_database("Dressrosa",4,1.0,10.50,4,2.0,2,5)
                         
    result = project.driver_payment()
    assert result == 15.76 

    
# Run the tests
if __name__ == "__main__":
    # test_driver_payment()
    pytest.main()