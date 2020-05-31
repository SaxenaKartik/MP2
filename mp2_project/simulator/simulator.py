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
        self.users_connected = entry["users_connected"][0]
        self.state = entry["state"]
        self.warning_bit = True if entry["warning_bit"] else False
        self.command = entry["command"]
        self.state = entry["state"]
        self.users_connected_list = entry["users_connected"][1]


class Simulator:
    def __init__(self, information, url, client_url):
        self.information = information
        self.state = State()
        self.observer = LocalServerObserver()
        self.url = url
        self.client_url = client_url
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
            self.observer.update("Verdict : Drone exists in db")
            patch = requests.patch(self.url + str(information.drone_id) + "/", data = {"state" : 0})
            if patch.status_code==200:
                self.observer.update("Verdict : Reset the drone state in db")
            else:
                self.observer.update("Verdict : Could not reset drone state in db")

        else:
            post = requests.post(url, data = entry)
            if post.status_code==201:
                self.observer.update("Verdict : Added new drone to database")
            else:
                self.observer.update("Verdict : Could not add drone to database")

    def check_users_connected(self, information):
        # Case 1: if new connected user does not exist in database : POST request for updating the user without logout time
        # Case 2: if new connected user exists on database but doesn't have a logout time : do nothing
        # Case 3: if new connected user exists on database and has a logout time : delete the old object and POST a new one

        # Case 4: if user exists on database with no logout time and is no longer connected : PATCH the logout time as to now
        # Case 5: if user exists on the database with logout time and is no longer connected : do nothing

        get = requests.get(self.client_url)
        client_list_db = {}
        if get.status_code == 200:
            for client in json.loads(get.text):
                client_list_db[client["client_id"]] =  client["logout_time"]
        else:
            self.observer.update("Verdict : Unable to fetch client information")
        # print(client_list_db)

        new_connected_clients = {}
        for user in self.information.users_connected_list:
            new_connected_clients[hashit(user[0])] = user[1]
        # print(new_connected_clients)

        for client in client_list_db:
            if client not in new_connected_clients:
                if client_list_db[client]==None:
                    # make a PATCH request to update logout time
                    logout_time = datetime.now()
                    patch = requests.patch(self.client_url + str(client) + "/", data = {"logout_time" : logout_time})
                    if patch.status_code==200:
                        self.observer.update("Verdict : Updated logout time of a drone in db -> " + str(client))
                    else:
                        self.observer.update("Verdict : Could not update the logout time")

        for user in new_connected_clients:
            if user not in client_list_db:
                # make POST request for the new user
                post = requests.post(self.client_url, data = {"client_id" : user, "ip_address": new_connected_clients[user], "drone" : self.information.drone_id})
                if post.status_code==201:
                    self.observer.update("Verdict : Added a new drone to the database -> " + str(user))
                else:
                    self.observer.update("Verdict : Could not add a new drone to the database")

            elif user in client_list_db and client_list_db[user]!=None:
                # make a delete request for old entry and make a POST request for new entry
                delete = requests.delete(self.client_url + str(user) + "/")
                if delete.status_code==204:
                    self.observer.update("Verdict : Deleted a drone from the database -> " + str(user))
                else:
                    self.observer.update("Verdict : Could not delete the drone from database")

                post = requests.post(self.client_url, data = {"client_id" : user, "ip_address": new_connected_clients[user], "drone" : self.information.drone_id})
                if post.status_code==201:
                    self.observer.update("Verdict : Added the drone back to the database -> "+ str(user))
                else:
                    self.observer.update("Verdict : Could not add drone back to the database")



    def start(self, information):
        assert self.state.number == 0, "start() must be called after initial state"
        self.state.number = 1
        self.state.name = "Access Point Setup"
        self.information = information
        self.check_users_connected(self.information)

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
        response = requests.patch(self.url + str(self.information.drone_id) + "/", data = entry)
        if response.status_code==200:
            self.observer.update("Verdict : Updated drone in database to state 1")
        else:
            self.observer.update("Verdict : Could not update drone to database")


    def fly(self, information):
        assert self.state.number == 1, "fly() must be called after Access Point setup state"
        self.state.number = 2
        self.state.name = "Flying"
        self.information = information
        self.check_users_connected(self.information)

        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        # make a post request based on information
        response = requests.patch(self.url + str(self.information.drone_id) + "/", data = entry)
        if response.status_code==200:
            self.observer.update("Verdict : Updated drone in database to state 2")
        else:
            self.observer.update("Verdict : Could not update drone to database")



    def pause(self, information):

        assert self.state.number == 1 or self.state.number == 2, "pause() must be called after WiFi setup state"
        self.state.number = 3
        self.state.name = "Paused WiFi connections"
        self.information = information
        self.check_users_connected(self.information)

        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        # make a post request based on information
        response = requests.patch(self.url + str(self.information.drone_id) + "/", data = entry)
        if response.status_code==200:
            self.observer.update("Verdict : Updated drone in database to state 3")
        else:
            self.observer.update("Verdict : Could not update drone to database")

    def resume(self, information):

        assert self.state.number==3, "resume() must be called after paused state"
        self.state.number = 4
        self.state.name = "Resumed WiFi connections"
        self.information = information
        self.check_users_connected(self.information)

        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        # make a post request based on information
        response = requests.patch(self.url + str(self.information.drone_id) + "/", data = entry)
        if response.status_code==200:
            self.observer.update("Verdict : Updated drone in database to state 4")
        else:
            self.observer.update("Verdict : Could not update drone to database")


    def stop(self, information):
        assert self.state.number in [0,1,2,3,4], "stop() can be called after any state [0,1,2,3,4]"
        self.state.number = 5
        self.state.name = "Stopped Access Point"
        self.information = information
        self.check_users_connected(self.information)

        entry = {
            "drone_id" : self.information.drone_id,
            "lat" : self.information.lat,
            "log" : self.information.log,
            "battery_level" : self.information.battery_level,
            "users_connected" : self.information.users_connected,
            "state" : self.information.state,
            "warning_bit" : self.information.warning_bit,
        }
        # make a post request based on information
        response = requests.patch(self.url + str(self.information.drone_id) + "/", data = entry)
        if response.status_code==200:
            self.observer.update("Verdict : Updated drone in database to state 5")
        else:
            self.observer.update("Verdict : Could not update drone to database")

class Controller:
    def __init__(self, information, url, client_url):
        self.simulator = Simulator(information, url, client_url)
        self.observer = LocalServerObserver()

    def start(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))
        self.observer.update("Command : " + information.command)
        self.simulator.start(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))

    def fly(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))
        self.observer.update("Command : " + information.command)
        self.simulator.fly(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))

    def pause(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))
        self.observer.update("Command : " + information.command)
        self.simulator.pause(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))

    def resume(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))
        self.observer.update("Command : " + information.command)
        self.simulator.resume(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))

    def stop(self, information):
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))
        self.observer.update("Command : " + information.command)
        self.simulator.stop(information)
        state = {"Number" : self.simulator.state.number, "Name" : self.simulator.state.name}
        self.observer.update("State : " + str(state))

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
        self.url = "http://192.168.43.34:8080/api/drone/"
        self.client_url = "http://192.168.43.34:8080/api/client/"
        # connection = requests.get(self.url + str(information.drone_id))
        # if connection.status_code!=200:
        self.controller = Controller(self.information, self.url, self.client_url)
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
        self.information.drone_id = hashit(self.information.drone_id)
        if self.information.state == 1 and self.controller.simulator.state.number == 0:
            # print("Here")
            self.information.command = "start"

        elif self.information.state == 2 and self.controller.simulator.state.number == 1:
            self.information.command = "fly"

        elif self.information.state == 3 and self.controller.simulator.state.number in [1,2]:
            self.information.command = "pause"

        elif self.information.state == 4 and self.controller.simulator.state.number == 3:
            self.information.command = "resume"

        elif self.information.state == 5 and self.controller.simulator.state.number in [0,1,2,3,4]:
            self.information.command = "stop"

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
            # self.observer.update(" " + str(self.controller.simulator.state.number))
            state = {"Number" : self.controller.simulator.state.number, "Name" : self.controller.simulator.state.name}
            self.observer.update("Verdict : No new command")
            self.observer.update("State : " +  str(state))


class Machine:
    def __init__(self):
        data = open("test_data.txt", "r")
        entry = json.loads(data.read())[0]
        # print(entry)
        self.observer = LocalServerObserver()
        self.exit_code = 0
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
        # print(self.information.state)
        if self.information.state==5:
            self.exit_code = 1


obj = Machine()

while(True):
    obj.fetch()
    time.sleep(1)
    obj.send()
    if obj.exit_code==1:
        obj.observer.update("Stopping the server")
        break
    time.sleep(5)
