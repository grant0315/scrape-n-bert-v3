import configparser as c
import os

class ConfigData:
    def __init__(self, path_to_config_file):
        # Init and set it to the path for the config file
        self.path_to_config_file = path_to_config_file
        config = c.ConfigParser()
        config.read(self.path_to_config_file)

        # Get general settings from config file
        self.output_file_name = config['General Settings']['OUTPUT_FILE_NAME']
        self.output_file_directory = config['General Settings']['OUTPUT_FILE_DIRECTORY']

        # Pull data from config file
        sections = config.sections()

        # For each domain, run the run.sh file in order to scrape.
        for section in sections:
            if section != "General Settings":
                shell_command = "sh run.sh " + "-d " + section + " " + "-c " +  config[section]["CSS_SELECTORS"] + " " + "-l " +  config[section]["DEPTH_LIMIT"] + " " + "-p " + config[section]["CLOSESPIDER_PAGECOUNT"]
                print(shell_command)

                os.system(shell_command)

config_p = ConfigData("/home/granthopkins/workspace/scrape-n-bert-v3-clone/config.ini")