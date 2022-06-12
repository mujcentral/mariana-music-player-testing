#################################################################################################################################
#
#           Mariana Player v0.7.0 dev
#     (Read help.md for help on commands)
#
#    Running the app:
#      For very first boot (SETUP):
#        Make sure you have python version < 3.10 to run this file (unless compatible llvmlite wheel bins exist...)
#     
#        QUICK-SETUP (NEW DROP-IN REPLACEMENT FOR MANUAL SETUP!)
#           Run INITSETUP.py and follow along with it's instructions (Run with "--help" flag for more info)
#          *NOTE: Don't run manual setup if you have already done a quick setup
#          *BENEFITS: Enjoy auto created ".bat" and ".ps1" runner files to automate successive runs of Mariana Player
#                                                                  |
#  +-----<--(You can skip to here after the QUICK-SETUP)---------<-+
#  |
#  |     MANUAL SETUP (Go through a tedious setup procedure)
#  |         Setup compatible architecture of VLC media player, install FFMPEG and add to path...
#  |         Install git scm if not already installed
#  v         Install given git package directly from url using: `pip install git+https://github.com/Vivojay/pafy@develop`
#  |         run `pip install -r requirements.txt`
#  |     
#  v         *OPTIONAL: Download and pip install unofficial binary for llvmlite wheel compatible with your python version
#  |         *NOTE: Specify py version < 3.10 in virtualenv (if installing optional llvmlite), as other py vers don't support llvmlite wheels :)
#  |     
#  +---> Firstly, look at help.md before running any py file
#         Run this file (main.py) on the very first bootup, nothing else (no flags, just to test bare minimum run)...
#         You are good to go...
#        *Note: If you encounter errors, look for online help as the current help file doesn't have fixes for common problems yet
#      
#      All successive boots (RUNNING NORMALLY):
#        just run this file (main.py) with desired flags (discussed in help.md)
#        and enjoy... (and possibly debug...)

# This app may take a LOT of time to load at first...
# Hence the loading prompt...

# Editor's Note: Make sure to brew a nice coffee beforehand... :)
#################################################################################################################################


# IMPORTS BEGIN #

# songindex and meaning
# songindex = -1   --> Song has stopped
# songindex = None --> Offline song streaming via path

import time, sys
APP_BOOT_START_TIME = time.time();                  print("Loaded 1/35",  end='\r')

import os;                                          print("Loaded 2/35",  end='\r')
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

CURDIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURDIR)

# TODO: Unclutter globals...
LOADED_MODULES_COUNT = 2    # Will be deleted once all modules have been imported
                            # so as to help in uncluttering global namespace
TOTAL_MODULES_COUNT = 35

def progress_loading_message(success=True):
    global LOADED_MODULES_COUNT
    LOADED_MODULES_COUNT += 1

    if success:
        print(f"Loaded {LOADED_MODULES_COUNT}/{TOTAL_MODULES_COUNT}", end='\r')

import re;                                          progress_loading_message()
import pygame;                                      progress_loading_message()
import random as rand;                              progress_loading_message()
import importlib;                                   progress_loading_message()
import colored;                                     progress_loading_message()
import subprocess as sp;                            progress_loading_message()
import restore_default;                             progress_loading_message()
import toml;                                        progress_loading_message()
import json;                                        progress_loading_message()
import webbrowser;                                  progress_loading_message()
import unidecode;                                   progress_loading_message()
import socket;                                      progress_loading_message()
import sounddevice;                                 progress_loading_message()
import contextlib;                                  progress_loading_message()

from shutil import copyfile;                        progress_loading_message()
from getpass import getpass;                        progress_loading_message()
from url_validate import url_is_valid;              progress_loading_message()
from tabulate import tabulate as tbl;               progress_loading_message()
from ruamel.yaml import YAML;                       progress_loading_message()
from collections.abc import Iterable;               progress_loading_message()
from logger import SAY, dt;                         progress_loading_message()
from multiprocessing import Process;                progress_loading_message()
from first_boot_welcome_screen import notify;       progress_loading_message()

online_streaming_ext_load_error = 0
comtypes_load_error = False # Made available after fix from comtypes issues #244, #180
                            # Previously: comtypes_load_error = True
lyrics_ext_load_error = 0
reddit_creds_are_valid = False

# try:
#     import librosa
#     print("Loaded 27/35",  end='\r') # Time taking import (Sometimes, takes ages...)
# except ImportError:
#     print("[WARN] Could not load music computation extension...")
#     print("[WARN] ...Skipped 27/35")

try:
    vas = importlib.import_module("beta.vlc-async-stream")
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    online_streaming_ext_load_error = 1
    print("[INFO] Could not load online streaming extension...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

try:
    YT_query = importlib.import_module("beta.YT_query")
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    if not online_streaming_ext_load_error:
        print("[INFO] Could not load online streaming extension...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

try:
    from beta.IPrint import IPrint, blue_gradient_print, loading, cols
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    lyrics_ext_load_error = 1
    print("[INFO] Could not load coloured print extension...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

try:
    os.chdir(CURDIR)
    from lyrics_provider import get_lyrics
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False) 
    print("[INFO] Could not load lyrics extension...")
    if not lyrics_ext_load_error:
        print("[INFO] ...Could not load online streaming extension...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

try:
    from beta import redditsessions
    if redditsessions.WARNING:
        progress_loading_message(success=False)
        print("[WARN] Could not load reddit-sessions extension...")
        print(f"[WARN] ...{redditsessions.WARNING}...")
        print(f"[WARN] ...Skipped {LOADED_MODULES_COUNT}/35")
    else:
        reddit_creds_are_valid = True
        progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    print("[INFO] Could not load reddit-sessions extension..., module 'praw' missing...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

try:
    from lyrics_provider.detect_song import get_song_info
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    print("[INFO] Could not load lyrics extension...")
    if not lyrics_ext_load_error:
        print("[INFO] ...Could not load online streaming extension...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")


try:
    from beta.master_volume_control import get_master_volume, set_master_volume
    progress_loading_message()
except Exception:
    progress_loading_message(success=False)
    comtypes_load_error = True
    SAY(visible=False, # global var `visible` hasn't been defined yet...
        log_message="comtypes load failed",
        display_message="", # ...because we don't want to display anything on screen to the user
        log_priority=2)

try:
    from beta.podcasts import get_latest_podbean_data, vendors as pod_vendors
    progress_loading_message()
except ImportError:
    progress_loading_message(success=False)
    print("[INFO] Could not load podcasts...")
    print(f"[INFO] ...Skipped {LOADED_MODULES_COUNT}/35")

os.chdir(CURDIR) # Bring program back to it's own directory...

# IMPORTS END #


# TODO: - Replace `err`s with `SAY`s
# TODO: - Rename SAY to `err` or `errlogger`... in whole codebase?
# TODO: - Add option to display type of error in display_message parameter of `SAY`
#         to print kind of log [ (debg)/(info)/(warn)/(fatl) ] ??

yaml = YAML(typ='safe')  # Allows for safe YAML loading

webbrowser.register_standard_browsers()

if not os.path.isdir('logs'): os.mkdir('logs')

def create_required_files_if_not_exist(*files):
    for file in files:
        if not os.path.isfile(file):
            with open(file, 'w', encoding="utf-8") as _:
                pass

create_required_files_if_not_exist(
    'logs/history.log',
    'logs/general.log',
)

FIRST_BOOT = False # Assume user is using app for considerable time
                   # so you don't want to annoy him with an
                   # annoying FIRST-TIME-WELCOME

try:
    with open('settings/system.toml', encoding='utf-8') as file:
        SYSTEM_SETTINGS = toml.load(file)
        FIRST_BOOT = SYSTEM_SETTINGS['first_boot']
except IOError:
    SYSTEM_SETTINGS = None

ISDEV = SYSTEM_SETTINGS['isdev'] # Useful as a test flag for new features

LAST_SESSION_DATA = None
with contextlib.suppress(Exception):
    with open('data/last_session.json', 'r', encoding="utf-8") as fp:
        LAST_SESSION_DATA = json.load(fp) # TODO: Fix the "None" error for `LAST_SESSION_DATA`

try:
    with open('lib.lib', encoding='utf-8') as logfile:
        paths = logfile.read().splitlines()
        paths = [path for path in paths if not path.startswith('#')]
        paths = list(set(paths))
except IOError:
    if not FIRST_BOOT:
        sys.exit("[INFO] Could not find lib.lib file, '\
                'please create one and add desired source directories. '\
                'Aborting program\n")


def first_startup_greet(is_first_boot):
    global SOFT_FATAL_ERROR_INFO

    if is_first_boot:
        try:
            import first_boot_setup
            if SOFT_FATAL_ERROR_INFO := first_boot_setup.fbs(
                about=SYSTEM_SETTINGS
            ):
                SOFT_FATAL_ERROR_INFO = "User skipped startup"
            reload_sounds(quick_load = False)
        except ImportError:
            sys.exit('[ERROR] Critical guide setup-file missing, please consider reinstalling this file or the entire program\nAborting Mariana Player. . .')

with contextlib.suppress(IOError):
    # Create a backup copy of 'user_data.yml' file to recover from possible losses
    # (yes, losses are possible and do take place
    #  relatively often for this particular file)

    read_user_data_from_backup = True
    raise_missing_user_data_fatal_error = True

    if os.path.isfile('user/user_data.yml'):
        with open('user/user_data.yml', encoding='utf-8') as u_data_file:
            USER_DATA = yaml.load(u_data_file)
            if USER_DATA is not None:
                read_user_data_from_backup = False
                raise_missing_user_data_fatal_error = False

                if (list(USER_DATA.keys()) == ['default_user_data']
                    and not FIRST_BOOT
                    and not ISDEV):
                    SAY(visible=visible,
                        display_message = '',
                        log_message = 'User data found to be empty, reverting to default',
                        log_priority = 3)

    if read_user_data_from_backup:
        if os.path.isfile('user/user_data.yml.bak'):
            with open('user/user_data.yml.bak', encoding='utf-8') as u_data_file:
                USER_DATA = yaml.load(u_data_file)
            if USER_DATA is not None:
                if os.path.isfile('user/user_data.yml'):
                    with contextlib.suppress(OSError):
                        os.remove('user/user_data.yml')
                    with contextlib.suppress(Exception):
                        copyfile(src='user/user_data.yml.bak', dst='user/user_data.yml')
                    raise_missing_user_data_fatal_error = False

    with contextlib.suppress(Exception):
        copyfile(src='user/user_data.yml', dst='user/user_data.yml.bak')

if raise_missing_user_data_fatal_error:
    SAY(visible=1,
        display_message = f'Encountered missing program file @{os.path.join(CURDIR, "user/user_data.yml")}',
        log_message = 'Aborting player because user data file was not found',
        log_priority = 1) # Log fatal crash
    sys.exit(1) # Fatal crash

try:
    with open('settings/settings.yml', encoding='utf-8') as u_data_file:
        SETTINGS = yaml.load(u_data_file)

except IOError:
    SAY(visible=1,
        display_message = f'Encountered missing program file @{os.path.join(CURDIR, "settings/settings.yml")}',
        log_message = 'Aborting player because settings file was not found',
        log_priority = 1) # Log fatal crash
    sys.exit(1) # Fatal crash


# Variables
APP_BOOT_END_TIME = time.time()
EXIT_INFO = 0
FATAL_ERROR_INFO = None
SOFT_FATAL_ERROR_INFO = None
RECENTS_QUEUE = []
YOUTUBE_PLAY_TYPE = None
SPECIAL_SONG_NAME_SYMBOLS = list(set('!@#$%^&*()_+=[]{}\\|\'":;<>?/~`'))
COLOR_RESET = colored.attr('reset')
NBSP = f'{COLOR_RESET}\u00A0'
BETA_STATUS = not False

isplaying = False
currentsong = None  # No audio playing initially
ismuted = False
lyrics_saved_for_song = False
currentsong_length = None
command_count = 0
volume_is_boosted = False # TODO: Keep this line as default value of `volume_is_boosted`.
                          # Also get from previous session volume if prev session caching is enabled in settings...
songindex = -1

# lyrics_window_note = "[Please close the lyrics window to continue issuing more commands...]"
current_media_type = None

# random song indices already used up when showing random 
random_indices_used=[]


# Note:
# NO SUCH THING AS current_media_player now
# 

# Log levels from logger.py -> [Only for REF]
# logleveltypes = {0: "none", 1: "fatal", 2: "warn", 3: "info", 4: "debug"}

# -- From System Settings --
# Supported file extensions (quite a lot are supported due to excellent support from `vlc`)
supported_file_types                = SYSTEM_SETTINGS["system_settings"]['supported_file_types']
disable_OS_requirement              = SYSTEM_SETTINGS['system_settings']['enforce_os_requirement']
max_wait_limit_to_get_song_length   = SYSTEM_SETTINGS['system_settings']['max_wait_limit_to_get_song_length']
MAX_RECENTS_SIZE                    = SYSTEM_SETTINGS["system_settings"]['max_recents_size']

# (For *.wav get_pos() in pygame provides played duration and not actual play position, therefore it has now been replaced
# by the much more reliable `vlc` library)

# -- From Settings --
visible                         = SETTINGS['visible']
loglevel                        = SETTINGS.get('loglevel')
DEFAULT_EDITOR                  = SETTINGS.get('editor path')
FALLBACK_RESULT_COUNT           = SETTINGS['display items count']['general']['fallback']
MAX_RESULT_COUNT                = SETTINGS['display items count']['general']['maximum']
max_yt_search_results_threshold = SETTINGS['display items count']['youtube-search results']['maximum']

class theme_colors: # This provides a quick and easy way to set colours to the player directly 
    def __init__(self, settings_dict):
        # Loading colour settings
        self.color_settings = settings_dict['color palette']

        # Colours from provided theme
        self.playing                        = colored.fg(self.color_settings['playing'])
        self.prim                           = colored.fg(self.color_settings['prim'])
        self.sec                            = colored.fg(self.color_settings['sec'])
        self.tert                           = colored.fg(self.color_settings['tert'])
        self.meta_info                      = colored.fg(self.color_settings['meta info'])
        self.error                          = colored.fg(self.color_settings['error'])
        self.exit_prompt                    = colored.fg(self.color_settings['exit prompt'])
        self.exit_statement                 = colored.fg(self.color_settings['exit statement'])
        self.oth                            = colored.fg(self.color_settings['oth'])

        self.author                         = colored.fg('grey_50') + colored.style.UNDERLINED

        self.prompt_foreground_1            = colored.fg(self.color_settings['prompt foreground 1'])
        self.prompt_background_1            = colored.bg(self.color_settings['prompt background 1'])

        self.prompt_foreground_2            = colored.fg(self.color_settings['prompt foreground 2'])
        self.prompt_background_2            = colored.bg(self.color_settings['prompt background 2'])

        self.prompt_foreground_3            = colored.fg(self.color_settings['prompt foreground 3'])
        self.prompt_background_3            = colored.bg(self.color_settings['prompt background 3'])

        self.prompt_foreground_4            = colored.fg(self.color_settings['prompt foreground 4'])
        self.prompt_background_4            = colored.bg(self.color_settings['prompt background 4'])

        self.prompt_foreground_5            = colored.fg(self.color_settings['prompt foreground 5'])
        self.prompt_background_5            = colored.bg(self.color_settings['prompt background 5'])

        self.prompt_not_playing_foreground  = colored.fg(self.color_settings['prompt not playing foreground'])
        self.prompt_not_playing_background  = colored.bg(self.color_settings['prompt not playing background'])

        self.user_commands                  = colored.fg(self.color_settings['user commands'])

_theme_colors = theme_colors(SETTINGS)

if not loglevel:
    restore_default.restore('loglevel', SETTINGS)
    loglevel = SETTINGS.get('loglevel')

# From last session info
use_last_saved_cached_volume = SETTINGS['prefs']['use last cached volume']
cached_volume = 0.9  # Must be det as a factor of max volume player volume (between 0 and 1 --> both inclusive)

if use_last_saved_cached_volume:
    print(0)
    if LAST_SESSION_DATA:
        print(1)
        with contextlib.suppress(Exception):
            print(2)
            cached_volume = LAST_SESSION_DATA['last_session_details']['cached_volume']

def OrderedSet(iterable):
    result = []
    [result.append(i) for i in iterable if i not in result]
    return result


# Flattens list of any depth
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


# Function to extract files from folders recursively
def audio_file_gen(Dir, ext):
    for root, dirs, files in os.walk(Dir):
        for filename in files:
            if os.path.splitext(filename)[1] == ext:
                yield os.path.join(root, filename)


def reload_sounds(quick_load = True, include_dl_dir=True):
    global _local_sound_files, _local_sound_files_names_only, _local_sound_files_names_enumerated, paths

    lib_found = True

    # Definition for quick-load
    if quick_load:
        # NOTE: 'data/snd_files.json' is the relpath to the quick-loads file
        if os.path.isfile('data/snd_files.json'):
            with open('data/snd_files.json', encoding="utf-8") as fp:
                _local_sound_files = json.load(fp)

        else: # Revert to full load (i.e. NOT resorting to quick_load because data/snd_files.json is unavailable)
            quick_load = False

    # Definition for full-load (non quick-load)
    if not quick_load: # (This may be used either as the first-time load or as a fallback for a failed quick-load)
        if os.path.isfile('lib.lib'):
            with open('lib.lib', encoding='utf-8') as logfile:
                paths = logfile.read().splitlines()
                paths = [path for path in paths if not path.startswith('#')]

                if include_dl_dir:
                    from beta import mediadl
                    dl_dir_setup_code = mediadl.setup_dl_dir(SETTINGS, SYSTEM_SETTINGS)
                    if dl_dir_setup_code not in range(4):
                        dl_dir = dl_dir_setup_code
                        if sys.platform == 'win32': dl_dir=dl_dir.replace('/', '\\')
                        else: dl_dir=dl_dir.replace('\\', '/')
                        paths.append(dl_dir)
                    else:
                        # ERRORS have already been handled and logged by `mediadl.setup_dl_dir()`
                        pass

                paths = list(OrderedSet(paths))

                # Use the recursive extractor function and format and store them into usable lists
                new_local_sound_files = [[list(audio_file_gen(paths[j], supported_file_types[i]))
                                       for i in range(len(supported_file_types))] for j in range(len(paths))]
                # Flattening irregularly nested sound files
                new_local_sound_files = list(flatten(new_local_sound_files))

                newly_added_files = [i for i in new_local_sound_files if i not in _local_sound_files]
                _local_sound_files = new_local_sound_files
                del new_local_sound_files
 
            with open('data/snd_files.json', 'w', encoding='utf-8') as fp:
                json.dump(_local_sound_files, fp, indent=2)

        else:
            lib_found = False
            SAY(visible=visible,
                log_message="Library file suddenly made unavailable",
                display_message="Library file suddenly vanished -_-",
                log_priority=2)


    if lib_found:
        _local_sound_files_names_only = [os.path.splitext(os.path.split(i)[1])[0] for i in _local_sound_files]
        _local_sound_files_names_enumerated = [(i+1, j) for i, j in enumerate(_local_sound_files_names_only)]

        if FIRST_BOOT:
            with open('data/snd_files.json', 'w', encoding='utf-8') as fp:
                json.dump(_local_sound_files, fp, indent=2)

    with contextlib.suppress(NameError):
        update_local_songs_info(add_file_paths = newly_added_files)

reload_sounds(quick_load = not FIRST_BOOT) # First boot requires quick_load to be disabled,
                                           # other boots can do away with quick_loads :)
available_random_indices = list(range(len(_local_sound_files_names_only)-1))

try:
    with open('data/track-infos.yml', encoding='utf-8') as fp:
        LOCAL_TRACK_INFOS = yaml.load(fp)

    if not LOCAL_TRACK_INFOS:
        LOCAL_TRACK_INFOS = {}
        for i in _local_sound_files:
            '''
            isFav:
                True --> Favourited
                False --> Unfavourited
                None --> Blacklisted
            '''
            LOCAL_TRACK_INFOS.update({
                i: {'isFav': False,
                    'isExplicit': None,
                    'timesPaused': 0,
                    'timesSeeked': 0,
                    'timesSkipped': 0,
                    'timesStopped': 0,
                    'trackLyrics': "",
                    'streamCount': 0, # A list of datetime stamps and length of this list gives count of streams
                    'tags': [],
                    'assoc-playlists': [], # Searching for playlists of which this song is a part (by user)
                   }})

    with open('data/track-infos.yml', 'w', encoding='utf-8') as fp:
        yaml.dump(LOCAL_TRACK_INFOS, fp)

except IOError:
    with open('data/track-infos.yml', 'w', encoding='utf-8') as fp:
        LOCAL_TRACK_INFOS = None
    # SAY(visible=1,
    #     display_message = f'Encountered missing program file @{os.path.join(CURDIR, "data/track-infos.yml")}',
    #     log_message = 'Aborting player because track data file was not found',
    #     log_priority = 1) # Log fatal crash
    # sys.exit(1) # Fatal crash

if _local_sound_files_names_only == []:
    if loglevel in [3, 4]:
        IPrint("[INFO] All source directories are empty, you may and add more source directories to your library", visible=visible)
        IPrint("[INFO] To edit this library file (of source directories), refer to the `help.md` markdown file.", visible=visible)

try: _ = sp.run('ffmpeg', stdout=sp.DEVNULL, stdin=sp.PIPE, stderr=sp.DEVNULL)
except FileNotFoundError: FATAL_ERROR_INFO = "ffmpeg not recognised globally, download it and add to path (system environment)"

try: _ = sp.run('ffprobe', stdout=sp.DEVNULL, stdin=sp.PIPE, stderr=sp.DEVNULL)
except FileNotFoundError: FATAL_ERROR_INFO = "ffprobe not recognised globally, download it and add to path (system environment)"

if reddit_creds_are_valid: r_seshs = redditsessions.get_redditsessions()
else: r_seshs = None


def device_is_connected(hostname="one.one.one.one"):
    with contextlib.suppress(Exception):
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True

    SAY(visible=visible,
        display_message = 'Device lost connection',
        log_message = 'Device lost connection',
        log_priority = 3)


    return False

def recents_queue_save(inf):
    """
    inf = {
        'yt_play_type': int,
        'type': int,
        'identity': (song_info_as_tuple) OR 'some/absolute/file/path',
    }
    inf is a dict of "yt_play_type" (applicable only for YT streams), "identity" and "type" of audio
    "identity" is a kind of unique locater for a audio. It can be a streaming url
    or the filepath of a locally streamed audio (as a string)

    Songs are pushed to the RECENTS_QUEUE and when it is full
    the oldest audios are removed first to clear space for the new ones

    RECENTS_QUEUE has a fixed size (determined by settings.yml)
    (max allowed value = 10,000,000 (1 Million) items)
    """

    global RECENTS_QUEUE, MAX_RECENTS_SIZE

    if current_media_type is None: # Streaming local/offline
        if songindex is None: # Playing via custom path
            inf = [None, 4, inf]
        else: # Playing from lib via index
            inf = [None, -1, inf]
    else: # Streaming online
        if current_media_type == 0: # From YouTube
            inf = [YOUTUBE_PLAY_TYPE, current_media_type, inf]
        else: # From other sources (webradio/podcast/media-link/reddit-sessions...)
            inf = [None, current_media_type, inf]

    # Clear atleast 1 space for the new item
    if len(RECENTS_QUEUE) == MAX_RECENTS_SIZE:
        del RECENTS_QUEUE[0]

    # Store item in the newly cleared space
    RECENTS_QUEUE.append(inf)

def save_this_session_data():
    with contextlib.suppress(Exception):
        APP_CLOSE_TIME = time.time()
        this_session_data = {
            "last_session_details": {
                "cached_volume": cached_volume,
                "last_song_streamed": currentsong,
                "stream_count": len(RECENTS_QUEUE),
                "total_time_app_was_open": APP_CLOSE_TIME - APP_BOOT_END_TIME,
                "number_of_commands_issued": command_count,
            }
        }

        with open('data/last_session.json', 'w', encoding='utf-8') as fp:
            json.dump(this_session_data, fp, indent=2)


def open_in_youtube(local_song_file_path):
    if local_song_detected_name := get_song_info(
        local_song_file_path, get_title_only=True
    ):
        _, youtube_search_query_url = YT_query.search_youtube(search=local_song_detected_name)
        webbrowser.open(youtube_search_query_url)
        return 0
    else:
        SAY(visible=visible,
            display_message = 'Could not detect the current audio',
            log_message = 'Could not detect the current audio',
            log_priority = 3)
        return 1

def get_current_progress():
    # print(-1)
    return (vas.vlc_media_player.get_media_player().get_time() / 1000)

def save_user_data():
    global USER_DATA

    total_plays = [j for i, j in
                   USER_DATA['default_user_data']['stats']['play_count'].items()
                   if i in ['local', 'radio', 'general', 'youtube', 'redditsession']]
    total_plays = sum(total_plays)
    USER_DATA['default_user_data']['stats']['play_count']['total'] = total_plays

    with open('user/user_data.yml', 'w', encoding="utf-8") as u_data_file:
        yaml.dump(USER_DATA, u_data_file)

def save_song_data():
    global currentsong_length, currentsong

    SONG_DATA = []
    with open('data/song_data.json', 'w', encoding="utf-8") as s_data_file:
        json.dump(SONG_DATA, s_data_file)

def exitplayer(sys_exit=False):
    global EXIT_INFO, APP_BOOT_START_TIME, USER_DATA, _theme_colors, COLOR_RESET

    stopsong()
    APP_CLOSE_TIME = time.time()

    time_spent_on_app = APP_CLOSE_TIME - APP_BOOT_END_TIME
    app_boot_time = APP_BOOT_END_TIME - APP_BOOT_START_TIME

    SAY(visible=visible,
        display_message = '',
        log_message = f'Time spent to boot app = {app_boot_time}',
        log_priority = 3)

    SAY(visible=visible,
        display_message = '',
        log_message = f'Time spent using app = {time_spent_on_app}',
        log_priority = 3)

    USER_DATA['default_user_data']['stats']['times_spent'].append(time_spent_on_app)
    save_user_data()

    IPrint(_theme_colors.exit_statement+'Exiting...'+COLOR_RESET, visible=visible)

    if sys_exit:
        sys.exit(f"{EXIT_INFO}")

# def loadsettings():
#     global settings
#     with open('', encoding='utf-8') as settingsfile:
#         settings = yaml.load(settingsfile)

def play_local_default_player(songpath, _songindex, is_queue=False):
    global isplaying, currentsong, currentsong_length, current_media_type, songindex
    global USER_DATA, SONG_CHANGED, COLOR_RESET

    try:
        if os.path.exists(songpath):
            vas.set_media(_type='local', localpath=songpath)
            vas.media_player(action='play')
            vas.vlc_media_player.get_media_player().audio_set_volume(int(cached_volume*100))

            isplaying = True
            currentsong = songpath
            current_media_type = None
            # songindex = None
            reloaded_index(make_changes_global=True)

            if _songindex: # Song from library via index
                IPrint(f':: {_theme_colors.playing}{_local_sound_files_names_only[int(_songindex)-1]}' + \
                    COLOR_RESET, visible=visible)

                # The user is unreliable and may enter the
                # audio path with weird inhumanly erratic and random
                # mix of upper and lower case characters.
                # Hence, we need to convert everything to lowercase...
                recents_queue_save((reloaded_index(), currentsong))

            else:
                if is_queue:
                    IPrint(f':: {_theme_colors.playing}queue' + \
                        COLOR_RESET, visible=visible)

                else:
                    # Stream offline via custom song path (if not already present in library)
                    IPrint(f':: {_theme_colors.playing}{os.path.splitext(os.path.split(songpath)[1])[0]}' + \
                        COLOR_RESET, visible=visible)
                    recents_queue_save(currentsong)

            USER_DATA['default_user_data']['stats']['play_count']['local'] += 1
            save_user_data()

            while not vas.vlc_media_player.get_media_player().is_playing(): pass # Wait until player actually starts playing

            # TODO: - Save all audio info in `data` dir
            # save_song_data()

            IPrint(f"{_theme_colors.meta_info}Attempting to calculate audio length{_theme_colors.meta_info}", visible=visible)
            length_find_start_time = time.time()
            while True:
                if vas.vlc_media_player.get_media_player().get_length():
                    currentsong_length = vas.vlc_media_player.get_media_player().get_length()/1000
                    break
                if time.time() - length_find_start_time >= max_wait_limit_to_get_song_length:
                    currentsong_length = -1
                    break

            if currentsong_length == -1:
                SAY(visible=visible,
                    log_message = "Cannot get length for vas media",
                    display_message = "",
                    log_priority=3)
            isplaying = True

            if not currentsong_length and currentsong_length != -1:
                get_currentsong_length()

            # Save current audio to log/history.log in human readable form
            SAY(visible=visible,
                display_message = '',
                out_file='logs/history.log',
                log_message = currentsong,
                log_priority = 3,
                format_style = 0)

        else:
            SAY(visible=visible,
                display_message = 'The song at the specified index does not exist (or has been removed). Recommended: Issue a reload',
                log_message = 'The song at the specified index does not exist (or has been removed). Recommended: Issue a reload',
                log_priority = 2)

    except Exception:
        #raise
        SAY(visible=visible,
            display_message=f"Failed to play \"{songpath}\"",
            log_message=f"Failed to play audio: \"{songpath}\"",
            log_priority=2,)



def voltransition(
    initial=cached_volume,
    final=cached_volume,
    disablecaching=False,  # NOT_USED: Enable volume caching by default
    transition_time=0.3,
    show_progress = False,
    # transition_time=1,
):
    global cached_volume, visible

    if not ismuted:
        for i in range(101):
            diffvolume = initial*100+(final-initial)*i
            time.sleep(transition_time/100)

            if show_progress and visible:
                print(f'{_theme_colors.prim}    -> {i}%', end='\r')
                print(COLOR_RESET, end = '\r')
            vas.vlc_media_player.get_media_player().audio_set_volume(int(diffvolume))

        # if not disablecaching:
        #     cached_volume = final


def vol_trans_process_spawn():
    vol_trans_process = Process(target=voltransition,
                                args=({'initial': cached_volume,
                                       'final': 0,
                                       'disablecaching': True}))
    vol_trans_process.start()
    vol_trans_process.join()

# https://stackoverflow.com/a/3463582/17685480
def remove_adjacent(seq): # works on any sequence, not just on numbers
    i = 1
    n = len(seq)
    while i < n: # avoid calling len(seq) each time around
        if seq[i] == seq[i-1]:
            del seq[i]
            # value returned by seq.pop(i) is ignored; slower than del seq[i]
            n -= 1
        else:
            i += 1
    
    #### return seq #### don't do this
    # function acts in situ; should follow convention and return None

def playpausetoggle(softtoggle=True,
                    use_multi=False,
                    transition_time=0.3,
                    show_progress=False): # Soft pause by default
    global isplaying, currentsong, cached_volume

    try:
        if currentsong:
            if isplaying:
                # with concurrent.futures.ProcessPoolExecutor() as executor:
                if use_multi:
                    vol_trans_process_spawn()
                else:
                    voltransition(initial=cached_volume,
                                  final=0,
                                  transition_time=transition_time*(softtoggle),
                                  disablecaching=True,
                                  show_progress=show_progress)
                # executor.submit(voltransition,
                #                 initial=cached_volume,
                #                 transition_time=transition_time*(softtoggle),
                #                 final=0,
                #                 disablecaching=True)

                vas.media_player(action='pausetoggle')

                if visible: print(' '*12, end='\r')
                IPrint("|| Paused", visible=visible)
                isplaying = False

            else:
                vas.media_player(action='pausetoggle')

                # with concurrent.futures.ProcessPoolExecutor() as executor:
                vas.vlc_media_player.get_media_player().audio_set_volume(0)

                if use_multi:
                    vol_trans_process_spawn()
                else:
                    voltransition(initial=0,
                                  final=cached_volume,
                                  transition_time=transition_time*(softtoggle),
                                  disablecaching=True,
                                  show_progress=show_progress)
                # executor.submit(voltransition, initial=0, final=cached_volume)
                if visible: print(' '*12, end='\r')
                IPrint("|> Resumed", visible=visible)
                isplaying = True
        else:
            isplaying = False
            SAY(visible=visible,
                display_message = 'Nothing to pause/unpause',
                log_message = 'Nothing to pause/unpause',
                log_priority = 2)

    except Exception:
        # raise
        SAY(visible=visible,
            log_priority=2,
            display_message=f'Failed to toggle play/pause for "{currentsong}"',
            log_message=f'Failed to toggle play pause for audio: "{currentsong}"',)


def stopsong():
    global isplaying, currentsong
    try:
        with contextlib.suppress(NameError):
            vas.media_player(action='stop')

            currentsong = None
            isplaying = False
            purge_old_lyrics_if_exist()
    except Exception:
        IPrint(f'Failed to stop: {currentsong}', visible=visible)

def searchsongs(queryitems, results_count=-1, play_from_results=0, search_type=0):
    global _local_sound_files_names_enumerated

    queryitems = [unidecode.unidecode(i) for i in queryitems]
    out = []

    for index, audio in _local_sound_files_names_enumerated:
        flag = True

        for queryitem in list(OrderedSet(queryitems)):
            # Remove speacial characters from query
            lhs = [i for i in queryitem.lower() if i not in SPECIAL_SONG_NAME_SYMBOLS]
            rhs = [i for i in unidecode.unidecode(audio).lower() if i not in SPECIAL_SONG_NAME_SYMBOLS]

            lhs = ''.join(lhs) # Join list of chars to form a string, [maybe unrequired]
            rhs = ''.join(rhs) # Join list of chars to form a string, [maybe unrequired]

            # Check if all query keywords exist in the given audio name
            if lhs not in rhs:
                # Atleast 1 keyword does NOT exist in the audio name, therefore, dismiss it
                flag = False # Dismiss audio

        if play_from_results == 1:
            # play first song from results
            if flag: return (index, audio)
        elif play_from_results >= 2 or play_from_results == 0:
            # play random song from results if play_from_results == 2
            # else do NOT play from search results...
            if len(out) == results_count: break # Stop after getting desired number of search results
            if flag: out.append((index, audio))

    return out

# TODO: - Implement librosa bpm + online bpm API features 
# def get_bpm(filename, duration=50, enable_round=True):
#     y, sr = librosa.load(filename, duration=duration)
#     tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#     if enable_round:
#         return round(tempo)
#     else:
#         return tempo

def fade_in_out(initvol=None,
                finalvol=None,
                fade_type=0,
                fade_duration=5,
                pretty_print=True,
                auto_pause_toggle=True):
    """
    To fade out, use fade_type = 1
    To fade in, use fade_type = 0
    """

    global cached_volume, isplaying, ismuted

    if initvol is None: initvol = cached_volume

    if ismuted:
        SAY(visible=visible,
            display_message='Cannot fade audio in or out when muted',
            log_message='Cannot fade audio in or out when muted',
            log_priority=3)

    if finalvol is not None: # Complex fade has been command issued,
                             # execute it

        # Music is paused, resume and then fade in to v > 0
        if finalvol != 0 and not isplaying and auto_pause_toggle:
            # Resume music
            IPrint("|> Resumed", visible=visible)
            vas.media_player(action='pausetoggle')
            isplaying = True

        voltransition(initial=initvol,
                      final=finalvol,
                      transition_time=fade_duration,
                      disablecaching=True,
                      show_progress=pretty_print)

        if finalvol != 0: cached_volume = finalvol
        if visible: print(' '*12, end='\r')

        if finalvol == 0:
            if isplaying and auto_pause_toggle:
                vas.media_player(action='pausetoggle')
                IPrint("|> Paused", visible=visible)
                isplaying = False

    elif fade_type == 0 and isplaying:
        SAY(visible=visible,
            display_message='Cannot fade in, audio already playing. Try pausing',
            log_message='Cannot fade in, audio already playing. Try pausing',
            log_priority=3)

    elif fade_type == 0 or isplaying:
        playpausetoggle(softtoggle = True,
                        transition_time=fade_duration,
                        show_progress=pretty_print)

    else:
        SAY(visible=visible,
            display_message='Cannot fade out, no audio playing',
            log_message='Cannot fade out, no audio playing',
            log_priority=3)

def enqueue(songindices):
    print(f'Enqueueing feature is still in progress... The developer {colored.fg("magenta_3a")}@{SYSTEM_SETTINGS["about"]["author"]}{colored.attr("reset")} will add this feature shortly...')
    '''
    # TODO: - Refine the following feature and add to production
    IPrint("Enqueueing", visible=visible)
    global song_paths_to_enqueue

    song_paths_to_enqueue = []

    for songindex in songindices:
        if int(songindex)-1 in range(len(_local_sound_files)):
            song_paths_to_enqueue.append(_local_sound_files[int(songindex)-1])
        else:
            IPrint(f"Skipping index: {int(songindex)-1}", visible=visible)

    if song_paths_to_enqueue:
        song_paths_to_enqueue = list(OrderedSet(song_paths_to_enqueue))
        for songpath in song_paths_to_enqueue:
            try:
                IPrint(f"Queued {song_paths_to_enqueue.index(songpath)+1}", visible=visible)
            except Exception:
                SAY(visible=visible,
                    display_message = "Queueing error",
                    log_message = "Could not enqueue one or more files",
                    log_pripority = 2)
                raise

        play_local_default_player(song_paths_to_enqueue, _songindex=None, is_queue=True)

    else:
        IPrint("No songs to queue", visible=visible)
    '''


def purge_old_lyrics_if_exist():
    lyrics_file_paths = ['temp/lyrics.txt', 'temp/lyrics.html']

    for lyrics_file_path in lyrics_file_paths:
        try:
            if os.path.isfile(lyrics_file_path):
                os.remove(lyrics_file_path)
        except Exception:
            raise

def local_play_commands(commandslist, _command=False):
    global cached_volume, currentsong_length, lyrics_saved_for_song

    purge_old_lyrics_if_exist()
    lyrics_saved_for_song = None

    if not _command:
        if len(commandslist) == 2:
            songindex = commandslist[1]
            if songindex.isnumeric():
                play_perm = 'y' # Value Init
                if int(songindex) in range(1, len(_local_sound_files)+1):
                    currentsong_length = None
                    if int(songindex) != -1:
                        try:
                            song_info = LOCAL_TRACK_INFOS.get(_local_sound_files[int(songindex)-1])
                            if song_info is None:
                                update_local_songs_info(add_file_paths = [_local_sound_files[int(songindex)-1]])
                                song_info = LOCAL_TRACK_INFOS.get(_local_sound_files[int(songindex)-1])
                            if song_info['isFav'] is None:
                                play_perm = input("This song is blacklisted. Are you sure you want to play it (y/[n])? ").strip()
                                if play_perm: play_perm = play_perm[0].lower()
                        except Exception:
                            raise

                    if play_perm == 'y':
                        play_local_default_player(songpath=_local_sound_files[int(songindex)-1],
                                                  _songindex=songindex)
                else:
                    if any(_local_sound_files):
                        SAY(visible=visible,
                            log_message='Out of bound audio index',
                            display_message=f'Song number {songindex} does not exist. Please input audio number between 1 and {len(_local_sound_files)}',
                            log_priority=3)

                    else:
                        SAY(visible=visible,
                            log_message='User attempted to play local audio, even though there are no audios in library',
                            display_message='There are no audios in library',
                            log_priority=2)

        else:
            # TODO: - Implement full queue functionality
            # as per `future ideas{...}.md`
            # Not yet implemented
            # This is just a sekeleton code for future

            songindices = commandslist[1:]
            _ = []
            for songindex in songindices:
                try:
                    if songindex.isnumeric():
                        _.append(songindex)
                except Exception:
                    pass

            songindices = _
            del _

            enqueue(songindices)
    else:
        currentsong_length = None
        play_local_default_player(songpath=_command[1:], _songindex=None)

def timeinput_to_timeobj(rawtime):
    try:
        if ':' in rawtime.strip():
            processed_rawtime = rawtime.split(':')
            processed_rawtime = [int(i) if i else 0 for i in processed_rawtime]

            # print(processed_rawtime)

            # timeobj: A list of the format [WHOLE HOURS IN SECONDS, WHOLE MINUTES in SECONDS, REMAINING SECONDS]
            timeobj = [value * 60 ** (len(processed_rawtime) - _index - 1)
                       for _index, value in enumerate(processed_rawtime)]

            totaltime = sum(timeobj)

            formattedtime = ' '.join([''.join(map(lambda x: str(x), i)) for i in list(
                zip(processed_rawtime, ['h', 'm', 's'][3-len(processed_rawtime):]))])

            if totaltime > currentsong_length:
                return ValueError
            else:
                return (formattedtime, totaltime)

        elif rawtime.strip() == '-0':
            return ('0', 0)

        elif rawtime.isnumeric():
            if int(rawtime) > currentsong_length:
                return ValueError
            processed_rawtime = list(
                map(lambda x: int(x), convert(int(rawtime)).split(':')))
            formattedtime = ' '.join([''.join(map(lambda x: str(x), i)) for i in list(
                zip(processed_rawtime, ['h', 'm', 's'][3-len(processed_rawtime):]))])
            # print (None, rawtime)
            return (formattedtime, rawtime)

    except Exception:
        # print (None, None)
        return (None, None)

def get_currentsong_length():
    global currentsong_length, currentsong_length
    # print(0)
    if currentsong:
        if not currentsong_length and currentsong_length != -1:
            currentsong_length = currentsong_length/1000
    # print(1)

    return currentsong_length

def song_seek(timeval=None, rel_val=None):
    global currentsong

    if timeval:
        try:
            vas.vlc_media_player.get_media_player().set_time(int(timeval)*1000)
            return True
        except Exception:
            return None
            # raise # TODO: - remove all "raise"d exceptions?

    elif not rel_val:
        SAY(visible=visible, display_message="Error: Can't seek in this audio",
            log_message=f'Unsupported codec for seeking audio: {currentsong}', log_priority=2)
        return None


def setmastervolume(value=None):
    global cached_volume

    if comtypes_load_error:
        SAY(visible=visible,
            log_message="comtypes functionality used even when not available",
            display_message="This functionality is unavailable",
            log_priority=3)
    else:
        if not value:
            value = cached_volume

        if value in range(101):
            set_master_volume(value)
        else:
            SAY(visible=visible, display_message='ERROR: Could not set master volume',
                log_message='Could not set master volume', log_priority=2)

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "{0:0>2.0f}:{1:0>2.0f}:{2:0>2.0f}".format(hour, minutes, seconds)

def isdecimal(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def rand_song_index_generate(no_repeat=False):
    global _local_sound_files_names_only, available_random_indices

    if len(_local_sound_files) == 0:
        SAY(visible=visible,
        log_message='User attempted to play local audio, even though there are no audios in library',
        display_message='There are no audios in library',
        log_priority=2)
        return None
    else:
        if no_repeat:
            if len(available_random_indices) == 1:
                # store last remaining unused random index
                return_index = available_random_indices[0]
                # refill `available_random_indices`, because all rand indices have been used up
                available_random_indices = list(range(len(_local_sound_files_names_only)-1))
                # return last remaining unused random index
                return return_index

            rand_song_index = rand.choice(available_random_indices)
            available_random_indices.remove(rand_song_index)

            return rand_song_index
        else:
            # Return any random index (which is valid and within bounds)
            return rand.randint(0, len(_local_sound_files_names_only)-1)

def update_local_songs_info(add_file_paths = None, remove_file_paths = None):

    global LOCAL_TRACK_INFOS

    # Info available
        # isFav
        # isExplicit
        # timesPaused
        # timesSeeked
        # timesSkipped
        # timesStopped
        # trackLyrics
        # streamCount

    # Info to be made available
        # effectiveStreamCount (>= 30 seconds effective duration)
        # effectiveStreamedDuration
        # timesStreamedfromStartToEnd
        # streamStartTimes

    # Stats to be made accessible to user

    if add_file_paths:
        for file in add_file_paths:
            '''
            isFav:
                True --> Favourited
                False --> Unfavourited
                None --> Blacklisted
            '''
            LOCAL_TRACK_INFOS.update({
                file: {'isFav': False,
                       'isExplicit': None,
                       'timesPaused': 0,
                       'timesSeeked': 0,
                       'timesSkipped': 0,
                       'timesStopped': 0,
                       'trackLyrics': "",
                       'streamCount': 0, # A list of datetime stamps and length of this list gives count of streams
                       'tags': [],
                       'assoc-playlists': [], # Searching for playlists of which this song is a part (by user)
                       }})

    if remove_file_paths:
        _ = [LOCAL_TRACK_INFOS.pop(file) for file in remove_file_paths]

    with open('data/track-infos.yml', 'w', encoding='utf-8') as fp:
        yaml.dump(LOCAL_TRACK_INFOS, fp)

def validate_time(rawtime):
    if rawtime is None: return
    rawtime = rawtime.replace(':', '')
    try:
        _ = float(rawtime)
    except Exception: # Not a real number
        return 2

    if '.' in rawtime: # +ve Non-Integer Number
        return 0       # Changed from "return 1" to "return 0"
                       # because +ve real numbers are valid seek values
                       # when rounded to the time-precision used in `vlc`
    elif float(rawtime) < 0: # -ve Non-Integer Number
        return 3
    else: # Integer Number --> Valid seek value
        return 0

# `media_url` is the only mandatory param in `play_vas_media`
def play_vas_media(media_url,
                   single_video = None,
                   media_name = None,
                   print_now_playing = True,
                   media_type = 'video',
                   show_link_chosen_msg = False):

    global isplaying, visible, currentsong, cached_volume
    global currentsong_length, current_media_type

    # Stop prev audios b4 loading VAS Media...
    stopsong()

    try:
        # VAS Media Load/Set
        if media_type == 'video': # This is actually meant for audio from a yt video and not a video itself
            YT_aud_url = vas.set_media(_type='yt_video', vidurl=media_url)
            current_media_type = 0

            if not media_name:
                try:
                    vid_info = YT_query.vid_info(media_url)
                    media_name = vid_info['title']
                except Exception:
                    media_name = '[VIDEO NAME COULD NOT BE RESOLVED]'
                    SAY(visible=visible,
                        display_message = '',
                        log_message = f'video name could not be resolved for:: {currentsong[1]}',
                        log_priority = 2)

            currentsong = (media_name, media_url, YT_aud_url)

            if print_now_playing and visible:
                if single_video:
                    IPrint(f"Playing YouTube search result:: {colored.fg('plum_1')}{media_name}{COLOR_RESET}", visible=visible)
                else:
                    IPrint(f"Chosen YouTube video:: {colored.fg('plum_1')}{media_name}{COLOR_RESET}", visible=visible)
                IPrint(f"{_theme_colors.exit_prompt}@{_theme_colors.prim}{media_url}{COLOR_RESET}", visible=visible)

        elif media_type == 'general':
            vas.set_media(_type='yt_audio', audurl=media_url)

            current_media_type = 1
            currentsong = media_url
            IPrint(f"Chosen custom media url:: {text_overflow_prettify(media_url)}", visible=visible*show_link_chosen_msg)

        elif media_type == 'radio':
            # Here `media_name` is actually the radio name
            vas.set_media(_type=f'radio/{media_name}') # No need for an explicit `audurl` here... (as per definition of vas.set_media)

            current_media_type = 2
            currentsong = media_name
            IPrint(f"Chosen radio: {colored.fg('light_goldenrod_1')}{currentsong}{COLOR_RESET}", visible=visible)

        elif media_type == 'redditsession':
            vas.set_media(_type='yt_audio', audurl=media_url)

            current_media_type = 3
            currentsong = (media_name, media_url)

        else:
            media_type = None
            SAY(visible=visible, display_message = "Invalid media type provided", log_message = "Invalid media type provided", log_priority = 2)

        if media_type == 'video': media_type = 'youtube'
        if media_type:

            # VAS Media Play
            vas.media_player(action='play')
            vas.vlc_media_player.get_media_player().audio_set_volume(int(cached_volume*100))

            # Save song to recents queue once it starts playing successfully
            recents_queue_save(currentsong)

            # TODO: - Save all audio info in `data` dir
            # save_song_data()

            # Save current audio to log/history.log in human readable form
            SAY(visible=visible,
                display_message = '',
                out_file='logs/history.log',
                log_message = [' \u2014 '.join(currentsong[:-1]) if type(currentsong)==tuple else currentsong][0],
                log_priority = 3,
                format_style = 0)

        currentsong_length = None

        USER_DATA['default_user_data']['stats']['play_count'][media_type] += 1
        save_user_data()

        while not vas.vlc_media_player.get_media_player().is_playing(): pass

        if current_media_type == 2:
            currentsong_length = -1
        else:
            IPrint(f"{_theme_colors.meta_info}Attempting to calculate audio length{_theme_colors.meta_info}", visible=visible)
            length_find_start_time = time.time()
            while True:
                if vas.vlc_media_player.get_media_player().get_length():
                    currentsong_length = vas.vlc_media_player.get_media_player().get_length()/1000
                    break
                if time.time() - length_find_start_time >= max_wait_limit_to_get_song_length:
                    currentsong_length = -1
                    break
        # currentsong_length gives output in ms, this will be converted to seconds when needed

        if currentsong_length == -1:
            SAY(visible=visible,
                log_message = "Cannot get length for vas media",
                display_message = "",
                log_priority=3)
        isplaying = True

    except ValueError:
        link_validity_string = url_is_valid(media_url, current_media_type != 1)
        SAY(visible=visible,
            display_message="Invalid media link provided",
            log_message="Invalid media link provided",
            log_priority=2)

def url_error_handle(url_error_code):
    if url_error_code == -1:
        SAY(visible=visible,
            display_message = 'An internet issue (SSL Error) was encountered, download failed',
            log_message = 'SSL error encountered, download failed',
            log_priority = 2)
        return True

    if url_error_code == -2:
        SAY(visible=visible,
            display_message = 'An internet issue (Proxy Error) was encountered, download failed',
            log_message = 'Proxy error encountered, download failed',
            log_priority = 2)
        return True

    return False


def choose_media_url(media_url_choices: list, yt: bool = True):
    global isplaying, currentsong

    if yt:
        if len(media_url_choices) == 1:
            media_name, media_url = media_url_choices[0]
            play_vas_media(media_name=media_name, media_url=media_url, single_video=True)

        else:
            chosen_index = input(f"{colored.fg('deep_pink_4c')}Choose video number between 1 and {len(media_url_choices)}" \
                                 f" (leave blank to skip): {colored.fg('navajo_white_1')}").strip()
            print(COLOR_RESET, end='')

            if chosen_index:
                try:
                    chosen_index = int(chosen_index)
                except Exception:
                    if visible:
                        print("ERROR: Invalid choice, choose again: ", end='\r')

                if chosen_index in range(1, len(media_url_choices)+1):
                    _, media_name, media_url = media_url_choices[chosen_index-1]
                    play_vas_media(media_name=media_name, media_url=media_url,
                                   single_video=False)
                elif visible:
                    print("ERROR: Invalid choice, choose again: ", end='\r')

                if visible: IPrint('\n', visible=visible)

def refresh_settings():
    global SYSTEM_SETTINGS, visible, supported_file_types, disable_OS_requirement, max_yt_search_results_threshold
    global max_wait_limit_to_get_song_length, FALLBACK_RESULT_COUNT, DEFAULT_EDITOR, MAX_RECENTS_SIZE

    try:
        with open('settings/system.toml', encoding='utf-8') as file:
            SYSTEM_SETTINGS = toml.load(file)
    except IOError:
        SYSTEM_SETTINGS = None

    try:
        with open('settings/settings.yml', encoding='utf-8') as u_data_file:
            SETTINGS = yaml.load(u_data_file)

    except IOError:
        SAY(visible=1,
            display_message = f'Encountered missing program file @{os.path.join(CURDIR, "settings/settings.yml")}',
            log_message = 'Aborting player because settings file was not found',
            log_priority = 1) # Log fatal crash
        sys.exit(1) # Fatal crash

    # Supported file extensions
    # (wav get_pos() in pygame provides played duration and not actual play position)
    supported_file_types = SYSTEM_SETTINGS["system_settings"]['supported_file_types'] 
    max_wait_limit_to_get_song_length = SYSTEM_SETTINGS['system_settings']['max_wait_limit_to_get_song_length']
    MAX_RECENTS_SIZE = SYSTEM_SETTINGS["system_settings"]['max_recents_size']

    visible = SETTINGS['visible']
    loglevel = SETTINGS.get('loglevel')
    DEFAULT_EDITOR = SETTINGS.get('editor path')
    FALLBACK_RESULT_COUNT = SETTINGS['display items count']['general']['fallback']
    MAX_RESULT_COUNT = SETTINGS['display items count']['general']['maximum']
    max_yt_search_results_threshold = SETTINGS['display items count']['youtube-search results']['maximum']

    if not loglevel:
        restore_default.restore('loglevel', SETTINGS)
        loglevel = SETTINGS.get('loglevel')

def reload_reddit_creds():
    global r_seshs

    try:
        from beta import redditsessions
        importlib.reload(redditsessions)

        if redditsessions.WARNING:
            if loglevel in [3, 4]:
                IPrint("[WARN] Could not load reddit-sessions extension...", visible=visible)
                IPrint(f"[WARN] ...{redditsessions.WARNING}...", visible=visible)
            reddit_creds_are_valid = False
        else:
            reddit_creds_are_valid = True
    except ImportError:
        if loglevel in [3, 4]:
            IPrint("[INFO] Could not load reddit-sessions extension..., module 'praw' missing...", visible=visible)

    if reddit_creds_are_valid: r_seshs = redditsessions.get_redditsessions()
    else: r_seshs = None

def text_overflow_prettify(text, length_thresh=100, end_length = 8, as_tuple=False):
    if length_thresh == 100:
        if as_tuple:
            final = (text[:92], text[-5:]) if len(text) > length_thresh else (text, None)
        else:
            final = f"{text[:92]}...{text[-5:]}" if len(text) > length_thresh else text
        return final
    elif length_thresh >= 14:
        if as_tuple:
            final = (text[:length_thresh-(end_length+3)], text[-end_length:]) if len(text) > length_thresh else (text, None)
        else:
            final = f"{text[:length_thresh-(end_length+3)]}...{text[-end_length:]}" if len(text) > length_thresh else text
        return final
    else:
        return


def get_prettified_recents(indices):
    global recents_QUEUE

    results = [] # prettified results (formatted as WYSIWYG)

    # results = [RECENTS_QUEUE[::-1][index] for index in indices]
    for index in indices:
        result= RECENTS_QUEUE[::-1][index]
        yt_play_type, media_player, inf = result

        if media_player == -1:
            # Offline stream from library via index
            cur_song = inf[1]
            cur_song = os.path.splitext(os.path.split(cur_song)[1])[0]
            result = f":: {colored.fg('plum_1')}{inf[0]}{COLOR_RESET} | {cur_song}"

        elif media_player == 0:
            yt_prefix = ["@yl", "@ys"][yt_play_type]
            result = (f"{_theme_colors.prim}{yt_prefix}: {colored.fg('aquamarine_3')}Title | {inf[0]}\n"
                      f"     {_theme_colors.sec}Link  | {inf[1]}{COLOR_RESET}")

        elif media_player == 1:
            result = f"{_theme_colors.prim}@media-link: {_theme_colors.oth}{text_overflow_prettify(inf)}{COLOR_RESET}"

        elif media_player == 2:
            result = f"{_theme_colors.sec}@webradio/{_theme_colors.oth}{inf}{COLOR_RESET}"

        elif media_player == 3:
            result = (f"{_theme_colors.prim}@rs: {colored.fg('aquamarine_3')}Session | {text_overflow_prettify(inf[0])}{COLOR_RESET}\n"
                      f"     {_theme_colors.tert}Link    | {text_overflow_prettify(inf[1])}{COLOR_RESET}")

        elif media_player == 4:
            # Offline stream from outside library via custom path
            result = f"{_theme_colors.sec}<path>/{_theme_colors.oth}{text_overflow_prettify(inf)}{COLOR_RESET}"

        results.append(result)

    return results

def lyrics_ops(show_window):
    global lyrics_saved_for_song, currentsong, ISDEV
    global visible

    refresh_lyrics = not (lyrics_saved_for_song == currentsong) # Song has changed since last save of lyrics,
                                                                # need to refresh the lyrics to match the current audio
    get_related = SETTINGS['get related songs']

    if currentsong:
        if current_media_type == 0:
            IPrint(f"Loading lyrics window for YT stream (Time taking)...", visible=visible)
            get_lyrics.show_window(refresh_lyrics = refresh_lyrics,
                                    max_wait_lim = max_wait_limit_to_get_song_length,
                                    get_related=get_related,
                                    show_window=show_window,
                                    weblink=currentsong[1],
                                    visible=visible,
                                    isYT=1)
        elif current_media_type == 1:
            IPrint(f"Loading lyrics window for online media stream (Time taking)...", visible=visible)
            get_lyrics.show_window(refresh_lyrics = refresh_lyrics,
                                    max_wait_lim = max_wait_limit_to_get_song_length,
                                    get_related=get_related,
                                    show_window=show_window,
                                    visible=visible,
                                    weblink=currentsong)
        elif current_media_type == 2:
            IPrint(f"Lyrics for webradio are not supported", visible=visible)
        elif current_media_type == 3:
            IPrint(f"Lyrics for reddit sessions are not supported", visible=visible)

        
        if current_media_type is not None:
            lyrics_saved_for_song = currentsong

        # elif ISDEV: # Song hasn't changes, no need to refresh lyrics
        #             # Just re-display the existing one
        #     print('Lyrics have already been loaded')

        if current_media_type is None:
            get_related = SETTINGS['get related songs']
            if get_related and lyrics_saved_for_song == currentsong: # True only if the audio has changed.
                                                                    # If it has, we need to get the related audios ONLY IF it is enabled in settings
                                                                    # If it's still the same audio, no need to get related audios again
                get_related = False

            refresh_lyrics = get_related

            if currentsong:
                if os.path.isfile(currentsong):
                    # IPrint(lyrics_window_note, visible=visible*show_window)
                    get_lyrics.show_window(refresh_lyrics = refresh_lyrics,
                                        max_wait_lim = max_wait_limit_to_get_song_length,
                                        get_related = get_related,
                                        show_window = show_window,
                                        visible=visible,
                                        songfile = currentsong)
                    lyrics_saved_for_song = currentsong

    os.chdir(CURDIR)

def reloaded_index(make_changes_global=False):
    if currentsong:
        try:
            reloaded_songindex = [i.lower() for i in _local_sound_files].index(currentsong.lower())+1
        except:
            reloaded_songindex = None

        if make_changes_global:
            global songindex
            songindex = reloaded_songindex

        return reloaded_songindex

    else:
        return -1

def current_local_song_index():
    if currentsong:
        if current_media_type is None: # Offline Streaming
            if isinstance(reloaded_index(), int):
                return songindex
            if songindex == None:
                return "<path>"

        elif current_media_type == 0: # YouTube Streaming
            if YOUTUBE_PLAY_TYPE == 0: # Stream from YT Link
                return "@yl"
            elif YOUTUBE_PLAY_TYPE == 1: # Stream from YT Search Result
                return "@ys"

        elif current_media_type == 1:
            return "@ml"

        elif current_media_type == 2:
            return "@wra"

        elif current_media_type == 3:
            return "@rs"

    return -1

def current_song_name(pretty_display = True, detailed_output = True):
    if detailed_output:
        if currentsong:
            if current_media_type is not None: # online streaming
                if current_media_type == 0:
                    if YOUTUBE_PLAY_TYPE == 0:
                        if pretty_display:
                            IPrint(f"{_theme_colors.exit_statement}@{COLOR_RESET}youtube-link: {colored.fg('aquamarine_3')}Title | {currentsong[0]}", visible=visible)
                            IPrint(f"               {colored.fg('navajo_white_1')}Link  | {currentsong[1]}{COLOR_RESET}", visible=visible)
                        else:
                            return currentsong[0]
                    elif YOUTUBE_PLAY_TYPE == 1:
                        if pretty_display:
                            IPrint(f"{_theme_colors.exit_statement}@{COLOR_RESET}youtube-search: {colored.fg('aquamarine_3')}Title | {currentsong[0]}", visible=visible)
                            IPrint(f"                 {colored.fg('navajo_white_1')}Link  | {currentsong[1]}{COLOR_RESET}", visible=visible)
                        else:
                            return currentsong[0]
                elif current_media_type == 1:
                    if pretty_display:
                        IPrint(f"{colored.fg('hot_pink_1a')}@{COLOR_RESET}media-link: {colored.fg('aquamarine_3')}{currentsong}{COLOR_RESET}", visible=visible)
                    else:
                        return currentsong
                elif current_media_type == 2:
                    if pretty_display:
                        IPrint(f"{_theme_colors.oth}@{COLOR_RESET}webradio/{colored.fg('navajo_white_1')}{currentsong}{COLOR_RESET}", visible=visible)
                    else:
                        return currentsong
                elif current_media_type == 3:
                    if pretty_display:
                        IPrint(f"{_theme_colors.prim}@{COLOR_RESET}redditsession: {colored.fg('aquamarine_3')}Session | {currentsong[0]}{COLOR_RESET}", visible=visible)
                        IPrint(f"                {colored.fg('navajo_white_1')}Link    | {currentsong[1]}{COLOR_RESET}", visible=visible)
                    else:
                        return currentsong[0]

            else: # offline streaming
                if pretty_display:
                    IPrint(f":: {_theme_colors.sec} {reloaded_index()}{COLOR_RESET} | {_theme_colors.sec}{currentsong}", visible=visible)
                else:
                    return currentsong
        else:
            # currentsong = None
            if pretty_display:
                IPrint(f"{_theme_colors.exit_statement}({_theme_colors.sec}Not Playing{_theme_colors.exit_statement}){NBSP}", visible=visible)
            else:
                return "(Not Playing)"

    else:
        if currentsong:
            if current_media_type is not None: # online streaming
                if current_media_type == 0:
                    if YOUTUBE_PLAY_TYPE == 0:
                        if pretty_display:
                            IPrint(f"@yl: {currentsong[0]}", visible=visible)
                        else:
                            return currentsong[0]
                    elif YOUTUBE_PLAY_TYPE == 1:
                        if pretty_display:
                            IPrint(f"@ys: {currentsong[0]}", visible=visible)
                        else:
                            return currentsong[0]
                elif current_media_type == 1:
                    if pretty_display:
                        IPrint(f"@ml: {currentsong}", visible=visible)
                    else:
                        return currentsong
                elif current_media_type == 2:
                    if pretty_display:
                        IPrint(f"@wra: {currentsong}", visible=visible)
                    else:
                        return currentsong
                elif current_media_type == 3:
                    if pretty_display:
                        IPrint(f"@rs: {currentsong[0]}", visible=visible)
                    else:
                        return currentsong[0]
            else: # offline streaming
                cur_song = os.path.splitext(os.path.split(currentsong)[1])[0]
                if pretty_display:
                    IPrint(f":: {colored.fg('plum_1')}{reloaded_index()}{colored.fg('deep_pink_4c')} | {colored.fg('navajo_white_1')}{cur_song}{NBSP}", visible=visible)
                else:
                    return cur_song
        else:
            # currentsong = None
            if pretty_display:
                IPrint(f"{_theme_colors.exit_statement}({_theme_colors.sec}Not Playing{_theme_colors.exit_statement}){COLOR_RESET}", visible=visible)
            else:
                return "(Not Playing)"


def display_and_choose_podbean(latest_podbeans,
                               commandslist,
                               result_count,
                               is_rss=False):

    podtype = ['podbean', 'rss'][is_rss]
    latest_podbeans_table = []

    if result_count is None:
        result_count = FALLBACK_RESULT_COUNT
    elif result_count == -1:
        result_count = None

    for pod in latest_podbeans[:result_count]:
        table_items_1 = [text_overflow_prettify(pod[key].strip('...'), length_thresh=60) if pod.get(key) else None for key in ['title', 'caption'] ]
        table_items_2 = [pod[key] if pod.get(key) else None for key in ['pub_date', 'is_explicit']]
        table_items = table_items_1+table_items_2
        latest_podbeans_table.append(table_items)

    podcast_sessions_count = len(latest_podbeans_table)

    if commandslist[0].startswith(('.', './')):
        # Play podcast session at particular index from extracted podcast data
        podbean_index = str(result_count)
    else:
        # Display extracted podcast data and ask from the user the session index to be played
        if podcast_sessions_count: # If podcast has data for >= 1 session
            IPrint(f"Showing [{podcast_sessions_count}] {podtype} session{'s' if podcast_sessions_count > 1 else ''}")
            IPrint(tbl([(i+1, *j) for i, j in enumerate(latest_podbeans_table)],
                        # missingval=f'{_theme_colors.exit_statement}( N/A ){colored.attr("reset")}',
                        missingval='( N/A )',
                        headers=('#', ['pod', 'title'][is_rss], 'caption', 'published on', 'is explicit'),
                        tablefmt='pretty',
                        colalign=('center','left',)),
                        visible=visible)
            IPrint('', visible=visible)
            podbean_index = input(f"{_theme_colors.oth}Enter {podtype} session number to tune into: {colored.fg('navajo_white_1')}")

            if visible:
                print(COLOR_RESET, end='')

        else: # If podcast is empty (i.e. 0 sessions)
            SAY(visible=visible,
                display_message="Podcast is empty",
                log_message="Podcast is empty",
                log_priority=2)

    if podbean_index.isnumeric():
        # Check to see if podcast session index is numeric
        podbean_index = int(podbean_index)-1
        if podbean_index in range(podcast_sessions_count):
            # A valid podcast session index has finally been selected
            IPrint(f"Attempting to play {podtype}: {colored.fg('green_1')}{latest_podbeans[podbean_index]['title']}{COLOR_RESET}", visible=visible)
            # TODO: - rm following 3 lines
            # print("Latest podbean")
            # print(latest_podbeans)
            # print()
            if latest_podbeans[podbean_index].get('url'):
                if caption := latest_podbeans[podbean_index].get('caption'):
                    if visible:
                        caption_shortened_1, caption_shortened_2 = text_overflow_prettify(caption, length_thresh=200, end_length=16, as_tuple=True)
                        caption_shortened_formatted = f"{_theme_colors.sec}{caption_shortened_1}"\
                                                      f"{_theme_colors.tert}..."\
                                                      f"{_theme_colors.sec}{caption_shortened_2}"\
                                                      f"{NBSP}"

                        print(caption_shortened_formatted) # This will only print if `visible` == True

                play_vas_media(media_url = latest_podbeans[podbean_index]['url'],
                               media_type='general',
                               show_link_chosen_msg=False)
            else:
                SAY(visible=visible,
                    display_message='Empty podcast... No usable link could be extracted',
                    log_message='Empty podcast',
                    log_priority=3)


    elif podbean_index.strip() == '':
        SAY(visible=visible,
            display_message=f'No {podtype} session number entered, skipping',
            log_message=f'{podtype.title()} session index left empty, skipped',
            log_priority=3)

    else:
        SAY(visible=visible,
            display_message=f'You have entered an invalid {podtype} session number',
            log_message=f'Invalid {podtype} session number entered',
            log_priority=2)

def search_results_table_header(display_table_formatted_sections, now_playing_marker=""):

    display_table_formatted_header = display_table_formatted_sections[:3]
    display_table_formatted_header[0] = (
        _theme_colors.tert + " "*len(now_playing_marker) +
        display_table_formatted_header[0] + COLOR_RESET
    )
    display_table_formatted_header[1] = (
        _theme_colors.sec + " "*len(now_playing_marker) +
        display_table_formatted_header[1] + COLOR_RESET
    )
    display_table_formatted_header[2] = (
        _theme_colors.tert + " "*len(now_playing_marker) +
        display_table_formatted_header[2] + COLOR_RESET
    )

    return display_table_formatted_header


def process(command):
    global _local_sound_files_names_only, visible, currentsong, isplaying, ismuted, cached_volume
    global current_media_type, DEFAULT_EDITOR, YOUTUBE_PLAY_TYPE, lyrics_saved_for_song
    global _theme_colors, command_count, volume_is_boosted, BETA_STATUS

    reloaded_index(make_changes_global=True)
    commandslist = command.strip().split()

    with contextlib.suppress(Exception):
        if vas.vlc_media_player.get_state().value == 6:
            currentsong = None
            isplaying = False

    if commandslist != []:  # Atleast 1 word

        # Quitting the player
        if commandslist in [['exit'], ['quit']]:
            perm = input(_theme_colors.exit_prompt+'Do you want to exit?' + _theme_colors.prim + '[Y]es / [N]o (default = N): '+_theme_colors.tert)
            print(COLOR_RESET, end = '')
            if perm.strip().lower() == 'y':
                return False


        # Quitting the player w/o conf
        elif commandslist in [['exit', 'y'], ['quit', 'y']]:
            return False

        command_count += 1

        if commandslist in [['all'], ['all*']]:
            command.endswith
            rescount = MAX_RESULT_COUNT

            results_enum = _local_sound_files_names_enumerated
            if not command.endswith('*'):
                results_enum = _local_sound_files_names_enumerated[:rescount]
            IPrint(tbl([(i, j) for i, j in results_enum], tablefmt='plain'), visible=visible)

        # TODO: Need to display files in n columns (Mostly 3 cols) depending upon terminal size (dynamically...)
        if commandslist[0] in ['list', 'ls']:

            if len(_local_sound_files) != 0:
                # TODO: Get values for `order_results` and `order_type` from SETTINGS
                indices = [] # Indices of audios to be displayed
                rescount = FALLBACK_RESULT_COUNT
                order_results = False
                order_type = 1 # Default value (1): Display in ascending order

                if 'o' in commandslist[1:]:
                    order_results = True
                if 'desc' in commandslist[1:]:
                    order_type = 0

                range_command_is_valid = True
                if '-' in command:

                    _command = command.replace('o', '').replace('desc', '')
                    _command = _command.strip().lstrip(commandslist[0]).split('-')

                    if len(_command) == 2:
                        try:
                            ls_x_to_y = list(map(lambda i:int(i.strip()), _command))
                            ls_x_to_y[0] -= 1
                            if ls_x_to_y[0] < ls_x_to_y[1]:
                                indices = list(range(*ls_x_to_y))
                            else:
                                SAY(visible=visible,
                                    display_message = 'Range order is reversed. It should be lower to upper',
                                    log_message = 'Invalid order of bounds for listing range of audios',
                                    log_priority = 2)
                                range_command_is_valid = False
                        except Exception:
                            SAY(visible=visible,
                                display_message = 'Invalid bounds for listing range of audios',
                                log_message = 'Invalid bounds for listing range of audios',
                                log_priority = 2)
                            range_command_is_valid = False
                    else:
                        SAY(visible=visible,
                            display_message = 'Invalid command for listing a range of audios',
                            log_message = 'Invalid command for listing a range of audios',
                            log_priority = 2)
                        range_command_is_valid = False
                else:
                    _commandslist = commandslist.copy()

                    if 'o' in commandslist: _commandslist.remove('o')
                    if 'desc' in commandslist: _commandslist.remove('desc')
                    if len([i for i in commandslist if i.isnumeric()]) == 1:
                        if commandslist[1].isnumeric():
                            rescount = int(commandslist[1])
                    else:
                        for i in commandslist[1:]:
                            if i.isnumeric():
                                if int(i)-1 not in indices:
                                    indices.append(int(i)-1)


                if indices:
                    results = [_local_sound_files_names_only[index] for index in indices]
                    results_enum = list(zip(indices, results))
                    if order_results:
                        results_enum = sorted(results_enum, key = lambda x: x[0], reverse = not order_type)

                if len([i for i in commandslist if i.isnumeric()]) == 0 and '-' not in command and len(commandslist) != 1:
                    # List files matching provided regex pattern
                    # Need to implement a check to validate the provided regex pattern
                    print(f'Regex search is still in progress... The developer {colored.fg("magenta_3a")}@{SYSTEM_SETTINGS["about"]["author"]}{colored.attr("reset")} will add this feature shortly...')
                    # regex_pattern
                    # regexp = re.compile(regex_pattern)

                else:
                    if len([i for i in commandslist if i.isnumeric()]) in [0, 1] and '-' not in command:
                        results_enum = list(enumerate(_local_sound_files_names_only[:rescount]))
                        if order_results:
                            results_enum = sorted(results_enum, key = lambda x: x[0], reverse = not order_type)

                    if indices or len([i for i in commandslist if i.isnumeric()]) in [0, 1]:
                        if range_command_is_valid:
                            IPrint(tbl([(i+1, j) for i, j in results_enum], tablefmt='plain'), visible=visible)


            else:
                SAY(visible=visible,
                    log_message='User attempted to play local audio, even though there are no audios in library',
                    display_message='There are no audios in library',
                    log_priority=2)

        elif commandslist[0] == '/open':
            if current_media_type is None:
                if len(commandslist) == 1: # To open current audio
                    if currentsong and device_is_connected():
                            try:
                                open_in_youtube(currentsong)
                            except OSError:
                                SAY(visible=visible,
                                    display_message="Video Load Error: Could not load video... (Maybe check your VPN?)",
                                    log_message="Video Load Error (Maybe VPN)",
                                    log_priority = 2)
                    else:
                        SAY(visible=visible,
                            display_message = 'No audio playing currently, try using "/open" with a audio number or path instead',
                            log_message = 'User issued "/open" as an isolated command even when no audio is currently playing',
                            log_priority = 2)

                elif len(commandslist) == 2: # To open custom audio
                    if commandslist[1].isnumeric(): # To open custom audio by index
                        song_index = int(commandslist[1])-1
                        songfile = _local_sound_files[song_index]
                        open_in_youtube(songfile)
                    else:
                        if os.path.isfile(commandslist[1]): # To open custom audio by absolute filepaths
                            songfile = commandslist[1]
                            open_in_youtube(songfile)
                        else:
                            SAY(visible=visible,
                                display_message = 'File path provided for "/open" is inexistent or invalid',
                                log_message = 'File path provided for "/open" is inexistent or invalid',
                                log_priority = 2)

            else:
                SAY(visible=visible,
                    display_message = '"/open" can only be used for local streaming, try "open" intead',
                    log_message = '"/open" cannot be used for online streaming, only local',
                    log_priority = 2)

        elif commandslist[0] in ['fav', 'bl', 'blacklisted']:
            command_is_fav = not ['fav', 'bl', 'blacklisted'].index(commandslist[0])
            songpath = current_song_name(pretty_display=False)
            current_song_data = None

            if songindex:
                current_song_data = LOCAL_TRACK_INFOS.get(songpath)

            if len(commandslist) == 1: # Isolated fav/blacklist command entered
                if current_song_data:
                    if command_is_fav:
                        IPrint("Yes" if current_song_data['isFav'] else "No", visible=visible)
                    else:
                        IPrint("Yes" if current_song_data['isFav'] is None else "No", visible=visible)
                else:
                    SAY(visible=visible,
                        display_message = 'No song playing currently',
                        log_message = 'No song playing currently',
                        log_priority = 2)

            elif len(commandslist) == 2:
                if commandslist[1] == '!': # Toggle fav/blacklist state
                    if current_song_data:
                        if songindex:
                            if command_is_fav:
                                LOCAL_TRACK_INFOS[songpath]['isFav'] = not LOCAL_TRACK_INFOS[songpath]['isFav']
                                feedback_message = [_theme_colors.error+"Unf", _theme_colors.prim+"F"]\
                                                   [LOCAL_TRACK_INFOS[songpath]['isFav']] + f'avourited{NBSP}song'
                            else:
                                if LOCAL_TRACK_INFOS[songpath]['isFav'] is None:
                                    LOCAL_TRACK_INFOS[songpath]['isFav'] = False
                                    feedback_message = f"{_theme_colors.prim}[-]{NBSP}Removed song from blacklist"
                                else:
                                    LOCAL_TRACK_INFOS[songpath]['isFav'] = None
                                    feedback_message = f"{_theme_colors.prim}[+]{NBSP}Added song to blacklist and removed from favs"

                            update_local_songs_info()
                            IPrint(f'{feedback_message} {_theme_colors.sec}@{_theme_colors.tert}{songindex-1}{COLOR_RESET}: "{_local_sound_files[songindex-1]}"')
                        else:
                            IPrint("Working on it") #TODO: Work on it
                            # IPrint('Favourited "{songpath}"')

                elif commandslist[1] in ['-', '+']: # Set fav/blacklist state to true/false
                    if current_song_data:
                        if songindex:
                            set_state = bool(['-', '+'].index(commandslist[1]))
                            if command_is_fav:
                                LOCAL_TRACK_INFOS[songpath]['isFav'] = set_state
                                feedback_message = [_theme_colors.error+"Unf", _theme_colors.prim+"F"]\
                                                   [set_state] + f'avourited{NBSP}song'
                            else:
                                if set_state:
                                    LOCAL_TRACK_INFOS[songpath]['isFav'] = None
                                    feedback_message = f"{_theme_colors.prim}[+]{NBSP}Added song to blacklist and removed from favs"
                                else:
                                    LOCAL_TRACK_INFOS[songpath]['isFav'] = False
                                    feedback_message = f"{_theme_colors.prim}[-]{NBSP}Removed song from blacklist"

                            update_local_songs_info()
                            IPrint(f'{feedback_message} {_theme_colors.sec}@{_theme_colors.tert}{songindex-1}{COLOR_RESET}: "{_local_sound_files[songindex-1]}"')
                        else:
                            IPrint("Working on it") #TODO: Work on it
                            # IPrint('Favourited "{songpath}"')

        elif commandslist[0] in ['favs', 'blacklist']:
            is_fav = commandslist[0] == 'favs'

            if len(commandslist) == 1:
                limited_result_count_search = MAX_RESULT_COUNT
            elif len(commandslist) == 2:
                if commandslist[1].isnumeric():
                    limited_result_count_search = int(commandslist[1])
                else:
                    SAY(visible=visible,
                        display_message = 'favourited song index is not valid',
                        log_message = 'No song playing currently',
                        log_priority = 2)

            if limited_result_count_search is None: # No favs
                IPrint(f"{_theme_colors.error} -- No {['blacklisted tracks', 'favs'][is_fav]} found -- {COLOR_RESET}", visible=visible)
            else:
                results = [
                                (_local_sound_files.index(info[0])+1, _local_sound_files_names_only[_local_sound_files.index(info[0])])
                                for info in LOCAL_TRACK_INFOS.items()
                                if (info[1]['isFav'] if is_fav else info[1]['isFav'] == None)
                            ]

                fav_count_exceeds_threshold = len(results) > limited_result_count_search
                results = results[:limited_result_count_search]

                favs_display_string_1 = f"{_theme_colors.prim}Showing"
                favs_display_string_2 = f"{[_theme_colors.sec if len(results)-1 else _theme_colors.tert][0]}"\
                                        f"{len(results)}{_theme_colors.prim}"
                favs_display_string_3 = ["blacklisted song"+'s'*(not len(results)), "favourites"][is_fav]
                # favs_display_string_4 = f"{[_theme_colors.sec if len(results)-1 else _theme_colors.tert][0]}{colored.style.UNDERLINED}{' '.join(myquery)}{COLOR_RESET}{NBSP}"

                # favs_display_string_1 = favs_display_string_2 = favs_display_string_3 = favs_display_string_4 = ""

                display_table = tbl(results,
                                    tablefmt='pretty',
                                    headers=('#', 'Song'),
                                    colalign=('center', 'left'))

                if BETA_STATUS:
                    display_table_formatted_sections = display_table.splitlines()
                    current_song_index_in_search_results = None

                    if songindex != -1:
                        with contextlib.suppress(StopIteration):
                            current_song_index_in_search_results = results.index(next(x for x in results if x[0] == songindex))

                        # if current_song_index_in_search_results is not None:
                            # now_playing_marker = "--@--> "
                            now_playing_marker = " :: "

                            display_table_formatted_sections = (
                                # Table header (First 3 lines)
                                search_results_table_header(display_table_formatted_sections, now_playing_marker),
                                # Part above now playing
                                display_table_formatted_sections[3:current_song_index_in_search_results+3],
                                # Now playing (if exists)
                                display_table_formatted_sections[current_song_index_in_search_results+3],
                                # Part below now playing
                                display_table_formatted_sections[current_song_index_in_search_results+3+1:],
                            )

                    # First line for description of query results
                    IPrint(f"{favs_display_string_1} {favs_display_string_2} "+
                           f"{favs_display_string_3}",
                           visible=visible)

                    # Fully formatted table header
                    if current_song_index_in_search_results is None:
                        now_playing_marker = ""
                        display_table_formatted_sections = (
                            search_results_table_header(display_table_formatted_sections, now_playing_marker),
                            display_table_formatted_sections[3:],
                        )
                    _ = [IPrint(i, visible=visible) for i in display_table_formatted_sections[0]]

                    # Part of table above "now-playing" song (if "now-playing" song is within the results)
                    # else, it just prints the entire table
                    _ = [IPrint(f"{len(now_playing_marker)*' '}{i}", visible=visible) for i in display_table_formatted_sections[1]]

                    if current_song_index_in_search_results is not None and songindex != -1:
                        # If "now-playing" song is within the results
                        # Highlighting the "now-playing" song 
                        IPrint(_theme_colors.prompt_foreground_1 + _theme_colors.prompt_background_1 + now_playing_marker +
                            _theme_colors.prompt_foreground_3 + _theme_colors.prompt_background_3 +
                            display_table_formatted_sections[2] + NBSP,
                            visible=visible)

                        # Part of table below "now-playing" song 
                        _ = [IPrint(f"{len(now_playing_marker)*' '}{i}", visible=visible) for i in display_table_formatted_sections[3]]


        elif commandslist == ['last']:
            last_index, last_name = _local_sound_files_names_enumerated[-1]
            IPrint(f">| {last_index} | {last_name}", visible=visible)

        # Misspelled podbean commands
        elif commandslist[0] in ['pod', 'podbean', '.pods', '.podbeans']:
            warn_msg = None
            if commandslist[0].startswith('.'):
                warn_msg=f'/? Invalid command {commandslist[0]}, perhaps you meant "{commandslist[0][:-1]}"'
            else:
                if len(commandslist) in [2, 3]:
                    if commandslist[1] == 'vendors':
                        result_count=FALLBACK_RESULT_COUNT
                        if len(commandslist) == 3:
                            if commandslist[2] == 'all': result_count=None
                            if commandslist[2].isnumeric(): result_count=int(commandslist[2])
                        if result_count and len(pod_vendors) > result_count:
                            IPrint("{0}Showing the first {1} vendors (you may change this 'fallback' result count in settings){2}".format(_theme_colors.prim, result_count, COLOR_RESET), visible=visible)
                        for pod_vendor in list(pod_vendors.keys())[:result_count]: print(f"  {colored.fg('aquamarine_3')}--> {COLOR_RESET}{pod_vendor}")
                    else:
                        warn_msg=f'/? Invalid command {commandslist[0]}, perhaps you meant "{commandslist[0]}s"'
                else:
                    warn_msg=f'/? Invalid command {commandslist[0]}, perhaps you meant "{commandslist[0]}s"'
            
            if warn_msg:
                SAY(visible=visible,
                    display_message=warn_msg,
                    log_message=f'podbean command assumed to be misspelled',
                    log_priority=3)


        # Podbean music: default vendor => 1001tracklists
        # Also supports valid custom rss links
        elif commandslist[0] in ['pods', 'podbeans', '.pod', '.podbean',
                                 '/rss', '/rss-link', './rss', './rss-link']:

            # Default Podcast Vendor from podbean (music podcast)
            podbean_vendor = '1001tracklists' # Bad idea to hardcode this. Try to get it from the podcasts.py file instead
            result_count = None # Falls back to `FALLBACK_RESULT_COUNT` automatically
                                # when the `display_and_choose_podbean` command is called

            if len(commandslist) in [2, 3]: # Either pod[bean]s <count> or
                                            # pod[bean]s <count> <vendor>
                if commandslist[0] in ['/rss', '/rss-link', './rss', './rss-link']:
                    # Playing from a custom rss link
                    rss_link = commandslist[1]
                    rss_index = None

                    if len(commandslist) == 3:
                        rss_index = commandslist[2]
                    rss_is_valid = url_is_valid(rss_link)
                    if rss_is_valid:
                        IPrint(f"Attempting to play {_theme_colors.sec}rss link{NBSP}", visible=visible)
                        latest_podbeans = get_latest_podbean_data(rss_link=rss_link)
                        display_and_choose_podbean(latest_podbeans=latest_podbeans,
                                                   commandslist=commandslist,
                                                   result_count=int(rss_index) if rss_index else None,
                                                   is_rss=True)
                    elif not url_error_handle(rss_is_valid):
                        SAY(visible=visible,
                            display_message = 'Invalid rss url provided',
                            log_message = 'Url for RSS media invalid',
                            log_priority = 2)
                else:
                    podbean_command_numbers_at = [i for i,j in enumerate(commandslist) if j.isnumeric()]

                    # Only podbean vendor has been provided
                    if len(podbean_command_numbers_at) == 0:
                        podbean_vendor = commandslist[1]
                    # Both podbean vendor has been provided
                    elif len(podbean_command_numbers_at) == 1:
                        result_count = int(commandslist[podbean_command_numbers_at[0]])
                        if len(commandslist) == 3:
                            podbean_vendor = commandslist[3-podbean_command_numbers_at[0]]
                    # Invalid rss/podcast command provided
                    else:
                        SAY(visible=visible,
                            display_message = 'Too many numbers provided, try using only 1',
                            log_message = 'Too many numbers provided for pod family of command',
                            log_priority = 2)

                    latest_podbeans = get_latest_podbean_data(vendor=podbean_vendor)
                    if latest_podbeans is not None:
                        IPrint(f"{['Show', 'Play'][commandslist[0][0] == '.']}ing from {colored.fg('green_1')}{podbean_vendor}{COLOR_RESET}", visible=visible)
                        display_and_choose_podbean(latest_podbeans=latest_podbeans,
                                                   commandslist=commandslist,
                                                   result_count=result_count,
                                                   is_rss=False)
                    elif podbean_vendor in ['vendor', 'vendors']: # No podcasts found for provided vendor
                        SAY(visible = visible,
                            display_message = 'Podbean vendor unknown. List vendors with "pod[bean] vendors"',
                            log_message = 'Unknown pod vendor mentioned',
                            log_priority = 2)


        if commandslist in [['recent', 'count'], ['recents', 'count']]:
            IPrint(f"Recents count: {len(RECENTS_QUEUE)}", visible=visible)

        elif commandslist[0] in ['recent', 'recents']:
            # TODO: Get values for `order_results` and `order_type` from SETTINGS
            indices = [] # Indices of audios to be displayed
            rescount = FALLBACK_RESULT_COUNT
            order_results = False
            order_type = 1 # Default value (1): Display in ascending order

            if 'o' in commandslist[1:]:
                order_results = True
            if 'desc' in commandslist[1:]:
                order_type = 0

            range_command_is_valid = True
            if '-' in command:

                _command = command.replace('o', '').replace('desc', '')
                _command = _command.strip().lstrip(commandslist[0]).split('-')

                if len(_command) == 2:
                    try:
                        recents_x_to_y = list(map(lambda i:int(i.strip()), _command))
                        recents_x_to_y[0] -= 1
                        if recents_x_to_y[0] < recents_x_to_y[1]:
                            indices = list(range(*recents_x_to_y))
                        else:
                            SAY(visible=visible,
                                display_message = 'Range order is reversed. It should be lower to upper',
                                log_message = 'Invalid order of bounds for listing range of recents',
                                log_priority = 2)
                            range_command_is_valid = False
                    except Exception:
                        SAY(visible=visible,
                            display_message = 'Invalid bounds for listing recents range',
                            log_message = 'Invalid bounds for listing range of recents',
                            log_priority = 2)
                        range_command_is_valid = False
                else:
                    SAY(visible=visible,
                        display_message = 'Invalid command for listing recents range',
                        log_message = 'Invalid command for listing a range of recents',
                        log_priority = 2)
                    range_command_is_valid = False
            else:
                _commandslist = commandslist.copy()

                if 'o' in commandslist: _commandslist.remove('o')
                if 'desc' in commandslist: _commandslist.remove('desc')
                if len([i for i in commandslist if i.isnumeric()]) == 1:
                    if commandslist[1].isnumeric():
                        rescount = int(commandslist[1])
                else:
                    for i in commandslist[1:]:
                        if i.isnumeric():
                            if int(i)-1 not in indices:
                                indices.append(int(i)-1)

            if indices:
                results = get_prettified_recents(indices)
                results_enum = list(zip(indices, results))

                if order_results:
                    results_enum = sorted(results_enum, key = lambda x: x[0], reverse = not order_type)

            if len([i for i in commandslist if i.isnumeric()]) == 0 and '-' not in command and len(commandslist) != 1:
                # List files matching provided regex pattern
                # Need to implement a check to validate the provided regex pattern
                print(f'Regex search is still in progress... The developer {colored.fg("magenta_3a")}@{SYSTEM_SETTINGS["about"]["author"]}{colored.attr("reset")} will add this feature shortly...')
                # regex_pattern
                # regexp = re.compile(regex_pattern)

            else:
                if len([i for i in commandslist if i.isnumeric()]) in [0, 1] and '-' not in command:
                    if rescount > len(RECENTS_QUEUE):
                        rescount = len(RECENTS_QUEUE)
                    results = get_prettified_recents(list(range(rescount)))
                    results_enum = list(enumerate(results))
                    if order_results:
                        results_enum = sorted(results_enum, key = lambda x: x[0], reverse = not order_type)

                if indices or len([i for i in commandslist if i.isnumeric()]) in [0, 1]:
                    if range_command_is_valid:
                        IPrint(tbl([(-(i+1), j) for i, j in results_enum], tablefmt='plain'), visible=visible)

        elif commandslist == ['last', 'played']:
            if RECENTS_QUEUE:
                if currentsong and len(RECENTS_QUEUE) >= 2:
                    IPrint(get_prettified_recents([1])[0], visible=visible)
                else:
                    IPrint(get_prettified_recents([0])[0], visible=visible)
            else:
                SAY(visible=visible,
                    display_message='No recents recorded yet for the current session',
                    log_message='No recents to display',
                    log_priority=2)

        elif commandslist[0] in ['exclude', 'include']:
            possible_download_keywords = ['download', 'downloads', 'dl', 'dls']
            if len(commandslist) == 2:
                if commandslist[1] in possible_download_keywords:
                    reload_sounds(quick_load = False,
                                  include_dl_dir = commandslist[0][:2] == 'in')

        elif commandslist in [['rss'], ['rss-link'], ['rss', 'link'], ['rss-links'], ['rss', 'links']]:
            SAY(visible=visible,
                display_message='/? Invalid command, perhaps you meant "ispl?" for "is playing?"',
                log_message=f'"ispl[aying]?" command assumed to be misspelled',
                log_priority=3)

        elif commandslist[0] == 'beta':
            if len(commandslist) == 1:
                IPrint(f'Beta features are switched {[_theme_colors.error, _theme_colors.prim][BETA_STATUS]}{["OFF", "ON"][BETA_STATUS]}{COLOR_RESET}', visible=visible)
            elif len(commandslist) == 2:
                if commandslist[1] == 'on':
                    print(f'Switched {_theme_colors.prim}> on <{COLOR_RESET} beta features')
                    BETA_STATUS = True
                elif commandslist[1] == 'off':
                    print(f'Switched {_theme_colors.error}> off <{COLOR_RESET} beta features')
                    BETA_STATUS = False
                else:
                    SAY(visible=visible,
                        display_message="Invalid beta command",
                        log_message="Invalid beta command",
                        log_priority=2)


        elif commandslist[0] == 'reload':
            include_dl_dir = True

            IPrint("Reloading sounds", visible=visible)

            if len(commandslist) in [2, 3]:
                possible_dl_exclusion_keywords_hyphenated = [
                    'exclude-dl', 
                    'exclude-dls',
                    'exclude-download',
                    'exclude-downloads'
                ]

                possible_dl_inclusion_keywords_hyphenated = [
                    'include-dl',
                    'include-dls',
                    'include-download',
                    'include-downloads'
                ]

                possible_dl_exclusion_keywords_space_sep = [
                    'exclude dl',
                    'exclude dls',
                    'exclude download',
                    'exclude downloads'
                ]

                possible_dl_inclusion_keywords_space_sep = [
                    'include dl',
                    'include dls',
                    'include download',
                    'include downloads'
                ]

                possible_dl_inclusion_keywords_concatenated = [
                    'includedl',
                    'includedls',
                    'includedownload',
                    'includedownloads'
                ]

                possible_dl_exclusion_keywords_concatenated = [
                    'excludedl',
                    'excludedls',
                    'excludedownload',
                    'excludedownloads'
                ]


                # print("'"+' '.join(commandslist[1:3])+"'")
                # print("'"+commandslist[1]+"'")

                if (
                        (' '.join(commandslist[1:3]) not in possible_dl_exclusion_keywords_space_sep and
                         ' '.join(commandslist[1:3]) not in possible_dl_inclusion_keywords_space_sep)
                         and
                        (commandslist[1] not in possible_dl_exclusion_keywords_hyphenated and
                         commandslist[1] not in possible_dl_inclusion_keywords_hyphenated and
                         commandslist[1] not in possible_dl_exclusion_keywords_concatenated and
                         commandslist[1] not in possible_dl_inclusion_keywords_concatenated)

                   ):
                    SAY(visible=visible,
                        display_message="Invalid keywords in reload command",
                        log_message="Invalid keywords in reload command",
                        log_priority=2)

                else:
                    include_dl_dir = not (commandslist[1] in possible_dl_exclusion_keywords_hyphenated or
                                          commandslist[1] in possible_dl_exclusion_keywords_concatenated or
                                          ' '.join(commandslist[1:3]) in possible_dl_exclusion_keywords_space_sep)


            elif len(commandslist) != 1:
                SAY(visible=visible,
                    display_message="Too many keywords in reload command",
                    log_message="Too many keywords in reload command",
                    log_priority=2)

            reload_sounds(quick_load=False, include_dl_dir=include_dl_dir)

            IPrint(f"Loaded {len(_local_sound_files)}", visible=visible)
            IPrint(f"Done", visible=visible)

        elif commandslist in [['hist'], ['history']]:
            path = 'logs/history.log'
            if sys.platform == 'win32': path=path.replace('/', '\\')
            else: path=path.replace('\\', '/')
            IPrint(f"Opening history log in explorer", visible=visible) # TODO: Change name from "explorer" to a neutral term for "file-explorer" for all OSs
            os.system(f'explorer /select, {path}')
            del path

        elif commandslist in [['hist', 'count'], ['history', 'count']]:
            hist_count = 0
            path = 'logs/history.log'

            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    hist_count = len(fp.readlines())

                if hist_count:
                    IPrint(f"History count: {hist_count}", visible=visible)
                else:
                    IPrint("No history has been recorded yet since the first time you opened the app", visible=visible)
            except Exception:
                SAY(visible=visible,
                    display_message="Error reading history file",
                    log_message="Error reading history file",
                    log_priority=2)
            

        elif commandslist in [['refresh'], ['refresh', 'all']]:
            if commandslist == ['refresh', 'all']:
                confirm_refresh = input("Confirm refresh all? (This will refresh data of your library files) (y/n): ").lower().strip()
                while confirm_refresh not in ['y', 'n', 'yes', 'no']:
                    confirm_refresh = input(f"{_theme_colors.error}[INVALID RESPONSE]{COLOR_RESET} Do you wish to confirm refresh? (y/n): ").lower().strip()

                if confirm_refresh in ['yes', 'y']:
                    IPrint("Reloading settings (1/4)", visible=visible)
                    refresh_settings()
                    _theme_colors = theme_colors(SETTINGS)

                    IPrint("Refreshing lyrics  (2/4)", visible=visible)
                    purge_old_lyrics_if_exist()
                    lyrics_saved_for_song = False
                    lyrics_ops(show_window=False)

                    IPrint("Reloading sounds   (3/4)", visible=visible)
                    reload_sounds(quick_load = False)
                    IPrint(f"  > Loaded {len(_local_sound_files)} sounds", visible=visible)

                    IPrint("Spawned meta getter background process (4/4)", visible=visible)
                    sp.Popen([sys.executable, 'meta_getter.py', str(supported_file_types)], shell=True)

                    IPrint("Done", visible=visible)

            else:
                IPrint("Reloading settings (1/3)", visible=visible)
                refresh_settings()

                IPrint("Refreshing lyrics  (2/3)", visible=visible)
                purge_old_lyrics_if_exist()
                lyrics_saved_for_song = False
                lyrics_ops(show_window=False)

                IPrint("Reloading sounds   (3/3)", visible=visible)
                reload_sounds(quick_load = False)
                IPrint(f"  > Loaded {len(_local_sound_files)} sounds", visible=visible)

                IPrint("Done", visible=visible)

        elif commandslist in [['refresh', 'lyrics'], ['refresh', 'lyr']]:
            if device_is_connected():
                IPrint("Refreshing lyrics...", visible=visible)
                purge_old_lyrics_if_exist()
                lyrics_saved_for_song = False
                lyrics_ops(show_window=False)

                IPrint("Done", visible=visible)

        elif commandslist == ['vis']:
            visible = not visible
            IPrint('visibility on', visible=visible)

        elif commandslist[0] in ['prev', '.prev', '-', '.-', 'next', '.next', '+', '.+']:
            valid_song_index_for_offsetting = False

            if current_media_type is None: # offline/local player currently active
                offset = None
                if songindex != -1: # Some song is loaded (Not stopped)
                    # if songindex == None: # Streaming offline song from custom path
                #         if RECENTS_QUEUE != []:
                #             valid_song_index_for_offsetting = True

                #     if valid_song_index_for_offsetting: pass
                    if len(commandslist) == 1: # default to 1 audio skip
                        offset = 1
                    elif len(commandslist) > 1:
                        if commandslist[1].isnumeric():
                            if int(commandslist[1]) != 0:
                                # number of audios to be skipped is provided by the user
                                # store offset as either +ve for fwd skip (next)
                                # or                     -ve for bwd seeks (prev)
                                offset = int(commandslist[1])
                            else:
                                SAY(visible=visible,
                                    display_message = 'Provided 0 audios to skip. Not allowed',
                                    log_message = 'Number of audios to skip was 0',
                                    log_priority = 2)
                        else:
                            SAY(visible=visible,
                                display_message = 'Number of audios to skip must be a positive integer',
                                log_message = 'Number of audios to skip wasn not a valid +ve int',
                                log_priority = 2)

                    if offset:
                        if commandslist[0] in ['prev', '.prev', '-', '.-']: offset *= -1
                        offsetted_index = songindex + offset
                        if offsetted_index in range(1, len(_local_sound_files)+1): # is some audio track found at the offsetted index?
                            if commandslist[0][0] == '.':
                                local_play_commands(commandslist=[None, str(offsetted_index)])
                            else:
                                IPrint(f"@{commandslist[0][0]}"+str(offset)*(offset!=1)+ f" {_theme_colors.exit_prompt}{offsetted_index}{colored.fg('aquamarine_3')} | {_local_sound_files_names_only[offsetted_index-1]}{COLOR_RESET}", visible=visible)
                        else:
                            if offset > 0:
                                if offsetted_index == 1:
                                    offset_err_disp_msg = 'Cannot skip backward as you have reached beginning of library'
                                    offset_err_log_msg = 'Reached beginning of library, cannot skip bwd'
                                else:
                                    offset_err_disp_msg = f'Number of audios to skip forward was too large, try "next" command with <= {len(_local_sound_files)-songindex} skips'
                                    offset_err_log_msg = 'Reached upper bound of index in library when skipping fwd'
                            else:
                                if offsetted_index == len(_local_sound_files_names_only):
                                    offset_err_disp_msg = 'Cannot skip forward as you have reached end of library'
                                    offset_err_log_msg = 'Reached end of library, cannot skip fwd'
                                else:
                                    offset_err_disp_msg = f'Number of audios to skip backward was too large, try "prev" command with <= {songindex-1} skips'
                                    offset_err_log_msg = 'Reached index 0 in library when skipping bwd'

                            SAY(visible=visible,
                                display_message = offset_err_disp_msg,
                                log_message = offset_err_log_msg,
                                log_priority = 2)

                # TODO: Reconsider below 2 ifs...
                if not valid_song_index_for_offsetting:
                    if songindex == -1:
                        SAY(visible=visible,
                            display_message = 'Cannot skip. No audio is currently playing',
                            log_message = 'Cannot skip when no audio is playing',
                            log_priority = 2)
                    if songindex is None:
                        IPrint(current_song_name(pretty_display=False), visible=visible*ISDEV)
                        IPrint(current_media_type, visible=visible*ISDEV)
                    #     SAY(visible=visible,
                    #         display_message = 'Cannot skip audios when playing individual audio files outside of your music library',
                    #         log_message = 'Cannot skip when playing explicit filepaths outside library',
                    #         log_priority = 2)

        elif commandslist in [['.'], ['now']]:
            if reloaded_index() == None:
                SAY(visible=visible,
                    display_message = 'Currently playing song has been unloaded from library',
                    log_message = 'Currently playing song has been unloaded from library',
                    log_priority = 3)

            current_song_name(detailed_output = False)

        elif commandslist in [['.*'], ['now*']]:
            if reloaded_index() == None:
                SAY(visible=visible,
                    display_message = 'Currently playing song has been unloaded from library',
                    log_message = 'Currently playing song has been unloaded from library',
                    log_priority = 3)
            current_song_name()

        elif commandslist[0].lower() == 'play':
            local_play_commands(commandslist=commandslist)

        if len(commandslist) == 2:
            if commandslist[1] == 'device':
                device_kind = None
                if commandslist[0] in ['output', 'input']:
                    device_kind = commandslist[0]
                elif commandslist[0] in ['out', 'in']:
                    device_kind = commandslist[0]+'put'

                if device_kind:
                    if sounddevice._initialized: sounddevice._terminate()
                    if not sounddevice._initialized: sounddevice._initialize()
                    if device_name := sounddevice.query_devices(kind = device_kind).get('name'):
                        IPrint(f"{colored.fg('navajo_white_1')}{device_kind} device: {COLOR_RESET}{device_name}", visible=visible)

        if commandslist[:2] in [['fade', 'in'], ['fade', 'out']]:
            try:
                """
                fade in  --> fade_type = 0
                fade out --> fade_type = 1
                """

                fade_type=(['in', 'out'].index(commandslist[1]))
                if len(commandslist) == 2:
                    fade_in_out(fade_type=fade_type)

                elif len(commandslist) == 3:
                    if isdecimal(commandslist[2]):
                        fade_duration = float(commandslist[2])
                        fade_in_out(fade_type=fade_type, fade_duration=fade_duration)

                    else:
                        SAY(visible=visible,
                            display_message='Fade duration must be a valid integer',
                            log_message='Fade duration is not a valid integer',
                            log_priority=2)

                else:
                    SAY(visible=visible,
                        display_message='Invalid use of fade command. Need to specify a single integer for fade duration',
                        log_message='Invalid use of fade in/out',
                        log_priority=2)

            except Exception:
                SAY(visible=visible,
                    display_message='Failed to fade in/out',
                    log_message='Failed to fade in/out',
                    log_priority=2)

        elif commandslist[0] in ['fade']:
            """
            Sample usage:
                Fade from current volume to 30% in 3 seconds -> fade to 30 in 3
                Fade from 20% to current volume in 2 seconds -> fade from 20 in 2
                Fade from 20% to 30% in 3 seconds            -> fade from 20 to 30 in 3
                Fade from 100% to 2% in 5 seconds (default)  -> fade from 100 to 2
            """

            if commandslist.count('from') == 0:
                initvol = cached_volume
            elif commandslist.count('from') == 1:
                _from_index = commandslist.index('from')
                if isdecimal(commandslist[_from_index+1]):
                    initvol = float(commandslist[_from_index+1])
                    initvol = initvol/100
                else:
                    SAY(visible=visible,
                        display_message = 'Invalid initial volume provided. Must be between 0 and 500',
                        log_message = 'Invalid initial volume provided',
                        log_priority = 2)
            elif commandslist.count('from') > 1:
                SAY(visible=visible,
                    display_message = 'Invalid fade command syntax (check initial volume)',
                    log_message = 'Invalid fade command syntax (initial volume)',
                    log_priority = 2)


            if commandslist.count('to') == 1:
                _to_index = commandslist.index('to')
                if isdecimal(commandslist[_to_index+1]):
                    finalvol = float(commandslist[_to_index+1])
                    finalvol = finalvol/100
                else:
                    SAY(visible=visible,
                        display_message = 'Invalid final volume provided. Must be between 0 and 500',
                        log_message = 'Invalid initial volume provided',
                        log_priority = 2)
            else:
                SAY(visible=visible,
                    display_message = 'Invalid fade command syntax (check final volume)',
                    log_message = 'Invalid fade command syntax (final volume)',
                    log_priority = 2)


            if commandslist.count('in') == 0:
                fade_duration = 5
            if commandslist.count('in') == 1:
                _in_index = commandslist.index('in')
                if isdecimal(commandslist[_in_index+1]):
                    fade_duration = float(commandslist[_in_index+1])
                else:
                    SAY(visible=visible,
                        display_message = 'Invalid final volume provided. Must be between 0 and 100',
                        log_message = 'Invalid initial volume provided',
                        log_priority = 2)

            elif commandslist.count('in') > 1:
                SAY(visible=visible,
                    display_message = 'Invalid fade command syntax (check duration)',
                    log_message = 'Invalid fade command syntax (duration)',
                    log_priority = 2)

            if len(commandslist) in range(3, 8):
                fade_in_out(initvol=initvol,
                            finalvol=finalvol,
                            fade_type=isplaying,
                            fade_duration=fade_duration)
            else:
                # TODO: Add exception handling with the `SAY` func
                raise Exception

        elif commandslist[0].lower() in ['m?', 'ism?', 'ismute?']:
            # TODO: - Make more reliable...?
            IPrint(int(ismuted), visible=visible)

        elif commandslist[0].lower() in ['isp?', 'ispl', 'isp']:
            SAY(visible=visible,
                display_message='/? Invalid command, perhaps you meant "ispl?" for "is playing?"',
                log_message='"ispl[aying]?" command assumed to be misspelled',
                log_priority=3)

        elif commandslist[0].lower() in ['ispl?', 'isplaying?']:
            # TODO: - Make more reliable...?
            IPrint(int(isplaying), visible=visible)

        elif commandslist[0].lower() in ['isl?', 'isloaded?']:
            # TODO: - Make more reliable...?
            if current_media_type is not None:
                IPrint(vas.vlc.media, visible=visible)
            IPrint(int(bool(currentsong)), visible=visible)

        elif commandslist[0].lower() == 'seek':
            if currentsong_length:
                if len(commandslist) == 2:
                    rawtime = None

                    if commandslist[1].startswith('+'):
                        if commandslist[1][1:].isdigit():
                            rawtime = str(int(get_current_progress()) + int(commandslist[1][1:]))

                    elif commandslist[1].startswith('-'):
                        if commandslist[1][1:].isdigit():
                            rawtime = str(int(get_current_progress()) - int(commandslist[1][1:]))

                    else:
                        rawtime = commandslist[1]
    
                    time_validity = validate_time(rawtime)

                    if not time_validity: # Raw time is valid
                        # Take a valid raw value for time from the user. Format is defined in the "seek" section of help
                        timeobj = timeinput_to_timeobj(rawtime)
                        if timeobj != ValueError:
                            if timeobj == (None, None):
                                SAY(visible=visible,
                                    display_message = 'Internal Error',
                                    log_message = 'Invalid time format: Invalid time object',
                                    log_priority = 2)
                            else:
                                _ = song_seek(timeval=timeobj[1])
                                if _:
                                    IPrint(f"Seeking to: {timeobj[0]}", visible=visible)

                        # TODO: - Make following error messages more meaningful by giving them more
                        # context depending on if absolute or relative seek was called...
                        
                        # E.g. say "reached beginning" instead of "seek val can't be -ve"
                        # When using relative seek

                        else:
                            SAY(visible=visible,
                                display_message="Error: Seek value too large for this audio",
                                log_message=f'Seek value too large for: {currentsong}',
                                log_priority=2)
                    elif time_validity == 1:
                        SAY(visible=visible,
                            display_message="Error: Seek value can't have a decimal point",
                            log_message=f'Seek value floating point for: {currentsong}',
                            log_priority=2)
                    elif time_validity == 2:
                        SAY(visible=visible,
                            display_message="Error: Seek value must be numeric",
                            log_message=f'Seek value non numeric for: {currentsong}',
                            log_priority=2)
                    elif time_validity == 3:
                        SAY(visible=visible,
                            display_message="Error: Seek value can't be negative",
                            log_message=f'Seek value negative for: {currentsong}',
                            log_priority=2)
                    else:
                        pass

                else:
                    SAY(visible=visible,
                        display_message="Error: Invalid Seek value",
                        log_message=f'Seek value invalid for: {currentsong}',
                        log_priority=2)

            else:
                if currentsong_length == -1:
                    SAY(visible=visible,
                        display_message="Error: Can't seek audio, as audio length could not be loaded",
                        log_message=f'Song length could not be loaded, cannot seek',
                        log_priority=2)
                else:
                    SAY(visible=visible,
                        display_message="Error: No audio to seek",
                        log_message=f'Seeked audio w/o playing any',
                        log_priority=2)

        # TODO: Complete this command 
        # TODO: Remove this entire elif check
        elif commandslist[0] == 'check_dev':
            print(current_song_name())

        elif commandslist in [['prog'], ['progress'], ['prog*'], ['progress*']]:
            if currentsong:
                if currentsong_length:
                    cur_len = currentsong_length
                else:
                    cur_len = get_currentsong_length()

                if cur_len != -1:
                    cur_prog = get_current_progress()

                    prog_sep = f"{colored.fg('green_1')}|{COLOR_RESET}"
                    prog_div = f"{colored.fg('navajo_white_1')}\u2014{COLOR_RESET}"

                    if commandslist[0].endswith('*'):
                        IPrint(f"elapsed: {colored.fg('deep_pink_1a')}{convert(round(cur_prog))} {prog_div} {colored.fg('deep_pink_1a')}{convert(round(cur_len))}"
                               f" {prog_sep} {COLOR_RESET}remaining: {_theme_colors.prim}{convert(round(cur_len-cur_prog))}"
                               f" {prog_sep} {COLOR_RESET}progress: {colored.fg('light_goldenrod_1')}{round(cur_prog/cur_len*100)}%", visible=visible)
                    else:
                        # IPrint(f"{colored.fg('deep_pink_1a')}{convert(round(cur_prog))}/{convert(round(cur_len))}", visible=visible)
                        IPrint(f"{colored.fg('deep_pink_1a')}{round(cur_prog)} {prog_div} {colored.fg('deep_pink_1a')}{round(cur_len)}"
                               f" {prog_sep} {_theme_colors.prim}{round(cur_len-cur_prog)}"
                               f" {prog_sep} {colored.fg('light_goldenrod_1')}{round(cur_prog/cur_len*100)}%", visible=visible)

                else:
                    SAY(visible=visible,
                        display_message = f'Progress cannot be displayed for audio of unknown length',
                        log_message = 'Progress undefined for audio of unknown length',
                        log_priority = 2)

            else:            
                SAY(visible=visible,
                    display_message = f'ERROR: Progress cannot be displayed, no audio is playing',
                    log_message = 'Progress undefined when no audio is playing',
                    log_priority = 2)

        elif '-' in commandslist[0].lower():
            if commandslist[0].lower().split('-')[0] in ['donwload', 'downlaod', 'donwlaod', 'donload', 'donlaod']:
                SAY(visible=visible,
                    display_message=f'/? Invalid command, perhaps you meant one of:\n'
                    f'  {colored.fg("magenta_3a")}download-yv:{colored.fg("light_sky_blue_1")} Download YouTube video\n'
                    f'  {colored.fg("magenta_3a")}download-ya:{colored.fg("light_sky_blue_1")} Download YouTube audio\n'
                    f'  {colored.fg("magenta_3a")}download-ml:{colored.fg("light_sky_blue_1")} Download custom media link'
                    f'{colored.attr("reset")}\n',
                    log_message=f'"download-(\'ys\'|\'yv\'|\'ml\')" command assumed to be misspelled', log_priority=3)

        if commandslist[0].lower() in ['download',  'download-yt',  'download-au',  'download-a',
                                         '/download', '/download-yt', '/download-au', '/download-a']:
            SAY(visible=visible,
                display_message=f'/? Invalid command, perhaps you meant one of:\n'
                f'  {colored.fg("magenta_3a")}download-yv:{colored.fg("light_sky_blue_1")} Download YouTube video\n'
                f'  {colored.fg("magenta_3a")}download-ya:{colored.fg("light_sky_blue_1")} Download YouTube audio\n'
                f'  {colored.fg("magenta_3a")}download-ml:{colored.fg("light_sky_blue_1")} Download custom media link'
                f'{colored.attr("reset")}\n',
                log_message=f'"download-(\'ys\'|\'yv\'|\'ml\')" command assumed to be misspelled', log_priority=3)


        # Download current/custom YouTube media (as video with audio)
        elif commandslist[0].lower() in ['download-yv', 'dl-yv']:
            if device_is_connected():
                # TODO: - Add way for user to customize download settings...
                continue_dl = False
                confirm_dl = False
                url = None

                if len(commandslist) == 1: # Download current/custom YouTube media
                    if current_media_type is None:
                        SAY(visible=visible,
                            log_message='Cannot download locally available audios',
                            display_message='Whoops! Looks like you\'re trying to download a audio already present in your local storage',
                            log_priority = 3)

                    else:
                        if currentsong is not None:
                            url = currentsong[1]
                            continue_dl = True
                        else:
                            url = None
                            IPrint("No audio currently playing", visible=visible)

                elif len(commandslist) == 2:
                    url = commandslist[1]
                    media_url_is_valid = url_is_valid(url = url)
                    if media_url_is_valid:
                        IPrint('Attempting to download YouTube video from:\n  '
                            f'{colored.fg("sandy_brown")}@{colored.fg("orchid_2")}{url}{colored.attr("reset")}',
                            visible=visible)
                        continue_dl = True
                    elif not url_error_handle(media_url_is_valid):
                            SAY(visible=visible,
                                log_message=f'Invalid YouTube URL for video download: {url}',
                                display_message=f'Invalid YouTube URL for video download: {url}',
                                log_priority = 3)

                if len(commandslist) in [1, 2] and url:
                    download_parmeters = {
                        "SETTINGS": SETTINGS,
                        "SYSTEM_SETTINGS": SYSTEM_SETTINGS,
                        "media_urls": url,
                        "typ": 1,
                        "quality": None,
                        "make_separate_mariana_dl_dir": None,
                        "dry_run": False,
                    }

                    if continue_dl:
                        confirm_dl = input("Do you want to confirm VIDEO download? (y/n): ").lower().strip()
                        while confirm_dl not in ['y', 'n', 'yes', 'no']:
                            confirm_dl = input("[INVALID RESPONSE] Do you want to confirm VIDEO download? (y/n): ").lower().strip()

                        if confirm_dl in ['yes', 'y']:
                            confirm_dl = True
                        else:
                            confirm_dl = False
                    
                    if confirm_dl:
                        SAY(visible=visible,
                            log_message='Download confirmed and initiated',
                            display_message='Your download has started',
                            log_priority = 3)
                        sp.Popen([sys.executable, 'beta/mediadl.py', json.dumps(download_parmeters)], shell=True)

        elif commandslist[0].lower() in ['download-ya', 'dl-ya']:
            if device_is_connected():
                # TODO: - Add way for user to customize download settings...
                continue_dl = False
                confirm_dl = False
                url = None

                if len(commandslist) == 1: # Download current/custom YouTube media
                    if current_media_type is None:
                        SAY(visible=visible,
                            log_message='Cannot download locally available audios',
                            display_message='Whoops! Looks like you\'re trying to download a audio already present in your local storage',
                            log_priority = 3)

                    else:
                        if currentsong is not None:
                            url = currentsong[1]
                            continue_dl = True
                        else:
                            url = None
                            IPrint("No audio currently playing", visible=visible)

                elif len(commandslist) == 2:
                    url = commandslist[1]
                    download_ya_is_valid = url_is_valid(url = url)
                    if download_ya_is_valid:
                        IPrint('Attempting to download YouTube audio from:\n  '
                            f'{colored.fg("sandy_brown")}@{colored.fg("orchid_2")}{url}{colored.attr("reset")}',
                            visible=visible)
                        continue_dl = True
                    elif not url_error_handle(download_ya_is_valid):
                        SAY(visible=visible,
                            log_message=f'Invalid YouTube URL for audio download: {url}',
                            display_message=f'Invalid YouTube URL for video download: {url}',
                            log_priority = 3)

                if len(commandslist) in [1, 2] and url:
                    download_parmeters = {
                        "SETTINGS": SETTINGS,
                        "SYSTEM_SETTINGS": SYSTEM_SETTINGS,
                        "media_urls": url,
                        "typ": 0,
                        "quality": None,
                        "make_separate_mariana_dl_dir": None,
                        "dry_run": False,
                    }

                    if continue_dl:
                        confirm_dl = input("Do you want to confirm AUDIO download? (y/n): ").lower().strip()
                        while confirm_dl not in ['y', 'n', 'yes', 'no']:
                            confirm_dl = input("[INVALID RESPONSE] Do you want to confirm AUDIO download? (y/n): ").lower().strip()

                        if confirm_dl in ['yes', 'y']:
                            confirm_dl = True
                        else:
                            confirm_dl = False
                    
                    if confirm_dl:
                        SAY(visible=visible,
                            log_message='Download confirmed and initiated',
                            display_message='Your download has started',
                            log_priority = 3)
                        sp.Popen([sys.executable, 'beta/mediadl.py', json.dumps(download_parmeters)], shell=True)

        elif commandslist[0].lower() == 'download-ml':
            pass

        elif commandslist == ['t']:
            IPrint(convert(get_current_progress()), visible=visible)

        # TODO: - Add interactive help commands (similar to the following for rand command)
        # with syntax ?<command-name> ...
        # elif commandslist == ['? rand']:  # Random comand help
        #     IPrint("", visible=visible)

        # If any random command is issued as it's arand variant
        # then random indices are repeated (within same session)
        # however, regular random commands never repeat indices (within same session)

        elif commandslist in [['.rand'], ['.arand']]:  # Play random audio
            rand_song_index = rand_song_index_generate(no_repeat=commandslist=='.rand')
            if rand_song_index:
                local_play_commands(commandslist=[None, str(rand_song_index)])

        elif commandslist in [['=rand'], ['=arand']]:  # Print random audio number
            rand_song_index = rand_song_index_generate(no_repeat=commandslist=='=rand')
            if rand_song_index:
                IPrint(rand_song_index, visible=visible)

        elif commandslist in [['rand'], ['arand']]:  # Print random audio name
            rand_song_index = rand_song_index_generate(no_repeat=commandslist=='rand')
            if rand_song_index:
                IPrint(_local_sound_files_names_only[rand_song_index], visible=visible)

        elif commandslist in [['rand*'], ['arand*']]:  # Print random audio path
            rand_song_index = rand_song_index_generate(no_repeat=commandslist=='rand*')
            if rand_song_index:
                IPrint(f"{rand_song_index+1}: {_local_sound_files[rand_song_index]}", visible=visible)

        elif commandslist in [['/rand'], ['/arand']]:
            rand_song_index = rand_song_index_generate(commandslist=='/rand')
            if rand_song_index:
                IPrint(f"{rand_song_index+1}: {_local_sound_files_names_only[rand_song_index]}", visible=visible)

        elif commandslist == ['reset']:
            if currentsong_length and currentsong_length != -1:
                try:
                    song_seek('0')
                except Exception:
                    SAY(visible=visible,
                        display_message="Error: Can't reset this audio",
                        log_message=f'Error in resetting: {currentsong}',
                        log_priority=2)
            else:
                SAY(visible=visible,
                    display_message="Error: No audio to seek",
                    log_message=f'Seeked audio w/o playing any',
                    log_priority=2)

        # The multifunctional dot subcommands (can be used as the first character of multiple commands)
        elif command[0] == '.':
            try:
                # Play by index
                if len(commandslist) == 1:
                    # Get info of currently loaded audio and display pleasantly...
                    # The info params displayed depend on those specified in the settings...
                    # getstats() # TODO: - Make such a function...???
                    if commandslist[0][1:].isnumeric():
                        local_play_commands(commandslist=[None, ''.join(commandslist[0][1:])])

                # Play/find by path
                elif command.startswith('. '):
                    # Find if path is a valid supported media file
                    path = ' '.join(commandslist[1:])
                    if os.path.isfile(path):
                        if os.path.splitext(path)[1] in supported_file_types:
                            IPrint(1, visible=visible)
                        else:
                            IPrint(0, visible=visible)
                    else:
                        IPrint(0, visible=visible)

                elif command.startswith('.'):
                    # Play media by path
                    if os.path.isfile(command.strip()[1:]):
                        local_play_commands(commandslist=[None, command[1:]],
                                            _command=command)

            except Exception:
                raise

        elif commandslist in [['clear'], ['cls']]:
            os.system('cls' if os.name == 'nt' else 'clear')
            if visible: showbanner()

        elif commandslist == ['p']:
            playpausetoggle()

        elif commandslist == ['ph']:
            playpausetoggle(softtoggle=False)

        # TODO: Refactor to replace two `SAY` funcs with one
        # Display song by index
        elif commandslist[0].isnumeric():  # Check if only a number is entered
            # global _local_sound_files
            if len(commandslist) == 1:
                valid_song_index_provided = False
                song_index_entered = int(commandslist[0])
                if song_index_entered > 0:
                    if song_index_entered <= len(_local_sound_files):
                        if os.path.isfile(_local_sound_files[(song_index_entered)-1]):
                            with contextlib.suppress(IndexError):
                                IPrint(colored.fg('aquamarine_3')+\
                                    f'@{song_index_entered}'+\
                                    _theme_colors.prim+\
                                    ' | '+\
                                    colored.fg('medium_orchid_1a')+\
                                    _local_sound_files_names_only[(song_index_entered)-1]+\
                                    COLOR_RESET, visible=visible)
                                valid_song_index_provided = True
                        else:
                            valid_song_index_provided = True
                            SAY(visible = visible,
                                display_message = 'Song at the specified index does not exist or has been removed from disk',
                                log_message = 'Song at the specified index does not exist or has been removed from disk',
                                log_priority = 2)

                    else:
                        valid_song_index_provided = True
                        SAY(visible = visible,
                            display_message = 'Song at the specified index does not exist or has been removed from disk',
                            log_message = 'Song at the specified index does not exist or has been removed from disk',
                            log_priority = 2)

                if not valid_song_index_provided:
                    SAY(visible = visible,
                        display_message = f'Please input audio number between 1 and {len(_local_sound_files)}',
                        log_message = 'Invalid song index provided for listing name',
                        log_priority = 2)

        elif commandslist in [['count'], ['howmany'], ['total']]:
            IPrint(len(_local_sound_files_names_only), visible=visible)

        elif commandslist[0] == 'weblinks':
            # TODO: Recollect what this feature was...
            # (...and make it...?)
            print(f'Weblinks feature is still in progress... The developer {colored.fg("magenta_3a")}@{SYSTEM_SETTINGS["about"]["author"]}{colored.attr("reset")} will add this feature shortly...')

        if commandslist[0] == 'open':
            if commandslist == ['open']:
                if currentsong and current_media_type is None:
                    if os.path.isfile(currentsong):
                        if os.path.splitext(currentsong)[1] in supported_file_types:
                            if sys.platform == 'win32':
                                currentsong=currentsong.replace('/', '\\')
                                IPrint(f"Opening currently playing audio: {currentsong}", visible=visible)
                                os.system(f'explorer /select, {currentsong}')
                            else:
                                currentsong=currentsong.replace('\\', '/')
                        else:
                            IPrint(0, visible=visible)
                    else:
                        IPrint(0, visible=visible)
                else:
                    if current_media_type is not None: # VLC
                        if current_media_type == 0:
                            webbrowser.open(f"{currentsong[1]}&t={int(get_current_progress())}s")
                        elif current_media_type == 1:
                            webbrowser.open(currentsong)
                        elif current_media_type == 2:
                            webbrowser.open(f"https://s2-webradio.antenne.de/{currentsong}")
                        elif current_media_type == 3:
                            webbrowser.open(currentsong[1])
                        else:
                            SAY(visible=visible,
                                display_message = '',
                                log_message = 'Received invalid type for current media',
                                log_priority = 2,
                                format_style = 1)
                    else:
                        SAY(visible=visible,
                            display_message = "No audio playing, no file selected to open",
                            log_message = "No audio playing, no file selected to open",
                            log_priority = 2)

            elif len(commandslist) > 1 and commandslist[1] in ['lib', 'library']:
                IPrint(fr'Opening library file in editor', visible=visible)
                if not DEFAULT_EDITOR:
                    restore_default.restore('editor path', SETTINGS)
                    DEFAULT_EDITOR = SETTINGS.get('editor path')

                sp.Popen([fr"{DEFAULT_EDITOR}", 'lib.lib'], shell = True)

            elif len(commandslist) > 1 and commandslist[1] in ['lyr', 'lyrics']:
                IPrint(fr'Opening lyrics file in editor', visible=visible)
                lyrics_ops(show_window = False)
                if not DEFAULT_EDITOR:
                    restore_default.restore('editor path', SETTINGS)
                    DEFAULT_EDITOR = SETTINGS.get('editor path')

                if os.path.isfile('temp/lyrics.txt'):
                    sp.Popen([fr"{DEFAULT_EDITOR}", 'temp/lyrics.txt'], shell = True)
                else:
                    SAY(visible=visible,
                        log_message = 'No lyrics available to view',
                        display_message = 'No lyrics available to view',
                        log_priority = 2)

            elif len(commandslist) > 1 and commandslist[1] in ['hist', 'history']:
                IPrint(fr'Opening history log file in editor', visible=visible)
                lyrics_ops(show_window = False)
                if not DEFAULT_EDITOR:
                    restore_default.restore('editor path', SETTINGS)
                    DEFAULT_EDITOR = SETTINGS.get('editor path')

                path = 'logs/history.log'
                if os.path.isfile(path):
                    sp.Popen([fr"{DEFAULT_EDITOR}", path], shell = True)
                else:
                    SAY(visible=visible,
                        log_message = 'No history file available to view',
                        display_message = 'No history file available to view',
                        log_priority = 2)
                del path

            else:
                if len(commandslist) == 2 and commandslist[1].isnumeric():
                    user_entered_song_index = int(commandslist[1])-1
                    if user_entered_song_index in range(len(_local_sound_files_names_only)):
                        path = _local_sound_files[user_entered_song_index]
                        if sys.platform == 'win32': path=path.replace('/', '\\')
                        else: path=path.replace('\\', '/')
                        IPrint(f"Opening audio at index {user_entered_song_index+1}: {_local_sound_files_names_only[user_entered_song_index]}", visible=visible)
                        os.system(f'explorer /select, {_local_sound_files[user_entered_song_index]}')
                else:
                    path = ' '.join(commandslist[1:])
                    if os.path.isfile(path):
                        if os.path.splitext(path)[1] in supported_file_types:
                            if sys.platform == 'win32': path=path.replace('/', '\\')
                            else: path=path.replace('\\', '/')
                            IPrint(f"Opening audio via path at: {path}", visible=visible)
                            os.system(f'explorer /select, {path}')
                        else:
                            SAY(visible=visible,
                                display_message = 'File type is unsupported, file existence cannot be guaranteed. (Will always be shown as 0)',
                                log_message = 'Existence of file of unsupported type cannot be guaranteed, will show as 0',
                                log_priority = 2)
                            IPrint(0, visible=visible)
                    else:
                        IPrint(0, visible=visible)

        elif commandslist in [['sm'], ['sync'], ['sync', 'media']]:
            if device_is_connected():
                IPrint("Syncing current media...", visible=visible)
                if current_media_type == 0: # If YT vid is playing...
                    IPrint(f"YouTube audio cannot be synced, only seeked", visible=visible)
                elif current_media_type == 1: # If audio is playing...
                    IPrint(f"media url cannot be synced, only seeked", visible=visible)
                elif current_media_type == 2: # If radio is playing...
                    vas.media_player(action='resync') # Resync radio to live stream
                elif current_media_type == 3: # If reddit-session is streaming...
                    # TODO: - Find a way to get the current stream timestamp of current RPAN session
                    print(f'Reddit session sync: The developer {colored.fg("magenta_3a")}@{SYSTEM_SETTINGS["about"]["author"]}{colored.attr("reset")} will add this feature shortly...')

        elif commandslist[0] == 'path':
            def display_current_song_path():
                if currentsong and current_media_type is None:
                    IPrint(f":: {colored.fg('plum_1')}{currentsong}{COLOR_RESET}", visible=visible)
                else:
                    IPrint(f"{_theme_colors.exit_statement}({_theme_colors.sec}Not Playing{_theme_colors.exit_statement}){COLOR_RESET}", visible=visible)

            if len(commandslist) == 1:
                display_current_song_path()

            elif len(commandslist) == 2:
                if commandslist[1].isdigit():
                    if int(commandslist[1]) > 0:
                        try:
                            IPrint(_local_sound_files[int(commandslist[1])-1], visible=visible)
                        except IndexError:
                            SAY(visible=visible,
                                display_message = f'Please input audio number between 1 and {len(_local_sound_files)}',
                                log_message = 'Invalid song index provided for listing name',
                                log_priority = 2)
                    else:
                        SAY(visible=visible,
                            display_message = f'Please input audio number between 1 and {len(_local_sound_files)}',
                            log_message = 'Invalid song index provided for listing name',
                            log_priority = 2)

                elif commandslist[1] == '.':
                    display_current_song_path()

                else:
                    SAY(visible=visible,
                        display_message = f'Invalid input for an audio number',
                        log_message = 'Invalid song index provided for listing name',
                        log_priority = 2)


        elif commandslist[0].lower() in ['find', 'f', 'rfind', 'rf', 'lfind', 'lf',
                                         '.find', '.f', '.rfind', '.rf', '.lfind', '.lf',
                                         '/find', '/f', '/rfind', '/rf', '/lfind', '/lf']:
            # The 'r' in "rf" and "rfind" stand for "raw" find
            # i.e. they do not smart search, but search for all queries as strings 
            # even if they are numeric... 
            #  
            # However, if you want the "find" command to smartly identify a number as the number of songs starting from the 1st index, 
            # you are better off using the regular f[ind] command
        
            # display_search_result_table = True

            play_from_results = 0 # Do NOT play song from results directly
            limited_result_count_search = False # Shows only first n results where n is entered by user
                                         # To disable this, use the rawfind command "rf[ind]"

            if len(commandslist) > 1:
                myquery = commandslist[1:]

                # Valid combinations of commands with raw-find are (. | /)[r]f[ind]
                #    Some valid commands are:
                #      ".rfind", ".find", "/rfind"
                #    Some invalid commands are:
                #      "r.find", "find.", "rfind.", "r/find"

                if commandslist[0][0] in ['r', '.', '/']:
                    with contextlib.suppress(ValueError): # If ValueError arises, we know that a raw search command has been issued
                        play_from_results = ['.', '/'].index(commandslist[0][0])+1

                else:
                    if commandslist[-1].isnumeric():
                        myquery = myquery[:-1]
                        limited_result_count_search = True

                search_type = 0
                """
                search_type:
                    # Already implemented
                    rf -> search for nums in song name (try to also get result count)
                    f -> ...
                    .f -> play first search result
                    /f -> play random from search result

                    # TODO: Implement the following search rules/params/settings
                    lf -> loose-find: if atleast one query term is in results or the result is a subset of or is equal to the entire query
                    0 -> normal
                    1 -> -fav
                    2 -> +bl
                    3 -> +bl,-fav or -fav,+bl
                """
                searchresults = searchsongs(queryitems=myquery,
                                            play_from_results=play_from_results,
                                            search_type=search_type)

                # The following command is inefficient, as it first collects all rsesults
                # and then displays the first x results (x is given by the user)
                # instead of only searching for the first x items and displaying all those items...
                #
                # TODO: Make reduced serch more efficient, by only searching for x items when asked...
                if limited_result_count_search:
                    searchresults = searchresults[:int(commandslist[-1])]

                if searchresults == []: # No search results (OR play first is true)
                    IPrint(f"{_theme_colors.error} -- No results found -- {COLOR_RESET}", visible=visible)
                else:
                    if play_from_results == 1:
                        # play first song from search results
                        local_play_commands(["play", str(searchresults[0])])

                    elif play_from_results == 2:
                        # play random song from results if play_from_results == 2
                        # else do NOT play from search results...
                        local_play_commands(["play", str(rand.choices(searchresults)[0][0])])

                    else:
                        found_display_string_1 = f"{_theme_colors.prim}Found"
                        found_display_string_2 = f"{[_theme_colors.sec if len(searchresults)-1 else _theme_colors.tert][0]}"\
                                                 f"{len(searchresults)}{_theme_colors.prim}"
                        found_display_string_3 = f"match{('es')*(len(searchresults)>1)} for:"
                        found_display_string_4 = f"{[_theme_colors.sec if len(searchresults)-1 else _theme_colors.tert][0]}{colored.style.UNDERLINED}{' '.join(myquery)}{COLOR_RESET}{NBSP}"

                        display_table = tbl([(i, text_overflow_prettify(text=j, length_thresh=100)) for i, j in searchresults],
                                            tablefmt='pretty',
                                            headers=('#', 'Song'),
                                            colalign=('center', 'left'))

                        if BETA_STATUS:
                            display_table_formatted_sections = display_table.splitlines()
                            current_song_index_in_search_results = None

                            if songindex != -1:
                                with contextlib.suppress(StopIteration):
                                    current_song_index_in_search_results = searchresults.index(next(x for x in searchresults if x[0] == songindex))

                                # if current_song_index_in_search_results is not None:
                                    # now_playing_marker = "--@--> "
                                    now_playing_marker = " :: "

                                    display_table_formatted_sections = (
                                        # Table header (First 3 lines)
                                        search_results_table_header(display_table_formatted_sections, now_playing_marker),
                                        # Part above now playing
                                        display_table_formatted_sections[3:current_song_index_in_search_results+3],
                                        # Now playing (if exists)
                                        display_table_formatted_sections[current_song_index_in_search_results+3],
                                        # Part below now playing
                                        display_table_formatted_sections[current_song_index_in_search_results+3+1:],
                                    )

                            # First line for description of query results
                            IPrint(f"{found_display_string_1} {found_display_string_2} "+
                                   f"{found_display_string_3} {found_display_string_4}",
                                   visible=visible)

                            # Fully formatted table header
                            if current_song_index_in_search_results is None:
                                now_playing_marker = ""
                                display_table_formatted_sections = (
                                    search_results_table_header(display_table_formatted_sections, now_playing_marker),
                                    display_table_formatted_sections[3:],
                                )
                            _ = [IPrint(i, visible=visible) for i in display_table_formatted_sections[0]]

                            # Part of table above "now-playing" song (if "now-playing" song is within the results)
                            # else, it just prints the entire table
                            _ = [IPrint(f"{len(now_playing_marker)*' '}{i}", visible=visible) for i in display_table_formatted_sections[1]]
    
                            if current_song_index_in_search_results is not None and songindex != -1:
                                # If "now-playing" song is within the results
                                # Highlighting the "now-playing" song 
                                IPrint(_theme_colors.prompt_foreground_1 + _theme_colors.prompt_background_1 + now_playing_marker +
                                    _theme_colors.prompt_foreground_3 + _theme_colors.prompt_background_3 +
                                    display_table_formatted_sections[2] + NBSP,
                                    visible=visible)

                                # Part of table below "now-playing" song 
                                _ = [IPrint(f"{len(now_playing_marker)*' '}{i}", visible=visible) for i in display_table_formatted_sections[3]]

        elif commandslist in [['s'], ['stop']]:
            stopsong()
            IPrint('Stopped', visible=visible) # Feedback to user

        elif commandslist[0].lower() in ['rm', 'del']:
            song_identifier = commandslist[1]
            song_path_is_valid = False
            print(song_identifier)

            if song_identifier.isnumeric():
                song_identifier = int(song_identifier)-1
                if song_identifier in range(len(_local_sound_files_names_only)):
                    song_path_is_valid = True
                    song_path = _local_sound_files[song_identifier]
                else:
                    SAY(visible=visible,
                        display_message = f'ERROR: Song index for deletion is out of range, try a value between 1 and {len(_local_sound_files)}',
                        log_message = 'Could not delete file from local storage',
                        log_priority = 2)

            if os.path.isfile(song_path):
                if os.path.splitext(song_path)[1] in supported_file_types:
                    song_path_is_valid = True

                    deletion_confirmation_permission = input(f"Are you sure you want to delete {_theme_colors.error}{song_path}{NBSP} (y/n)? ")

                    if deletion_confirmation_permission.lower() == "y":
                        try:
                            os.remove(song_path)
                            IPrint(f"Successfully deleted {_theme_colors.prim}{song_path}{NBSP}")
                        except OSError:
                            SAY(visible=visible,
                                display_message = 'Could not delete the file from disk',
                                log_message = 'Could not delete file from local storage',
                                log_priority = 2)
                    else:
                        IPrint(f"{_theme_colors.sec}Aborted deletion{NBSP}")

            if not song_path_is_valid:
                SAY(visible=visible,
                    display_message = 'File to be deleted was not found',
                    log_message = 'Invalid song path fro deletion',
                    log_priority = 2)



        elif commandslist in [['m'], ['mute']]:
            if currentsong:
                try:
                    if ismuted:
                        vas.vlc_media_player.get_media_player().audio_set_mute(1)
                        IPrint('Unmuted', visible=visible) # Feedback to user
                    else:
                        vas.vlc_media_player.get_media_player().audio_set_mute(0)
                        vas.vlc_media_player.get_media_player().audio_set_volume(int(cached_volume*100))
                        IPrint('Muted', visible=visible) # Feedback to user

                    ismuted = not ismuted
                except Exception:
                    # raise
                    SAY(visible=visible,
                        display_message = 'Some internal issue occured while muting player',
                        log_message = 'Some internal issue occured while muting player',
                        log_priority = 2)

        elif commandslist in [['lyr'], ['lyrics']]:
            lyrics_ops(show_window = True)

        elif commandslist[0].lower() in ['v', 'vol', 'volume', 'vh', 'volh', 'volumeh']:
            try:
                if len(commandslist) == 2 and commandslist[1].isnumeric():
                    if '.' in commandslist[1]:
                        SAY(visible=visible, display_message='Volume must not have decimal point precision',
                            log_message='Volume set to decimal percentage', log_priority=2)
                    else:
                        change_vol_flag = True
                        volper = int(commandslist[1])

                        if volper > 100: # Volume boost requested by user
                            artificially_boosted_volume_perm = 'yes'
                            if volper in range(501): # Check if boost is within limits
                                if volume_is_boosted:
                                    # Warn user: "Vol is boosted, quality maybe bad"
                                    IPrint(f"{_theme_colors.prim}Volume is > 100%, (not recommended). Lower to <= 100% for better sound quality{NBSP}")
                                else:
                                    # Ask user: Really want to boost vol?
                                    change_vol_flag = False
                                    artificially_boosted_volume_perm = input(f"Do you really want to boost volume to {volper}% (y/n)? ").lower().strip()
                                    if artificially_boosted_volume_perm in ['yes', 'y', 'no', 'n']: # Valid permission for boosting volume (valid by default if volper <= 100)
                                        if artificially_boosted_volume_perm in ['yes', 'y']: # Permission granted
                                            volume_is_boosted = True
                                            change_vol_flag = True
                                    else:
                                        SAY(visible=visible,
                                            display_message='Invalid permission for boosting volume',
                                            log_message='Invalid permission for boosting volume',
                                            log_priority=2)
                            else:
                                change_vol_flag = False
                                SAY(visible=visible, display_message='Volume percentage is out of range, it must be between 0 and 500',
                                    log_message='Volume percentage out of range', log_priority=2)

                        else:
                            # No boost requested (simple vol change)
                            if volume_is_boosted: volume_is_boosted = False

                        # Volume actually changes here
                        if change_vol_flag:
                            if commandslist[0].lower().endswith('h'):
                                # Hard volume change
                                vas.vlc_media_player.get_media_player().audio_set_volume(volper)
                                # cached_volume = volper/100

                            else:
                                if not isplaying:
                                    # Hard volume change
                                    vas.vlc_media_player.get_media_player().audio_set_volume(volper)

                                else:
                                    # Soft volume change
                                    initvol = cached_volume
                                    finalvol = volper/100
                                    fade_duration = 0.3 # TODO: Link to settings

                                    if abs(initvol-finalvol):
                                        fade_in_out(initvol=initvol,
                                                    finalvol=finalvol,
                                                    fade_type=isplaying,
                                                    fade_duration=fade_duration,
                                                    pretty_print=False,
                                                    auto_pause_toggle=False)

                                    # cached_volume = volper/100

                            cached_volume = volper/100
                            IPrint(f"}}}} {int(cached_volume*100)}%", visible=visible) # Feedback to user

                elif len(commandslist) == 1:
                    IPrint(f"}}}} {int(cached_volume*100)}%", visible=visible) # Feedback to user

            except Exception:
                # raise # --> Needed for debugging
                SAY(visible=visible,
                    display_message = 'Some internal issue occured while setting player volume',
                    log_message = 'Some internal issue occured while setting player volume',
                    log_priority = 2)

        elif commandslist[0].lower() in ['mv', 'mvol', 'mvolume']:
            # '''
            try:
                if len(commandslist) == 2 and commandslist[1].isnumeric():
                    if '.' in commandslist[1]:
                        SAY(visible=visible, display_message='System volume must not have decimal point precision',
                            log_message='System volume set to decimal percentage', log_priority=2)
                    else:
                        volper = int(commandslist[1])
                        if volper in range(101):
                            setmastervolume(value=volper)
                        else:
                            SAY(visible=visible, display_message='System volume percentage is out of range, it must be between 0 and 100',
                                log_message='System volume percentage out of range', log_priority=2)

                elif len(commandslist) == 1:
                    if comtypes_load_error:
                        SAY(visible=visible,
                            log_message="comtypes functionality used even when not available",
                            display_message="This functionality is unavailable",
                            log_priority=3)
                    else:
                        try:
                            IPrint(f"}}}} {get_master_volume()}%", visible=visible) # Feedback to user
                        except Exception:
                            SAY(visible=visible, display_message='ERROR: Couldn\'t get system master volume', log_message=f'Unknown error while getting master volume as percent: {currentsong}', log_priority=2)

            except Exception:
                SAY(visible=visible,
                    display_message = 'Some internal issue occured while setting the system volume',
                    log_message = 'Some internal issue occured while setting the system volume',
                    log_priority = 2)

        elif commandslist in [['l'], ['len'], ['length']]:
            if currentsong and currentsong_length != -1:
                if currentsong_length:
                    IPrint(convert(currentsong_length), visible=visible)
                else:
                    IPrint(convert(get_currentsong_length()), visible=visible)

        elif commandslist in [['lib'], ['library']]:
            IPrint("Opening location of library file", visible=visible)
            sp.Popen(f'explorer /select, lib.lib')

        elif commandslist[0] == 'view':
            if len(commandslist) == 2:
                if commandslist[1] in ['lib', 'library']:
                    IPrint("Opening library file in browser for viewing", visible=visible)
                    if webbrowser._tryorder in [['windows-default', 'C:\\Program Files\\Internet Explorer\\IEXPLORE.EXE'], ['windows-default'], None]:
                        for brave_path in SYSTEM_SETTINGS['system_settings']['brave_paths']:
                            if os.path.exists(brave_path):
                                break

                        try:
                            webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
                            webbrowser.get('brave').open_new(os.path.join(CURDIR, 'lib.lib'))
                        except Exception:
                            webbrowser.open(os.path.join(CURDIR, 'lib.lib'))

                    else:
                        try:
                            webbrowser.get('brave').open_new(os.path.join(CURDIR, 'lib.lib'))
                        except Exception:
                            webbrowser.open(os.path.join(CURDIR, 'lib.lib'))

                elif commandslist[1] in ['lyr', 'lyrics']:
                    if device_is_connected():
                        IPrint("Attempting to open lyrics file in browser for viewing", visible=visible)
                        lyrics_ops(show_window = False)
                        if webbrowser._tryorder in [['windows-default'], None]:
                            for brave_path in SYSTEM_SETTINGS['system_settings']['brave_paths']:
                                if os.path.exists(brave_path):
                                    break

                            webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
                            if os.path.isfile('temp/lyrics.html'):
                                webbrowser.get('brave').open_new(os.path.join(CURDIR, 'temp/lyrics.html'))
                            else:
                                SAY(visible=visible,
                                    log_message = 'No lyrics available to view',
                                    display_message = 'No lyrics available to view',
                                    log_priority = 2)
                        else:
                            if os.path.isfile('temp/lyrics.html'):
                                try:
                                    webbrowser.get('brave').open_new(os.path.join(CURDIR, 'temp/lyrics.html'))
                                except Exception:
                                    webbrowser.open(os.path.join(CURDIR, 'temp/lyrics.html'))
                            else:
                                SAY(visible=visible,
                                    log_message = 'No lyrics available to view',
                                    display_message = 'No lyrics available to view',
                                    log_priority = 2)

        elif commandslist in [['music-downloads'], ['md']]:

            if device_is_connected():
                from beta import mediadl
                dl_dir_setup_code = mediadl.setup_dl_dir(SETTINGS, SYSTEM_SETTINGS)
                if dl_dir_setup_code not in range(4):
                    dl_dir = dl_dir_setup_code
                    if sys.platform == 'win32': dl_dir=dl_dir.replace('/', '\\')
                    else: dl_dir=dl_dir.replace('\\', '/')
                    IPrint(f"Opening downloads directory: {dl_dir}", visible=visible)
                    os.system(f'explorer {dl_dir}')
                else:
                    # ERRORS have already been handled and logged by `mediadl.setup_dl_dir()`
                    pass

        elif commandslist[0] in ['/ys', '/youtube-search']:
            # E.g. /ys "The Weeknd Blinding Lights"
            #                       or
            #      /ys "The Weeknd Blinding Lights" 4

            if device_is_connected():
                YOUTUBE_PLAY_TYPE = 1
                try:
                    user_query = list(re.finditer(r'\"(.+?)"', command))
                    if len(user_query):
                        query_re_obj = user_query[0]
                        qr_span = query_re_obj.span()
                        qr_val = query_re_obj.group()[1:-1].strip()
                        rescount = command[qr_span[1]:].strip()
                    else: # User casually forgot to place query in double quotes..., let's assume they're there
                        qr_val = ' '.join(commandslist[1:])
                        rescount=''

                    ytv_choices = None

                    if rescount == '':
                        try:
                            ytv_choices = [YT_query.search_youtube(search=qr_val)]
                        except OSError:
                            SAY(visible=visible,
                                display_message = 'Video Load Error: Could not load video... (Maybe check your VPN?)',
                                log_message = 'Video load error: Could not load video (Maybe VPN Error?)',
                                log_priority = 2)

                    elif rescount.isnumeric():
                        if int(rescount) == 1:
                            try:
                                ytv_choices = [YT_query.search_youtube(search=qr_val)]
                            except OSError:
                                SAY(visible=visible,
                                    display_message = 'Video Load Error: Could not load video... (Maybe check your VPN?)',
                                    log_message = 'Video load error: Could not load video (Maybe VPN Error?)',
                                    log_priority = 2)

                        elif int(rescount) in range(2, max_yt_search_results_threshold+1):
                            ytv_choices = YT_query.search_youtube(
                                search=qr_val, rescount=int(rescount))
                        else:
                            if int(rescount) <= 0:
                                SAY(visible=visible,
                                    display_message = f'YT result count should be > {0}, please retry',
                                    log_message = 'Subceeded lower threshold for YT search result count',
                                    log_priority = 2)

                            if int(rescount) > max_yt_search_results_threshold:
                                SAY(visible=visible,
                                    log_message = 'Exceeded upper threshold for YT search result count',
                                    display_message = f'YT results limit exceeded, retry with result count <= {max_yt_search_results_threshold} (can be changed in settings)',
                                    log_priority = 2)

                    else:
                        SAY(visible=visible,
                            log_message = 'Invalid value for YT search result count',
                            display_message = f'Invalid value for YT search result count',
                            log_priority = 2)

                    if ytv_choices:
                        choose_media_url(media_url_choices=ytv_choices)

                except Exception:
                    # raise
                    SAY(visible=visible,
                        display_message="Invalid YouTube search, type: [/youtube-search | /ys] \"<search terms>\" [<result_count>]",
                        log_message="Invalid YouTube search by user",
                        log_priority=2)

        elif commandslist[0].lower() in ['/yl', '/youtube-link']:

            if device_is_connected():
                YOUTUBE_PLAY_TYPE = 0
                if len(commandslist) == 2:
                    media_url = commandslist[1]
                    media_url_is_valid = url_is_valid(media_url)
                    if media_url_is_valid:
                        try:
                            play_vas_media(media_url=media_url, single_video=True)
                        except OSError:
                            SAY(visible=visible,
                                display_message = 'Video Load Error: Could not load video... (Maybe check your internet connection or VPN?)',
                                log_message = 'Video load error: Could not load video',
                                log_priority = 2)

                    elif not url_error_handle(media_url_is_valid):
                        SAY(visible=visible, display_message='Entered Youtube URL is invalid', log_message='Entered Youtube URL is invalid', log_priority = 2)
                else:
                    SAY(visible=visible,
                        display_message = "Invalid YouTube-link command (too long)", # Too many args
                        log_message = "Invalid YouTube-link command (too long)",
                        log_priority = 2)

        elif commandslist[0] in ['/ml', '/media-link']:

            if device_is_connected():
                if len(commandslist) == 2:
                    user_aud_url = commandslist[1]
                    user_aud_url_is_valid = url_is_valid(user_aud_url)
                    if user_aud_url_is_valid:
                        play_vas_media(media_url = commandslist[1], media_type='general')
                    elif not url_error_handle(user_aud_url_is_valid):
                        SAY(visible=visible,
                            display_message = "Invalid media link (or maybe internet is down)",
                            log_message = "Invalid media link (or maybe internet is down)",
                            log_priority = 2)
                else:
                    SAY(visible=visible,
                        display_message = "Invalid media-link command (too long)",  # Too many args
                        log_message = "Invalid media-link command (too long)",
                        log_priority = 2)

        elif commandslist[0] in ['/wra', '/webradio']:

            if device_is_connected():
                if len(commandslist) == 1: # Default station is coffee if not stated otherwise
                    r_station = 'coffee'
                elif len(commandslist) == 2:
                    r_station = commandslist[1].strip()

                if len(commandslist) in [1, 2]:
                    r_stations = 'coffee chillout lounge'.split()

                    radio_media = None
                    if r_station.isnumeric():
                        if int(r_station)-1 in range(len(r_stations)):
                            r_station = r_stations[int(r_station)-1]
                            radio_media = r_station
                    elif r_station in r_stations: # TODO: - print these values in help...
                        radio_media = r_station

                    if radio_media:
                        play_vas_media(media_url=None, media_type='radio', media_name=r_station)
                    else:
                        SAY(visible=visible,
                            display_message = f'Unknown webradio station {colored.fg("navajo_white_1")}"{r_station}"{colored.fg("magenta_3a")} selected'+\
                                            '\n'+f'Choose one of the following stations ({colored.fg("navajo_white_1")}index or name{colored.fg("magenta_3a")}):',
                            log_message=f'Unknown webradio station "{r_station}" selected',
                            log_priority = 2)
                        IPrint(tbl([(f"{_theme_colors.exit_prompt}/wra {i+1}{COLOR_RESET}", j) for i, j in enumerate(r_stations)], tablefmt='plain'), visible=visible)
                else:
                    SAY(visible=visible,
                        display_message = "Unknown webradio command (too long)",
                        log_message = "Unknown webradio command (too long)",
                        log_priority = 2)


        elif commandslist[0] in ['/rs', '/reddit-sessions', '/reddit-session', '/rpan']:
            if device_is_connected():
                reload_reddit_creds()

                if r_seshs:
                    global r_seshs_data
                    r_seshs_data, rs_params = redditsessions.display_seshs_as_table(r_seshs)
                    r_seshs_data_processed = [[i+1]+j for i,j in enumerate([list(i.values()) for i in r_seshs_data])]
                    if len(commandslist) == 1:
                        r_seshs_table = tbl(r_seshs_data_processed,
                                            tablefmt='simple',
                                            headers=["#", "RPAN Session"]+[*rs_params[1:]])
                        IPrint(r_seshs_table, visible=visible)
                        IPrint('\n', visible=visible)
                        sesh_index = input(f"{_theme_colors.oth}Enter RPAN session number to tune into: {colored.fg('navajo_white_1')}")
                        print(COLOR_RESET, end='')
                    elif len(commandslist) == 2:
                        sesh_index = commandslist[1]

                    if len(commandslist) <= 3:
                        if sesh_index.strip():
                            IPrint("[INFO] Reddit sessions sometimes may take ages to start and seek...", visible=visible)
                        else:
                            IPrint(f"{colored.fg('hot_pink_1a')}Skipping RPAN stream (left empty){COLOR_RESET}")
                        if sesh_index.isnumeric():
                            sesh_index = int(sesh_index)-1
                            if sesh_index in range(len(r_seshs_data)):
                                sesh_name=r_seshs_data[sesh_index].get('title')
                                if not sesh_name: sesh_name = '[UNRESOLVED REDDIT SESSION]'
                                IPrint(f"Tuning into RPAN: {colored.fg('indian_red_1b')}{sesh_name}{COLOR_RESET}", visible=visible)
                                play_vas_media(media_url=r_seshs[sesh_index]['audiolink'],
                                            media_type='redditsession',
                                            media_name=sesh_name)
                        else:
                            if sesh_index.strip():
                                SAY(visible=visible,
                                    display_message=f'You have entered an invalid RPAN session number',
                                    log_message=f'Invalid RPAN session number entered',
                                    log_priority=2)
                    else:
                        SAY(visible=visible,
                            display_message=f'You have entered an invalid reddit session command',
                            log_message=f'Invalid reddit session command entered',
                            log_priority=2)

        elif commandslist in [['vivojay', 'favourite'], ['vivojay', 'fav']]:
            if device_is_connected():
                one_of_dev_fav_song = 'https://www.youtube.com/watch?v=izWf40-3n1Y'
                YOUTUBE_PLAY_TYPE = 0
                one_of_dev_fav_song_url_is_valid = url_is_valid(one_of_dev_fav_song)
                if one_of_dev_fav_song_url_is_valid:
                    try:
                        play_vas_media(media_url=one_of_dev_fav_song, single_video=True)
                    except OSError:
                        SAY(visible=visible,
                            display_message = 'Video Load Error: Could not load video... (Maybe check your internet connection or VPN?)',
                            log_message = 'Video load error: Could not load video',
                            log_priority = 2)
                elif not url_error_handle(one_of_dev_fav_song_url_is_valid):
                    SAY(visible=visible,
                        display_message='developer @vivojay\'s fav song\'s youtube link isn\'t alive anymore !',
                        log_message='developer @vivojay\'s fav song\'s youtube link isn\'t alive anymore !',
                        log_priority = 2)

        save_this_session_data()

def get_current_datetime(time_format='%d-%b-%Y %I:%M:%S %p'):
    result_date = dt.strftime(dt.now(), time_format)
    return result_date.split()

def mainprompt():
    global visible, currentsong_length, COLOR_RESET
    song_just_became_unavailable = False

    while True:
        try:
            connector_unit = "\u2501"

            cur_song_len = connector_unit*2
            cur_prog = connector_unit*3
            cur_prog_as_percentage = connector_unit*2
            cur_song = f"{_theme_colors.prompt_not_playing_foreground}{_theme_colors.prompt_not_playing_background}\u250F{connector_unit*2}(Not Playing)"
            cur_song_formatting = _theme_colors.prompt_not_playing_foreground+_theme_colors.prompt_not_playing_background
            arrowhead='❱'
            # current_datetime = get_current_datetime()

            with contextlib.suppress(AttributeError):
                if currentsong:
                    cur_prog = convert(get_current_progress())
            with contextlib.suppress(TypeError):
                if currentsong:
                    if currentsong_length != -1:
                        cur_song_len = convert(currentsong_length)
            with contextlib.suppress(AttributeError):
                if currentsong:
                    if currentsong_length not in [-1, None]:
                        cur_prog_as_percentage = round(get_current_progress()/currentsong_length*100)
                        cur_prog_as_percentage = f"{cur_prog_as_percentage}%"

            play_status_string = ''

            if currentsong:
                is_fav = None # Unknown fav status
                current_song_data = LOCAL_TRACK_INFOS.get(current_song_name(pretty_display=False))

                if current_song_data:
                    if current_song_data['isFav'] is None:
                        is_fav = -1
                    else:
                        is_fav = current_song_data['isFav']

                fav_info_string = ['', '', '❤️', '⛔'][[None, False, True, -1].index(is_fav)]
                if fav_info_string: fav_info_string = " / "+fav_info_string

                if BETA_STATUS:
                    play_status_string =  ['||', '|>'][isplaying]

                cur_song_formatting = _theme_colors.prompt_foreground_1+_theme_colors.prompt_background_1
                cur_song = current_song_name(pretty_display=False, detailed_output=False)

                # Remove some unwanted characters of the song-name from main prompt
                cur_song = ''.join([character for character in cur_song if character not in list('()[]{};')])
                # cur_song = text_overflow_prettify(cur_song, 30) # Old style

                # Manage song title overflow...
                cur_song = text_overflow_prettify(cur_song, 50)
                cur_song = f"{cur_song_formatting}\u250F{connector_unit}" \
                           f"{_theme_colors.prompt_foreground_4}{_theme_colors.prompt_background_4}{connector_unit}({_theme_colors.prompt_foreground_4}{_theme_colors.prompt_background_4}{current_local_song_index()}{fav_info_string}){connector_unit}{cur_song_formatting}{connector_unit}{cur_song}"
                # cur_song = cur_song_formatting+cur_song

                # TODO: Make the following if-statement point out when a track becomes unavailable
                if not ISDEV:
                    if (not song_just_became_unavailable): # FIXME: Broken rule, please do sumn :( 
                        if reloaded_index() == None: # TODO: Change as per new rules of songindex
                            song_just_became_unavailable = True

                    else:
                        if isinstance(reloaded_index(), int):
                            song_just_became_unavailable = False

                    if song_just_became_unavailable:
                        SAY(visible=visible,
                            display_message = 'Currently playing song has just been unloaded from library',
                            log_message = 'Currently playing song has just been unloaded from library',
                            log_priority = 3)

            # additional_prompt_info_string = f"|{COLOR_RESET}({' '.join(current_datetime)}){_theme_colors.prompt_background_1}{_theme_colors.prompt_foreground_1}|"
            # additional_prompt_info_string = f"{_theme_colors.prompt_foreground_1}{_theme_colors.prompt_background_1} {current_datetime[0]} {_theme_colors.prompt_foreground_2}{_theme_colors.prompt_background_2} {current_datetime[1]} {_theme_colors.prompt_background_3}{_theme_colors.prompt_foreground_3}{NBSP}{arrowhead}"

            # additional_prompt_info_string = f"{cur_song} {_theme_colors.prompt_foreground_2}{_theme_colors.prompt_background_2} {cur_prog} {_theme_colors.prompt_background_3}{_theme_colors.prompt_foreground_3} {cur_song_len} {_theme_colors.prompt_background_4}{_theme_colors.prompt_foreground_4} {cur_prog_as_percentage} {_theme_colors.prompt_background_5}{_theme_colors.prompt_foreground_5} > " # Old style

            additional_prompt_info_string = f"{cur_song} {NBSP} \n{cur_song_formatting}\u2517{connector_unit*2}{_theme_colors.prompt_foreground_2}{_theme_colors.prompt_background_2}"+connector_unit*(not not currentsong)+f"{cur_prog}{connector_unit}{_theme_colors.prompt_background_3}{_theme_colors.prompt_foreground_3}{connector_unit}{cur_song_len}{connector_unit}{_theme_colors.prompt_background_4}{_theme_colors.prompt_foreground_4}{connector_unit}{cur_prog_as_percentage}{connector_unit}{_theme_colors.prompt_foreground_5}{COLOR_RESET}{connector_unit}{play_status_string}{connector_unit}{arrowhead}"

            # Main music player prompt
            prompt = additional_prompt_info_string+\
                     NBSP+\
                    _theme_colors.user_commands

            command = input(prompt) if visible else getpass(prompt)
            print(COLOR_RESET, end='')
            outcode = process(command)

            if outcode == False:
                exitplayer()
                break

        except KeyboardInterrupt:
            IPrint('\n', visible=visible)


def showversion():
    global visible, SYSTEM_SETTINGS
    if visible and SYSTEM_SETTINGS:
        with contextlib.suppress(Exception):
            print(f"v{_theme_colors.tert}{SYSTEM_SETTINGS['ver']['maj']}.{SYSTEM_SETTINGS['ver']['min']}.{SYSTEM_SETTINGS['ver']['rel']}"+\
                  f" {_theme_colors.sec}@{_theme_colors.author}{SYSTEM_SETTINGS['about']['author']}{_theme_colors.prim}{NBSP}"+\
                  COLOR_RESET)
            print()


def showbanner():
    global visible
    banner_lines = []

    if visible:
        with contextlib.suppress(IOError):
            with open('res/banner.banner', encoding='utf-8') as file:
                banner_lines = file.read().splitlines()
                maxlen = len(max(banner_lines, key=len))
                if maxlen % 10 != 0:
                    maxlen = (maxlen // 10 + 1) * 10 # Smallest multiple of 10 >= maxlen,
                                                     # Since 10 is the length of cols...
                                                     # So lines will be printed with full olor range
                                                     # and would be more visually pleasing...
                banner_lines = [(x + ' ' * (maxlen - len(x))) for x in banner_lines]
                for banner_line in banner_lines:
                    blue_gradient_print(banner_line, cols+cols[::-1])
    
    if visible: showversion()

def run():
    global disable_OS_requirement, visible, USER_DATA

    if disable_OS_requirement and sys.platform != 'win32':
        IPrint("WARNING: OS requirement is disabled, performance may be affected on your Non Windows OS", visible=visible)

    USER_DATA['default_user_data']['stats']['log_ins'] += 1
    save_user_data()

    pygame.mixer.init()

    if FIRST_BOOT:
        startup_sound_path = "res/first_boot_startup_sound.mp3"
        if os.path.isfile(startup_sound_path):
            pygame.mixer.music.load(startup_sound_path)
            pygame.mixer.music.play()
        notify(Time = 6000) # For 6 seconds
        pygame.mixer.quit()

    if visible: showbanner()
    mainprompt()


def startup():
    global disable_OS_requirement, SOFT_FATAL_ERROR_INFO

    try: first_startup_greet(FIRST_BOOT)
    except Exception: raise

    # Spawn get_media process in the bg
    if _local_sound_files != [] and FIRST_BOOT:
        sp.Popen([sys.executable, 'meta_getter.py', str(supported_file_types)], shell=True)

    if not disable_OS_requirement:
        if sys.platform != 'win32':
            sys.exit('ABORTING: This program will not work on'
            'Non-Windows Operating Systems') # Testing has been done on Non-Windows OS
                                             # and this program definitely doesn't work in those OSes
    if not SOFT_FATAL_ERROR_INFO: # End program silently if SOFT_FATAL_ERROR_INFO is set
        if FATAL_ERROR_INFO:
            IPrint(f"FATAL ERROR ENCOUNTERED: {FATAL_ERROR_INFO}", visible=visible)
            IPrint("Exiting program...", visible=visible)
            sys.exit(1) # End program...forcefully...
        else: run()


if __name__ == '__main__':
    startup()
else:
    print(' '*30, end='\r')  # Get rid of the current '\r'...

# Way to convert chars outside BMP to unicode:
# out_str = test_str.encode('utf-16','surrogatepass').decode('utf-16')
# 
# Remove the `ISDEV`s
# 
