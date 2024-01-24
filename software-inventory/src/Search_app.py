import requests,csv,os
from datetime import date
from dotenv import load_dotenv
today = date.today()
load_dotenv()
ENV_FILE = os.getenv('KANDJI_API_KEY')
headers = {'Authorization':f'Bearer {ENV_FILE}','Accept':'application/json'}
searchApp = "Postman"
users_containing = []
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
    specificApps = []
    for i in deviceArray[:10000]:
        tempArr=[]
        deviceId = i["device_id"]
        url = f'https://juspay.clients.eu.kandji.io/api/v1/devices/{deviceId}/apps'
        resp = requests.get(url,headers=headers).json()
        print(i["username"])
        # print(resp["apps"])
        for j in resp["apps"]:
            tempArr.append(j["app_name"])
        if searchApp in tempArr:
            # users_containing.append(i["username"])
            specificApps.append([i["device_id"],i["username"],searchApp])

        targetArr.append([i["device_id"],i["username"],tempArr])    
    
    # return targetArr
    return specificApps

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
    print(getInventoryArr)
    writeToCsv(getInventoryArr)