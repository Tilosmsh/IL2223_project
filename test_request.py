import requests
import os.path
import csv
import json
import requests
import time
from datetime import datetime


with open("./test.csv", "w") as f:
    headers = ["referenceTime", "t", "ws", "prec1h", "fesn1h", "vis", "confidence", "congestionLevel"]

    csv_writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)

    if f.tell() == 0:
        csv_writer.writeheader()  # file doesn't exist yet, write a header

    # Get traffic data of E4 entering KTH Kista from tomtom API, updated in real time

    response_tomtom = requests.get(
                'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=azGiX8jKKGxCxdsF1OzvbbWGPDuInWez&point=59.39575,17.98343')
    json_response_tomtom = json.loads(response_tomtom.text)  # get json response

    currentSpeed = json_response_tomtom["flowSegmentData"]["currentSpeed"]
    freeFlowSpeed = json_response_tomtom["flowSegmentData"]["freeFlowSpeed"]
    congestionLevel = currentSpeed/freeFlowSpeed

    confidence = json_response_tomtom["flowSegmentData"]["confidence"] # Reliability of the traffic data, by percentage


    # Get weather data from SMHI, updated hourly

    response_smhi = requests.get(
                'https://opendata-download-metanalys.smhi.se/api/category/mesan1g/version/2/geotype/point/lon/17.983/lat/59.3957/data.json')
    json_response_smhi = json.loads(response_smhi.text) 

    # weather data manual https://opendata.smhi.se/apidocs/metanalys/parameters.html#parameter-wsymb
    referenceTime = json_response_smhi["referenceTime"]

    t             = json_response_smhi["timeSeries"][0]["parameters"][0]["values"][0] # Temperature
    ws            = json_response_smhi["timeSeries"][0]["parameters"][4]["values"][0] # Wind Speed
    prec1h        = json_response_smhi["timeSeries"][0]["parameters"][6]["values"][0] # Precipation last hour
    fesn1h        = json_response_smhi["timeSeries"][0]["parameters"][8]["values"][0] # Snow precipation last hour
    vis           = json_response_smhi["timeSeries"][0]["parameters"][9]["values"][0] # Visibility

    
    csv_writer.writerow({"referenceTime": referenceTime, 
                        "t": t, 
                        "ws": ws, 
                        "prec1h": prec1h, 
                        "fesn1h": fesn1h, 
                        "vis": vis, 
                        "confidence": confidence, 
                        "congestionLevel": congestionLevel})  # write to csv

print("done")