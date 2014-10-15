# -*- coding: utf-8 -*-

# Scrapy settings for nfl_stats_scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nfl_stats_scrape'

SPIDER_MODULES = ['nfl_stats_scrape.spiders']
NEWSPIDER_MODULE = 'nfl_stats_scrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nfl_stats_scrape (+http://www.yourdomain.com)'
