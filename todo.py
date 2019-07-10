#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime, timedelta

# TODO: calendar view, like a calendar app
#   an idea is to make neat button DOMs after file names.
#   use shelve for local db of current files, and render from that db
#   Some shelve module, and sort into monthly buckets, create link DOM
#   for each filename in bucket
TODAY = datetime.now()


def ordinal(monthDay):
    ordInd = ["th", "st", "nd", "rd"]

    if monthDay % 10 in [1, 2, 3] and monthDay not in [11, 12, 13]:
        return ordInd[monthDay % 10]
    else:
        return ordInd[0]


def latestNum():
    filenums = set()
    for file in os.listdir('.'):
        filename = os.fsdecode(file)
        if filename.endswith(".md"):
            try:
                filenums.add(int(re.search(r'[0-9]+', filename).group()))
            except:
                continue
    return max(filenums)


def checkToday():
    latestMD = f"td{latest}.md"
    with open(latestMD) as f:
        firstline = f.readline()

    if re.findall(r'(\d+)', firstline)[1] == TODAY.strftime("%Y%m%d"):
        print(f"{latestMD} already exists")
        os.system(f"vi {latestMD}")
        return True
    return False


def retrieveLatest():
    latestMD = f"td{latest}.md"
    with open(latestMD) as f:
        firstline = f.readline()
        theRest = f.read()

    newFirstline = firstline[:-13] + TODAY.strftime("%Y%m%d") + ".md)\n"

    with open(latestMD, "w") as f:
        f.write(newFirstline)
        f.write(theRest)

    return '\n'.join(
        re.findall(r'(\-   \[ \] .+)', theRest)
    )


def makenew():
    today = TODAY.strftime("%Y%m%d")
    firstline = f'[<-](./td{latest}.md) {today} [->](./td{today}.md)'

    # TODO: modify latest post's top line to link to today
    # copy tasks from previous entry
    tasks = retrieveLatest()
    # with open(f'td{latest}.md') as f:
    #     tasks = '\n'.join(
    #         re.findall(r'(\-   \[ \] .+)', f.read())
    #     )

    template = f"""
---
#### Yesterday:
###### What did I learn?
-   

###### What did I read?
-   

###### What did I do to help my future?
-   

#### Now:


#### Today ({TODAY.strftime("%A")}):
###### Events:


###### Outcomes, Goals, Questions:
{tasks}

###### Accomplishments:
-   

"""
    # date header
    date = int(TODAY.strftime('%-d'))
    footer = f'<title>\n    Todo | {TODAY.strftime("%B")} {date}{ordinal(date)}\n</title>'

    # create file
    newMD = f'td{TODAY.strftime("%Y%m%d")}.md'
    with open(newMD, 'w+') as f:
        f.write(firstline)
        f.write(template)
        f.write(footer)

    # run command
    print(f"{newMD} created")
    # os.system(f"vi {newMD}")

if __name__ == "__main__":
    latest = latestNum()

    # input mode
    if len(sys.argv) == 1:
        mode = 'new'
    elif len(sys.argv) == 2:
        mode = sys.argv[1]
    else:
        mode = input("(n)ew / (v)iew: ")
        # mode = None

    if re.match(r'n|e', mode) != None:  # new | edit
        if not checkToday():
            makenew()
    elif re.match(r'v', mode) != None:  # view in chrome
        print(f"opening td{latest}.md")
        os.system(f'open -a "Google Chrome" td{latest}.md')
    elif re.match(r'test', mode) != None:  # test
        updateLatest()
        pass

