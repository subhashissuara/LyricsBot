# ------------------------------------------
# Writtern by Subhashis Suara / QuantumBrute
# ------------------------------------------

import praw
import prawcore
import prawcore.exceptions
import time
import datetime
import lyricsgenius
import logging

# --------------------------------------------------------------------------------

subreddit_name = '' # Mention the subreddit that bot should work on
genius = lyricsgenius.Genius("") # Genius APi Authentication

#---------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, filename='LyricsBot_Logs.log', filemode='a', format='%(levelname)s - %(message)s') # Setting up logging
logging.info("--------------------------------------------------")

logging.info("Starting Bot...")
print("Starting Bot...")

logging.info(datetime.datetime.now())

reddit = praw.Reddit(client_id= '',         
                     client_secret= '',
                     username= '',
                     password= '',
                     user_agent= '') # Login to reddit API

logging.info("Logged In!\n")
print("Logged In!\n")

subreddit = reddit.subreddit(subreddit_name)

print("Searching for songs...")

def lyrics():
    for submission in subreddit.new(limit=1):
        if submission.saved:
            continue
        search = submission.title
        if "(" in search:
            search = search.split()
            logging.info(f"Song Post Found! OP: {submission.author}")
            print(f"Song Post Found! OP: {submission.author}")
            submission.save()
            dash_counter = 0
            for dash in search:
                if dash == "-":
                    break
                dash_counter += 1
            artist_name = ' '.join(search[0:(dash_counter)])
            search = ' '.join(search[(dash_counter):len(search)])
            search = search.split()
            for bracket_counter in range(len(search)):
                if "(" in search[bracket_counter]:
                    break
            song_name = ' '.join(search[1:(bracket_counter)])
            song = genius.search_song(song_name, artist_name) # Get lyrics from Genius API
            if song != None:
                reply = f'''{song.lyrics}
                        \n\n^bleep. ^bloop. ^I ^am ^a ^bot!
                        \n_^Contact ^for ^mods ^: ^([here](https://www.reddit.com/message/compose?to=/r/{subreddit_name}))_
                        \n_^Created ^by ^([u/QuantumBrute](https://np.reddit.com/message/compose/?to=QuantumBrute&subject= From {subreddit_name}))_'''
                bot_reply = submission.reply(reply)
                bot_reply.mod.distinguish(sticky=True)
                logging.info("Lyrics posted successfully!\n")
                print("Lyrics posted successfully!\n")
            else:
                logging.warning(song)
                print(song)
                print('\n')
            print("Searching for songs...")




def main():
    while True:
        try:
            lyrics()

        except prawcore.exceptions.RequestException as err:
            logging.warning(f"Reddit API error. Reddit may be unstable. Error: {err}") # f replaces the value of err in {err}, alternative of format

        except praw.exceptions.APIException as err:
            logging.exception(f"API Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except praw.exceptions.ClientException as err:
            logging.exception(f"PRAW Client Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except prawcore.exceptions.ServerError as err:
            logging.warning(f"PRAW Server Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except prawcore.exceptions.NotFound as err:
            logging.exception(f"PRAW NotFound Error! - Sleeping. Error: {err}")
            time.sleep(120)

        except KeyboardInterrupt:
            logging.warning("Caught KeyboardInterrupt")

        except Exception as err:
            logging.critical(
                f"General Exception in main loop - Sleeping 5 min. Error: {err}"
            )
            time.sleep(300)
        

if __name__ == "__main__": 
    main()