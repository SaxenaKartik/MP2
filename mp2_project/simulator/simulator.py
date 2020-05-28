# state based simulator
# issuing API based request to the server
import requests
import hashlib
from datetime import datetime
import json

def hashit(k : str):
    hash = hashlib.sha1()
    hash.update(k.encode('utf-8'))
    return  hash.hexdigest()[:-10]


class State:
    def __init__(self):
        self.number = 0
        self.name = "Initial"

class Information:
    def __init__(self, hash_drone_id, battery_level):
        self.drone_id = hash_drone_id
        self.battery_level = battery_level
        self.command = None



class Simulator:
    def __init__(self, information, url):
        self.information = information
        self.state = State()
        self.observer = LocalServerObserver()

        # make post request to initiate the drone
        response = requests.post(url, data = {'drone_id' : information.drone_id, 'battery_level' : information.battery_level})
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
        self.observer = Observer()

    def start(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update(state)
        self.observer.update(information)
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

    def __init__(self, hash_drone_id):
        # check if drone is already present in the database
        self.observer = LocalServerObserver()
        self.information = Information(hash_drone_id, 100)
        self.url = "http://192.168.1.101:8080/api/drone/"
        connection = requests.get(self.url + str(hash_drone_id))
        if connection.status_code!=200:
            self.controller = Controller(self.information, self.url)
        else:
            self.observer.update("Drone already exists in database")

    def fetch_information(self, hash_drone_id):
        # open a file to get local information
        # overwrite the server information based on local information
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


class Machine:
    def __init__(self):
        self.drone_id = "00000000e215b4a2"
        self.drone_id = hashit(self.drone_id)
        print(self.drone_id)
        self.view = LocalServerView(self.drone_id)
        self.information = Information(self.drone_id, 100)

    def fetch(self):
        information_set = self.view.fetch_information(self.drone_id)
        self.information = information_set

    def send(self):
        self.view.send_information(self.information)


obj = Machine()
# obj.fetch()
# obj.send()
