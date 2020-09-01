import praw
import string
import re
from collections import Counter
from praw.models import Comment
from praw.models import Submission

searchingtext = '#The winner is: ['
parentSearchText = '/u/BoyAndHisBot '

masterList = {}

def init():
    reddit = praw.Reddit(<username_here>)
    reddit.read_only = True
    buildHistorgramOfDeath(reddit, "BoyAndHisBot")
    # print(masterList)
    print(f"Have records of {len(masterList)} different raffle spots")
    inputLoop()

def buildHistorgramOfDeath(redditInstance, userName):
    comments = redditInstance.redditor(userName).comments.new(limit=None)
    winningnumbers = {}
    counters = {}
    for comment in comments:
        parentBody = comment.parent().body
        if comment.body.startswith(searchingtext) and parentBody.lower() != '[deleted]':
            # print(comment.parent().body)
            outOf = re.search(r'\/?u\/BoyAndHisBot (.*)', parentBody, re.IGNORECASE)
            # if(int(outOf.group(1)) > 100):
            #     continue
            result = re.search(r'#The winner is: \[(.*)\]', comment.body)
            # print (result)
            results = winningnumbers.get(outOf.group(1), [])
            results.append(result.group(1))
            winningnumbers[outOf.group(1)] = results

    for key in winningnumbers:
        val = winningnumbers[key]
        cnt = Counter()
        for number in val:
            cnt[number] += 1
        counters[key] = cnt
    global masterList
    masterList = counters

def inputLoop():
    val = ''
    while val != 'quit':
        val = input('How many slots: ')
        if val != 'quit':
            try:
                print(masterList[val])
            except KeyError:
                print(f"No entries for {val} slots")


init()