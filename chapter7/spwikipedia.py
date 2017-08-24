"""
Example Route To Construct:

https://wikimedia.org/api/rest_v1/ +
metrics/pageviews/per-article/ +
en.wikipedia/all-access/user/ +
LeBron_James/daily/2015070100/2017070500 +

"""
import requests
import pandas as pd
import time
import wikipedia

BASE_URL =\
 "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user"

def construct_url(handle, period, start, end):
    """Constructs a URL based on arguments

    Should construct the following URL:
    /LeBron_James/daily/2015070100/2017070500 
    """

    
    urls  = [BASE_URL, handle, period, start, end]
    constructed = str.join('/', urls)
    return constructed

def query_wikipedia_pageviews(url):

    res = requests.get(url)
    return res.json()

def wikipedia_pageviews(handle, period, start, end):
    """Returns JSON"""

    constructed_url = construct_url(handle, period, start,end)
    pageviews = query_wikipedia_pageviews(url=constructed_url)
    return pageviews

def wikipedia_2016(handle,sleep=0):
    """Retrieve pageviews for 2016""" 
    
    print("SLEEP: {sleep}".format(sleep=sleep))
    time.sleep(sleep)
    pageviews = wikipedia_pageviews(handle=handle, 
            period="daily", start="2016010100", end="2016123100")
    if not 'items' in pageviews:
        print("NO PAGEVIEWS: {handle}".format(handle=handle))
        return None
    return pageviews

def create_wikipedia_df(handles):
    """Creates a Dataframe of Pageviews"""

    pageviews = []
    timestamps = []    
    names = []
    wikipedia_handles = []
    for name, handle in handles.items():
        pageviews_record = wikipedia_2016(handle)
        if pageviews_record is None:
            continue
        for record in pageviews_record['items']:
            pageviews.append(record['views'])
            timestamps.append(record['timestamp'])
            names.append(name)
            wikipedia_handles.append(handle)
    data = {
        "names": names,
        "wikipedia_handles": wikipedia_handles,
        "pageviews": pageviews,
        "timestamps": timestamps 
    }
    df = pd.DataFrame(data)
    return df    


def create_wikipedia_handle(raw_handle):
    """Takes a raw handle and converts it to a wikipedia handle"""

    wikipedia_handle = raw_handle.replace(" ", "_")
    return wikipedia_handle

def create_wikipedia_nba_handle(name):
    """Appends basketball to link"""

    url = " ".join([name, "(basketball)"])
    return url

def wikipedia_current_nba_roster():
    """Gets all links on wikipedia current roster page"""

    links = {}
    nba = wikipedia.page("List_of_current_NBA_team_rosters")
    for link in nba.links:
        links[link] = create_wikipedia_handle(link)
    return links

def guess_wikipedia_nba_handle(data="data/nba_2017_br.csv"):
    """Attempt to get the correct wikipedia handle"""

    links = wikipedia_current_nba_roster() 
    nba = pd.read_csv(data)
    count = 0
    verified = {}
    guesses = {}
    for player in nba["Player"].values:
        if player in links:
            print("Player: {player}, Link: {link} ".format(player=player,
                 link=links[player]))
            print(count)
            count += 1
            verified[player] = links[player] #add wikipedia link
        else:
            print("NO MATCH: {player}".format(player=player))
            guesses[player] = create_wikipedia_handle(player)
    return verified, guesses

def validate_wikipedia_guesses(guesses):
    """Validate guessed wikipedia accounts"""

    verified = {}
    wrong = {}
    for name, link in guesses.items():
        try:
            page = wikipedia.page(link)
        except (wikipedia.DisambiguationError, wikipedia.PageError) as error:
            #try basketball suffix
            nba_handle = create_wikipedia_nba_handle(name)
            try:
                page = wikipedia.page(nba_handle)
                print("Initial wikipedia URL Failed: {error}".format(error=error))
            except (wikipedia.DisambiguationError, wikipedia.PageError) as error:
                print("Second Match Failure: {error}".format(error=error))
                wrong[name] = link
                continue
        if "NBA" in page.summary:
            verified[name] = link
        else:
            print("NO GUESS MATCH: {name}".format(name=name))
            wrong[name] = link
    return verified, wrong

def clean_wikipedia_handles(data="data/nba_2017_br.csv"):
    """Clean Handles"""

    verified, guesses = guess_wikipedia_nba_handle(data=data)
    verified_cleaned, wrong = validate_wikipedia_guesses(guesses)
    print("WRONG Matches: {wrong}".format(wrong=wrong))
    handles = {**verified, **verified_cleaned}
    return handles

def nba_wikipedia_dataframe(data="data/nba_2017_br.csv"):
    handles = clean_wikipedia_handles(data=data)
    df = create_wikipedia_df(handles)    
    return df

def create_wikipedia_csv(data="data/nba_2017_br.csv"):
    df = nba_wikipedia_dataframe(data=data)
    df.to_csv("data/wikipedia_nba.csv")


if __name__ == "__main__":
    create_wikipedia_csv() 