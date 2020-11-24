import requests
import json
import re
import utils

api_base_url = "https://dev.takamaka.io/api/V2/testapi/"

api_listtransactions = api_base_url + "listtransactions"


def listtransactionspost(address):
    with requests.session() as s:
        data = {'address': address}
        r = s.post(api_listtransactions, data=data)
    result = ""
    if r.text != "":
        result = json.loads(r.text)
    return result


def main():
    from_address = ['sZh2gyX7qDu8mAQBWDvDyij6zL1VSHr2-k8nFAP7AB8.', '7COyhKDyouXbtvi48jxFwC7pMG3eXqrW7Al4hjFab0w.',
                    'Msun9pWhL4MeyEgz-DegzqQWOT5Z-TE1WxSqy2YFZ5I.']

    siths = utils.load_resource("siths.txt")
    api = utils.get_api_tweepy()

    for single_from in from_address:
        trx_list = listtransactionspost(single_from)
        twitter_users_to_be_processed = {}

        for single_trx in trx_list:
            if single_trx['SITH'] not in siths and 'message' in single_trx \
                    and single_trx['message'] != '' \
                    and re.search('tw_user_id=\d{1,}tw_user_name=(.*)tw_id_reply_to=(.*)',
                                  single_trx['message']) is not None:
                twitter_users_to_be_processed[single_trx['message'].split("tw_id_reply_to=")[
                    1]] = "Thank you @{} for your interest, check your balance ;-)".format(
                    single_trx['message'].split("tw_user_name=")[1].split("tw_id_reply_to")[0])
                #

                siths.append(single_trx['SITH'])
                utils.update_resource(siths, 'siths.txt')

        if len(twitter_users_to_be_processed.items()) > 0:
            for tweet_reply_to_id, msg in twitter_users_to_be_processed.items():
                api.update_status(msg, tweet_reply_to_id)


if __name__ == "__main__":
    main()
