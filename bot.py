import telepot, requests, re, random, time, urllib3
from telepot.loop import MessageLoop
from datetime import datetime as dt
from data import *
import wikipedia
from bs4 import BeautifulSoup
import wordninja


def ch_wiki(query, chat_id, msg_id, long=False):
    try:
        if long:
            bot.sendMessage(chat_id, wikipedia.summary(query, sentences=8),
                            reply_to_message_id=msg_id)
        else:
            bot.sendMessage(chat_id, wikipedia.summary(query, sentences=2),
                            reply_to_message_id=msg_id)
    except Exception:
        bot.sendMessage(chat_id, "Oops, please try again!",
                        reply_to_message_id=msg_id)


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


def ch_weather(chat_id, msg_id, city='Singapore'):
    # using openweathermap.org API
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city, w_key)
    r = requests.get(url).json()
    if r['cod'] != '404':
        data = r['main']
        curr_temp = data['temp']
        curr_pres = data['pressure']
        curr_hum = data['humidity']
        desc = r['weather'][0]['description']

        ch_response = f"*{city.capitalize()}*\n\n" + \
                      f"Temperature: {curr_temp} \u2103\n" + \
                      f"Pressure: {curr_pres} hPa\n" + \
                      f"Humidity: {curr_hum} %\n" + \
                      f"Description: {desc}"
        bot.sendMessage(chat_id, ch_response, parse_mode='Markdown',
                        reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id, "Oops, please try again!",
                        reply_to_message_id=msg_id)


def ch_transit(chat_id, msg_id, origin, destination):
    o = origin.replace(' ', '+')
    d = destination.replace(' ', '+')
    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
    mode = 'transit'
    api_key = gm_key
    nav_request = f"origin={o}&destination={d}&mode={mode}&key={api_key}"
    response = requests.get(base_url + nav_request).json()
    if response['status'] != 'OK':
        bot.sendMessage(chat_id, "Oops, please refine your search!",
                        reply_to_message_id=msg_id)
        return

    routes = response['routes'][0]
    ch_response = f"Duration: {routes['legs'][0]['duration']['text']}\n"
    step = 1
    for r in routes['legs'][0]['steps']:
        ch_response += f"\n{step}. {r['html_instructions']}"
        if r['travel_mode'] == 'TRANSIT':
            ch_response += f"\n - Alight at {r['transit_details']['arrival_stop']['name']}"
        elif r['travel_mode'] == 'WALKING':
            sub_r = r['steps']
            for s in sub_r:
                if 'html_instructions' in s.keys():
                    text = BeautifulSoup(s['html_instructions'], features='html.parser').get_text()
                    # fuck you html
                    raw_text = text.split(' ')
                    processed_text = []
                    for i in range(len(raw_text)):
                        if "Destination" in raw_text[i] or "Take" in raw_text[i]:
                            processed_text.append(' '.join(wordninja.split(raw_text[i])))
                        else:
                            processed_text.append(raw_text[i])

                    text = ' '.join(processed_text)
                    # text = ' '.join(wordninja.split(text))
                    ch_response += f"\n - {text}"
        ch_response += '\n'
        step += 1

    bot.sendMessage(chat_id, ch_response, reply_to_message_id=msg_id)


def ch_define(chat_id, query, msg_id):
    # using Oxford Dictionaries API
    endpoint = "entries"
    language_code = "en-us"
    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + query.lower()
    r = requests.get(url, headers = {"app_id": od_app_id, "app_key": od_key})
    if r.status_code == 200:
        senses = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = [senses[i]['definitions'] for i in range(len(senses))]
        query_formatted = query.lower().capitalize()
        ch_response = f"*{query_formatted}*\n\n"
        if len(definitions) > 1:
            count = 1
            for d in definitions:
                ch_response += f"{str(count)}. {d[0].capitalize()}\n\n"
                count += 1
        else:
            ch_response += f"{definitions[0][0].capitalize()}\n\n"
        bot.sendMessage(chat_id, ch_response.rstrip(), parse_mode='Markdown',
                        reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id, "Oop, please try again!",
                        reply_to_message_id=msg_id)


def ch_cap(grades, chat_id, msg, msg_id):
    denom = 0
    try:
        for i in range(len(grades)):
            if grades[i] < 0:
                raise Exception
            denom += grades[i]
            grades[i] = int(grades[i]) * g_scores[i]
        total = sum(grades)
        cap = round(total/denom, 2)
        #target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, "CAP: " + str(cap),
                        reply_to_message_id=msg_id)
    except:
        bot.sendMessage(chat_id, "Sorry, invalid input!",
                        reply_to_message_id=msg_id)


def get_user(uid):
    return bot.getChat(uid)['first_name']


def command_handle(chat_id, msg, msg_id, cmd, text=''):
    # HELP
    if cmd == 'help' or cmd == 'help@tebby_bot':
        response = "tebby lives to serve:\n"
        for c in avail_cmd:
            response += c + "\n"
        bot.sendMessage(chat_id, response.rstrip())

    # 8BALL
    elif cmd == '8ball' and text:
        bot.sendMessage(chat_id, random.choice(ball_response),
                        reply_to_message_id=msg_id)

    # SLAP
    elif cmd == 'slap':
        if len(text) > 1:
            target = " ".join(text[1:])
        else:
            target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, target + " " + random.choice(slap))

    # WIKI
    elif cmd == 'wiki' and text:
        ch_wiki(text, chat_id, msg_id)
    elif cmd == 'wikilong' and text:
        ch_wiki(text, chat_id, msg_id, long=True)

    # CAP CALCULATOR
    elif cmd == 'cap':
        grades = list(map(int, list(text)))
        ch_cap(grades, chat_id, msg, msg_id)

    # WEATHER
    elif cmd == 'weather':
        if text:
            ch_weather(chat_id, msg_id, text)
        else:
            ch_weather(chat_id, msg_id)

    # DIRECTIONS - TRANSIT
    elif cmd == 'transit':
        origin, destination = text.split(' ; ')
        if not origin or not destination:
            bot.sendMessage(chat_id, "Oops, please try again!",
                            reply_to_message_id=msg_id)
        else:
            ch_transit(chat_id, msg_id, origin, destination)

    # DEFINITION
    elif cmd == 'define' and text:
        query = text
        ch_define(chat_id, query, msg_id)

    # CAT
    elif cmd == 'cat':
        bot.sendPhoto(chat_id, cat(), caption=random.choice(captions),
                      reply_to_message_id=msg_id)

    # DOG
    elif cmd == 'dog':
        bot.sendPhoto(chat_id, dog(), caption=random.choice(captions),
                      reply_to_message_id=msg_id)


def admin_handle(text):
    # ANNOYING TOGGLE
    if text[0] == 'annoy':
        global annoy_mode
        if text[1] == 'off':
            annoy_mode = False
        elif text[1] == 'on':
            annoy_mode = True
        print("annoy_mode has been set to:", annoy_mode)
    # TWSS TOGGLE
    elif text[0] == 'twss':
        global twss_mode
        if text[1] == 'off':
            twss_mode = False
        elif text[1] == 'on':
            twss_mode = True
        print("twss_mode has been set to:", twss_mode)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    msg_id = telepot.message_identifier(msg)[1]
    print(dt.now().strftime("%H:%M:%S"), content_type, chat_type, chat_id, end=' ')

    if content_type == 'text':
        text = msg['text']
        uid = msg['from']['id']
        print(get_user(uid))
        #print("{user} : {msg}".format(user=get_user(uid), msg=text))

        # COMMANDS
        if text.startswith('/'):
            lst = text[1:].split(' ')
            if len(lst) > 1:
                command_handle(chat_id, msg, msg_id, lst[0], ' '.join(lst[1:]))
            else:
                command_handle(chat_id, msg, msg_id, lst[0])
            return

        # ADMIN COMMANDS
        elif text.startswith('!'):
            admin_handle(text[1:].split())
            return

        # GREETINGS
        elif 'teb' in text.lower():
            bot.sendMessage(chat_id, random.choice(intro))

        # ANNOYING MODE
        elif annoy_mode:
            # OVER-GREET
            if any(word in greets for word in text.lower().split()):
                bot.sendMessage(chat_id, random.choice(intro))
            # CAT
            elif 'cat' in text.lower():
                bot.sendPhoto(chat_id, cat(), caption=random.choice(captions))
            # DOG
            elif 'dog' in text.lower():
                bot.sendPhoto(chat_id, dog(), caption=random.choice(captions))
        # TWSS MODE
        elif twss_mode and set(text.lower().split()).intersection(twss):
            bot.sendMessage(chat_id, "That's what she said.")

    else:
        print()


# Main loop runs here
bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()
print('Bot initialized :)')
annoy_mode = False
twss_mode = True
while 1:
    time.sleep(30)
