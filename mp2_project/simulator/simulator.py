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
    def __init__(self, drone_id):
        self.type = None
        self.drone_id = drone_id
        self.lat = None
        self.log = None
        self.battery_level = None
        self.users_connected = None


class Simulator:
    def __init__(self, information):
        self.information = information
        self.state = State()

        # make post request to initiate the drone

    def start(self, information):
        assert self.state.number == 0, "start() must be called after initial state"
        self.state.number = 1
        self.state.name = "Access Point Setup"
        self.information = information

        # make a post request based on information
        if self.information.type!=None
            pass


    def fly(self, information):
        assert self.state.number == 1, "fly() must be called after Access Point setup state"
        self.state.number = 2
        self.state.name = "Flying"
        self.information = information

        # make a post request based on information
        if self.information.type!=None
            pass

    def pause(self, information):
        assert self.state.number == 1 or self.state.number == 2, "pause() must be called after WiFi setup state"
        self.state.number = 3
        self.state.name = "Paused WiFi connections"
        self.information = information

        # make a post request based on information
        if self.information.type!=None
            pass

    def resume(self, information):
        assert self.state.number==3, "resume() must be called after paused state"
        self.state.number = 4
        self.state.name = "Resumed WiFi connections"
        self.information = information

        # make a post request based on information
        if self.information.type!=None
            pass

    def stop(self, information):
        assert self.state.number == 4, "stop() must be called after flying state"
        self.state.number = 5
        self.state.name = "Stopped Access Point"
        self.information = information

        # make a post request based on information
        if self.information.type!=None
            pass


class Controller:
    def __init__(self, information):
        self.simulator = Simulator(information)
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
        self.information = Information(drone_id)
        self.controller = Controller(self.information)

class LocalServerView(View):

    def __init__(self):
        super().__init__()

    def fetch_information(self, local_information):
        # fetch information of the current state of simulator
        # build information set based on current state and the valid drone information
        drone_id = "00000000e215b4a2"
        hash_drone_id = hashit(drone_id)
        server_information = requests.get("http://127.0.0.1:8080/api/drone/" + str(hash_drone_id))
        server_information_dict = json.loads(server_information.text)
        server_information_code = server_information.status_code

        if server_information_code==200:
            type = "PATCH"
        else:
            type = "POST"


    def send_information(self, information):
        # use the valid information set to update the simulator state and call valid function of the controller
