# state based simulator
# issuing API based request to the server
import requests
import hashlib

def hashit(k : str):
    hash = hashlib.sha1()
    hash.update(k.encode('utf-8'))
    return  hash.hexdigest()[:-10]


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



class Controller(self):
    def __init__(self, simulator, observer, information):
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


class LocalServerView(View):
