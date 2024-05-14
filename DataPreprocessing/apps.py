import os
from Log.logger import Logger
from Data.TrainingDataSet.Columns import Columns
import pandas as pd

class Datapreprocessing():
    def __init__(self, processId="testing"):
        self.processId = processId
        self.logPath = "Log\Datapreprocessing.log"
        self.path = "Data\TrainingDataSet"
        log = Logger(self.logPath, self.processId)
        log.loggerCall("DataProcessing Initiate", "Information")
        # Check if the log directory exists, if not, create it
        log_directory = os.path.dirname(self.logPath)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

    def textDataToCsvConvertion(self):
        log = Logger(self.logPath, self.processId)
        try:
            log.loggerCall("textDataToCsvConvertion method Invoked", "Information")
            fileList = os.listdir(self.path)
            processed_dir = "Data\ProcessedTrainDataset"
            if not os.path.exists(processed_dir):
                os.mkdir(processed_dir)
                log.loggerCall("ProcessedTrainDataset directory created", "Information")

            for file in fileList:
                if file[:5] == 'train' or file[:3] == 'RUL':
                    with open(os.path.join(self.path, file), "r") as rawData:
                        raw = rawData.readlines()
                        if file[:3] == 'RUL':
                            with open(os.path.join(processed_dir, file[:9] + ".csv"), "w+") as cleanData:
                                for data in raw:
                                    cleanData.write(data.replace(" ", ","))
                        else:
                            with open(os.path.join(processed_dir, file[:11] + ".csv"), "w+") as cleanData:
                                for data in raw:
                                    cleanData.write(data.replace(" ", ","))            
        except Exception as error:
            log = Logger(self.logPath, self.processId)
            log.loggerCall("DataProcessing got an Exception saying " + str(error), "Information")
    
    def load_and_merge_data(self, dataset_number):
        # Define file paths
        data_file = f"Data/ProcessedTrainDataset/train_FD00{dataset_number}.csv"
        label_file = f"Data/ProcessedTrainDataset/RUL_FD00{dataset_number}.csv"
        
        # Load data and label
        data = pd.read_csv(data_file, names=Columns)
        label = pd.read_csv(label_file, names=["RemainingUsefulLife"])
        
        # Get unique unit numbers
        unique_units = data["unit number"].unique()
        
        # Create a dictionary to map unit numbers to RUL values
        unit_rul_mapping = {}
        
        # Assign RUL values for each unit
        for unit in unique_units:
            unit_rul_mapping[unit] = label.iloc[0]["RemainingUsefulLife"]  # Assuming the RUL values are the same for all observations of each unit
        
        # Map RUL values to each observation in data based on unit number
        data["EngineLifeLeft"] = data["unit number"].map(unit_rul_mapping)
        return data

    def cleaningData(self):
        for i in range(1, 5):
            merged_data = self.load_and_merge_data(i)
            print(merged_data.shape, 1, merged_data.head(1))
            pass

obj = Datapreprocessing()
obj.cleaningData()
