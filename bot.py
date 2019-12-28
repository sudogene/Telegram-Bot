import telepot, requests, re, random, time, json
from telepot.loop import MessageLoop
from datetime import datetime as dt
from data import *
import wikipedia


def wiki(query, chat_id, long=False):
    try:
        if long:
            bot.sendMessage(chat_id, wikipedia.summary(query))
        else:
            bot.sendMessage(chat_id, wikipedia.summary(query, sentences=2))
    except Exception as ex:
        bot.sendMessage(chat_id, str(ex))
        
def cat():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    return contents[0]['url']

def dog_helper():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def dog():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = dog_helper()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def ch_weather(chat_id, city='Singapore'):
    # using openweathermap.org API
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city, w_key)
    r = requests.get(url).json()
    if r['cod'] != '404':
        data = r['main']
        curr_temp = data['temp']
        curr_pres = data['pressure']
        curr_hum = data['humidity']
        desc = r['weather'][0]['description']

        ch_response = city + "\n\n" + \
                      f"Temperature: {curr_temp} \u2103\n" + \
                      f"Pressure: {curr_pres} hpa\n" + \
                      f"Humidity: {curr_hum} %\n" + \
                      f"Description: {desc}"
        bot.sendMessage(chat_id, ch_response)
    else:
        bot.sendMessage(chat_id, "Oops, please try again!")

def ch_define(chat_id, query):
    # using Oxford Dictionaries API
    endpoint = "entries"
    language_code = "en-us"
    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + query.lower()
    r = requests.get(url, headers = {"app_id": od_app_id, "app_key": od_key})
    if r.status_code == 200:
        definitions = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
        ch_response = query.lower() + "\n"
        for d in definitions:
            ch_response += d + "\n"
        bot.sendMessage(chat_id, ch_response.rstrip())
    else:
        bot.sendMessage(chat_id, "Oop, please try again!")
    

def ch_cap(grades, chat_id, msg):
    denom = 0
    try:
        for i in range(len(grades)):
            if grades[i] < 0:
                raise Exception
            denom += grades[i]
            grades[i] = int(grades[i]) * g_scores[i]
        total = sum(grades)
        cap = round(total/denom, 2)
        target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, target + "'s CAP: " + str(cap))
    except:
        bot.sendMessage(chat_id, "Sorry, invalid input!")

def get_user(uid):
    return bot.getChat(uid)['first_name']

def command_handle(text, chat_id, msg):
    # HELP
    if text[0] == 'help':
        response = "tebby lives to serve:\n"
        for cmd in avail_cmd:
            response += cmd + "\n"
        bot.sendMessage(chat_id, response.rstrip())

    # 8BALL
    elif text[0] == '8ball' and len(text) > 1:
        bot.sendMessage(chat_id, random.choice(ball_response))
    
    # SLAP
    elif text[0] == 'slap':
        if len(text) > 1:
            target = " ".join(text[1:])
        else:
            target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, target + " " + random.choice(slap))

    # WIKI
    elif text[0] == 'wiki':
        wiki(" ".join(text[1:]), chat_id)
    elif text[0] == 'wikilong':
        wiki(" ".join(text[1:]), chat_id, long=True)

    # CAP CALCULATOR
    elif text[0] == 'cap':
        grades = list(map(int, list(text[1:])))
        ch_cap(grades, chat_id, msg)
    
    # WEATHER
    elif text[0] == 'weather':
        if len(text) > 1:
            ch_weather(chat_id, ' '.join(text[1:]))
        else:
            ch_weather(chat_id)

    # DEFINITION
    elif text[0] == 'define' and len(text) > 1:
        query = ' '.join(text[1:])
        ch_define(chat_id, query)



def admin_handle(text):
    # ANNOYING TOGGLE
    if text[0] == 'ann':
        global annoying
        if text[1] == 'off':
            annoying = False
        elif text[1] == 'on':
            annoying = True
        print("Annoying has been set to:", annoying)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(dt.now().strftime("%H:%M:%S"), content_type, chat_type, chat_id, end=' ')

    if content_type == 'text':
        text = msg['text']
        uid = msg['from']['id']
        print("{user} : {msg}".format(user=get_user(uid), msg=text))

        # COMMANDS
        if text.startswith('/'):
            command_handle(text[1:].split(), chat_id, msg)
            return
        # ADMIN COMMANDS
        elif text.startswith('!'):
            admin_handle(text[1:].split())
            return
        
        # CAT
        elif 'cat' in text.lower():
            bot.sendPhoto(chat_id, cat(), caption=random.choice(captions))
        # DOG
        elif 'dog' in text.lower():
            bot.sendPhoto(chat_id, dog(), caption=random.choice(captions))
        
        elif set(text.lower().split()).intersection(twss):
            bot.sendMessage(chat_id, "That's what she said")

        # GREETINGS
        elif 'teb' in text.lower():
            bot.sendMessage(chat_id, random.choice(intro))
        elif annoying:
            if any(word in greets for word in text.lower().split()):
                bot.sendMessage(chat_id, random.choice(intro))
        
    else:
        print()





# Main loop runs here
bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()
print('Initialised.')
annoying = False
while 1:
    time.sleep(10)

