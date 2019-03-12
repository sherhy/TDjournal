#!/usr/bin/env python3
import os, re, sys
from datetime import datetime, timedelta

# TODO: arrow keys for navigation
# TODO: calendar view, like a calendar app
TODAY = datetime.now()
def ordinal(monthDay):
    ordInd = ["th", "st", "nd", "rd"]

    if monthDay % 10 in [1, 2, 3] and monthDay not in [11, 12, 13]:
        return ordInd[monthDay % 10]
    else:
        return ordInd[0]

# TODO: change naming scheme to dates, but in a way that's 
#       backwards compatible and can be later removed
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
        print(f"opening existing file: {latestMD}")
        os.system(f"vi {latestMD}")
        return True
    return False

# TODO: copy tasks from previous entry
def makenew():
    tomorrow = (TODAY + timedelta(days=1)).strftime("%Y%m%d")
    # TODO: broken link when firstline's tomorrow file doesn't exist
    firstline = f'[<-](./td{latest}.md) { TODAY.strftime("%Y%m%d")} [->](./td{tomorrow}.md)'

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
- 

###### Outcomes, Tasks, Questions:
- 

###### Accomplishments:
- 

"""
    
    date = int(TODAY.strftime('%-d'))
    footer = f'<title>Todo | {TODAY.strftime("%B")} {date}{ordinal(date)}</title>'

    # create file
    newMD = f'td{TODAY.strftime("%Y%m%d")}.md'
    with open(newMD, 'w+') as f:
        f.write(firstline)
        f.write(template)
        f.write(footer)

    # run command
    print(f"vi {newMD}")
    os.system(f"vi {newMD}")

if __name__=="__main__":
    latest = latestNum()
    
    # input mode
    if len(sys.argv) == 1: mode = input("(n)ew / (v)iew: ")
    elif len(sys.argv) == 2: mode = sys.argv[1]   
    else: mode = None

    if re.match(r'n|e',mode) != None: #new | edit
        if not checkToday(): 
            makenew()
    elif re.match(r'v',mode) != None: #view
        print(f"opening td{latest}.md")
        os.system(f"open td{latest}.md")
    else: print("comon")
