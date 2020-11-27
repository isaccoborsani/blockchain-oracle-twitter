import os
import re
import utils
import time
import datetime


def clean_twitter_users():
    twitter_users = utils.load_resource("twitter_users.txt")
    cleaned_twitter_users = []
    for single_user_row in twitter_users:
        t1 = datetime.datetime.fromtimestamp(float(single_user_row.split(" ")[1]) / 1000.0)
        t2 = datetime.datetime.fromtimestamp(time.time())
        difference = t2 - t1
        if difference.seconds < 300:
            cleaned_twitter_users.append(single_user_row)

    return cleaned_twitter_users


def get_twitter_user_ids(twitter_users):
    ret = []
    for single in twitter_users:
        ret.append(int((single.split(" ")[0])))

    return ret


def main():
    bash_command = "java -cp ./takamakachain-1.0-SNAPSHOT-jar-with-dependencies.jar " \
                   " -Djava.awt.headless=true " \
                   "com.h2tcoin.takamakachain.main.DirectCall -e=test -w=walletIsacco -s=asdasdasd -i=0 -p=\"{} 10 " \
                   "10\" -m=\"tw_user_id={}tw_user_name={}tw_id_reply_to={}\" "

    api = utils.get_api_tweepy()
    mentions = api.mentions_timeline(count=10)

    already_processed_mentions = utils.load_resource("already_processed_mentions.txt")

    last_twitter_users = clean_twitter_users()
    twitter_user_ids = get_twitter_user_ids(last_twitter_users)

    for tweet in mentions:
        tweet_id = str(tweet.id)
        if tweet_id not in already_processed_mentions:
            already_processed_mentions.append(str(tweet.id))
            m = re.search('[0-9a-zA-Z\.\_\-]{44}', tweet.text)

            if str(tweet.user.id) not in twitter_user_ids and m is not None:
                os.system(bash_command.format(m.group(0), tweet.user.id, tweet.user.screen_name, tweet.id))
                last_twitter_users.append(str(tweet.user.id) + " " + str(round(time.time() * 1000)))
            else:
                continue

    utils.update_resource(last_twitter_users, 'twitter_users.txt')
    utils.update_resource(already_processed_mentions, 'already_processed_mentions.txt')


if __name__ == "__main__":
    main()
