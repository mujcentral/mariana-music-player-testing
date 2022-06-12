```
Easter Eggs (Fun stuff)
Make into an executable release -> Host on GitHub
IMPLEMENT QUEUE PLAYING
Currently beta features are switched on by default and cannot be opted out of; Change this...

Run a "related-songs-getter" type function to get similar song to the ones you listen to
and package into a playlist (Mariana's own simple playlist format??
                             or prebuilt playlist formats e.g. m3u etc...)

MIGRATE ENTIRELY TO python-vlc FOR PLAYING SONGS OF ANY KIND(CODEC)...

Timed tagging and commenting withing songs:
    timed tagging/comenting will generate an editable yml file with some custom extension
        (maybe as an srt file??)

MAKE THE STEP-BY-STEP WIZARD FOR INITIAL SETUP A BREEZE... (Already kinda is...?)
    ASK 3 QUESTIONS                         ??? (Do we really need it?)
    TELL 3 THINGS                           ??? (Do we really need it?)
    ASK IF YOU WANT TO START APP NOW...     ??? (Do we really need it?)

Save all recursive file paths from all lib dirs in a libpaths files for quick reload 
Mark unplayable/corrupt song files and exclude them from libpaths
    Exclude the unplayable/corrupt from libpaths.yml "general" heading and shift them to "corrupt"
    These marked files WILL STILL be listed in "all" command but will not be directly searchable using the f[ind] command...
    unless the find command is issued with the extra option "c" (for corrupt)

Blacklisting will exclude the unplayable/corrupt from libpaths.yml "general" heading and shift them to "blacklist"
    These marked files WILL STILL be listed in "all" command but will not be directly searchable using the f[ind] command...
    unless the find command is issued with the extra option "b" (for corrupt)

Favourited files will be moved in libpaths.yml from "general" heading to "blacklist"
    These marked files WILL STILL be listed in "all" command but will not be directly searchable using the f[ind] command...
    unless the find command is issued with the extra option "b" (for corrupt)

Find command will be issuable with the following options:
    c: Show only corrupt/unplayable files
    b: Show only blacklisted files
    a: Show only  files
    t <tag_name>: Show only files with given tag (if multiple tags specified, then all tags mst be present)
    f: Show only favourited files
    

Many Great Visualizers (2D and 3D, color changing, other effects....)
Song Videos from youtube (if available) ... ? (May not be implemented)

Log time taken to load this cli tool on every boot and append data to data/app.yml under the "boot_params" heading

Separate error message if deleted file is attempted to be played
Make a temp folder: create ffmpeg version of wav file to mp3 (named cur_V.wav)??
Tone generator (Play sin/sqaure/sawtooth/triangle waves (ora combination) at a given freq, ADSR and volume)
	Can also be recorded...

Free movies
	Downloadable (if licensed)
	Streamable
	Recommendations Support
	New releases + Actors news (Mostly about recommended movie stars + Major stars...
		... --> Most watched movie stars' news floats to top)

Support artists
	Links to their linktree ... and/or
	Donations Page + Website
	Bandcamp
	Deezer
	Spotify
	YouTube
	Wikipedia

Float search results from favs to another table above the other/non-fav results' table (colour in a different scheme from settings)
Sink search results from blacklist to another table below the other/non-fav results' table if f[ind]\[+bl\] is issued (colour in a different scheme from settings)
Show relative numbering of songs from currently playing song if its present in the search results (colour in a different scheme from settings)
Play a song with last remembered position and applied effects
Record sessions
Take regular auto backups of open sessions and offer to reopen them on next bootup
Set volume to default session volume value defined in settings (default=90)
[online + offline] live feed and time-synced commenting + reactions + emojis (dynamic) + stickers

Data for deleted files should be marked as deleted (can be prompted for later deletion if needed)
Record Main System while playing a certain song, to calculate a user's weighted liking to that song
Depending on the player and system vol, actively prevent setting volume to a value higher than some healthy threshold to avoid ear damage (this is calculated better with a function of replaygain, player volume and system volume)...
    (Show a continuous warning if this is disabled --> warnings themselves may/may not be disableable)

Make player more interactive if the current user's settings allow for it...

Get MFCC data from all lib songs and analyse the moods, genres, bpm (tempo), key (scale), energetics, danceability
    Write the analyzed data into a yml file called lib_analyses.yml in genres/genres folder

Set Artist name if not already mentioned in the metadata
Show lyrics in time sync if available, else show the whole lyrics on html page
    else

Quickly fingerprint audio and reliably find and separately save duplicates...
Give short summaries about user's listening habits
See "what others are listening" feature to show other users' listening habits summaries (if they choose to make it public)

Make a `library` command to display all songs + their info in a tabular form (Like a CLI version of Windows File Explorer, but for sound files only)
Make small GUI display for current song progress
Record command history and logs in "historydump.log" and "generallogs.log" respectively
Allow users to enter a PRIVATE SESSION/MODE (Displayed with a "P" before the prompt arrow) (No history/log is ever saved for priv sessions)
If a queue is requested during a play-queue, then the new queue overrides the play-queue.
In any other case, the new queue/play-queue is appended to the previous

Favouriting/Blacklisting
    fav   ==> show favourited status for currently playing song
    fav ! ==> toggle favourited status for currently playing song
    fav + ==> add currently playing song to favourites
    fav - ==> remove currently playing song from favourites

    fav <num1> [<num2> [<num3> [...]]]   ==> show favourited status for songs at provided indices
    fav + <num1> [<num2> [<num3> [...]]] ==> add songs at provided indices to favourites
    fav - <num1> [<num2> [<num3> [...]]] ==> remove songs at provided indices from favourites

    [blacklist|bl]   ==> show blacklist status for currently playing song
    [blacklist|bl] ! ==> toggle blacklist status for currently playing song
    [blacklist|bl] + ==> add currently playing song to blacklist
    [blacklist|bl] - ==> remove currently playing song from blacklist

    [blacklist|bl] <num1> [<num2> [<num3> [...]]]   ==> show blacklist status for song(s) at provided indices
    [blacklist|bl] + <num1> [<num2> [<num3> [...]]] ==> add song(s) at provided indices to blacklist
    [blacklist|bl] - <num1> [<num2> [<num3> [...]]] ==> remove song(s) at provided indices from blacklist

    f[fav]
    f[bl]
    f[-fav]
    f[+bl]
    f[-fav,+bl] | f[+bl,-fav] -> (No spaces within '[]')
    f[tag1,tag2,-fav] -> (Only songs with atleast one provided tags set AND not in favs)

Blacklisted songs won't be shown in default search results
Blacklisted songs will ask for confirmation before being playing in a queue/individual-song/playlist/etc...

The shuffle command will shuffle the current play-queue
The shuffle command can shuffle the current queue or any of the other requested "named queues" (Beta)
	Syntax:
		shuffle [q name]

Loops will be given preference over queues and play-queues, i.e. if a song is looped from within a queue,
then it will keep looping until the loop is closed. After the loop is closed,
the remaining queued songs will start playing as usual until the queue(s) end(s).
Make it colourful. Make display tasty and colourful with borders and themes!
If opening for the first time, find and save songs with their indices in "library.yml"
For all subsequent loads, use enumerated song paths cached in this file.
For refreshing this list, just type the refresh command and effect will take place immediately

Make an elaborate and heavily organized and detailed settings YAML file and markdown + html documentation.
Get list of available bluetooth + connected audio output devices… and highlight the current one. Define a simple command to view + change output devices
All Songs (`all`) should display in exactly 3 columns (not `library`)
Command to show now-playing/<number> in file explorer
Any and all setting changes should be saved/recorded and loaded on each startup/boot
Any and all settings must refresh and come into effect immediately upon issuing the appropriate command w/o the need for rebooting the player

Stream music directly:
	Create a "temp" directory in the program's main dir
	Convert wav to mp3 using FFMPEG
	Cast using SHOUTcast protocol

If all dirs empty, print no files warning (in the beginning)
Various type of tagging is allowed, e.g.:
	Genre
	Colour
	Custom (List of custom tags will be created, you may choose one or create new)

color code song indices by play freq:
  (Upper limits are excluded in range)
  key:	meaning	  abs(play_count)  rel (%)
    0:  never     0                0%
    1:  least     -                0-4%
    2:  less      4-15             4-10%
    3:  moderate  15-100           10-42%
    4:  more      100-inf          42-80%
    5:  most      -                80-100%

  relative plays (%) = (abs play_count)/(total play_count)*100 %

Connect to popular free radio service
Podcasts
    Connect to popular free podcast service(s)
    Allow to open a text file and read content from it in a podcast-like voice
        Using openAI perhaps?
        (beta feat: maybe add pauses, noises, crackles, etc... for a more natural podcast room/environment experience)
    Get Reddit post (podcast-like) texts from subreddits like:
    (preferably long, storylike texts)
        casualconversations
        seriousconversations
        talesfromtechsupport
        talesfromretail
        letsnotmeet
        creepyencounters
        worldnews
        financialindependence
        amitheasshole
        nosleep
        tifu
        legaladvice
        idontworkherelady
        confession
        relationships
        relationship_advice
        justnomil

Reddit RPAN - Add sync feature
Reddit sessions by famous* players:
    e.g.    @jonathandaleofficial
            @saxsquatch
            ...
Connect to popular free lyrics service (shazamio)
Hide/blacklist songs
Clear recents/history logs/etc….
Set metadata:
	Artist
	Song name
    .. (Few others?)
ReplayGain support
Easy way to rename and delete files from disk
The 'now' command should show if a 'queue' is playing or a 'sequence' or a 'play-queue'

Remote playback from/to other's systems

Copy/Replace a file into a converted format

Make Externally controllable (via keyboard keys...)?

Color coded convert() function for time!...

Use alternative: https://github.com/itspoma/audio-fingerprint-identifying-python.git
    for quicker fingerprinting and lyrics extraction...

If help or config file is not available or is corrupted, prompt user to download required files from GitHub or use default
If default file is not available or is corrupted, prompt user to download required files from GitHub or close program, play beep at the end


VAS Checklist:
    [ ] Add song stop detect; raise flag on song stop when played as VAS
    [x] Radio
    [x] Play single video as audio
    [x] Video list, pick video, play as audio
    [x] Reddit Sessions

Make everything configurable, including:
    Making commands (un)available
implement rel_val: rel_val = +5 means seek +5000 ms relative to cur pos
Make a new command t*: must show: (<abs_progress\> / <total_length\>) + (percent_complete)
Show a small GUI window for constant progress display... (Requires multiprocessing??)
Allow decimal-point time seeking for VAS media type

Save various user logins with completely separate encrypted data (this info is stored in a salted+peppered hash)...
...which is only decrypted once that user successfully logs in. Users may also log out of the app explicitly whenever they so choose

Emails (optional):
    Get emails (optional) for:
    Your most-listened songs/artists/genre
    Newly released music similar to your taste
    Fresh pop/viral/hit music
    News about artists/songs and the like...

    Control emailing frequency (minimum: once-per-6-months; maximum: once-per-day )

Set volume at boot to: `override_default_boot_volume` or set it to remember last session's volume

Get list of urls of `n` newly released songs from whatever sources possible (any 3rd party api or one of the moajor players listed below...)
Connect with Music Streaming Services?? E.g.
    YTMusic?
    Spotify?
    Deezer?
    SoundCloud?
    LastFM?
    Other...
    (`n` maybe adjustable via the config/commandline/fallback_value/etc...)

Make the (ls|list) feature way more powerful and robust, migrate from (f[ind]) to (ls|list)
    i.e. deprecate (f[ind])... (but not completely remove it yet...)

Give users a short note about the fact that importing modules no.: 7, 17, 22, 23, and 24
    take a longer time than usual

ACTUALLY MAKE USE OF the `loglevel` variable, it's not just for fun :meh:
    for refs: loglevels have the following values:
        {
            0: "none",  # Don't log anything, not even fatal crashes (LIKE WHUT?)
            1: "fatal", # Only log fatalities
            2: "warn",  # Log fatalities + warnings
            3: "info",  # Log fatalities + warnings + info
            4: "debug"  # Log pretty much every single line of code, this's going to take my whole day :(
        }

Make a feature to toggle auto-wallpaper (Takes wallpaper image from shazam cover-art (if detected), else fallback to default image)
Make a refresh [ settings | lyrics ] function to selectively refresh them individually
Make a prettier CSS
Make a number of CSS templates to choose from via settings
Allow option to add user's own custom CSS (with a few required params, otherwise it won't work)
Music collab via public and private access tokens (Someone can "tune-in" to another user's session securely)...
... Implementation will be difficult... Adding security even more so
Make a small desktop always-on-top display widget for the currently playing song and progress (landscape) with seek bar
  Visibility may be toggled from within mariana-player
  GUI window features may be force disabled from within settings by user
Make an auto update checker and patcher --> ask for rebooting app now or later... 
Add a command to open a file in default player?? (This may counter progress)
Add a command to explicitly check for updates (Will throw an error if "offline only" mode is enabled in settings)
Add a confirmation to ask the user before redirecting them to the webbrowser (for "view lyrics" and "open" [when streaming online media])
Make heavily customizable themes/prompt-symbols and shareable/importable/exportable settings
Add telemetry feature?? (Disable by default and ask for enabling in first boot setup) -- Do not nag user to enable it
  Send emails anonymously and securely (via TLS encryption)
Add real time speech identification to show podcast text in a GUI widget
Debug: Lyrics don't work for /ml
fade should have from/to volume checks and time interval must be within a realistic limit (defined within system.toml)
/ml video glitch remove?
live colour change... (auto cls after command is issued)
download podcasts
download settings (more granular control needed --> Try GUI + CLI + settings-file integrations)
replay current song: command = ".."
Allow podcast downloads (multiple at once should also be allowed --> better download status display)
Random functions suite:
  
DJ Mode (Changes Mixing Style to crossfade (hopefully with BPM and key shifts))
Show name of YouTube video when URL is entered
Lyrics display explicit lyrics separate icon display on top left (Not just a unicode)
More animated + fun icons + modern smoothed design + more themes + more settings...
Download:
  Download song with thumbnail metadata (if available) + Artist Names + Year of release + Album Name + BPM
  Migrate to yt_dlp for faster downloads...
  If just the "download" command is issued, prompt smart download of either currently playing audio as audio or video as video
  Directly from YouTube/Spotify/SoundCloud search result(s) <--> same as search and play or searches only
  Password Protect Download Permission (To only allow the authorized user to download songs for themselves)
  Allow multiple links download. Show a tabulated list of downloads...
  ...allow multiple downloads from tables too...
  When multiple links are displayed for download... allow multiple downloads..
  ...(after space-sep selection of all desired songs) at once (using multiprocessing) 
  ...Show a tabulated list of downloads...
  Show download(s) progress in "GUI notification area" (fade in and out)
      in bottom right (for Windows)...
      in location set in settings/prefs (for Macs)...
  If results_count > default_results_count, show a warning
  Show estimated-time-remaining + estimated-download-speed + Errors... (maybe in a GUI window?)
  Separate command to display just the file type (extension/metadata/header...?)
  Change colour of DOWNLOAD STATUS CODE (Downloading, Downloaded, Failed, etc)
  Limit number of notifiation pile (Changeable from settings)
  Download from Spotify songs/playlists/albums/etc...
  Download from SoundCloud...
  Download currently playing song
  Allow downloads of unavailable/18+/("I understand and wish to proceed" type)/etc... videos
  Allow downloads of metadata (selectable --> Settings+CLI+Default)

If podcast is paused for a long time (threshold time set in settings)...
  ...seek back 10 or 20 seconds (set in settings) automatically before resuming

Smooth transition --> Crossfade (x seconds) --> Changeable oin settings [default = 1s; range = {0-12}]
Allow realtime queue manipulation features like: 
  lol 

Mode:
  Journey mode:   (Play Indie/Long-Drive Songs and the like in an infinite queue...)
  Radio mode:     (Play random songs from the internet in an infinite queue...)
  DJ mode:        (Play random songs from the internet in an infinite queue...
                   ...but add perfectly-timed effects like a live-DJ...
                   ...complete with features such as smart-detection of crossfade-length/strength + ...
                   ...crossfading both songs (current+next) individually and adding slight pitch-shift + bpm-shift...
                   ...for gracefully crossfading songs)
  Surprise mode:  (Play random songs from the internet in an infinite queue but add perfectly-timed effects like a live-DJ ...)
  Recommend mode: (Play random songs from the internet in an infinite queue but add perfectly-timed effects like a live-DJ ...)
  Auto mode:      (Play songs in an infinite queue from the library in order of their names ...)

Allow changing settings directly from CLI/App (CLI == App)
Give user an indication next to song name for whether it is a video or audio
Music Tagging
  Tag rules and about:
      Are case insensitive (any tag uppercase will be converted to lowercase)
      May or may not have aliases
      Tag names MUST be atleast 4 chars long
      Song tags are listed as their aliases and ntot by full name by default...
      ...but you may change this behaviour in the settings
      Only the first 3 tags will be mentioned (and an ellipsis "..." will be shown if there are more tags associated with the song)
      Song tags will be enlisted only 'ls' command isissued with the "long listing" option...
      ...ls -l...
      ...This command was intentionally made this way to look familiar to linux users for their ease of use
      Tags must be unique
      Tag aliases must also be unique
      Tag must not be one of the preprovided tags
      Tag alias must not be one of the preprovided tag aliases
      Tag alias must be either 2 or 3 chars only
      IF IN CASE you exhaust all possible 2 and 3 letter alias permutations...
      ...you may NOT make any new tag aliases, all successive tags MUST be created without aliases...
      ...and referenced accordingly with their full tag-name
      May have any number of non-consecutive spaces (all non-consecutive spaces will be force-reduced to 1 automatically)...
      ... E.g.:
      ... "hello  world" --> "hello world"
      ... "my sweet  dream  " --> "my sweet dream"
      Tags are searchable (E.g. search all songs with tags "jams" and "emotional" --> /f [jams em])...
      ...Tags can be provided either as aliases or full names
      Tags of a particular song can be listed
      Tag names are editable
      Tags of a particular song are changeable (CRUD supported)
      
  Allow use of preprovided tags such as:
                             ____
                                 \
    NSFW              (!)     |  |
    NSFL              (~)     |  | ---------------- (Meta)
    MISC              (.)     |  |
    MYSTERY           (?)     |  |
                            _____/


                             ____
                                 \
    bouncy            (en)    |  |
    chilled           (mo)    |  |
    dark              (vi)    |  |
    emotional         (ch)    |  |
    energetic         (sa)    |  |
    experimental      (ha)    |  |
    fast              (ho)    |  |
    groovy            (dr)    |  |
    happy             (ps)    |  |
    hollow            (ex)    |  | ---------------- (Feeling)
    modern            (sl)    |  |
    mood              (fs)    |  |
    piano             (sm)    |  |
    psychedelic       (up)    |  |
    retro             (md)    |  |
    sad               (pn)    |  |
    slow              (vn)    |  |
    smooth            (rt)    |  |
    summer            (gr)    |  |
    uplifting         (by)    |  |
    vibe              (em)    |  |
    vintage           (su)    |  /
                             ____


                             ____
    archaic           (_ar)   |  \
    hellscape         (_he)   |  | ----------------- (Special)
    hypermelody       (_hy)   |  |
    sonic             (_so)   |  |
                             ____/


                             ________________________________________________________
                                                                                     \
    acoustic          (ac)    | -- (a)                                               |
    afro              (af)    |                                                      |
    alt               (al)    |                                                      |
    anime             (an)    |                                                      |
    arab              (ar)    |                                                      |
    bebop             (bl)    | -- (b)                                               |
    blues             (bl)    |                                                      |
    childrens         (ch)    | -- (c)                                               |
    classical         (cl)    |                                                      |
    country           (em)    |                                                      |
    dance             (da)    | -- (d)                                               |
    dubstep           (db)    |                                                      |
    easy              (ea)    | -- (e)                                               |
    electronic        (el)    |                                                      |
    emo               (em)    | --- (A "feeling" tag, also classified as a genre)    |
    frenchpop         (fr)    | -- (f)                                               |
    folk              (fl)    |                                                      |
    funk              (fu)    |                                                      |
    glitchcore        (gc)    | -- (g)                                               |
    goth              (go)    |                                                      |
    grunge            (gr)    |                                                      |
    hardcore          (ha)    | -- (h)                                               |
    harddance         (ha)    |                                                      |
    hiphop            (hh)    |                                                      |
    house             (ho)    |                                                      |
    hyperpop          (hy)    |                                                      |
    indiepop          (ip)    | -- (i)                                               |
    industrial        (in)    |                                                      |
    indierock         (ir)    |                                                      | ----------------- (Genre)
    jazz              (jz)    | -- (j)                                               |
    jpop              (jp)    |                                                      |
    kayokyoku         (ky)    | -- (k)                                               |
    kpop              (kp)    |                                                      |
    latin             (la)    | -- (l)                                               |
    lofi              (lo)    |                                                      |
    metal             (me)    | -- (m)                                               |
    neo               (no)    | -- (n)                                               |
    newwave           (nw)    |                                                      |
    noise             (no)    |                                                      |
    opera             (op)    | -- (o)                                               |
    pcmusic           (pc)    | -- (p)                                               |
    pop               (po)    |                                                      |
    postpunk          (pp)    |                                                      |
    punk              (pu)    |                                                      |
    rap               (ra)    | -- (r)                                               |
    reggaeton         (rg)    |                                                      |
    rnb               (rb)    |                                                      |
    rock              (ro)    |                                                      |
    sadcore           (sc)    | -- (s)                                               |
    shoegaze          (sz)    |                                                      |
    slowcore          (sl)    |                                                      |
    soul              (so)    |                                                      |
    stripped          (st)    |                                                      |
    terrorcore        (te)    | -- (t)                                               |
    thrash            (th)    |                                                      |
    trance            (tr)    |                                                      |
    trap              (tp)    |                                                      |
    vocal             (vo)    | -- (v)                                               |
    world             (wo)    | -- (w)                                               |
                             ________________________________________________________/



  Custom Tags (Displayed as prefixed by a '/'). E.g.:
      /jams
      /hard
      /thug life
      /bubbly and cheerful


Comments and Description
  Allow CRUD
  May be used for searching songs

Get a summary of:
  Time spent on app in total (per session, last session and total+average of all seshs)
    average number of skips per song
    pauses per song
    sections of songs most listened
    time taken between pauses in each song
    .

Show YouTube view count, upload date, like count, video redirect/pop-up button
Podcast infos:
	isFavs
	lastProgress
	bookmarkedRegions
	...

DEBUG:
	ERROR: 't' is not a valid URL. Set --default-search "ytsearch" (or run  youtube-dl "ytsearch:t" ) to search YouTube
    DOWNLOAD STATUS CODE: 5

pod vendors all must be limited by max count from settings
only the first "default-count" current play queue items must be displayed at a time and a question should ask to show more if "all" is mentioned...
	should say "showing the first {default} podcast vendors"
"pod vendors fav[s]" should display favourited pod vendors
"pods fav" should display a list of favourited podcast sessions (mix of all pod vendors with >= 1 fav pods)
remember player volume (v[ol[ume]]) per output device and change to this value when user types in a(v | vol | volume)
copy all settings to default settings as well
A way for users to view the colors and their codenames to use in settings
A way to change settings w/o leaving the player interface
Refresh (Not Playing) lower half prompt to default/unloaded prompt string
in history, save local songs with their index
Migrate from `colored` to `rich`
Option to make your playlists publicly available
Should work from any directory...
Prompt line 1 must have a different color for song num and name
  also they should be separated by the connector unicode
Downloads:
  Sometimes audio and video doesn't remain correctly aligned
Not all podcast rss links are correctly parsed (some don't show urls) .... otherwise errors aren't produced :)
When seeking songs, the crossfade must take volume value automatically (also, blacklisted/muted parts of song must be skipped/muted/etc... when seeked to that point... (if possible))
Duplicate songs remover (asks before deleting dupes/copies)
Instead of showing (N/A) as the currently playing song... show @ys / @yl / @al etc... :)
Instead of podcast link... display it as: "@pod <podcast-title>"
Git file management for songs (Shows newly added songs, time of addition/removal, etc...)
Recents, favourites, history, downloads, settings, etc... are all encrypted and only accessible by the user unless shared to another
Change output/input devices...
Command to check validity of a url --> Syntax: ?<url>
Rename commands to make them more sensible/meaningful 
Show a better/more-colourful "now" output
DEBUG: 1) Download not working sometimes, throws error:...
            ERROR: 't' is not a valid URL. Set --default-search "ytsearch" (or run  youtube-dl "ytsearch:t" ) to search YouTube...
            ...try printing the command before executing it in youtube-dl OR...
            
            403 forbidden errors to be hidden from user --> Instead retry <retries_count> times (changeable from settings)
            
            ...

       Hide errors like:...
       ...[h264 @ 0000020e3f975340] co located POCs unavailable

          [h264 @ 0000020e4870d900] get_buffer() failed...
       ...[h264 @ 0000020e4870d900] thread_get_buffer() failed...
       ...[h264 @ 0000020e4870d900] decode_slice_header error...
       ...[h264 @ 0000020e4870d900] no frame!

          [0000020e4828ad60] mmdevice audio output error: cannot initialize COM (error 0x80010106)

      2) Fatal Error in text-encoding on issuing "/open"
      3) Fatal Error: Index out of range in ls command
      4) Fatal Error: play/pause (and many other commands) rely on vas.

/ml should also have a title (extracted via youtube-dl) and link <-- Perhaps using the oembed link? or the prepared-unused pafy function...
/open should open time-synced video
Display prettier, more colourful tables...
Display "oldness/newness" (as in date-downloaded/date-added-to-lib) and...
..."experience" (as in number of times played <-- based on some function of abs/rel play counts?)
Allow custom defined timestamps (Allow CRUD)
Command history + Reissuing
Allow songs to be searched with alias/substitute names
Make custom commands using the `#` power command:
  To make a new command alias, just write "set #<new_command_alias> <existing_command>"
  E.g. to make "dla" the alias for "download-ya", you can do
  "set #dla odwnload-ya"
To call custom commands, you can issue the command as follows:
  "#<command_alias>"
  E.g. using the prev example....
  "#dla" will download the currently streaming online media as audio...
    ... and can also be used with its usual meaning and syntaxes intact
    E.g. #dla <some_youtube_url> will download audio from that YT url

prog[ress][*] should give an error if no song is playing

Add support for free audiobooks (downloadable) (maybe from librivox...)
Show volume as a rounded int percentage
Podcasts:
  Show "Downloading fresh podcast data for today"
Debug volume change without playing any song
Seek relatively using a <timeobject>
Save actual play-time (total + unmuted) + last-stop-position
Open current song's video in video-view
Download current song's video
Podcast:
  Show official website linked with the podcast
  Show official donations page for podcast
  Show official donations page for podcast
Record listen_count for each song and give stats every x hours/days/weeks/months/years/etc...
  Suggest songs listened to often
  Display the song-of-the-month (song listened to the most during the whole month)
  Display the song-of-the-year (song listened to the most during the whole year)
Show more suggestions: E.g. /? Invalid command "downlaod-ya", did you mean "download-ya" ?
Show song/podcast name when playing from youtube or podbean
Add feature to autocorrect commands
Notify if file has already been downloaded or is already queued for downloading (and display its index)
Volume changes must be smooth (default wait time = 0.2s)
Hard volume changes must be issued with (v|vol|volume)h or m(v|vol|volume)h

Do not refresh lyrics (when issuing refresh command solely) if lyrics haven't been loaded atleast once already
Add feature to scour:
  New releases by artists you hear most
  New releases by popular artists
  Hot/Viral Songs
  Artist Quotes/News
Get app community news
Feature for Auto-Updates (run explicit updates with the "app-update" command)
Feature for Explicit-Updates (run explicit updates with the "app-update" command)
  Play a short "beep" sound and show logo (enable/disable this feature in settings) whenever the app is opened after update
Allow file all simple file + file-tag operations (rm/cp/mv and tag ops) and MAKE APPROPRIATE CHANGES in song_data.yml and other data stores and info logs
Allow playing songs from history
Allow rich displaying of songs from history
Make commands more streamlined and predictable...
Fade function for mv (master-volume) as-well
random audio (optional repeat, no repeat by default)
log data about each audio path
    timestamp of each stream start and pause/end (int --> in unix time??)
    list of tags (str List)
    favourited? (bool)
    corrupted? (bool)
    blacklisted? (bool)
    duration played (int --> in ms)

    # Maybe
    estimated bpm
    estimated key/scale
Find
  Allowed parameters (Combinations of params is allowed --> complex anding and oring will be allowed):
    range of creation-dates
    range of last-played-dates
    range of average-duration-played-in-single-listens
    range of average-duration-played-in-total
    range of song-index
    count of listens/plays
  Allow some deviation (Can be set with the "/tol" parameter (for tolerance))
Allow find-and-play-first to play the first song from the search results
Allow find-and-play-popular to play the most listened song from the search results (if > 1 song has max listen counts, play the first one)
Allow find-and-play-relevant to play the first relevant song from the search results
Remove Video Glitching/Aliasing
Improve quality of vid stream (It's quite bad)
Some media play-length is incorrectly displayed
When [.]next is issued while streaming online songs, you will either get "finding similar songs, please be patient..." ...
  ... or the next recommended song to listen
Check ping and internet connection speed
List newly downloaded/added songs (untracked tracks + correspoding indices) --> user recommendations
Migrate to ACRCloud for audio fingerprinting and cover song detection
Migrate to lyricsgenius or musixmatch(Japan Law...) for lyrics
Integrations to add:
  Lyricsgenius/Musixmatch
  Librivox Audiobooks (License needed?)
  Spotify
  YTMusic
  LastFM
  Soundcloud
  Deezer
  Reddit (More Support, not just hot live-seshs, also new live-seshs and all...)
  More live radios
  More live telecasts
  Artist tours/live preformances (Dates)
  Artists' links to twitter+IG, + Their bio etc...
  Short News (as audio clips) (From Google/etc...)
  JCS Criminal Psychology
  Mr Nightmare
  Bandcamp
  https://strepsil.net/
  Programmer Music
  Gamer Music
  Discogs

random generators persistent across multiple sessions
Auto exit after song/range of songsnumber of songs/queue/playlist/play-queue ends or after a specified time (using timeobject)
Use musicbrainz database to collect album info...?
Ability to follow artists/genres
Show/search and play albums (also show album+track art) which include the currently playing soundcloud/YT soundtrack
Options to show a full-size/mid-size/small-size/bottom-cornet-widget album/track art as a GUI window/turntable/... with option for a spinning vinyl effect... :)
command to show the newly added songs on from last active reload (however ago that may have been)
disallow repeated download of the same song

"suggest" or similar command will suggest local + online recommendations
"home" or similar command will list suggestions (albeit slightly differently)...
	...alongwith that, it will also provide short news clip teasers (with links to full news)...
	...and similar info regarding new shows (
		...highlighting/starring the ones near your...
			...location if you have enabled your location to be tracked...
			...or have manually set a location
		...
	)...
	...infos will include artist bio updations + occasional donation notifs ...(
		...new releases by followed artists/similar genres to yours...
			...with links to their website/donation-page
		...news + articles regarding artists + genres + movie stars
	)...
	...songs you heard in the past
	...songs you haven't heard / heard less of in the past (downloaded)
	...songs you heard a lot
	...first few favourited songs/queues/albums

Add Music Rooms Feature
Add YouTube livestream (audio or video) sessions support

Add support for voice commands (smart discard noises + bg music etc from voice)
Find queues with similar params (using either of findqueue|findq|fq commands)

Extend Support to Macbooks + Linux Systems + Mobile???...
Make into a WebApp/Website

Use ytmusicapi module (change in system.toml and INSTALLATION.py):
  Needs Python >= 3.6

Maybe migrate from pafy to ytmusic (see which parts are better, only migrate part by part...)
  Get artist/albim/song(s)/ from search [Helps in limiting search result count and returning correct number of results...]
  Get albums from artists
  Get songs + covert arts from albums
  Get lyrics + all info from songs
  Get charts

Allow vid id instead of url for /yl (with appropriate internet + url validation checks)
Allow auto part-selection (i.e. play only certain range of song times and skip (or change volume of or mute) others)
  E.g.
  A song may have initial 10 seconds of noise, so you can remove that part
  A song may have noise or silence in seconds 22-42, so you can remove that part
  Autogain can be applied to full songs or parts to control gain dynamically (poor man's compressor) to reduce/squish large gain deltas...

Manual song/track control-records
  Multiple controllable track parameters (mentioned elsewhere) can be controlled in realtime and these changes can be recordedd and replayed
  A song may have a quieter part from 50-1:07 times, louder part from 0:45-55 times, and noises/silence from 0:3-0:44 and 45:00-46 time ranges...
  ...these ranges can be appropriately gained up or down and/or silenced manually and saved...
  ...so that whenever user plays this song later, the controls automatically replay as they were saved...

Allow macro support

Make it HIGHLY customizable (riceable --> Both CLI and GUI):
  Customize prompt ot show combinations of the following information: 
    Command index (a number (1-indexed) that keeps increasing by 1 after every command you issue (empty/non-empty/valid/invalid))
    Current datetime (In multiple formats too, Optionally, also a timezone (either full-name or condensed))
    No of favourited songs
    No of total songs in library
    Time spent listening to current song
    Time spent using the app since current boot
    No of bootups since unboxing
    A badge (Kind of like XP level since unboxing time) which gives users an overall sense of their scrobble/stream count + time spent...
    ...using the app since its unboxing (this info is stored in a salted+peppered hash)...
    ...There are 16 levels of XP

      1)  Novice
      2)  Wanderer
      3)  Explorer
      4)  Whippersnapper
      5)  Trainee
      6)  Veteran
      7)  Melophile
      8)  Melomaniac
      9)  MusicChad
      10) Pro
      11) Summerfester
      12) SoundClouder
      13) Bandcamper
      14) Billboarder
      15) GrammyWinner
      16) G.O.A.T. (Unlocks a secret hidden feature in player) --> But can it be open-source then!??...
            ...maybe yes...using Mariana's own private-databases' GET requests..
            G.O.A.T. member names appear in the publicly accessible "Mariana's Official Open G.O.A.T.s Database" (MOOG-DB)...
            G.O.A.T.s get exclusive MOOG Member-Only perks

Make a GUI version:
  Completely glassy interface --> Make it a part of an app-suite (preferably for OS) with all glass interface (varying blurs/effects)
  Add a minimal-view mode to only see combinations (custom) of:
    Song Name
    Song Artwork | Custom Wallpaper | Solic Colour | One of the many pattern designs
    Realtime Song Lyrics | Scrollable Song Lyrics
    Artist Name

    Change entire look | arrangement | curvature of element corners/edges | bg image
    Add custom effects on button-designs (gradient | solid colours | (dark|bright)ening | filter effects)...
    ...Also add on-hover and on-click animations like Glow | Shimmer | Ripple | ColourTide | ShadowDance | Random
    Thin vs THICCC Progressbar
    Smooth transition when changing/previewing any setting
    Nice feedbaks/hints whenever something happens (including new music news/emails etc...)

  Add Support for realtime effects like:
    Tapestop
    Disk Scratch
    Nightcore
    Vaporwave
    Pitch Modulation/Correction
    BPM Modulation/Correction
    Stem separation
    EQing
    Magic effects (Mystery stuff?)
    Vox effects
    Flanger
    Phaser
    Stereo
    Filters
    Multi-channel outputting
    Reverbs (>10 types)
    Delays
    Distortions
    Compression
    Limiter
    Looping/Stuttering/Glitching


-----------------------------------------------------------------------------------
Footnotes:
*They may not be that famous, but I think they're atleast regular and noticeable when I see them on r/redditsessions...
You guys can tell me more great subs/sites/people if u want, and I might add them!
```

