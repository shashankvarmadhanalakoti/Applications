import requests,csv,os
from datetime import date
from dotenv import load_dotenv
today = date.today()
load_dotenv()
ENV_FILE = os.getenv('KANDJI_API_KEY')
print(ENV_FILE)
def getUsers():
    length = 99999
    offset = 0
    headers = {'Authorization':f'Bearer {ENV_FILE}','Accept':'application/json'}
    finalArr= []
    while length!=0:
        url = "https://juspay.clients.eu.kandji.io/api/v1/devices?limit=300&offset="+str(offset)
        resp = requests.get(url,headers=headers).json()
        for i in resp:
            # print(i)
            if i['user']!='':
                tempArr = [i['device_name'],i['serial_number'],i['user']['email'],i['user']['name'],i['os_version'],i['model'],i['last_check_in']]
            else:
                tempArr = [i,'',['serial_number'],'','','','']
            finalArr.append(tempArr)
        # breaks
        length = len(resp)
        offset+=300

    cols = ['Endpoint Name','Serial Number','Azure ID','User Name','OS Version','Model','last_check_in']
    with open(f'{today}-KandjiUsers.csv','w') as f:
        writer = csv.DictWriter(f,fieldnames=cols,delimiter='\t')
        writer.writeheader()
        for i in finalArr:
            writer.writerow({'Endpoint Name':i[0],'Serial Number':i[1],'Azure ID':i[2],'User Name':i[3],'OS Version':i[4],'Model':i[5],'last_check_in':i[6]})