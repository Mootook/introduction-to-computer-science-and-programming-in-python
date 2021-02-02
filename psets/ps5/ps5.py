# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:
import re
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
  def __init__(self, guid, title, description, link, pubdate):
    self.guid = guid
    self.title = title
    self.description = description
    self.link = link
    self.pubdate = pubdate
  
  def get_guid(self):
    return self.guid

  def get_title(self):
    return self.title

  def get_description(self):
    return self.description

  def get_link(self):
    return self.link

  def get_pubdate(self):
    story_pubdate = self.pubdate
    if story_pubdate.tzinfo == None:
      story_pubdate = story_pubdate.replace(tzinfo=pytz.timezone("EST"))
    else:
      story_pubdate = story_pubdate.astimezone(pytz.timezone("EST"))
    return story_pubdate



#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
class Trigger(object):
  def evaluate(self, story):
    """Returns True if an alert should be
    generatedfor the given news item, or False otherwise."""
    raise NotImplementedError
# Problem 2
class PhraseTrigger(Trigger):
  def __init__(self, phrase):
    super().__init__()
    self.phrase = phrase
  
  def is_phrase_in(self, text):
    parse = text 
    for c in string.punctuation:
      parse = parse.replace(c, ' ')
    ret_string  = " ".join(parse.split()).lower()
    phrase = self.phrase.lower()
    return re.search(r'\b' + phrase + r'\b', ret_string)

# Problem 3
class TitleTrigger(PhraseTrigger):
  def __init__(self, phrase):
    super().__init__(phrase)

  def evaluate(self, story):
    return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
  def __init__(self, phrase):
    super().__init__(phrase)

  def evaluate(self, story):

    return self.is_phrase_in(story.get_description())
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
class TimeTrigger(Trigger):
  def __init__(self, time):
    super().__init__()
    self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
  def evaluate(self, story):
    return story.get_pubdate() < self.time

class AfterTrigger(TimeTrigger):
  def evaluate(self, story):
    return story.get_pubdate() > self.time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
  def __init__(self, trigger):
    super().__init__()
    self.t = trigger

  def evaluate(self, story):
    return not self.t.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
  def __init__(self, t1, t2):
    super().__init__()
    self.t1 = t1 
    self.t2 = t2
  
  def evaluate(self, story):
    return self.t1.evaluate(story) and self.t2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
  def __init__(self, t1, t2):
    super().__init__()
    self.t1 = t1 
    self.t2 = t2

  def evaluate(self, story):
    return self.t1.evaluate(story) or self.t2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    print(triggerlist)
    parsed_stories = []
    for s in stories:
      for t in triggerlist:
        if t.evaluate(s):
          parsed_stories.append(s)
    return parsed_stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_dict = {}
    triggers_to_add = [] # read off trigger_dict for each index
    for trigger in lines:
      trigger_spec = trigger.split(',')
      if trigger_spec[0] == 'ADD':
        triggers_to_add += trigger_spec[1:]
      else:
        trigger_name = trigger_spec[0]
        trigger_type = trigger_spec[1]
        if trigger_type == "TITLE":
          trigger_phrase = trigger_spec[2]
          trigger_dict[trigger_name] = TitleTrigger(trigger_phrase)
        elif trigger_type == "DESCRIPTION":
          trigger_phrase = trigger_spec[2]
          trigger_dict[trigger_name] = DescriptionTrigger(trigger_phrase)
        elif trigger_type == "AFTER":
          trigger_time = trigger_spec[2]
          trigger_dict[trigger_name] = AfterTrigger(trigger_time)
        elif trigger_type == "BEFORE":
          trigger_time = trigger_spec[2]
          trigger_dict[trigger_name] = BeforeTrigger(trigger_time)
        elif trigger_type == "NOT":
          not_trigger = trigger_spec[2]
          trigger_dict[trigger_name] = NotTrigger(trigger_dict[not_trigger])
        elif trigger_type == "AND":
          trigger_one = trigger_spec[2]
          trigger_two = trigger_spec[3]
          trigger_dict[trigger_name] = AndTrigger(trigger_dict[trigger_one], trigger_dict[trigger_two])
        elif trigger_type == "OR":
          trigger_one = trigger_spec[2]
          trigger_two = trigger_spec[3]
          trigger_dict[trigger_name] = OrTrigger(trigger_dict[trigger_one], trigger_dict[trigger_two])
    res_triggers = map(lambda t: trigger_dict[t], triggers_to_add)
    return res_triggers




SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # Commented because Yahoo throws an error
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

