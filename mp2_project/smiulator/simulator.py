# state based simulator
# issuing API based request to the server
import requests
import hashlib




class State:
    def __init__(self):
        self.number = 0
        self.name = "Initial"

class Simulator:
    def __init__(self, information):
        self.information = information
        self.state = State()
        # make a post request based on information

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




class Observer:
    def update(self, log):
        pass

class LocalServerObserver(Observer):
    def update(self, log):
        print(log)

class View:
    def __init__(self):


class LocalServerView(View):
