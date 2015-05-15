# Reddit RSS to Telegram #

This script uses the reddit RSS feeds to scrap images and send them to a favorite group of yours.

## Instructions ##
* Download and install [vysheng's tg-cli](https://github.com/vysheng/tg)
* Sign in to vysheng's tg, find the id of the group you want to send photos to by using chat_info
* `mv sample.config.py config.py`
* Inside config.py,
  * subreddits is the array of subreddits on reddit that you want to follow
  * togroup is where you should paste the id you found earlier
  * tgdir is the relative path to vysheng's tg on your computer. 
