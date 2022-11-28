import datetime
import os
import shutil
import base64
import os, uuid
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pathlib

## q1
def getDigitFromString(string_digit):
    digits_dic = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "zero":0}
    return digits_dic[string_digit] if string_digit in digits_dic else False


## q2
def sumListOfNumbers(numbers_list):
   return s if [[s:=0],[[s:=s+number] for number in numbers_list]] else None

## q2
def sumListOfNumbers(numbers_list):
   return [[s:=0],[[s:=s+number] for number in numbers_list]][1][-1][0]


## q3
def removeVowels(word):
    return ''.join([char for char in word if char not in "auoie"])

## q4
def countEightsAndZeros(btm, top):
    return len([1 for i in range(btm,top+1) if '0' in str(i) or '8' in str(i)])


## q5
def save_data(file_name, objects):
    f = open(file_name, "w")
    for element in objects: f.write(str(element) + " : " + str(type(element)) + "\n")
    f.close()


def load_data(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    l = []
    for line in lines:
        splited = line.split(":")
        val, typ = splited[0], splited[1]
        if "int" in typ:
            l.append(int(val))
        if "float" in typ:
            l.append(float(val))
        if "bool" in typ:
            l.append(bool(val))
        if "str" in typ:
            l.append(val[:-1])
    f.close()
    return l

## q6
def timeTill_Birthday(bday):
    now_date = datetime.datetime.now().date()
    closest_bday = datetime.date(year=now_date.year, month=bday.month, day=bday.day)
    delta = int((closest_bday - now_date).days)
    if delta > 0:
        days = str(delta)
    else:
        if delta == 0:
            print("Happy Birthday!!!")
            return ""
        days = str(365+delta)
    return days + " days till birthday :)"


## q7

def copyDirectoryFilterByType(src_dir, dst_dir, formats_to_include=[]):
    os.mkdir(dst_dir)
    copyRec(src_dir, dst_dir, formats_to_include)

def copyRec(src_dir, dst_dir, formats_to_include=[]):
    for element in os.listdir(src_dir):
        src_path = src_dir + "/" + element
        dst_path = dst_dir + "/" + element
        if os.path.isdir(src_path):
            os.mkdir(dst_path)
            copyRec(src_path, dst_path, formats_to_include)
        if os.path.isfile(src_path):
            format = src_path.split(".")[-1]
            if format in formats_to_include:
                shutil.copyfile(src_path, dst_path)

## q8
def copyFilesContainer():
    container_name = "python"
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=onboardingpractice;AccountKey=7nUB5BsakecXpB7r2ETp02p+DKjv8ZBJ3uWqNUqq4orYq+V8C+vTGKiSPUPNJoa1PJ702mYKQuBq+AStFz+bzQ==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    os.mkdir(str(pathlib.Path().resolve()) + "/decodedFiles")
    for blob in blob_list:
        file_path = str(pathlib.Path().resolve()) + "/" + blob.name
        with open(file=str(pathlib.Path().resolve())+"/"+blob.name, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())
        decoded_file_path = str(pathlib.Path().resolve()) + "/decodedFiles/" + blob.name[:-4] + "_decoded.txt"
        print(decoded_file_path)
        decoded_file = open(decoded_file_path, 'w')
        file = open(file_path)
        with open(file_path) as my_file:
            for line in my_file:
                b = base64.b64decode(line)
                decoded_file.write(b.decode("utf-8"))
        decoded_file.close()
        file.close()

    container_name = "decodedcontainer"
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=pythonexerciseomer;AccountKey=2fjlv0VlFNxw0K0AEany/JV1FzSNM/wuNBTOxeQncHDjFuTv8UzwI9Ib3lOo/1k2YMSx3ebfRcqm+AStoRxxqA==;EndpointSuffix=core.windows.net")
    for file in os.listdir(str(pathlib.Path().resolve()) + "/decodedFiles"):
        print(file)
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file)
        print("\nUploading to Azure Storage as blob:\n\t" + file)
        # Upload the created file
        with open(file=str(pathlib.Path().resolve()) + "/decodedFiles/" + file , mode="rb") as data:
            blob_client.upload_blob(data)




