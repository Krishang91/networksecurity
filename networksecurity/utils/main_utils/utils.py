import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np 
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool =False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            return yaml.dump(content,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
def save_numpy_array_data(filepath:str,array:np.array):
    
    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
def save_object(filepath:str,obj:object):
    
    try:
        logging.info("entered the save_object method of MainUtils class")
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    try:
        report = {}
        for model_name, model in models.items():
            # Get parameters for this specific model
            params = param[model_name]
            
            # Perform GridSearchCV
            gs = GridSearchCV(model, params, cv=3)
            gs.fit(x_train, y_train)
            
            # Set best parameters and fit model
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)  # This should be y_train, not x_test
            
            # Make predictions
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            
            # Calculate scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            # Store results
            report[model_name] = test_model_score
        
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)  # Better to raise your custom exception