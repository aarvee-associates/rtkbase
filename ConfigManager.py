# This module aims to make working with RTKLIB configs easier
# It allows to parse RTKLIB .conf files to python dictionaries and backwards
# Note that on startup it reads on of the default configs
# and keeps the order of settings, stored there

class ConfigManager:

    def __init__(self, config_path = None):

        if config_path is None:
            self.config_path = "/home/reach/RTKLIB/app/rtkrcv/"
        else:
            self.config_path = config_path

        self.default_rover_config = "reach_rover_default.conf"

        self.buff_options = {}
        self.buff_dict = {}
        self.buff_dict_order = []
        self.readConfig(self.default_rover_config) # we do this to load config order from default reach base config

        self.buff_dict = {}

    def readConfig(self, from_file):
        self.buff_dict = {}
        self.buff_dict_order = []

        with open(self.config_path + from_file, "r") as f:
            for line in f:
                separated_lines = line.split() # separate lines with spaces, get rid of extra whitespace
                length = len(separated_lines)

                # check if the line is empty or commented
                if length > 0:
                    if separated_lines[0][0] != "#":
                        param = separated_lines[0] # get first part of the line, before the equal sign
                        val = separated_lines[1][1:] # get the second part of the line, discarding "=" symbol

                        if length > 3:
                            options = separated_lines[3]
                            # some of the options are comments only
                            if ":" in options:
                                self.buff_options[param] = options

                        self.buff_dict[param] = val
                        self.buff_dict_order.append(param) # this is needed to conserve the order of the parameters in the config file

    def writeConfig(self, to_file, dict_values = None):

        if dict_values == None:
            dict_values = self.buff_dict

        print("Printing temp config" + str(dict_values))

        print("Printing temp config we're about to write")
        with open(self.config_path + to_file, "w") as f:
            line = "# rtkrcv options for rtk (2015, v.2.4.2)"
            f.write(line + "\n\n")
            for key in self.buff_dict_order:
                k = str(key)
                v = str(dict_values[key])

                line = k + " " * (19 - len(k)) + "=" + v

                print("line = " + line)
                # check if options are available
                if key in self.buff_options:
                    line += " # " + self.buff_options[key]

                f.write(line + "\n")
