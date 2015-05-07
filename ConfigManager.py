from gevent import monkey
monkey.patch_all()

from flask.ext.socketio import SocketIO, emit

# This module aims to make working with RTKLIB configs easier
# It allows to parse RTKLIB .conf files to python dictionaries and backwards
# Note that on startup it reads on of the default configs 
# and keeps the order of settings, stored there 

class ConfigManager:
    
    def __init__(self, socketio = None):
        self.config_path = ""
        self.default_base_config = "reach_base_default.conf"
        self.default_rover_config = "reach_rover_default.conf"
        self.custom_config = ""
        self.buff_dict = {}
        self.buff_dict_order = []
        self.readConfig(self.default_base_config) # we do this to load config order from default reach base config
        self.buff_dict = {}
        self.socketio = socketio

    def readConfig(self, from_file):
        self.buff_dict = {}
        self.buff_dict_order = []

        with open(from_file, "r") as f:
            for line in f:
                separated_lines = line.split() # separate lines with spaces, get rid of extra whitespace
                length = len(separated_lines)

                # check if the line is empty or commented
                if length > 0:
                    if separated_lines[0][0] != "#":
                        param = separated_lines[0] # get first part of the line, before the equal  

                        val = separated_lines[1][1:] # get the second part of the line, discarding "=" symbol

                        self.buff_dict[param] = val
                        self.buff_dict_order.append(param) # this is needed to conserve the order of the parameters if the config file

    def writeConfig(self, to_file, dict_values = None):

        if dict_values == None:
            dict_values = self.buff_dict

        with open(to_file, "w") as f:
            for key in self.buff_dict_order:
                line = key + " " * (19 - len(key)) + "=" + self.buff_dict[key]
                f.write(line + "\n")

    def sendConfig(self, config_filename = None):

        # either read settings from the buffer, or update buffer by the filename.conf
        if config_filename == None:
            dict_values = self.buff_dict
        else:
            self.readConfig(config_filename)
            dict_values = self.buff_dict

        self.socketio.emit("config for " + config_filename, dict_values, namespace = "/test")



cm = ConfigManager()
print("Default order is: ")
print(cm.buff_dict_order)

cm.readConfig("rtk_startup.conf")
cm.writeConfig("rtk_startup2.conf")
