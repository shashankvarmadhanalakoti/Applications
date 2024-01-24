import requests,csv,os
from datetime import date
from dotenv import load_dotenv
today = date.today()
load_dotenv()
ENV_FILE = os.getenv('KANDJI_API_KEY')
headers = {'Authorization':f'Bearer {ENV_FILE}','Accept':'application/json'}
default_apps = ['Activity Monitor', 'AirPort Utility','App Store', 'Audio MIDI Setup', 'Automator', 'Bluetooth File Exchange', 'Books', 'Boot Camp Assistant', 'Calculator', 'Calendar', 'Chess', 'Clock', 'ColorSync Utility', 'Console', 'Contacts', 'Dictionary', 'Digital Color Meter', 'Disk Utility', 'FaceTime', 'FindMy', 'Font Book', 'Freeform', 'Grapher', 'Home', 'Image Capture','Keychain Access', 'Launchpad', 'Mail', 'Maps', 'Messages', 'Migration Assistant', 'Mission Control', 'Music', 'News', 'Notes', 'Photo Booth', 'Photos', 'Podcasts', 'Postman', 'Preview', 'QuickTime Player', 'Reminders', 'Safari', 'Screenshot', 'Script Editor', 'Shortcuts', 'Siri','Stickies', 'Stocks', 'System Information', 'System Settings', 'TV', 'Terminal', 'TextEdit', 'Time Machine', 'VoiceMemos', 'VoiceOver Utility', 'Weather']
def getDevices():
    length = 99999
    offset = 0
    targetArr= []
    while length!=0:
        url = "https://juspay.clients.eu.kandji.io/api/v1/devices?limit=300&offset="+str(offset)
        resp = requests.get(url,headers=headers).json()
        for i in resp:
            if i['user']!='':
                targetArr.append({"device_id":i["device_id"],"username":i["user"]["name"]})
        length = len(resp)
        offset+=300
    return targetArr


def getInventory(deviceArray):
    targetArr = []
    for i in deviceArray[:10]:
        tempArr=[]
        deviceId = i["device_id"]
        url = f'https://juspay.clients.eu.kandji.io/api/v1/devices/{deviceId}/apps'
        resp = requests.get(url,headers=headers).json()
        print(i["username"])
        for j in resp["apps"]:
            if j["app_name"] not in default_apps:
                tempArr.append(j["app_name"])

        targetArr.append([i["device_id"],i["username"],tempArr])    
    return targetArr

def writeToCsv(inventoryArray):
    cols = ['Device ID','Username','Applications']
    with open(f'{today}.csv','w') as f:
        writer = csv.DictWriter(f,fieldnames=cols,delimiter='\t')
        writer.writeheader()
        for i in inventoryArray:
            writer.writerow({'Device ID':i[0],'Username':i[1],'Applications':i[2]})
    

if __name__ == "__main__":
    arr = [{'device_id': 'dc08ba4e-913d-4cce-9bdb-0acc65fcae8e', 'username': 'zeeshan.alam'}]
    devicesArr = getDevices()
    getInventoryArr = getInventory(devicesArr)
    writeToCsv(getInventoryArr)