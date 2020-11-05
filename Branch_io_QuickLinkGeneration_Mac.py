
from tqdm import * 
from requests import post,get
from json import dumps, loads
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
import sys 
import os
from pymsgbox import confirm
import base64
from csv import writer
import ssl


Property = confirm("Please Choose the domain you want to create link for?",buttons = ["cashkaro","earnkaro"])




try:
    os.mkdir(f"{Property}_Output")
except:
    pass

# API_URI = "https://api2.branch.io/v2/logs?app_id=816330814798188722"
API_URI = "https://api2.branch.io/v1/url"

def Define_AcessToken():
    if Property == "cashkaro": 
        Access_Token = "key_live_nfNXstvhmXbdOmWAccVYzemoDvhlO0oV" 
    elif Property == "earnkaro":
        Access_Token = "key_live_hpK2iKNJZel77knxvSCjaphpCtdeG0ef" 
    return Access_Token        

# def Define_AcessToken():
#     if Property == "cashkaro": 
#         Access_Token = "key_test_bkGWrCCgh8enLmWzipRZBmfhrDeaH0cY" 
#     elif Property == "earnkaro":
#         Access_Token = "key_test_khT8eJVK2ghY2lcCAUudgiggAFdcHPY9" 
#     return Access_Token        


def Exit(error=True):

    x = input("\nERROR DETECTED PRESS ENTER TO EXIT....... ") if error else input("\n\nCODE EXECUTED SUCESSFULLLY PRESS ENTER TO EXIT....... ")
    sys.exit()


def print_log(text, r_end = False, up = True):
    if up:
        text = text.upper()
    if r_end:
        print("[ INFO ] -- BRANCH_LINK_GENERATOR- {} -- {} ".format(datetime.now(),text) + (" "*((50-len(text)))) ,  end="\r")
    else :
        print("[ INFO ] -- BRANCH_LINK_GENERATOR- {} -- {} ".format(datetime.now(),text) + (" "*((50-len(text)))) )


def Sleeper(seconds):
    for i in range(seconds):
        print_log("Sleeping for {} seconds". format(seconds-i), r_end = True)
        sleep(1)


def Input_Check_APP_URI(input_dict, i):
    if not input_dict["App_URI"].lower().startswith(f"{Property}://".lower()):
        print_log("ERROR IN APP URI ON ROW NUMBER {}".format(i+2))
        print_log("APP URI {} IS INVALID PLEASE CORRECT AND RESTART".format(input_dict["App_URI"]))
        print_log(f"Comments : APP URI MUST START WITH {Property}://")
        Exit()
    if ".com" in input_dict["App_URI"].lower() or ".com" in input_dict["App_URI"].lower():
        print_log("ERROR IN APP URI ON ROW NUMBER {}".format(i+2))
        print_log("Comments : APP URI MUST NOT CONTAIN .com or .in in it")
        Exit()
    return True


def Input_Check_WEB_URL(input_dict,i):
    if not input_dict["WEB_URL"].lower().startswith(f"https://{Property}.com".lower()):
        print_log("ERROR IN WEB_URL ON ROW NUMBER {}".format(i+2))
        print_log("Web URL {} IS INVALID PLEASE CORRECT AND RESTART".format(input_dict["WEB_URL"]))
        print_log(f"Comments : WEB_URL MUST START WITH https://{Property}.com")
        Exit()
    return True
        
def input_Check_Channel(input_dict, AdminValidations, i):
    if input_dict["Channel"] == "":
        print_log(f"CHANNEL ON ROW {i+2} CANNOT BE LEFT BLANK !!!!")
        Exit()
    elif input_dict["Channel"] not in AdminValidations["Channel"].tolist():
        print_log(f"CHANNEL ON ROW {i+2} ::  {input_dict['Channel']} IS NOT PRESENT IN THE ADMIN VALIDATION DOC !!!", up = False)
        print_log(f"PLEASE ASK ROHAN/ROHIT/YATIN/ARUN TO ADD {input_dict['Channel']} AS A CHANNEL IN THE ADMIN VALIDATION DOC !!!", up = False)
        Exit()
    return True

def input_Check_Feature(input_dict, AdminValidations, i ):
    if input_dict["Feature"] == "":
        print_log(f"FEATURE ON ROW {i+2} CANNOT BE LEFT BLANK !!!!")
        Exit()
    elif input_dict["Feature"] not in AdminValidations["Feature"].tolist():
        print_log(f"FEATURE ON ROW {i+2} :: {input_dict['Feature']} IS NOT PRESENT IN THE ADMIN VALIDATION DOC !!!", up = False)
        print_log(f"PLEASE ASK ROHAN/ROHIT/YATIN/ARUN TO ADD {input_dict['Feature']} AS A FEATURE IN THE ADMIN VALIDATION DOC !!!",up = False)
        Exit()
    return True

def input_Check_OWNER(input_dict, AdminValidations, i ):
    if input_dict["Owner"] == "":
        print_log(f"OWNER ON ROW {i+2} CANNOT BE LEFT BLANK !!!!")
        Exit()
    # elif input_dict["Owner"] not in AdminValidations["Owner"].tolist():
    #     print_log(f"OWNER :: {input_dict['Owner']} DONOT HAVE PERMISSION TO CREATE QUICK LINKS !!!", up = False)
    #     print_log(f"PLEASE ASK ROHAN/ROHIT/YATIN/ARUN TO ADD {input_dict['Owner']} AS A OWNER IN THE ADMIN VALIDATION DOC !!!",up = False)
    #     Exit()
    return True


def Ip_check(AdminValidations):
    print_log("GETTING IP RESTRICTIONS !!!")
    if AdminValidations['IP_Protection'].tolist()[0].lower().replace(' ','') == "yes":
        AllowedIP = '219.65.46.134'
        print_log(f"IP Restricted only Ip Allowed is :: {AllowedIP}")
        ip = get('https://checkip.amazonaws.com').text.strip()

        if ip == AllowedIP:
            True
        else:
            print_log(f"Your IP :: {ip} Does not match with the Allowed IP :: {AllowedIP}")
            print_log(f"Please Connect to the VPN")
            Exit()
    else:
        print_log("admin privileges All IPs Allowed")


def ReadFile():
    print_log("Reading File Started")
    QuickLinkShell  = pd.read_excel("QuickLinkShell.xlsx", sheet_name = "Input Sheet", dtype = "str")
    QuickLinkShell  = QuickLinkShell.dropna(subset = ['App_URI'])
    QuickLinkShell = QuickLinkShell.fillna("").to_dict("records")
    print_log("Reading File Succesful")
    return QuickLinkShell


def Validation(QuickLinkShell, AdminValidations):
    Ip_check(AdminValidations)      
    print_log("Starting Validation Checking for File")
    counter=0
    for i,record in enumerate(QuickLinkShell):
        print_log("Validating the File."+ counter *".", r_end = True)
        sleep(.2)
        Input_Check_APP_URI(record,i)
        Input_Check_WEB_URL(record,i)
        input_Check_Channel(record, AdminValidations, i)
        input_Check_Feature(record, AdminValidations, i )
        input_Check_OWNER(record, AdminValidations, i )

        counter += 2
        counter = 0 if counter == 8 else counter 
    print_log("File Succesfully validated.")





def WebLink(link, refid, refname):
    if refid == "": return link
    if refname == "" : refname = "Cashkaro"
    return link.split('?')[0] + f"?r={refid}&fname={refname}"


def Andriod_Link(input_dict):
    if input_dict["Mandatory_App_Install"].lower() == "yes":
        return f"https://play.google.com/store/apps/details?id=com.{Property}"
    else:
        return WebLink(input_dict["WEB_URL"] , input_dict["ReferralID"], input_dict["ReferralName"])




def Define_Payload(input_dict):    
    headers = {"Content-Type": "application/json",}           
    
    payload = {
      "branch_key": Define_AcessToken(),
      "channel": input_dict["Channel"],
      "feature": input_dict["Feature"],
      "campaign": input_dict["Campaign"],
      "type" : 2,
      "data": {
        "$deeplink_path":           WebLink(input_dict["WEB_URL"] , input_dict["ReferralID"], input_dict["ReferralName"]),
        "$android_deeplink_path":   input_dict["App_URI"] + "?r={}".format(input_dict["ReferralID"]) if input_dict["ReferralID"] != "" else input_dict["App_URI"] ,
        "refName"               :   input_dict["ReferralName"],
        "$desktop_url":             WebLink(input_dict["WEB_URL"], input_dict["ReferralID"], input_dict["ReferralName"]),
        "$android_url":             Andriod_Link(input_dict),
        "$ios_url":                 WebLink(input_dict["WEB_URL"], input_dict["ReferralID"], input_dict["ReferralName"]),
        "$marketing_title" :        f"{input_dict['Channel']}_" + str(datetime.now()),
        "Creation_Date"  : datetime.now().strftime("%d-%b-%Y"),
        "Offer"          :input_dict["Offer"] ,
        "Cashback"       :input_dict["Cashback"]   ,
        "CreativeType"   :input_dict["CreativeType"]   ,
        "Retailer"       :input_dict["Retailer"]   ,
        "Channel Type"   :input_dict["Channel Type"]   ,
        "influencer_name": input_dict['influencer_name'],
        "Owner"          :input_dict["Owner"] ,
        "Time"           :input_dict["Time"]   ,
        "BannerLocation" :input_dict["BannerLocation"]   ,
        "Segment"        :input_dict["Segment"] ,
        "VideoType"      :input_dict["VideoType"] ,
        "Device Type"    :input_dict["Device Type"] ,
        "OptimizedFor"   :input_dict["OptimizedFor"] ,
        "ReferralID"   : input_dict["ReferralID"]
      }
    }
    return headers, payload

def main(headers, payload):
    for i in range(5):
        branch_quick_link_api_response = post(API_URI, headers = headers, data = dumps(payload), timeout=20)
        print_log(f"Attempting for the {i} time", r_end = True)
        if branch_quick_link_api_response.status_code ==200:
            print_log(branch_quick_link_api_response.json()['url'],up = False)
            return branch_quick_link_api_response.json()['url']
            break
        Sleeper(3)

print("\n")
print_log(f"WELCOME TO {Property} BRANCH QUICK LINK GENERATOR")
print("\n")

try:
    print_log("GETTING ADMIN PERMISSIONS !!!! ")
    AdminValidations = pd.read_csv('https://branchquicklinkadmin.s3.ap-south-1.amazonaws.com/QuickLinkValidations.csv?versionId=null')
    print_log("ADMIN PERMISSIONS GRANTED SUCCESFULLY !!!! ")

except:
    print_log("UNABLE TO CONNECT TO PLEASE CHECK YOUR INTERNET CONNECTION AND TRY AGAIN !!!!")  
    Exit()




if __name__ == "__main__":
    QuickLinkInput = ReadFile()
    Validation(QuickLinkInput, AdminValidations)

    with open("{}_Output\\QuickLinks_{} {}.csv".format(Property,Property,datetime.now().strftime("%d-%b-%Y-%H %M %S")), 'w', newline ="") as f:
        writer = writer(f,delimiter = "~")
        writer.writerow(["QuickLink","App_URI","Mandatory_App_Install","WEB_URL","Channel","Feature","Campaign","Offer","Cashback",
            "CreativeType","Retailer", 'ReferralID' , 'ReferralName' ,"Channel Type","VideoType", "influencer_name", "Owner","Time","BannerLocation",
            "Segment","Device Type","OptimizedFor"])
        for input_dict in QuickLinkInput:
            headers, payload = Define_Payload(input_dict)
            link = main(headers, payload)
            writer.writerow([link, input_dict["App_URI"], input_dict["Mandatory_App_Install"], input_dict["WEB_URL"], input_dict["Channel"], input_dict["Feature"], input_dict["Campaign"], input_dict["Offer"], 
                input_dict["Cashback"], input_dict["CreativeType"], input_dict["Retailer"], input_dict['ReferralID'] , input_dict['ReferralName'], 
                input_dict["Channel Type"], input_dict["VideoType"], input_dict["influencer_name"] ,input_dict["Owner"], input_dict["Time"], input_dict["BannerLocation"], 
                input_dict["Segment"], input_dict["Device Type"],
                input_dict["OptimizedFor"]])
    print("\n")
    print_log("File Created Succesfully")    
    Exit(error=False)
