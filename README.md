# Tebby :bear::robot:
## The API-wielding Telegram Bot

**Main:** ['TebbyBot.py'](TebbyBot.py)
**Telegram:** @tebby_bot

### :thought_bubble: Background
Tebby started out as a light-hearted Telegram bot for sending cats and dogs images to users.
With the help of several useful APIs out there, this bot has become relatively useful while
maintaining a good amount of casual fun. Send a `/help` to `@tebby_bot` to get started.

Telegram Command | Info | API used
-------- | -------- | ------
/weather | Gets the weather and temperature of a given country name | [OpenWeatherMap](https://openweathermap.org/api)
/covid | Gets the updated COVID-19 cases of a given country code | [TrackCorona](https://www.trackcorona.live/api)
/news | Gets the top headlines of a given country code | [News API](https://newsapi.org/)
/transit | Returns step-by-step instructions for transit from one place to another | [Google Maps Platform](https://developers.google.com/maps/documentation)
/wiki | Provides Wikipedia summary of a query. Uses [goldsmith's](https://github.com/goldsmith/Wikipedia) wikipedia library
/define | Gets definition of a word | [Oxford Dictionaries]{https://developer.oxforddictionaries.com/}
/google | Returns top urls of a google search. Uses [MarioVilas'](https://github.com/MarioVilas/googlesearch) google search library
/choose | Randomly chooses between choices given by indecisive users
/slap | Inspired from and tribute to [IRC](https://en.wikipedia.org/wiki/Wikipedia:Whacking_with_a_wet_trout) wet trout feature
/award | Similar to the slap feature except it's good
/8ball | Emulates the [Magic 8-ball](https://en.wikipedia.org/wiki/Magic_8-Ball)
/roll | Rolls an `x` sided dice `y` times, as requested by the user
/media | Returns a menu of commands for triggering amusement, usually in the form of Telegram voice or gif.

