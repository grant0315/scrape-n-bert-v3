import configparser
import bertopic_wrapper.main as bert
import os
import sys

class ConfigData:
    def __init__(self, path_to_config_file):
        # Init and set it to the path for the config file
        self.path_to_config_file = path_to_config_file
        config = configparser.ConfigParser()
        config.read(self.path_to_config_file, encoding='utf-8-sig')

        # Get general settings from config file
        self.output_file_directory = config['General Settings']['OUTPUT_FILE_DIRECTORY']

        # Create new scraped_data folder
        try:
            os.mkdir(self.output_file_directory + "/scraped_data")
        except FileExistsError as e:
            print("!=== Scraped_data folder already exists ===!") 
            pass

        # Pull data from config file
        sections = config.sections()

        # For each domain, run the run.sh file in order to scrape.
        for section in sections:
            if section != "General Settings":
                section_file_name = self.create_scrapy_content_file_name(str(section))
                print(section_file_name)
                shell_command = "sh run_spider.sh " + "-o " + section_file_name + " " + "-d " + str(section) + " " + "-c " +  config[section]["CSS_SELECTORS"] + " " + "-l " +  config[section]["DEPTH_LIMIT"] + " " + "-p " + config[section]["CLOSESPIDER_PAGECOUNT"]
                print(shell_command)

                os.system(shell_command)
                
                # Move scraped data to scraped_data in output directory
                os.replace("./recursive_spider/" + section_file_name, self.output_file_directory + "/scraped_data/" + section_file_name)

    def run_bert_with_individual_domains(self):

        config = configparser.ConfigParser()
        config.read(self.path_to_config_file, encoding='utf-8-sig')

        # Pull data from config file
        sections = config.sections()

        # For each domain, run the run.sh file in order to scrape.
        for section in sections:
            if section != "General Settings":
                in_file_name = self.create_scrapy_content_file_name(section)
                in_file_path = config["General Settings"]["OUTPUT_FILE_DIRECTORY"] + "/scraped_data/" + in_file_name
                print(in_file_path)

                bt = bert.BertopicTraining(in_file_path, str(sys.argv[2]), in_file_name)
                bt.trainModel()

    def create_scrapy_content_file_name(self, domain):
        file_name = domain.replace('.', '_').replace('/', '_')
        file_name += '.jl'
        return str(file_name)

print(sys.argv[1])

config_p = ConfigData(str(sys.argv[1]))
config_p.run_bert_with_individual_domains()