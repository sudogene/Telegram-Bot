from Batteries import *
from Logger import Logger
import telepot, requests, re, random, time, urllib3, wordninja, wikipedia, googlesearch
from telepot.loop import MessageLoop
import datetime as dt
from bs4 import BeautifulSoup

class TebbyBot:
    def __init__(self, has_started=True):
        self.bot = telepot.Bot(token)
        self.has_started = has_started
        self.logger = Logger('log.txt')

        print(f"Tebby initialized! {emoji['tebby']}{emoji['robot']}")


    def run(self):
        '''
        Main message loop that runs forever.
        '''
        MessageLoop(self.bot, self.handle).run_as_thread()
        print("Running...")
        while True:
            time.sleep(30)


    def get_user(self, uid):
        '''
        Returns the first name of the Telegram user.
        '''
        return self.bot.getChat(uid)['first_name']


    def handle(self, msg):
        '''
        The main handle function used in MessageLoop.
        Prints a log of the message type and calls either admin commands or regular commands.
        '''
        content_type, chat_type, chat_id = telepot.glance(msg)
        msg_id = telepot.message_identifier(msg)[1]
        log = f'{str(dt.date.today())} {dt.datetime.now().strftime("%H:%M:%S")} {content_type} {chat_type} {chat_id}'
        if content_type == 'text':
            log += f' {self.get_user(msg["from"]["id"])}: {msg["text"]}'

        msg_timestamp = dt.datetime.fromtimestamp(int(msg['date']))
        time_now = dt.datetime.now()
        if ((time_now - msg_timestamp).seconds / 60) > 5:
            log = '[NOT PROCESSED] ' + log
            self.logger.log(log)
            return

        self.logger.log(log)

        if content_type == 'text':
            text = msg['text']
            uid = msg['from']['id']

            # ADMIN COMMANDS
            if text.startswith('!'):
                self.admin_handle(text[1:].split())
                return

            # DOES NOT PROCESS IF NOT STARTED
            elif not self.has_started:
                return

            # SEND TO COMMAND HANDLER
            elif text.startswith('/'):
                text = text.replace('@tebby_bot', '')
                lst = text[1:].split(' ')
                if len(lst) > 1:
                    self.cmd_handle(chat_id, msg_id, msg, lst[0], ' '.join(lst[1:]))
                else:
                    self.cmd_handle(chat_id, msg_id, msg, lst[0])
                return

            # BRUH MOMENT
            elif 'bruh' in text.lower():
                self.bot.sendVoice(chat_id, open('bruh.mp3', 'rb'))

            # GREETINGS
            elif 'teb' in text.lower().split() or 'tebby' in text.lower().split():
                self.bot.sendMessage(chat_id, random.choice(intro))


    # Admin Handle
    def admin_handle(self, text):
        '''
        Admin commands begin with '!'
        To make internal changes to the bot.
        '''
        if text[0] == 'start':
            if text[1] == 'on':
                self.has_started = True
            else:
                self.has_started = False
            print("Started: ", has_started)


    ##########################
    #     Command Handle     #
    ##########################
    def cmd_handle(self, chat_id, msg_id, msg, cmd, text=''):
        '''
        User commands begin with '/'
        Calls command_handler helper functions (ch)'
        '''
        if cmd == 'help':
            response = "Tebby lives to serve\n"
            for c in avail_cmd:
                response += c + "\n"
            self.bot.sendMessage(chat_id, response.rstrip(), disable_notification=True)

        # HELP MEDIA
        elif cmd == 'media':
            response = "Tebby recommends \U0001F4FD\U0001F3B6\n"
            for c in avail_media:
                response += c + "\n"
            self.bot.sendMessage(chat_id, response.rstrip(), disable_notification=True)

        # SOURCE
        elif cmd == 'tebby':
            response = "Tebby's source code!\nhttps://github.com/sudogene/Telegram-Bot"
            self.bot.sendMessage(chat_id, response, reply_to_message_id=msg_id,
                disable_notification=True)

        # MEDIA
        elif cmd in media_get.keys():
            # For single files
            media_file = media_get[cmd]
            if media_file[-1] == '3':
                # mp3 file
                self.bot.sendVoice(chat_id, open(media_file, 'rb'),
                    disable_notification=True)
            else:
                # mp4 file, most probably gif
                self.bot.sendDocument(chat_id, open(media_file, 'rb'),
                    disable_notification=True)

        # MEDIA COMBOS
        elif cmd == 'shoberdance':
            self.bot.sendMessage(chat_id, 'dancin till you break your bone!',
                disable_notification=True)
            self.bot.sendDocument(chat_id, open('shober.mp4', 'rb'),
                disable_notification=True)
            self.bot.sendVoice(chat_id, open('dancin.mp3', 'rb'),
                disable_notification=True)
        elif cmd == 'lol':
            voice = f'laugh{random.randint(1, 3)}.mp3'
            self.bot.sendVoice(chat_id, open(voice, 'rb'), disable_notification=True)

        # THIS OR THAT
        elif cmd == 'choose':
            '''
            Simple function to randomly choose between some choices.
            The choices must be separated by ' or ' string.
            '''
            if not text or ' or ' not in text:
                self.bot.sendMessage(chat_id, help_usage['choose'],
                    reply_to_message_id=msg_id, disable_notification=True)
            else:
                choices = text.split(' or ')
                choice = random.choice(choices)
                self.bot.sendMessage(chat_id, choice, reply_to_message_id=msg_id)

        # DICE ROLL
        elif cmd == 'roll':
            '''
            Rolls an x sided dice y times.
            Defaults to rolling a six-sided dice once.
            '''
            if text:
                try:
                    lst_text = map(int, text.split(' ')[:2])
                    num_side, num_roll = lst_text
                    if num_side < 1 or num_roll < 1:
                        raise Exception
                except:
                    self.bot.sendMessage(chat_id, help_usage['roll'],
                        reply_to_message_id=msg_id, disable_notification=True)
                    return
            else:
                num_side = 6
                num_roll = 1
            self.ch_roll(chat_id, msg_id, num_side, num_roll)

        elif cmd == 'roll2':
            '''
            Rolls a six-sided dice twice.
            '''
            self.ch_roll(chat_id, msg_id, 6, 2)

        # 8BALL
        elif cmd == '8ball' and text:
            '''
            Random response from 8-ball.
            Don't use this to make life decisions.
            '''
            self.bot.sendMessage(chat_id, f"{emoji['8ball']} {random.choice(ball_response)}",
                reply_to_message_id=msg_id)

        # SLAP
        elif cmd == 'slap':
            '''
            Slaps the target name if given, else slaps you.
            '''
            if len(text) > 1:
                target = text
            else:
                target = self.get_user(msg['from']['id'])
            self.bot.sendMessage(chat_id, target + " " + random.choice(slap))

        # AWARD
        elif cmd == 'award':
            '''
            Awards the target name if give, else awards you.
            '''
            if len(text) > 1:
                target = text
            else:
                target = self.get_user(msg['from']['id'])
            self.bot.sendMessage(chat_id, target + " " + random.choice(award))

        # WIKI
        elif cmd == 'wiki' and text:
            '''
            Wikipedia. Kinda sucky currently, the formatting is weird.
            '''
            self.ch_wiki(chat_id, msg_id, text)
        elif cmd == 'wikilong' and text:
            self.ch_wiki(chat_id, msg_id, text, long=True)

        # CAP CALCULATOR
        elif cmd == 'cap':
            '''
            Calculates CAP from a string of space-delimited grade numbers.
            '''
            try:
                grades = list(map(int, text.split(' ')))
                self.ch_cap(chat_id, msg_id, grades, msg)
            except:
                self.bot.sendMessage(chat_id, help_usage['cap'],
                    reply_to_message_id=msg_id, disable_notification=True)

        # WEATHER
        elif cmd == 'weather':
            '''
            Uses OpenWeatherMap API.
            Query with country name, defaults to Singapore.
            '''
            if text:
                if len(text) == 2:
                    try:
                        text = code_to_name[text]
                        self.ch_weather(chat_id, msg_id, text)
                    except:
                        self.bot.sendMessage(chat_id, "Oops, please try again!",
                            reply_to_message_id=msg_id, disable_notification=True)
                else:
                    self.ch_weather(chat_id, msg_id, text)
            else:
                self.ch_weather(chat_id, msg_id)

        # NEWS
        elif cmd == 'news':
            '''
            Uses News API. Returns top 5 news headlines.
            Query with country code, defaults to sg.
            '''
            if text:
                if len(text) > 2:
                    try:
                        text = name_to_code[text]
                        self.ch_news(chat_id, msg_id, text)
                    except:
                        self.bot.sendMessage(chat_id, "Oops. please try again!",
                            reply_to_message_id=msg_id, disable_notification=True)
                else:
                    self.ch_news(chat_id, msg_id, text)
            else:
                self.ch_news(chat_id, msg_id)

        # DIRECTIONS - TRANSIT
        elif cmd == 'transit':
            '''
            Uses Google Maps services, currently only supports public transportation.
            Requires current and destination to be separated by ' ; ' string.
            '''
            if not text or ' to ' not in text:
                self.bot.sendMessage(chat_id, help_usage['transit'],
                    reply_to_message_id=msg_id, disable_notification=True)
                return
            origin, destination = text.split(' to ')
            self.ch_transit(chat_id, msg_id, origin, destination)

        # GOOGLE SEARCH
        elif cmd == 'google' or cmd == 'g':
            '''
            Due to certain limitations, this function will only produce the urls
            of the top 5 google search results. No accessing of urls is done.
            '''
            if text:
                self.ch_gglsearch(chat_id, msg_id, text)
            else:
                self.bot.sendMessage(chat_id, "Give Tebby something to search!",
                    reply_to_message_id=msg_id, disable_notification=True)

        # COVID19 CASES
        elif cmd == 'covid':
            '''
            Grabs cases from trackcorona.live using country codes
            Stay safe everyone.
            '''
            if text:
                if len(text) > 2:
                    try:
                        text = name_to_code[text]
                        self.ch_covid(chat_id, msg_id, text)
                    except:
                        self.bot.sendMessage(chat_id, "Oops. please try again!",
                            reply_to_message_id=msg_id, disable_notification=True)
                else:
                    self.ch_covid(chat_id, msg_id, text)
            else:
                self.ch_covid(chat_id, msg_id)

        # DEFINITION
        elif cmd == 'define' and text:
            self.ch_define(chat_id, msg_id, text)

        elif cmd == 'pronounce' and text:
            #ch_pronounce(chat_id, msg_id, text)
            # WORK IN PROGRESS
            pass

        # CAT
        elif cmd == 'cat':
            self.bot.sendPhoto(chat_id, self._cat_url(), caption=random.choice(captions),
                reply_to_message_id=msg_id, disable_notification=True)

        # DOG
        elif cmd == 'dog':
            self.bot.sendPhoto(chat_id, self._dog_url(), caption=random.choice(captions),
                reply_to_message_id=msg_id, disable_notification=True)

        # BTC
        elif cmd == 'btc':
            #https://pro.coinmarketcap.com/account
            url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            parameters = {
              'start':'1',
              'limit':'1',
              'convert':'SGD'
            }
            headers = {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': coin_key,
            }
            s = requests.Session()
            s.headers.update(headers)
            r = s.get(url, params=parameters)
            try:
                data = r.json()['data'][0]
                name = f"{data['name']} Rates"
                sgd = round(data['quote']['SGD']['price'], 2)
                percent_1h = round(data['quote']['SGD']['percent_change_1h'], 2)
                percent_24h = round(data['quote']['SGD']['percent_change_24h'], 2)
                percent_7d = round(data['quote']['SGD']['percent_change_7d'], 2)


                res = f"\n1 BTC = {sgd} SGD\n\nPercent changes in\n1 hr: {percent_1h}%\n24 hr: {percent_24h}%\n7 d: {percent_7d}%"
                res = name + res

                self.bot.sendMessage(chat_id, res, disable_notification=True, reply_to_message_id=msg_id,
                    parse_mode='Markdown',)

            except:
                self.bot.sendMessage(chat_id, "??", disable_notification=True, reply_to_message_id=msg_id)


    ##############################
    #   Command Handle Helpers   #
    ##############################
    def ch_roll(self, chat_id, msg_id, num_side, num_roll):
        '''
        # special Telegram dice roll animation
        if num_side == 6 and num_roll == 1:
            self.bot.sendMessage(chat_id, "\U0001F3B2")
            return
        '''

        if num_roll > 100:
            self.bot.sendMessage(chat_id, f"Don't be malicious! {emoji['sad']}",
                            reply_to_message_id=msg_id, disable_notification=True)
            return
        res = []
        try:
            for i in range(num_roll):
                res.append(str(random.randint(1, num_side)))
            ch_response = ", ".join(res)
            self.bot.sendMessage(chat_id, ch_response,
                            reply_to_message_id=msg_id, disable_notification=True)
        except:
            self.bot.sendMessage(chat_id, "Don't be malicious! {emoji['sad']}",
                            reply_to_message_id=msg_id, disable_notification=True)


    def ch_wiki(self, chat_id, msg_id, query, long=False):
        try:
            if long:
                self.bot.sendMessage(chat_id, wikipedia.summary(query, sentences=5),
                                reply_to_message_id=msg_id, disable_notification=True)
            else:
                self.bot.sendMessage(chat_id, wikipedia.summary(query, sentences=2),
                                reply_to_message_id=msg_id, disable_notification=True)
        except Exception:
            self.bot.sendMessage(chat_id, "Oops, that's a strange query!",
                            reply_to_message_id=msg_id, disable_notification=True)


    def ch_cap(self, chat_id, msg_id, grades, msg):
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
            self.bot.sendMessage(chat_id, "CAP: " + str(cap),
                            reply_to_message_id=msg_id, disable_notification=True)
        except:
            self.bot.sendMessage(chat_id, help_usage['cap'],
                            reply_to_message_id=msg_id, disable_notification=True)


    def ch_weather(self, chat_id, msg_id, city='Singapore'):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={w_key}"
        r = requests.get(url).json()
        if r['cod'] != '404':
            data = r['main']
            curr_temp = data['temp']
            curr_feels = data['feels_like']
            curr_pres = data['pressure']
            curr_hum = data['humidity']
            desc = r['weather'][0]['description'].capitalize()
            weather_id = r['weather'][0]['id']
            if weather_id != '800':
                try:
                    icon = ow_emoji[str(weather_id)[0]]
                except:
                    print("No icon for weather id:", weather_id)
                    icon = ''

            ch_response = f"*{city.capitalize()}* {icon}\n\n" + \
                          f"{desc}\n" + \
                          f"Temperature: {curr_temp} \u2103\n" + \
                          f"Feels like: {curr_feels} \u2103\n" + \
                          f"Pressure: {curr_pres} hPa\n" + \
                          f"Humidity: {curr_hum} %\n"

            self.bot.sendMessage(chat_id, ch_response, parse_mode='Markdown',
                reply_to_message_id=msg_id)
        else:
            self.bot.sendMessage(chat_id, f"The site is feeling under the weather {emoji['sadcry']}",
                reply_to_message_id=msg_id, disable_notification=True)


    def ch_news(self, chat_id, msg_id, country="sg"):
        api_key = news_key
        url = f"http://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}&pageSize=4"
        r = requests.get(url).json()

        status = r['status']
        if status != 'ok':
            self.bot.sendMessage(chat_id, f"Sorry Tebby can't reach the site... {emoji['sad']}")
            return

        ch_response = ""
        articles = r['articles']
        for article in articles:
            if article['title'].startswith("Morning Briefing:"):
                continue
            ch_response += "*" + article['title']  + "*\n"
            if article['description'] != None:
                ch_response += article['description'] + "\n\n"
            else:
                ch_response += "\n"

        ch_response = ch_response.strip()
        self.bot.sendMessage(chat_id, ch_response, parse_mode='Markdown',
                        reply_to_message_id=msg_id, disable_notification=True)


    def ch_transit(self, chat_id, msg_id, origin, destination):
        o = origin.replace(' ', '+')
        d = destination.replace(' ', '+')
        base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
        mode = 'transit'
        api_key = gm_key
        nav_request = f"origin={o}&destination={d}&mode={mode}&key={api_key}"
        response = requests.get(base_url + nav_request).json()
        if response['status'] != 'OK':
            self.bot.sendMessage(chat_id, "Oops, please refine your search!",
                            reply_to_message_id=msg_id, disable_notification=True)
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

        self.bot.sendMessage(chat_id, ch_response, reply_to_message_id=msg_id,
            disable_notification=True)


    def ch_gglsearch(self, chat_id, msg_id, query):
        urls = [url for url in googlesearch.search(query, stop=4)]
        ch_response = "Here are the top 4 results!\n\n"
        '''
        for url in urls:
            r = requests.get(url)
            ch_response += f"{fromstring(r.content).findtext('.//title')}\n{url}\n\n"
        '''
        n = 1
        for url in urls:
            ch_response += f"{n}. {url}\n\n"
            n += 1

        ch_response = ch_response.strip()
        self.bot.sendMessage(chat_id, ch_response,
            reply_to_message_id=msg_id, disable_notification=True)


    def ch_covid(self, chat_id, msg_id, query='sg'):
        url1 = 'https://www.trackcorona.live/api/countries'

        r= requests.get(url1)
        if not r:
            self.bot.sendMessage(chat_id, f"Sorry Tebby can't reach the site... {emoji['sad']}",
                reply_to_message_id=msg_id, disable_notification=True)
            return
        try:
            r = r.json()['data']
            i = 0
            while (True):
                if r[i]['country_code'] == query:
                    break
                i += 1
            raw = r[i]
            date = raw["updated"].split()[0]
            ch_response = f'*Cases in {raw["location"]}*\nDate: {date}\n\nConfirmed: {raw["confirmed"]}\nRecovered: {raw["recovered"]}\nDeath: {raw["dead"]}'
            self.bot.sendMessage(chat_id, ch_response, parse_mode='Markdown', reply_to_message_id=msg_id)

        except:
            self.bot.sendMessage(chat_id, "Oops, something went wrong!",
                reply_to_message_id=msg_id, disable_notification=True)


    def _ch_oxford_helper(self, query):
        endpoint = "entries"
        language_code = "en-us"
        url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + query.lower()
        r = requests.get(url, headers = {"app_id": od_app_id, "app_key": od_key})
        if r.status_code == 200:
            return r
        else:
            return None


    def ch_define(self, chat_id, msg_id, query):
        '''
        Uses Oxford Dictionaries API for definitions.
        In the future, there might be a word pronounciation function.
        '''
        r = self._ch_oxford_helper(query)
        if r:
            senses = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
            definitions = [senses[i]['definitions'] for i in range(len(senses)) if 'definitions' in senses[i].keys()]
            query_formatted = query.lower().capitalize()
            ch_response = f"*{query_formatted}*\n\n"
            if len(definitions) > 1:
                count = 1
                for d in definitions:
                    ch_response += f"{str(count)}. {d[0].capitalize()}\n\n"
                    count += 1
            else:
                ch_response += f"{definitions[0][0].capitalize()}\n\n"
            self.bot.sendMessage(chat_id, ch_response.rstrip(), parse_mode='Markdown',
                reply_to_message_id=msg_id, disable_notification=True)
        else:
            self.bot.sendMessage(chat_id, "Oop, please try again!",
                reply_to_message_id=msg_id, disable_notification=True)


    def _cat_url(self):
        contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
        return contents[0]['url']


    def _dog_helper(self):
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        return url


    def _dog_url(self):
        allowed_extension = ['jpg','jpeg','png']
        file_extension = ''
        while file_extension not in allowed_extension:
            url = self._dog_helper()
            file_extension = re.search("([^.]*)$",url).group(1).lower()
        return url

    def ch_meme(self, chat_id, msg_id):
        random_url = random.choice(meme_urls)
        try:
            start = datetime.now()
            self.bot.sendPhoto(chat_id, random_url, reply_to_message_id=msg_id, disable_notification=True)
            end = datetime.now()
            if (end - start).seconds > 5:
                print("Time exceeded:", random_url)
        except:
            print("Failed:", random_url)


    ''' TODO
    def ch_pronounce(chat_id, msg_id, query):
        r = self_ch_oxford_helper(query)
        if r:
            audio = r.json()['results'][0]['lexicalEntries'][0]['pronunciations'][1]
            audio_url = audio['audioFile']
            r = requests.get(audio_url)
            bot.sendVoice(chat_id, ('temp.mp3', r.content), reply_to_message_id=msg_id, disable_notification=True)
        else:
            bot.sendMessage(chat_id, "Oop, please try again!",
                            reply_to_message_id=msg_id, disable_notification=True)
    '''


if __name__ == '__main__':
    # You can leave this bit out if you're using a paid PythonAnywhere account
    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
    # end of the stuff that's only needed for free accounts

    tebby = TebbyBot()
    tebby.run()

