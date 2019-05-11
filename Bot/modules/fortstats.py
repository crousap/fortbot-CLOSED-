import requests, math, json

FORTNITE_API_KEY = "d1585f66-ee86-4658-87e9-0385a86e8aa8"


def get_ratio(username):
    link = 'https://api.fortnitetracker.com/v1/profile/pc/' + username
    response = requests.get(link, headers={'TRN-Api-Key': FORTNITE_API_KEY})
    if response.status_code == 200:
        collection = response.json()
        if 'error' in collection:
            return "-1"
        else:
            for data_item in collection['lifeTimeStats']:
                if data_item['key'] == 'K/d':
                    ratio = data_item['value']
                    return float(ratio)
        return "-1"
    else:
        return "-2"

def chose_role(UserKda):
    if UserKda == "-1":
        return "-1"
    RoleFile = "modules/fortroles.json"
    with open(RoleFile, 'r') as OTempFile:
        KDA_ROLES = json.load(OTempFile)
        for kda in KDA_ROLES:
            if UserKda >= KDA_ROLES[kda]:
                return kda

def KdaRole(username: str):
    return chose_role(get_ratio(username))


