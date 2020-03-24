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
    ch_response += f"Distance: {routes['legs'][0]['distance']['text']}\n"
    step = 1
    for r in routes['legs'][0]['steps']:
        ch_response += f"\n{step}. {r['html_instructions']} ({r['distance']['text']})"
        if r['travel_mode'] == 'TRANSIT':
            td = r['transit_details']
            arr = td['arrival_stop']['name']
            if td['line']['vehicle']['type'] == 'SUBWAY':
                ch_response += f"\n - Alight at {arr} ({td['line']['name']}, {td['num_stops']} stop)"
            elif td['line']['vehicle']['type'] == 'BUS':
                ch_response += f"\n - Alight at {arr} (Bus {td['line']['name']}, {td['num_stops']} stop)"
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
                    ch_response += f"\n - {text} ({s['distance']['text']})"
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

def ch_roll(num_side, num_roll, chat_id, msg_id):
    if num_roll > 100:
        bot.sendMessage(chat_id, "Oops, too malicious!",
                        reply_to_message_id=msg_id)
        return
    res = []
    try:
        for i in range(num_roll):
            res.append(str(random.randint(1, num_side)))
        ch_response = ", ".join(res)
        bot.sendMessage(chat_id, ch_response,
                        reply_to_message_id=msg_id)
    except:
        bot.sendMessage(chat_id, "Oops, too malicious!",
                        reply_to_message_id=msg_id)

def get_user(uid):
    return bot.getChat(uid)['first_name']


def command_handle(chat_id, msg, msg_id, cmd, text=''):
    # HELP
    if cmd == 'help' or cmd == 'help@tebby_bot':
        response = "Tebby lives to serve:\n"
        for c in avail_cmd:
            response += c + "\n"
        bot.sendMessage(chat_id, response.rstrip())
    # HELP-media
    if cmd == 'media':
        response = "Tebby has an assortment:\n"
        for c in avail_media:
            response += c + "\n"
        bot.sendMessage(chat_id, response.rstrip())

    # MEDIA
    elif cmd == 'bbygurl':
        bot.sendVoice(chat_id, open('babygurl.mp3', 'rb'))
    elif cmd == 'yahh':
        bot.sendVoice(chat_id, open('yah.mp3', 'rb'))
    elif cmd == 'ted':
        bot.sendVoice(chat_id, open('tedtalk.mp3', 'rb'))
    elif cmd == 'ring':
        bot.sendVoice(chat_id, open('skype.mp3', 'rb'))
    elif cmd == 'shober':
        bot.sendVideo(chat_id, open('shober.mp4', 'rb'))
    elif cmd == 'dolphon':
        bot.sendVoice(chat_id, open('dolphin.mp3', 'rb'))

    # DICE ROLL
    elif cmd == 'roll':
        if text:
            try:
                lst_text = map(int, text.split(' ')[:2])
                num_side, num_roll = lst_text
                if num_side < 1 or num_roll < 1:
                    raise Exception
            except:
                bot.sendMessage(chat_id, "Oops, invalid input!",
                                reply_to_message_id=msg_id)
                return
        else:
            num_side = 6
            num_roll = 1
        ch_roll(num_side, num_roll, chat_id, msg_id)

    elif cmd == 'roll2':
        ch_roll(6, 2, chat_id, msg_id)

    # 8BALL
    elif cmd == '8ball' and text:
        bot.sendMessage(chat_id, random.choice(ball_response),
                        reply_to_message_id=msg_id)

    # SLAP
    elif cmd == 'slap':
        if len(text) > 1:
            target = text
        else:
            target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, target + " " + random.choice(slap))

    # AWARD
    elif cmd == 'award':
        if len(text) > 1:
            target = text
        else:
            target = get_user(msg['from']['id'])
        bot.sendMessage(chat_id, target + " " + random.choice(award))

    # WIKI
    elif cmd == 'wiki' and text:
        ch_wiki(text, chat_id, msg_id)
    elif cmd == 'wikilong' and text:
        ch_wiki(text, chat_id, msg_id, long=True)

    # CAP CALCULATOR
    elif cmd == 'cap':
        grades = list(map(int, text.split(' ')))
        print(grades)
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
    # ON/OFF BOT
    elif text[0] == 'start':
        global has_started
        if text[1] == 'off':
            has_started = False
        elif text[1] == 'on':
            has_started = True
        print("has_started has been set to:", has_started)



def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    msg_id = telepot.message_identifier(msg)[1]
    print(dt.now().strftime("%H:%M:%S"), content_type, chat_type, chat_id, end=' ')

    if content_type == 'text':
        text = msg['text']
        uid = msg['from']['id']
        print(get_user(uid))
        #print("{user} : {msg}".format(user=get_user(uid), msg=text))

        # ADMIN COMMANDS
        if text.startswith('!'):
            admin_handle(text[1:].split())
            return

        elif not has_started:
            return

        # COMMANDS
        elif text.startswith('/'):
            lst = text[1:].split(' ')
            if len(lst) > 1:
                command_handle(chat_id, msg, msg_id, lst[0], ' '.join(lst[1:]))
            else:
                command_handle(chat_id, msg, msg_id, lst[0])
            return

        elif 'bruh' in text.lower():
            bot.sendVoice(chat_id, open('bruh.mp3', 'rb'))

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



# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts



# Main loop runs here
init_input = input("Process all messages? - Y/N : ")
has_started = True if init_input.upper() == 'Y' else False
#has_started = False

bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()
print('Bot initialized :)')
annoy_mode = False
twss_mode = False

while 1:
    time.sleep(30)
