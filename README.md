# Tebby :teddy_bear::robot:
## The API-wielding Telegram Bot

**Main code:** [TebbyBot.py](TebbyBot.py)

**Telegram:** `@tebby_bot`
### :thought_balloon: Background
Tebby started out as a light-hearted Telegram bot using [nickoala's](https://github.com/nickoala/telepot) Telepot for sending cats and dogs images to users.
With the help of several useful APIs out there, this bot has become relatively useful while
maintaining a good amount of casual fun. Currently, this bot's codes are being hosted by [PythonAnywhere](https://www.pythonanywhere.com) for free. Given the nature of being free, there are several limitations including a restricted list of websites that their platform can access. Since Tebby is somewhat casual and non-profit, I have no
plans to switch over to a paid account. Send a `/help` to `@tebby_bot` to get started!

### :keyboard: List of User Commands
Updated as of 13th April 2020.

Some commands require inputs, while others will have defaults. Most of the commands that require input of country or location will default to Singapore. Country codes follow [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes). If API and Python libraries are not mentioned in the command description, then it most likely involves [Requests](https://requests.readthedocs.io/en/master/) and web scraping.

Command | Description | API used
-------- | -------- | ------
`/weather` | Gets the weather and temperature of a given `country name` | [OpenWeatherMap](https://openweathermap.org/api)
`/covid` | Gets the updated COVID-19 cases of a given `country code` | [TrackCorona](https://www.trackcorona.live/api)
`/news` | Gets the top headlines of a given `country code` | [News API](https://newsapi.org/)
`/transit` | Returns step-by-step instructions for transit from `x` to `y`, as requested by user | [Google Maps Platform](https://developers.google.com/maps/documentation)
`/wiki` | Provides Wikipedia summary of a `query`<br>Uses [goldsmith's](https://github.com/goldsmith/Wikipedia) wikipedia library
`/define` | Gets definition of a `word` | [Oxford Dictionaries](https://developer.oxforddictionaries.com/)
`/google` | Returns top urls of a google search `query`<br>Uses [MarioVilas'](https://github.com/MarioVilas/googlesearch) google search library
`/choose` | Randomly chooses between `choices` given by indecisive users
`/slap` | Inspired from and tribute to [IRC](https://en.wikipedia.org/wiki/Wikipedia:Whacking_with_a_wet_trout) wet trout feature
`/award` | Similar to the slap feature except it's good
`/8ball` | Emulates the [Magic 8-ball](https://en.wikipedia.org/wiki/Magic_8-Ball)
`/roll` | Rolls an `x` sided dice `y` times, as requested by the user
`/media` | Returns a menu of commands for triggering amusement,<br>usually in the form of voice or gif
`/cat` | Returns a random cat image | [TheCatApi](https://docs.thecatapi.com/)
`/dog` | Returns a random dog image


### :microscope: TODO
- Add a `/ask` which is similar to [Google's featured snippet](https://support.google.com/websearch/answer/9351707?p=featured_snippets&hl=en-SG&visit_id=637223398998406223-969856675&rd=1). I'm eyeing [DuckDuckGo's Instant Answer API](https://duckduckgo.com/api) too...<br>If successful, there may not be a need for `/google` and `/wiki`.
- Update `/wiki` as it is relatively buggy/ugly.
- Find ways to make `/google` friendlier than just dumping urls to users.
- Add `/forecast` for weather forecast, or add forecast to the current `/weather` command.
- Make `/transit` more flexible and able to provide driving routes too.
