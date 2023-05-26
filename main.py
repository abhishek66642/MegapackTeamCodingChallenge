# Import Statements
from typing import Union
from fastapi import FastAPI,Response,status
from pydantic import BaseModel
import json
from datetime import datetime

# In Memory Buffer for non persistent storage of incorrectly formatted strings
incorrectly_formatted_strings = []

# Intitializing FastAPI object
app = FastAPI() 

class Data(BaseModel):
    data:str

@app.get("/")
def read_root():
    return {"message": "Tesla Megapack Coding Challenge"}

#POST definitions
@app.post("/temp")
async def read_json(__data_string__:Data,response:Response):
    """
    FastAPI Post Response Function to check the temperature 
    and return response whether it's over specified temperature,
    If invalid formatted string is sent, HTTP 404 error 
    is raised 
    """

    try:
        data_list = __data_string__.data.split(":")

        # Checking Correct Formatting of Response Body String 
        if (len(data_list)!=4 or 
            data_list[2]!="'Temperature'"):
            raise ValueError
        else:
            # Checking Conversion of Data Types with try catch block
            __device_id__ = int(data_list[0])
            __epoch_ms__ = int(data_list[1])
            __temperature__ = float(data_list[3])
        
        # Checking >=90.0 temperature condition
        if (__temperature__>=90.0):
            # Required Date Time Format
            __date_format__ = "%Y/%m/%d %H:%M:%S"
            
            # Formatting Epoch timestamp to stored format
            __formatted_datetime__ = datetime.fromtimestamp(__epoch_ms__/1000.0).strftime(__date_format__)
            
            return {"overtemp":True,
                    "device_id":__device_id__,
                    "formatted_time":__formatted_datetime__
                    }
        else:
            return {"overtemp":False}
    except ValueError:
        print ("Incorrect Formatting specified in Request Body")
        response.status_code = status.HTTP_404_NOT_FOUND
        incorrectly_formatted_strings.append(__data_string__.data)
        return {"error":"bad request"}

@app.get("/errors")
def get_errors():
    """
    GET Request to get incorrectly formatted strings
    """
    return {"errors":incorrectly_formatted_strings}

@app.delete("/errors")
def delete_errors():
    """
    DELETE Request to clear the Errors buffer which contains
    incorrectly formatted strings.
    """
    global incorrectly_formatted_strings
    incorrectly_formatted_strings = []
    return {"message":"Successfully Cleared Buffer"}
