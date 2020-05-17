#!/usr/bin/env -S python -u

import argparse
import time
import os
import http.client
import json
import sys
from slack import WebClient

twitch_access_token_expires_in = 0 # parameter (seconds in integer)
twitch_access_token = "" # parameter (string)

def main():
    parser = argparse.ArgumentParser(description="YouTube notifications")
    parser.add_argument("-c", "--channel", default="#video", help="Slack channel")
    parser.add_argument("-n", "--notifications", default="#ci",
                        help="Slack channel notifications for errors or warnings")
    parser.add_argument("-i", "--interval", default=30, help="Update interval in seconds", type=int)
    parser.add_argument("-u", "--users", default="", help="YouTube channels")
    args = parser.parse_args()

    slack = WebClient(token=os.environ["SLACK_API_KEY"])

    remember_online_users = []

    YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

    def is_live(user):
        connection = http.client.HTTPSConnection("www.googleapis.com")
        connection.request("GET", ("/youtube/v3/search"
                                   + "?part=snippet"
                                   + "&channelId=" + user
                                   + "&type=video"
                                   + "&eventType=live"
                                   + "&key=" + YOUTUBE_API_KEY))
        return int(json.loads(connection.getresponse().read().decode('utf8'))['pageInfo']['totalResults']) >= 1

    while(True):
        try:
            for user in args.users.split(","):
                if is_live(user):
                    print("YOUTUBE_LIVE: {}".format(user))
                    if user not in remember_online_users:
                        remember_online_users.append(user)
                        slack.chat_postMessage(channel=args.channel,
                                               attachments=[{"text": "YOUTUBE_LIVE: https://www.youtube.com/channel/{}".format(user),
                                                             "color": "#ff0000"}])
                else:
                    if user in remember_online_users:
                        remember_online_users.remove(user)
        except Exception as exception:
            print(exception)
            slack.chat_postMessage(channel=args.notifications,
                                   attachments=[{"text": "ERROR: yeastizzy: Failed to fetch YouTube users status",
                                                 "color": "#ff0000"}])
        print("Online users: {}\n".format(",".join(remember_online_users)))
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
