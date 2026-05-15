# OpenSniper V1.0 (first ever public release idk if it's gonna go well lol)

# in retaliation against monetized software, this has been made.

print("by .lunary. fr fr")

# .lunary. on dc, dms open, i take suggestions and listen to my beautiful community
# if i dont respond on .lunary. then dm lunatic.dev (alternate acc)

# i don't put my discord server and credits in the ui because im legit and not a bum
# discord.gg/7zuFCT8kYJ

# wild guess: doggie will verify grief on 4th of april
#     /\
#     |
# that didnt age well

#   [ <<TIDAL<<< ]
#   [ >>>WAVE>>> ]

# these packages are built into python so i dont need to check if they're installed or not
from pathlib import Path
import subprocess
import threading
import datetime
import logging
import asyncio
import ctypes
import math
import time
import json
import sys
import os
import re

# stop discord from yapping in the console
for logger_name in ["discord", "discord.client", "discord.http", "discord.gateway"]:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.WARNING)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

# function to install packaages if missing (package = import)
def ensure(name, pkg=None):
    try:
        __import__(name)
    except ImportError:
        print("installing:", name)
        pkg = pkg or name

        subprocess.check_call([
            sys.executable, "-m", "pip", "install", pkg
        ])

        __import__(name)
        

# --------------------------------------------------------------



# === importing packages === #

ensure("requests")
ensure(
    "discord",
    "https://github.com/dolfies/discord.py-self/archive/refs/heads/main.zip" # you need git if u want this to install
)
ensure("colorama")
ensure("PyQt6")

# ---

import requests
import discord

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QVariantAnimation
from PyQt6.QtGui import QIntValidator
from discord.ext import commands
from PyQt6.QtGui import QColor
from colorama import init

init() # colorama helps show colors in consoles where text color is not supported

# === importing packages === #



# -------------------------------



# === settings === # 

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

SETTINGS_PATH = BASE_DIR / "settings.json"

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_settings():
    # create file with {} if it doesn't exist
    if not SETTINGS_PATH.exists():
        # ensure parent directory exists
        ensure_directory(SETTINGS_PATH.parent)
        with open(SETTINGS_PATH, "w") as f:
            f.write("{}")  # default empty JSON
        return {}
    
    # if it exists, load it
    with open(SETTINGS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # if the file is corrupt, reset to {}
            return {}

def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

def check_token_access(token):
    headers = { "Authorization": token }
    rq = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if rq.status_code != 200:
        return False
    else:
        return True
        
def check_cookie_access(cookie: str) -> bool :
    try:
        resp = requests.post("https://auth.roblox.com/v1/logout", cookies={".ROBLOSECURITY": cookie})
        TokenTest = resp.headers.get("x-csrf-token")
        if TokenTest:
            return True
    except Exception as e:
        return False
        
def verify_access():
    obtainedToken = False
    obtainedCookie = False
    obtained = False
    while not obtained:
        if obtainedToken and obtainedCookie:
            obtained = True
            print("\n\n\n\033[92mI'm done setting it up!\033[0m")
            continue
        if not obtainedToken:
            if not settings.get("discordToken", None):
                print("\n\033[91mYou don't have a discord token set up.\033[0m")
                
                tkn = input("\n\n\033[90m(needed for sniping, look up a tutorial on how to get it if u don't know how)\n\033[93mInsert discord token to access messages\n\033[90m> \033[96m")
                print("\033[0m")
                if check_token_access(tkn):
                    settings['discordToken'] = tkn
                    save_settings(settings)
                    print("\n\033[92mValid token, updated settings.json!\033[0m")
                    obtainedToken = True
                else:
                    print("\n\033[91mInvalid token.\033[0m")
                    continue
            else:
                if check_token_access(settings.get("discordToken", None)):
                    print("\n\033[92mToken from settings.json valid\033[0m")
                    obtainedToken = True
                else:
                    print("\n\033[91mToken from settings.json is invalid, insert a new one.\033[0m")
                    settings['discordToken'] = ""
                    save_settings(settings)
                    continue
                    
        if not obtainedCookie:        
            if not settings.get("robloxCookie", None):
                print("\n\033[91mYou don't have a roblox cookie set up.\033[0m")
                
                cookie = input("\n\n\033[90m(protects you from joining other games, it can be any cookie, even an alt, it just needs to be valid.)\n\033[93mInsert a roblox cookie to resolve share links\n\033[90m> \033[96m")
                print("\033[0m")
                if check_cookie_access(cookie):
                    settings['robloxCookie'] = cookie
                    save_settings(settings)
                    print("\n\033[92mValid cookie, updated settings.json!\033[0m")
                    obtainedCookie = True
                else:
                    print("\n\033[91mInvalid cookie.\033[0m")
                    continue
            else:
                if check_cookie_access(settings.get("robloxCookie", None)):
                    print("\n\033[92mCookie from settings.json valid\033[0m")
                    obtainedCookie = True
                else:
                    print("\n\033[91mCookie from settings.json is invalid, insert a new one.\033[0m")
                    settings['robloxCookie'] = ""
                    save_settings(settings)
                    continue
    
if not settings.get("whitelisted_channels", []):
    settings['whitelisted_channels'] = [
                                        1282554696032194593,   # others channel
                                        1282542323590496277,   # biomes channel
                                        1282543762425516083,   # merchants channel
                                        1396065160354988132    # boss raid channel
                                       ]
    save_settings(settings)

if settings.get("blacklisted_content", []) is None:
    settings["blacklisted_content"] = []
    save_settings(settings)

if settings.get("console_enabled") is None:
    settings['console_enabled'] = True
    save_settings(settings)

if settings.get("glitch_enabled") is None:
    settings['glitch_enabled'] = True
    save_settings(settings)
    
if settings.get("dreamspace_enabled") is None:
    settings['dreamspace_enabled'] = True
    save_settings(settings)

if settings.get("cyberspace_enabled") is None:
    settings['cyberspace_enabled'] = True
    save_settings(settings)
    
if settings.get("singularity_enabled") is None:
    settings['singularity_enabled'] = True
    save_settings(settings)
    
if settings.get("custom_keywords_enabled") is None:
    settings['custom_keywords_enabled'] = False
    save_settings(settings)
    
if settings.get("custom_keywords") is None:
    settings['custom_keywords'] = ["", "", ""]
    save_settings(settings)

if settings.get("ignore_newer_accounts") is None:
    settings['ignore_newer_accounts'] = True
    save_settings(settings)
    
if settings.get("ignore_newer_accounts_MinAgeInDays") is None:
    settings['ignore_newer_accounts_MinAgeInDays'] = 7
    save_settings(settings)
    
if settings.get("show_ignore_logs") is None:
    settings['show_ignore_logs'] = True
    save_settings(settings)
    
if settings.get("alwaysontop_enabled") is None:
    settings['alwaysontop_enabled'] = True
    save_settings(settings)
    


# === settings === # 



# -------------------------------



# === sum constants === #

# sum_roles_idk_what_ill_do_with_them = {
#     "sol": "1197265038780678234",
#     "abomination": "1197265005066862643",
#     "luminosity": "1197265126517125311",
#     "oblivion": "1186579376406536255",
#     "memory": "1200695738506686464",
#     "oppression": "1199003278202122250",
#     "glitch": "1203579223588216842",
#     "aegis": "1204254360255864833",
#     "sovereign": "1271825230792359996",
#     "elude": "1271825651737034863",
#     "ruins": "1208737041248952350",
#     "gargantua": "1217305828147855491",
#     "abyssal hunter": "1232332529118482512",
#     "archangel": "1332476212047642729",
#     "lotusfall": "1232332045032620124",
#     "bloodlust": "1234899158033498132",
#     "impeached": "1271850493567569970",
#     "symphony": "1411472422355603566",
#     "overture": "1255019425753464904",
#     "matrix": "1296229031620120719",
#     "chromatic": "1238786194092064768",
#     "hades": "1238786753821671455",
#     "galaxy": "1271851500422823948",
#     "arcane": "1255018334362275890",
#     "bounded": "1313287432577355816",
#     "undead": "1345627607114186805",
#     "precious": "1217629072369127534"
# }

# === sum constants === # 



# -------------------------------



# === keywords son === #

# turns <space> into spaces
def clean_keywords(keywords):
    return [kw.replace("<space>", " ") for kw in keywords]

# fetches keywords (who would've thought)
def fetch_keywords(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = json.loads(response.text)

        GKeywords = clean_keywords(data.get("requiredG", []))
        DKeywords = clean_keywords(data.get("requiredD", []))
        JKeywords = clean_keywords(data.get("requiredJ", []))
        IKeywords = clean_keywords(data.get("ignoreKeywords", []))
        CKeywords = clean_keywords(data.get("requiredC", []))
        SKeywords = clean_keywords(data.get("requiredS", []))
        return GKeywords, DKeywords, JKeywords, IKeywords, CKeywords, SKeywords

    except Exception as e:
        print(f"Error fetching or parsing keywords: {e}")
        return [], [], [], [], []

# compares removed / new keywords and prints what got changed 
def compare_lists(name, old_list, new_list):
    added = [item for item in new_list if item not in old_list]
    removed = [item for item in old_list if item not in new_list]

    if added or removed:
        print(f"\033[94mChanges in {name}:\033[90m ")
        if added:
            print(f"  \033[92m+ Added:\033[90m {added}")
        if removed:
            print(f"  \033[91m- Removed:\033[90m {removed}")
    else:
        print(f"\033[90mNo changes in {name}.\033[90m ")

# initial load of keywords
GKeywords, DKeywords, JKeywords, IKeywords, CKeywords, SKeywords = fetch_keywords("https://raw.githubusercontent.com/Lunatic-T/Websniper/refs/heads/main/Keywords.json")

# calling this function will refetch the keywords from github and apply any new changes
def loadkw():
    global GKeywords, DKeywords, JKeywords, IKeywords, CKeywords, SKeywords

    url = "https://raw.githubusercontent.com/Lunatic-T/Websniper/refs/heads/main/Keywords.json"
    glitchk, dreamk, jesterk, ignorek, cyberk, singularityk = fetch_keywords(url)

    if glitchk and dreamk and jesterk and ignorek and cyberk and singularityk:
        changed = False
        if compare_lists("GKeywords", GKeywords, glitchk):
            changed = True
        if compare_lists("DKeywords", DKeywords, dreamk):
            changed = True
        if compare_lists("JKeywords", JKeywords, jesterk):
            changed = True
        if compare_lists("IKeywords", IKeywords, ignorek):
            changed = True
        if compare_lists("CKeywords", CKeywords, cyberk):
            changed = True
        if compare_lists("SKeywords", SKeywords, singularityk):
            changed = True

        if changed:
            print("\033[96mRefreshed Keyword List\033[90m ")
        # update globals to the new lists so next compare works correctly
        GKeywords = glitchk
        DKeywords = dreamk
        JKeywords = jesterk
        IKeywords = ignorek
        CKeywords = cyberk
        SKeywords = singularityk

# === keywords son === #



# -------------------------------



# === deeplink conversion === #

# search definitions
regex_share = re.compile(r"https:\/\/www\.roblox\.com/share\?code=([a-zA-Z0-9]+)")
regex_private = re.compile(
    r"https:\/\/www\.roblox\.com/games/15532962292(?:\/[^\s?]+)?(?:\?privateServerLinkCode=([a-zA-Z0-9]+))?"
)
regex_link = re.compile(r'https://(?:www\.)?roblox\.com/[^\s,]*', re.IGNORECASE)

# main converter function
def convert_to_deeplink(link: str) -> str | None:
    match_share = regex_share.match(link)
    match_private = regex_private.match(link)

    if match_share:
        access_code = match_share.group(1)
        deeplink = (
            f"roblox://navigation/share_links?code={access_code}&type=Server&pid=share&is_retargeting=true"
        )
        print("\033[34mConverted share link for joining\033[0m ")
        return deeplink

    if match_private:
        access_code = match_private.group(1)
        if access_code is None:
            print("\033[31mprivate server is none, cannot grab server link\033[0m ")
            return None
        deeplink = f"roblox://placeID=15532962292&linkCode={access_code}"
        print("\033[34mConverted private server link for joining\033[0m ")
        return deeplink

    print(f"Invalid link: {link}")
    return None
    
# link extraction fr
def extract_share_code(url: str) -> str | None:
    match = regex_share.match(url)
    if match:
        return match.group(1)
    return None
    
def extract_link_code(url: str) -> str | None:
    match = regex_private.match(url) # old regex: re.search(r'\?privateServerLinkCode=([0-9]+)', url)
    if match:
        return match.group(1)
    return None

def extract_placeid(url: str) -> str | None:
    match = re.search(r'roblox\.com/games/(\d+)', url)
    if match:
        return match.group(1)
    return None
    
# === deeplink conversion === #



# -------------------------------



# === solving link === #

def fetchcsrf():
    csrf_req = requests.post("https://auth.roblox.com/v1/logout", cookies={".ROBLOSECURITY": settings.get("robloxCookie", "")})
    return csrf_req.headers.get("x-csrf-token")
    
def csrfget():
    csrf = fetchcsrf()
    if not csrf:
        print("Could not get CSRF Token.")
        return None
    return csrf


def resolvesharelink(sharelink):
    res = requests.post("https://apis.roblox.com/sharelinks/v1/resolve-link", headers={"x-csrf-token": csrfget(), "Content-Type": "application/json"}, cookies={".ROBLOSECURITY": settings.get("robloxCookie", "")}, json={"linkId": sharelink, "linkType": "Server"})
    if res.ok:
        psdata = res.json().get("privateServerInviteData")
        if not psdata:
            print("NO PS DATA SON")
            return None
        if psdata.get("status") != "Valid":
            print("status not valid")
            return None
        return psdata.get("placeId"), psdata.get("linkCode"), psdata.get("ownerUserId")
        
def resolveprivatelink(linkcode):
    res = requests.post("https://gamejoin.roblox.com/v1/join-private-game", cookies={".ROBLOSECURITY": settings.get("robloxCookie", "")}, headers={"Content-Type": "application/json", "X-CSRF-TOKEN": csrfget(), "User-Agent": "Roblox/WinInet", "Referer": f"https://www.roblox.com/games/15532962292/", "Origin": "https://roblox.com"}, json={"placeId": 15532962292, "linkCode": linkcode})
    if res.ok:
        data = res.json()
        if not data:
            return None
        if not data["joinScript"]:
            return None
        if not data["joinScript"]["PrivateServerOwnerID"]:
            return None
        return data["joinScript"]["PrivateServerOwnerID"]

# === solving link === #



# -------------------------------



# === discord signals handling === #

bot = commands.Bot(command_prefix="4545645doggie_verify_grief_gd_op_doggie_verification_son156323") # im forced to put a command prefix because nothing is perfect in life

@bot.event
async def on_ready():
    print(f"\033[92mLogged in as \033[96m{bot.user}\033[92m.\033[0m")

@bot.event
async def on_message(m): # on message detects ALL messages, so we need to filter them by channels ok ohh

    if m.channel.id not in settings.get("whitelisted_channels", []): # filtering channels son
        return
    
    # ignore dms fr
    if m.guild is None:
        return
    
    
    # the message text (duh)
    msg_text = m.content
    
    # get this dude's acc age
    account_age = (datetime.datetime.now(datetime.timezone.utc) - m.author.created_at).days

    # get his roles (last 3 roles frr)
    roles = [role.name for role in m.author.roles[1:][-3:]]
    
    
    urls = regex_link.findall(msg_text.lower()) # findin urls
    
    if not urls:
        return
        
    link = urls[0] # gettin first url only
    
    # ignoring ppl who have sent bad links
    if str(m.author.id) in settings.get("blacklisted_content", []):
        print(f"that guy is blacklisted: <@{m.author.id}>")
        return
        
    # ignoring bad links
    if link in settings.get("blacklisted_content", []):
        print(f"this guy sent a blacklisted link: <@{m.author.id}> ({link})")
        return
        
    # ignoring newer users based on settings sonn
    if settings.get("ignore_newer_accounts") and account_age < settings.get("ignore_newer_accounts_MinAgeInDays"):
        return
    
    clean_text = re.sub(r'[^a-zA-Z0-9 ]+', '', msg_text.lower()) # this keeps only letters n numbers because sometimes ppl say g↓l↓i↓t↓c↓h or smth
	
    # ignoring messages with words like "spotted the sol" so it can tell whether a message is legit or not
    for kw in IKeywords:
        if kw.lower() in clean_text:
            if settings.get("show_ignore_logs"):
                
                if len(msg_text) >= 150:
                    print(f"\n\033[90;1m(only showing first 150 characters)\n\033[91mIgnored bcs of \"{kw.lower()}\": \033[90m{msg_text[:150]}\033[0m")
                else:
                    print(f"\n\033[91mIgnored bcs of \"{kw.lower()}\": \033[90m{msg_text}\033[0m")
            return

    kw_found = ""
    
    # finding words we want
    if settings.get("glitch_enabled", True):
        for kw in GKeywords:
            if kw.lower() in clean_text:
                deeplink = convert_to_deeplink(link)
                if not deeplink:
                    print("\033[91mLink is not valid, cannot join.\033[0m")
                    return
                kw_found = kw.lower()
                print(deeplink)
                os.startfile(deeplink)
                break
        
    if settings.get("dreamspace_enabled", True) and not kw_found:
        for kw in DKeywords:
            if kw.lower() in clean_text:
                deeplink = convert_to_deeplink(link)
                if not deeplink:
                    print("\033[91mLink is not valid, cannot join.\033[0m")
                    return
                kw_found = kw.lower()
                print(deeplink)
                os.startfile(deeplink)
                break
                
    if settings.get("cyberspace_enabled", True) and not kw_found:
        for kw in CKeywords:
            if kw.lower() in clean_text:
                deeplink = convert_to_deeplink(link)
                if not deeplink:
                    print("\033[91mLink is not valid, cannot join.\033[0m")
                    return
                kw_found = kw.lower()
                print(deeplink)
                os.startfile(deeplink)
                break
                
    if settings.get("singularity_enabled", True) and not kw_found:
        for kw in SKeywords:
            if kw.lower() in clean_text:
                deeplink = convert_to_deeplink(link)
                if not deeplink:
                    print("\033[91mLink is not valid, cannot join.\033[0m")
                    return
                kw_found = kw.lower()
                print(deeplink)
                os.startfile(deeplink)
                break
                
    if settings.get("custom_keywords_enabled", True) and not kw_found:
        for kw in settings.get("custom_keywords", []):
            if kw.lower() in clean_text:
                deeplink = convert_to_deeplink(link)
                if not deeplink:
                    print("\033[91mLink is not valid, cannot join.\033[0m")
                    return
                kw_found = kw.lower()
                print(deeplink)
                os.startfile(deeplink)
                break
                
    if not kw_found:
        return
        
    place_id = ""
    link_code = ""
    user_id = ""
        
    # grabbin info 
    if extract_share_code(link):
        data = resolvesharelink(extract_share_code(link))
        if data is None:
            print("no share link data. could be invalid.")
            return
        place_id, link_code, user_id = data
            
    elif extract_link_code(link):
        place_id = extract_placeid(link)
        link_code = extract_link_code(link)
        user_id = resolveprivatelink(link_code)
        
        if not user_id:
            print("private server link could be invalid, could not fetch server owner id.")
            return
    
    # showin info
    print("\a", "\n" * 5)
    print(f"\033[94mKeyword Detected: \033[93m'{kw_found}'\033[0m\n")
    
    print(f'\033[1;38;2;19;38;210;49m--- Message Content ---\033[0m')
    print(f' \033[96m• {m.content}\033[0m\n')
    
    print(f'\033[1;38;2;19;38;210;49m--- Message Sender Info ---\033[0m')
    print(f'\033[0;38;2;157;157;157;49m • User ID: \033[0;38;2;190;190;190;49m{m.author.id}\033[0m')
    if roles:
        formatted = "\033[1;38;2;215;215;215;49m" + ", ".join(roles) + "\033[0m"
        print(f'\033[0;38;2;157;157;157;49m • Roles: \033[0m{formatted}\033[0m')
    print(f'\033[0;38;2;157;157;157;49m • Display Name: \033[0;38;2;190;190;190;49m{m.author.display_name}\033[0m')
    print(f'\033[0;38;2;157;157;157;49m • Username: \033[0;38;2;190;190;190;49m{m.author.name}\033[0m\n')
    
    print(f'\033[1;38;2;19;38;210;49m--- Roblox Server Link Info ---\033[0m')
    if str(place_id) == "15532962292":
        print(f"\033[0;38;2;157;157;157;49m • Game ID: \033[0;38;2;190;190;190;49m{place_id} \033[0m\033[92m(Sol's RNG)\033[0m")
    else:
        print(f"\033[0;38;2;157;157;157;49m • Game ID: \033[0;38;2;190;190;190;49m{place_id} \033[0m\033[1;31m(NOT SOL'S RNG)\033[0m")
    print(f'\033[0;38;2;157;157;157;49m • Owner Roblox ID: \033[0m\033[0;38;2;190;190;190;49m{user_id}')
    print(f'\033[0;38;2;100;100;100;49m • linkCode: \033[0m\033[0;38;2;75;75;75;49m{link_code} (not important)\033[0m\n')
    
    # protectin u 
    if place_id is not None and str(place_id) != "15532962292":
        # dodgin' bullets
        os.startfile("roblox://placeID=1") # this just makes u leave the game and brings u to a no access screen since u cant join place id 1
        
        # blacklisting
        settings["blacklisted_content"] = settings.get("blacklisted_content", [])
        
        settings["blacklisted_content"].append(str(m.author.id))
        settings["blacklisted_content"].append(str(link))
        
        # saving their crimes so the sniper doesnt touch the link or user again
        save_settings(settings)
        
def start_bot():
    global bot
    verify_access()
    print("Ok")
    asyncio.run(bot.run(token=settings.get("discordToken", None)))

# now moving on to defining the ui

# ---------------- TITLE BAR ----------------
class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("titlebar")
        self.setFixedHeight(44)
        self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 10, 0)
        layout.setSpacing(0)

        # App title
        self.title = QtWidgets.QLabel("OpenSniper")
        self.title.setObjectName("title")
        layout.addWidget(self.title)

        layout.addStretch()

        # Grip dots
        grip = QtWidgets.QLabel("· · · · · · · · · · · · · · · · · · · · · · · · · · · · \n · · · · · · · · · · · · · · · · · · · · · · · · · · · · ")
        grip.setObjectName("grip")
        grip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(grip)

        layout.addStretch()

        # Close button
        self.close_btn = QtWidgets.QPushButton("✕")
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setFixedSize(26, 26)
        layout.addWidget(self.close_btn)

    def _set_glow(self, active: bool):
        self.setProperty("glowing", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

# ---------------- JELLY DRAG ---------------- (fun lil dragging motions)
class JellyMixin:
    def _jelly_setup(self):
        self._drag_active   = False
        self._drag_offset   = QtCore.QPoint()
        self._target_x      = float(self.x())
        self._target_y      = float(self.y())
        self._current_x     = float(self.x())
        self._current_y     = float(self.y())
        self._vx = self._vy = 0.0
        self._spring        = 0.28
        self._damping       = 0.72

        self._jelly_timer = QtCore.QTimer(self)
        self._jelly_timer.setInterval(15)
        self._jelly_timer.timeout.connect(self._animate_jelly)
        self._jelly_timer.start()

    def _jelly_press(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.titlebar._set_glow(True)

    def _jelly_move(self, event: QtGui.QMouseEvent):
        if self._drag_active:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self._target_x = float(new_pos.x())
            self._target_y = float(new_pos.y())

    def _jelly_release(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_active = False
            self.titlebar._set_glow(False)

    def _animate_jelly(self):
        dx = self._target_x - self._current_x
        dy = self._target_y - self._current_y
        dist = math.hypot(dx, dy)

        if dist > 0:
            fx = (dx / dist) * dist * self._spring
            fy = (dy / dist) * dist * self._spring
        else:
            fx = fy = 0.0

        self._vx = (self._vx + fx) * self._damping
        self._vy = (self._vy + fy) * self._damping

        if abs(self._vx) < 0.1: self._vx = 0.0
        if abs(self._vy) < 0.1: self._vy = 0.0

        self._current_x += self._vx
        self._current_y += self._vy

        self.move(int(self._current_x), int(self._current_y))
        
class CenterDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

# ---------------- UI ----------------
class UI(QtWidgets.QWidget, JellyMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenSniper")
        self.setFixedSize(420, 550)
        
        if settings.get("alwaysontop_enabled"):
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        
        # ---- shadow container ----
        self.container = QtWidgets.QFrame(self)
        self.container.setGeometry(10, 10, 400, 400)
        self.container.setObjectName("container")

        outer = QtWidgets.QVBoxLayout(self.container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---- title bar ----
        self.titlebar = TitleBar(self)
        self.titlebar.close_btn.clicked.connect(self.exit)
        self.titlebar.mousePressEvent   = self._jelly_press
        self.titlebar.mouseMoveEvent    = self._jelly_move
        self.titlebar.mouseReleaseEvent = self._jelly_release
        outer.addWidget(self.titlebar)
        
        sep = QtWidgets.QFrame()
        sep.setObjectName("separator")
        sep.setFixedHeight(2)
        outer.addWidget(sep)

        # ---- content area ----
        content = QtWidgets.QWidget()
        content.setObjectName("content")
        layout = QtWidgets.QVBoxLayout(content)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 2, 16, 2)
        
        sep = QtWidgets.QFrame()
        sep.setObjectName("separatorbottom")
        sep.setFixedHeight(2)
        layout.addWidget(sep)

        self.glitch_button = QtWidgets.QPushButton("Snipe Glitch biome")
        self.glitch_button.setObjectName("button")
        self.glitch_button.clicked.connect(self.toggle_glitch)
        self.glitch_button.setMaximumHeight(28)
        self.glitch_button.setMinimumHeight(28)
        layout.addWidget(self.glitch_button)
        
        self.dreamspace_button = QtWidgets.QPushButton("Snipe Dreamspace")
        self.dreamspace_button.setObjectName("button")
        self.dreamspace_button.clicked.connect(self.toggle_dreamspace)
        self.dreamspace_button.setMaximumHeight(28)
        self.dreamspace_button.setMinimumHeight(28)
        layout.addWidget(self.dreamspace_button)
        
        self.cyberspace_button = QtWidgets.QPushButton("Snipe Cyberspace")
        self.cyberspace_button.setObjectName("button")
        self.cyberspace_button.clicked.connect(self.toggle_cyberspace)
        self.cyberspace_button.setMaximumHeight(28)
        self.cyberspace_button.setMinimumHeight(28)
        layout.addWidget(self.cyberspace_button)
        
        self.singularity_button = QtWidgets.QPushButton("Snipe Singularity")
        self.singularity_button.setObjectName("button")
        self.singularity_button.clicked.connect(self.toggle_singularity)
        self.singularity_button.setMaximumHeight(28)
        self.singularity_button.setMinimumHeight(28)
        layout.addWidget(self.singularity_button)
        
        self.toggle_custom_keywords_button = QtWidgets.QPushButton("Snipe using custom keywords")
        self.toggle_custom_keywords_button.setObjectName("button")
        self.toggle_custom_keywords_button.clicked.connect(self.toggle_custom_keywords)
        self.toggle_custom_keywords_button.setMaximumHeight(28)
        self.toggle_custom_keywords_button.setMinimumHeight(28)
        layout.addWidget(self.toggle_custom_keywords_button)
        
        self.sep = QtWidgets.QFrame()
        self.sep.setObjectName("uiseparator")
        self.sep.setFixedHeight(1)
        
        layout.addSpacing(8)
        layout.addWidget(self.sep)
        layout.addSpacing(8)
        
        self.settings_button = QtWidgets.QPushButton("Settings")
        self.settings_button.setObjectName("button")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setMaximumHeight(32)
        self.settings_button.setMinimumHeight(32)
        
        layout.addWidget(self.settings_button)
        
        self.console_button = QtWidgets.QPushButton("Console logs")
        self.console_button.setObjectName("button")
        self.console_button.clicked.connect(self.toggle_console)
        self.console_button.setMaximumHeight(32)
        self.console_button.setMinimumHeight(32)
        
        layout.addWidget(self.console_button)
        
        self.alwaysontop_button = QtWidgets.QPushButton("Window stays on top")
        self.alwaysontop_button.setObjectName("button")
        self.alwaysontop_button.clicked.connect(self.toggle_alwaysontop)
        self.alwaysontop_button.setMaximumHeight(32)
        self.alwaysontop_button.setMinimumHeight(32)
        
        layout.addWidget(self.alwaysontop_button)
        
        self.set_gradient_button(self.glitch_button, QColor("#589C22"), QColor("#000000"),angle=90,enabled=settings["glitch_enabled"])
        self.set_gradient_button(self.dreamspace_button, QColor("#BF71AF"), QColor("#7D0076"),angle=135,enabled=settings["dreamspace_enabled"])
        self.set_gradient_button(self.cyberspace_button, QColor("#176087"), QColor("#1730a7"),angle=180,enabled=settings["cyberspace_enabled"])
        self.set_gradient_button(self.singularity_button, QColor("#332800"), QColor("#C2B357"),angle=0,enabled=settings["singularity_enabled"])
        self.set_gradient_button(self.toggle_custom_keywords_button, QColor("#B0B0B0"), QColor("#787878"),angle=270,enabled=settings["custom_keywords_enabled"])                        
        self.set_gradient_button(self.console_button, QColor("#0b0b0b"), QColor("#5b5b5b"),angle=-90,enabled=settings["console_enabled"])
        self.set_gradient_button(self.alwaysontop_button, QColor("#80333e"), QColor("#2b2b2b"),angle=90,enabled=settings["alwaysontop_enabled"])                    
        

        layout.addStretch(1)
        outer.addWidget(content)

        self.apply_style()
        self._jelly_setup()
        
    def exit(self):
        print("\n\033[92mUser ordered exit")
        time.sleep(0.05)
        sys.exit()

    # ---------- ui helpers ----------
    def _add_text_input(self, parent_layout, text, default):
        row = QtWidgets.QVBoxLayout()
        
    
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        line_edit = QtWidgets.QLineEdit()
        line_edit.setText(str(default))
        line_edit.setObjectName("textinput") 
        line_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        line_edit.setMinimumHeight(1)
        line_edit.setMaximumHeight(32)
        line_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        
        row.addWidget(label)
        row.addSpacing(4)
        row.addWidget(line_edit)
        parent_layout.addLayout(row)
    
        return line_edit
        
    def set_gradient_button(self, button, color1, color2, angle=45, enabled=True):
        anim = QVariantAnimation()
        anim.setDuration(250)
        
        enabled = not enabled
    
        start = 0.0 if not enabled else 1.0
        end = 1.0 if not enabled else 0.0
    
        base = QColor("#2b2b2b")
        
        
        def angle_to_qt_gradient(angle):
            rad = math.radians(angle)
        
            dx = math.cos(rad)
            dy = math.sin(rad)
        
            x1 = 0.5 - dx * 0.5
            y1 = 0.5 - dy * 0.5
            x2 = 0.5 + dx * 0.5
            y2 = 0.5 + dy * 0.5
        
            return x1, y1, x2, y2
    
        def lerp(a, b, t):
            return a + (b - a) * t
    
        def make_style(t):
            c1 = QColor(color1)
            c2 = QColor(color2)
    
            c1 = QColor(
                int(lerp(base.red(), c1.red(), t)),
                int(lerp(base.green(), c1.green(), t)),
                int(lerp(base.blue(), c1.blue(), t))
            )
    
            c2 = QColor(
                int(lerp(base.red(), c2.red(), t)),
                int(lerp(base.green(), c2.green(), t)),
                int(lerp(base.blue(), c2.blue(), t))
            )
    
            x1, y1, x2, y2 = angle_to_qt_gradient(angle)
    
            return f"""
            QPushButton {{
                border: none;
                color: white;
                background: qlineargradient(
                    x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                    stop: 0 {c1.name()},
                    stop: 1 {c2.name()}
                );
            }}
            """
    
        def on_value(v):
            button.setStyleSheet(make_style(v))
    
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.valueChanged.connect(on_value)
        anim.start()
    
        button._anim = anim

    def _label_wrap(self, text, widget):
        row = QtWidgets.QVBoxLayout()
        row.setSpacing(2)
        row.setContentsMargins(0, 2, 0, 2)
        row.addWidget(QtWidgets.QLabel(text))
        row.addWidget(widget)
        return row
        
    def fade_button(self, button, start_color, end_color, duration=100):
        anim = QVariantAnimation()
        anim.setDuration(duration)
        anim.setStartValue(start_color)
        anim.setEndValue(end_color)
    
        def on_value_changed(value):
            button.setStyleSheet(f"background-color: {value.name()};")
    
        anim.valueChanged.connect(on_value_changed)
        anim.start()
    
        button._anim = anim

    # ---------- ui functions ----------
    def toggle_glitch(self):
        settings["glitch_enabled"] = not settings.get("glitch_enabled")
        save_settings(settings)
        self.set_gradient_button(self.glitch_button, QColor("#589C22"), QColor("#000000"),angle=90,enabled=settings["glitch_enabled"])
        
    def toggle_dreamspace(self):
        settings["dreamspace_enabled"] = not settings.get("dreamspace_enabled")
        save_settings(settings)
        self.set_gradient_button(self.dreamspace_button, QColor("#BF71AF"), QColor("#7D0076"),angle=135,enabled=settings["dreamspace_enabled"])
        
    def toggle_cyberspace(self):
        settings["cyberspace_enabled"] = not settings.get("cyberspace_enabled")
        save_settings(settings)
        self.set_gradient_button(self.cyberspace_button, QColor("#176087"), QColor("#1730a7"),angle=180,enabled=settings["cyberspace_enabled"])
            
    def toggle_singularity(self):
        settings["singularity_enabled"] = not settings.get("singularity_enabled")
        save_settings(settings)
        self.set_gradient_button(self.singularity_button, QColor("#332800"), QColor("#C2B357"),angle=0,enabled=settings["singularity_enabled"])
        
    def toggle_custom_keywords(self):
        settings["custom_keywords_enabled"] = not settings.get("custom_keywords_enabled")
        save_settings(settings)
        self.set_gradient_button(self.toggle_custom_keywords_button, QColor("#B0B0B0"), QColor("#787878"),angle=270,enabled=settings["custom_keywords_enabled"])                  
            
    def open_settings(self):
        toggle_settings()
        
    def toggle_console(self):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            return
    
        current = settings.get("console_enabled", True)
        new_state = not current
        settings["console_enabled"] = new_state
        save_settings(settings)
        self.set_gradient_button(self.console_button, QColor("#0b0b0b"), QColor("#5b5b5b"),angle=-90,enabled=new_state)
        
        if new_state:
            ctypes.windll.user32.ShowWindow(hwnd, 9)
        else:
            ctypes.windll.user32.ShowWindow(hwnd, 0)

            
    def toggle_alwaysontop(self):
        flags = self.windowFlags()
        settings["alwaysontop_enabled"] = not settings.get("alwaysontop_enabled")
        save_settings(settings)
        
        if settings.get("alwaysontop_enabled"):
            self.setWindowFlags(flags | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~QtCore.Qt.WindowType.WindowStaysOnTopHint)
            
        self.show()
        self.set_gradient_button(self.alwaysontop_button, QColor("#80333e"), QColor("#2b2b2b"),angle=90,enabled=settings.get("alwaysontop_enabled"))
    # ---------- style ----------
    def apply_style(self):
        self.setStyleSheet("""
        QWidget {
            font-family: "Segoe UI", Inter, sans-serif;
            color: #eaeaea;
        }

        #container {
            background-color: #0f0f0f;
            border-radius: 16px;
        }

        /* ---- title bar ---- */
        #titlebar {
            background-color: #141414;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        }

        /* glow state – toggled by setProperty("glowing", True) */
        #titlebar[glowing="true"] {
            background-color: qradialgradient(
                cx:0.5, cy:0,  radius:1.2,
                fx:0.5, fy:0,
                stop:0   rgba(80, 80, 255, 120),
                stop:0.5 rgba(40, 40, 180, 40),
                stop:1   rgba(20, 20, 20,   0)
            );
        }

        QLabel#title {
            font-size: 14px;
            font-weight: 600;
        }

        QLabel#grip {
            font-size: 11px;
            color: #333;
            letter-spacing: 2px;
        }

        QPushButton#close_btn {
            background: transparent;
            border: none;
            color: #555;
            font-size: 13px;
            border-radius: 13px;
        }
        QPushButton#close_btn:hover {
            background: #2a2a2a;
            color: #eaeaea;
        }

        /* ---- separators ---- */
        #separator {
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #080808,
                stop:1 #1f1f1f
            );
        }
        
        #uiseparator {
            background-color: #1f1f1f;
            padding: 40px;
        }

        /* ---- content ---- */
        #content {
            background: transparent;
        }

        QLabel#status {
            background-color: #1a1a1a;
            padding: 6px;
            border-radius: 8px;
        }
        
        QLineEdit {
            background-color: #1a1a1a;
            border: 1px solid #2a2a2a;
            font-size: 11px;
            border-radius: 8px;
            padding: 8px;
            color: #eaeaea;
        }

        QPushButton#button {
            font-size: 13px;
            background-color: #2b2b2b;
            border-radius: 8px;
            border: 1px solid #1c1c1c;
            padding: 2px;
            color: #eaeaea;
        }
        
        QPushButton#button:hover    { border-color: #222222; }
        QPushButton#button:pressed  { border-color: #101010; }
        
        QLineEdit:hover    { border-color: #222222; }
        
        
        """)
        
class SettingsUI(QtWidgets.QWidget, JellyMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(420, 500)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        
        # ---- shadow container ----
        self.container = QtWidgets.QFrame(self)
        self.container.setGeometry(10, 10, 400, 480)
        self.container.setObjectName("container")

        outer = QtWidgets.QVBoxLayout(self.container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ---- title bar ----
        self.titlebar = TitleBar(self)
        self.titlebar.title.setText("Settings fr")
        self.titlebar.close_btn.clicked.connect(toggle_settings)
        self.titlebar.mousePressEvent   = self._jelly_press
        self.titlebar.mouseMoveEvent    = self._jelly_move
        self.titlebar.mouseReleaseEvent = self._jelly_release
        outer.addWidget(self.titlebar)

        sep = QtWidgets.QFrame()
        sep.setObjectName("separator")
        sep.setFixedHeight(2)
        outer.addWidget(sep)

        # ---- content area ----
        content = QtWidgets.QWidget()
        content.setObjectName("content")
        layout = QtWidgets.QVBoxLayout(content)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 4, 16, 4)
        
        layout.addSpacing(8)

        self.ina_min_days_old_input = self._add_text_input(layout, "Ignore messages from accounts under X days old", "")
        self.ina_min_days_old_input.editingFinished.connect(
            lambda: self.ina_settings_min_days_old(self.ina_min_days_old_input.text())
        )
        self.ina_min_days_old_input.setValidator(QIntValidator(0, 999))
        
        self.ina_min_days_old_input.setText(str(settings.get('ignore_newer_accounts_MinAgeInDays', 7)))

        self.ina_toggle_button = QtWidgets.QPushButton("Ignore messages from newer accounts")
        self.ina_toggle_button.setObjectName("button")
        self.ina_toggle_button.clicked.connect(self.toggle_ina)
        self.ina_toggle_button.setMaximumHeight(32)
        self.ina_toggle_button.setMinimumHeight(32)
        layout.addSpacing(8)
        layout.addWidget(self.ina_toggle_button)
            
        self.sep = QtWidgets.QFrame()
        self.sep.setObjectName("uiseparator")
        self.sep.setFixedHeight(1)
        
        layout.addSpacing(8)
        layout.addWidget(self.sep)  
        
        self.show_ignore_logs_button = QtWidgets.QPushButton("Show ignored messages in console")
        self.show_ignore_logs_button.setObjectName("button")
        self.show_ignore_logs_button.clicked.connect(self.toggle_ignore_logs)
        self.show_ignore_logs_button.setMaximumHeight(32)
        self.show_ignore_logs_button.setMinimumHeight(32)
        
        layout.addSpacing(8)
        layout.addWidget(self.show_ignore_logs_button)
        
        self.set_gradient_button(self.ina_toggle_button, QColor("#006FD1"), QColor("#002445"), angle=90, enabled=settings["ignore_newer_accounts"])
        self.set_gradient_button(self.show_ignore_logs_button, QColor("#380B00"), QColor("#A64A29"), angle=90, enabled=settings["show_ignore_logs"])

        self.sep = QtWidgets.QFrame()
        self.sep.setObjectName("uiseparator")
        self.sep.setFixedHeight(1)

        layout.addSpacing(8)
        layout.addWidget(self.sep)
        
        self.custom_keywords_input = self._add_text_input(layout, "Custom keywords (seperate with space)", "")
        self.custom_keywords_input.setMinimumHeight(48)
        self.custom_keywords_input.setMaximumHeight(48)
        self.custom_keywords_input.editingFinished.connect(
            lambda: self.custom_keywords_edit(self.custom_keywords_input.text().lower())
        )
        
        self.custom_keywords_input.setText(" ".join(settings.get('custom_keywords')))
        
        self.sep = QtWidgets.QFrame()
        self.sep.setObjectName("uiseparator")
        self.sep.setFixedHeight(1)

        layout.addSpacing(8)
        layout.addWidget(self.sep)
        
        self.whitelisted_channels_input = self._add_text_input(layout, "Whitelisted Channels (seperate with space)", "")
        self.whitelisted_channels_input.setMinimumHeight(32)
        self.whitelisted_channels_input.setMaximumHeight(32)
        self.whitelisted_channels_input.editingFinished.connect(
            lambda: self.whitelisted_channels_edit(self.whitelisted_channels_input.text().lower())
        )
        
        whitelisted = []
        
        for item in settings.get('whitelisted_channels'):
            whitelisted.append(str(item))
        
        self.whitelisted_channels_input.setText(" ".join(whitelisted))

        
        sep = QtWidgets.QFrame()
        sep.setObjectName("separatorbottom")
        sep.setFixedHeight(2)
        layout.addWidget(sep)
        layout.addStretch(1)
        outer.addWidget(content)

        self.apply_style()
        self._jelly_setup()
        
    # ---------- ui helpers ----------
    def _add_text_input(self, parent_layout, text, default):
        row = QtWidgets.QVBoxLayout()
        
    
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        line_edit = QtWidgets.QLineEdit()
        line_edit.setText(str(default))
        line_edit.setObjectName("textinput") 
        line_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        line_edit.setMinimumHeight(1)
        line_edit.setMaximumHeight(32)
        line_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        
        row.addWidget(label)
        row.addSpacing(4)
        row.addWidget(line_edit)
        parent_layout.addLayout(row)
    
        return line_edit
        
    def set_gradient_button(self, button, color1, color2, angle=45, enabled=True):
        anim = QVariantAnimation()
        anim.setDuration(250)
        
        enabled = not enabled
    
        start = 0.0 if not enabled else 1.0
        end = 1.0 if not enabled else 0.0
    
        base = QColor("#2b2b2b")
        
        
        def angle_to_qt_gradient(angle):
            rad = math.radians(angle)
        
            dx = math.cos(rad)
            dy = math.sin(rad)
        
            x1 = 0.5 - dx * 0.5
            y1 = 0.5 - dy * 0.5
            x2 = 0.5 + dx * 0.5
            y2 = 0.5 + dy * 0.5
        
            return x1, y1, x2, y2
    
        def lerp(a, b, t):
            return a + (b - a) * t
    
        def make_style(t):
            c1 = QColor(color1)
            c2 = QColor(color2)
    
            c1 = QColor(
                int(lerp(base.red(), c1.red(), t)),
                int(lerp(base.green(), c1.green(), t)),
                int(lerp(base.blue(), c1.blue(), t))
            )
    
            c2 = QColor(
                int(lerp(base.red(), c2.red(), t)),
                int(lerp(base.green(), c2.green(), t)),
                int(lerp(base.blue(), c2.blue(), t))
            )
    
            x1, y1, x2, y2 = angle_to_qt_gradient(angle)
    
            return f"""
            QPushButton {{
                border: none;
                color: white;
                background: qlineargradient(
                    x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                    stop: 0 {c1.name()},
                    stop: 1 {c2.name()}
                );
            }}
            """
    
        def on_value(v):
            button.setStyleSheet(make_style(v))
    
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.valueChanged.connect(on_value)
        anim.start()
    
        button._anim = anim

    def _label_wrap(self, text, widget):
        row = QtWidgets.QVBoxLayout()
        row.setSpacing(2)
        row.setContentsMargins(0, 2, 0, 2)
        row.addWidget(QtWidgets.QLabel(text))
        row.addWidget(widget)
        return row
        
    def fade_button(self, button, start_color, end_color, duration=100):
        anim = QVariantAnimation()
        anim.setDuration(duration)
        anim.setStartValue(start_color)
        anim.setEndValue(end_color)
    
        def on_value_changed(value):
            button.setStyleSheet(f"background-color: {value.name()};")
    
        anim.valueChanged.connect(on_value_changed)
        anim.start()
    
        button._anim = anim
        
    # ---------- ui functions ----------
    def toggle_ina(self):
        settings['ignore_newer_accounts'] = not settings.get("ignore_newer_accounts")
        save_settings(settings)
        self.set_gradient_button(self.ina_toggle_button, QColor("#006FD1"), QColor("#002445"), angle=90, enabled=settings["ignore_newer_accounts"])

    def toggle_ignore_logs(self):
        settings['show_ignore_logs'] = not settings.get("show_ignore_logs")
        save_settings(settings)
        self.set_gradient_button(self.show_ignore_logs_button, QColor("#380B00"), QColor("#A64A29"), angle=90, enabled=settings["show_ignore_logs"])
 
    def ina_settings_min_days_old(self, age):
        self.ina_min_days_old_input.clearFocus()
        settings['ignore_newer_accounts_MinAgeInDays'] = int(age)
        self.ina_min_days_old_input.setText((str(int(age))))
        save_settings(settings)

    def custom_keywords_edit(self, kws):
        self.custom_keywords_input.clearFocus()
        keywords = kws.split()
        settings['custom_keywords'] = keywords
        save_settings(settings)

    def whitelisted_channels_edit(self, channels):
        self.whitelisted_channels_input.clearFocus()
        whitelisted_channels = [
            int(x) for x in channels.split()
            if x.isdigit()
        ]
    
    
        settings['whitelisted_channels'] = whitelisted_channels
        save_settings(settings)
        
    
    # ---------- style ----------
    def apply_style(self):
        self.setStyleSheet("""
        QWidget {
            font-family: "Segoe UI", Inter, sans-serif;
            color: #eaeaea;
        }

        #container {
            background-color: #0f0f0f;
            border-radius: 16px;
        }

        /* ---- title bar ---- */
        #titlebar {
            background-color: #141414;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        }

        /* glow state – toggled by setProperty("glowing", True) */
        #titlebar[glowing="true"] {
            background-color: qradialgradient(
                cx:0.5, cy:0,  radius:1.2,
                fx:0.5, fy:0,
                stop:0   rgba(80, 80, 255, 120),
                stop:0.5 rgba(40, 40, 180, 40),
                stop:1   rgba(20, 20, 20,   0)
            );
        }

        QLabel#title {
            font-size: 14px;
            font-weight: 600;
        }

        QLabel#grip {
            font-size: 11px;
            color: #333;
            letter-spacing: 2px;
        }

        QPushButton#close_btn {
            background: transparent;
            border: none;
            color: #555;
            font-size: 13px;
            border-radius: 13px;
        }
        QPushButton#close_btn:hover {
            background: #2a2a2a;
            color: #eaeaea;
        }

        /* ---- separators ---- */
        #separator {
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #080808,
                stop:1 #1f1f1f
            );
        }
        
        #uiseparator {
            background-color: #1f1f1f;
            padding: 40px;
        }

        /* ---- content ---- */
        #content {
            background: transparent;
        }

        QLabel#status {
            background-color: #1a1a1a;
            padding: 6px;
            border-radius: 8px;
        }
        
        QLineEdit {
            font-size: 13px;
            background-color: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 8px;
            padding: 8px;
            color: #eaeaea;
        }

        QPushButton#button {
            font-size: 13px;
            background-color: #2b2b2b;
            border-radius: 8px;
            border: 1px solid #1c1c1c;
            padding: 2px;
            color: #eaeaea;
        }
        
        QPushButton#button:hover    { border-color: #222222; }
        QPushButton#button:pressed  { border-color: #101010; }
        
        QLineEdit:hover    { border-color: #222222; }
        
        
        """)
        
# run everything
threading.Thread(target=start_bot, daemon=True).start()
        
app = QtWidgets.QApplication(sys.argv)

def toggle_settings():
    if settings_window.isVisible():
        settings_window.hide()
    else:
        settings_window.show()
        settings_window.raise_()
        settings_window.activateWindow()

settings_window = SettingsUI()

window = UI()
window.show()
sys.exit(app.exec())
