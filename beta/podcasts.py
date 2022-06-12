import os
import json
import requests

from collections import OrderedDict
from datetime import datetime as dt
from dateutil import parser as dtparser
from natsort import humansorted

current_date = dt.today().date()

# Unix epoch in "%a, %d %b %Y %H:%M:%S %z" format
# Calculated using dt.utcfromtimestamp(0).strftime("%a, %d %b %Y %H:%M:%S %z")
DEFAULT_TIME = None

# TODO: Add a WHOLE LOT more.... and read from a file instead
# TODO: Better still, get podbeans API to search for urls for you...

# Some predefined podbean podcasts with corresponding links
vendors = {
    "1001tracklists": "https://feed.podbean.com/tracklists/feed.xml",
    "a_date_with_dateline": "https://feeds.megaphone.fm/adatewithdateline",
    "anything_for_selena": "https://rss.wbur.org/anythingforselena/podcast",
    "bishop_td_jakes_full-legnth_sermons_and_interviews": "https://www.spreaker.com/show/2978578/episodes/feed",
    "cleaning_up_the_mental_mess_with_dr._caroline_leaf": "https://anchor.fm/s/236705fc/podcast/rss",
    "crime_junkie": "https://feeds.simplecast.com/qm_9xx0g",
    "critical_role": "https://feed.podbean.com/geekandsundry/feed.xml",
    "dateline_nbc": "https://podcastfeeds.nbcnews.com/dateline",
    "dead_eyes": "https://www.omnycontent.com/d/playlist/77bedd50-a734-42aa-9c08-ad86013ca0f9/2d19c94e-5da0-4ea5-95b1-ad8d012c3386/3c109dc9-8fa7-4ea7-b84b-ad8d012c3390/podcast.rss",
    "dear_hank_&_john": "https://feeds.simplecast.com/9YNI3WaL",
    "down_the_rabbit_hole": "https://feed.podbean.com/downthetrabbitholes/feed.xml",
    "ezra_klein_show": "https://feeds.simplecast.com/82FI35Px",
    "friday_night_comedy_bbc_radio": "https://podcasts.files.bbci.co.uk/p02pc9pj.rss",
    "hbr_ideacast": "http://feeds.harvardbusiness.org/harvardbusiness/ideacast",
    "jocko_podcast": "https://feeds.redcircle.com/64a89f88-a245-4098-8d8d-496325ec4f74",
    "joshua_live_and_the_law_of_attraction": "https://feed.podbean.com/joshualive/feed.xml",
    "life_is_short_with_justin_long": "https://rss.art19.com/life-is-short-with-justin-long",
    "maintenance_phase": "https://feeds.simplecast.com/ZK9BGVQN",
    "mark_levin_podcast": "https://feeds.megaphone.fm/mark-levin-podcast",
    "mental_oasis": "https://feed.podbean.com/mentaloasis/feed.xml",
    "midnight_miracle": "https://feeds.megaphone.fm/LM6964003519",
    "no_such_thing_as_a_fish": "https://audioboom.com/channels/2399216.rss",
    "overcome_depression_+_thrive": "http://overcomedepressionandthrive.com/feed/podcast",
    "overdue": "https://www.omnycontent.com/d/playlist/77bedd50-a734-42aa-9c08-ad86013ca0f9/e7707767-fd61-4887-b6ee-ad88014933e3/b9defaac-c62e-4810-bc36-ad88014933fb/podcast.rss",
    "planet_money": "https://feeds.npr.org/510289/podcast.xml",
    "podnews": "https://podnews.net/rss",
    "projeto_mayhem": "https://feed.podbean.com/projetomayhem/feed.xml",
    "pursuit_of_wonder": "https://podsync.hobbitton.at/Pursuit_of_Wonder.xml",
    "rudolf_steiner_audio": "https://feed.podbean.com/rudolfsteiner/feed.xml",
    "self_improvement_daily": "https://anchor.fm:443/s/471bee4/podcast/rss",
    "storytime_with_seth_rogen": "https://feeds.simplecast.com/ZK9BGVQN",
    "ted_talks_daily": "http://feeds.feedburner.com/TEDTalks_audio",
    "the_blemished_brain": "https://feed.podbean.com/mattiekk/feed.xml",
    "the_daily": "https://feeds.simplecast.com/54nAGcIl",
    "the_daily_show_with_trevor_noah_ears_edition": "https://feeds.megaphone.fm/the-daily-show",
    "the_depression_files": "https://feed.podbean.com/allevin18/feed.xml",
    "the_grant_williams_podcast": "https://feed.podbean.com/ttmygh/feed.xml",
    "the_innerfrench_podcast": "http://podcast.innerfrench.com/feed.xml",
    "the_ken_coleman_show": "https://thekencolemanshow.libsyn.com/rss",
    "the_ramsey_show": "https://daveramsey.libsyn.com/rss",
    "the_survival_podcast": "https://www.thesurvivalpodcast.com/feed/podcast",
    "the_trueman_show": "https://feed.podbean.com/jornluka/feed.xml",
    "VORW_voice_of_the_report_of_the_week": "https://feeds.soundcloud.com/users/soundcloud:users:289346094/sounds.rss",
    "vox_conversations": "https://feeds.megaphone.fm/theezrakleinshow"
}

vendors = OrderedDict(humansorted(vendors.items()))

def get_pub_date(pod, pod_d_type=0):
    pub_date = pod.get('published_date')
    return dtparser.parse(pub_date) if pub_date else DEFAULT_TIME

def refresh_podcast_data(rss_link, output_file):
    from pyPodcastParser.Podcast import Podcast

    response = requests.get(rss_link)
    podcast = Podcast(response.content)
    podcasts_raw = []

    for item in [pod.to_dict() for pod in podcast.items]:
        if item not in podcasts_raw:
            podcasts_raw.append(item)

    with open(output_file, 'w', encoding='utf-8') as fp:
        json.dump({"podcasts_raw": podcasts_raw,
                   "last_write_date": current_date.strftime('%d-%m-%Y')}, fp, indent=3)

    return podcasts_raw

def get_latest_podbean_data(vendor = '', rss_link = None):
    global saved_podcast_data, last_podcast_data_write_date, current_date
    podcasts_raw = None
    saved_podcast_data = None
    last_podcast_data_write_date = None

    if rss_link:
        output_file = 'data/podbean_custom_rss.json'
        podcasts_raw = refresh_podcast_data(rss_link=rss_link, output_file=output_file)
    else:
        rss_link = vendors.get(vendor)
        if not rss_link: return
        output_file = 'data/podbean_{}.json'.format(vendor)

        if os.path.isfile(output_file):
            with open(output_file, 'r', encoding='utf-8') as fp:
                try: saved_podcast_data = json.load(fp)
                except json.decoder.JSONDecodeError: pass

                try: last_podcast_data_write_date = dt.strptime(saved_podcast_data['last_write_date'], '%d-%m-%Y').date()
                except Exception: pass

                # Saved data exists and was successfully loaded
                if saved_podcast_data:
                    if (
                           (last_podcast_data_write_date is not None and \
                            last_podcast_data_write_date < current_date) or not \
                            last_podcast_data_write_date
                        ):
                        # If a write date exists and it's older than today, or if it doesn't exist, refresh the data
                        podcasts_raw = refresh_podcast_data(rss_link=rss_link, output_file=output_file)
                    else:
                        # Load existing data, because it is already up to date
                        podcasts_raw = saved_podcast_data['podcasts_raw']
                else:
                    # Data is corrupt/incomplete, refresh the data
                    podcasts_raw = refresh_podcast_data(rss_link=rss_link, output_file=output_file)
        else:
            # No data exists, refresh the data
            podcasts_raw = refresh_podcast_data(rss_link=rss_link, output_file=output_file)



    # podcast_urls = [pod.get('enclosure_url') for pod in podcasts_raw]
    podcasts = [{'is_explicit':  pod.get('itunes_explicit'),
                 'caption':      pod.get('itunes_subtitle'),
                 'artwork':      pod.get('itune_image'),
                 'url':          pod.get('enclosure_url'),
                 'pub_date':     get_pub_date(pod),
                 'title':        pod.get('title')} for pod in podcasts_raw]

    # return podcasts

    # Sorting podcasts by date of publish (newest first)
    podcasts.sort(key=lambda x: x['pub_date'],
                  reverse=True)

    return podcasts


# podnews_rss_url = 'https://podnews.net/rss'
# response = requests.get(podnews_rss_url)
# podcast = Podcast(response.content)

if __name__ == "__main__":
    os.chdir('..')
    final = get_latest_podbean_data('bishop_td_jakes_full-legnth_sermons_and_interviews')
    print(final)
