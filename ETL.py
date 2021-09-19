import json
# import boto3
import csv
from datetime import datetime, timedelta
from datetime import date
import dateutil.parser
import re
import io
import codecs

# %%
print('hello')
with open('file.json', 'r', encoding='UTF-8') as json_data:
    serojb = json_data.read()
print(serojb)


# %%

def index_err(error):
    """
    :param error:
    :return: Index that contain exception
    """
    charloc = error.find('char')
    endnum = error.find(')', charloc)
    errorstr = error[charloc + 5:endnum]
    errornum = int(errorstr) - 1

    return errornum
# %%
def deleter(error, string):
    """
    try to delete characters make exception and make Valid JSON
    :param error: json.JSONDecodeError Error
    :param string: string
    """
    global obj
    err = True
    while err == True:
        try:
            indexerr = index_err(error)
            string = string[:indexerr] + string[indexerr + 1:]
            # print('change to', string)
            obj = json.loads(string)
            err = False
        except json.JSONDecodeError as e:
            error = e.__str__()
            return deleter(error, string)
    return obj

# %%
for row in serojb.split("\n"):
    if row:
        data = row[1:-1]
        try:
            cleanstr = data.replace("\\\"", "\"").replace("\"[", "[").replace("]\"", "]").replace("\\\\\"",
                                                                                                  "\"").replace(
                "\\\\\\\\\"", "").replace("/\\\\\\\\", "/\\\\\\\\\"")
            # Valid JSON
            # try to delete characters make exception
            print('string replaced' ,cleanstr)
            try:
                obj = json.loads(cleanstr)
            except json.JSONDecodeError as e:
                errorstr = e.__str__()
                obj = deleter(errorstr , cleanstr)
            print('valid json :' ,obj)


            newElement = {}
            # newElement["kafka_topic"] = file["topic"][7:-1]
            newElement["customerId"] = obj["customerId"]
            newElement["id"] = obj["id"]
            newElement = {"customerId": obj["customerId"], "id": obj["id"],
                          "timestamp": dateutil.parser.isoparse(obj["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")}
            # timestamp1=dateutil.parser.isoparse(obj["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            # newElement["timestamp"] = obj["timestamp"]
            if "fs_mid" in obj["properties"]:
                newElement["fs_mid"] = obj["properties"]["fs_mid"][0]
            else:
                print("Oops! 'fs_mid' missing for id =", newElement["id"], "at timestamp =", newElement["timestamp"])
                newElement["fs_mid"] = ""
            if "fs_survey_response_id" in obj["data"]:
                newElement["fs_survey_response_id"] = obj["data"]["fs_survey_response_id"]
            else:
                print("Oops! 'fs_survey_response_id' missing for id =", newElement["id"], "at timestamp =",
                      newElement["timestamp"])
                newElement["fs_survey_response_id"] = ""
            newElement["event_name"] = obj["name"]
            newElement["app_id"] = obj["appId"]
        except Exception as e:
            print("Oopsss!", e.args, "occurred, due to")
            print("Raw Data --->", data)
            print("Parsed String --->", cleanstr)
            # remove fs_text until , then make a clearstr2

# %%
