# state based simulator
# issuing API based request to the server
import requests
import hashlib
from datetime import datetime
import json
import time

def hashit(k : str):
    hash = hashlib.sha1()
    hash.update(k.encode('utf-8'))
    return  hash.hexdigest()[:-10]


class State:
    def __init__(self):
        self.number = 0
        self.name = "Initial"

class Information:
    def __init__(self, entry):
        self.drone_id = entry["drone_id"]
        self.lat = entry["lat"]
        self.log = entry["log"]
        self.battery_level = entry["battery_level"]
        self.users_connected = entry["users_connected"]
        self.state = entry["state"]
        self.warning_bit = True if entry["warning_bit"] else False
        self.command = entry["command"]
        self.state = entry["state"]


class Simulator:
    def __init__(self, information, url):
        self.information = information
        self.state = State()
        self.observer = LocalServerObserver()
        self.url = url
        # make post request to initiate the drone
        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        connection = requests.get(self.url + str(information.drone_id))
        if connection.status_code==200:
            self.observer.update("Drone exists in db")
        else:
            response = requests.post(url, data = entry)
            if response.status_code==201:
                self.observer.update("Added new drone to database")
            else:
                self.observer.update("Could not add drone to database")

    def start(self, information):
        assert self.state.number == 0, "start() must be called after initial state"
        self.state.number = 1
        self.state.name = "Access Point Setup"
        self.information = information

        # make a post request based on information
        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        response = requests.post(self.url, data = entry)
        if response.status_code==201:
            self.observer.update("Updated drone in database to state 1")
        else:
            self.observer.update("Could not update drone to database")


    def fly(self, information):
        assert self.state.number == 1, "fly() must be called after Access Point setup state"
        self.state.number = 2
        self.state.name = "Flying"
        self.information = information

        # make a post request based on information


    def pause(self, information):
        assert self.state.number == 1 or self.state.number == 2, "pause() must be called after WiFi setup state"
        self.state.number = 3
        self.state.name = "Paused WiFi connections"
        self.information = information

        # make a post request based on information


    def resume(self, information):
        assert self.state.number==3, "resume() must be called after paused state"
        self.state.number = 4
        self.state.name = "Resumed WiFi connections"
        self.information = information

        # make a post request based on information


    def stop(self, information):
        assert self.state.number == 4, "stop() must be called after flying state"
        self.state.number = 5
        self.state.name = "Stopped Access Point"
        self.information = information

        # make a post request based on information

class Controller:
    def __init__(self, information, url):
        self.simulator = Simulator(information, url)
        self.observer = LocalServerObserver()

    def start(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information.command)
        self.simulator.start(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)

    def fly(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information)
        self.simulator.fly(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)

    def pause(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information)
        self.simulator.pause(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)

    def resume(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information)
        self.simulator.resume(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)

    def stop(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information)
        self.simulator.stop(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)

class Observer:
    def update(self, log):
        pass

class LocalServerObserver(Observer):
    def update(self, log):
        print(log)

class View:
    def __init__(self):
        pass

class LocalServerView(View):

    def __init__(self, information):
        # check if drone is already present in the database
        self.observer = LocalServerObserver()
        self.information = information
        self.url = "http://192.168.1.101:8080/api/drone/"
        # connection = requests.get(self.url + str(information.drone_id))
        # if connection.status_code!=200:
        self.controller = Controller(self.information, self.url)
        # else:
        # self.observer.update("Drone exists in database")

    def fetch_information(self):
        # open a file to get local information
        # overwrite the server information based on local information
        data = open("test_data.txt", "r")
        data = json.loads(data.read())[-1]
        # print(data["state"])
        self.information = Information(data)

        # print(self.information.state, self.controller.simulator.state.number)

        if self.information.state == 1 and self.controller.simulator.state.number == 0:
            # print("Here")
            self.information.command = "start"

        elif self.information.state == 2 and self.controller.simulator.state.number == 1:
            self.information.command = "fly"

        elif self.information.state == 3 and (self.controller.simulator.state.number == 1 or self.controller.simulator.state.number == 2):
            self.information.command = "pause"

        elif self.information.state == 4 and self.controller.simulator.state.number == 3:
            self.information.command = "resume"

        elif self.information.state == 5 and self.controller.simulator.state.number == 4:
            self.information.command = "stop"
            self.exit_code = 1

        else:
            self.information.command = ""
        # print(self.information.command)
        return self.information


    def send_information(self, information):
        # use the valid information set to update the simulator state and call valid function of the controller
        if information.command == "start":
            self.controller.start(information)

        if information.command == "fly":
            self.controller.fly(information)

        if information.command == "pause":
            self.controller.pause(information)

        if information.command == "resume":
            self.controller.resume(information)

        if information.command == "stop":
            self.controller.stop(information)

        if information.command == "":
            self.observer.update("No changes found! Maintaining the same state : " + str(self.controller.simulator.state.number))

class Machine:
    def __init__(self):
        data = open("test_data.txt", "r")
        entry = json.loads(data.read())[0]
        # print(entry)
        self.observer = LocalServerObserver()
        # validating the entry

        if "drone_id" not in entry or entry["drone_id"]=="":
            self.observer.update("Invalid first entry! Must have drone_id for registration")
            return

        if entry["state"]!=0:
            self.observer.update("Initial state must be 0")
            return

        if entry["warning_bit"]:
            self.observer.update("Please check the battery, warning_bit has been set")

        if entry["battery_level"]<30:
            self.observer.update("Drone must be charged")
            entry["warning_bit"] = True


        entry["drone_id"] = hashit(entry["drone_id"])
        # print(entry["drone_id"])
        self.information = Information(entry)
        data.close()
        self.view = LocalServerView(self.information)

    def fetch(self):
        information_set = self.view.fetch_information()
        self.information = information_set
        # print(information_set.command)
    def send(self):
        self.view.send_information(self.information)


obj = Machine()
# obj.fetch()
# obj.send()

while(True):
    obj.fetch()
    time.sleep(1)
    obj.send()
    time.sleep(5)
    if obj.exit_code==1:
        obj.observer.update("Stopping the server")
