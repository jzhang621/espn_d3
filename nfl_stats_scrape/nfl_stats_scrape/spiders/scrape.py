import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from nfl_stats_app.app import client

TABLE_HEADING_MAP = {0: 'Passing', 1: 'Rushing', 2: 'Receiving', 8: 'Defense'}
app_client = client.Client()

class NFLStatsSpider(CrawlSpider):

  name = 'nfl_stats_scrape'
  allowed_domains = ['footballdb.com']
  start_urls = ['http://www.footballdb.com/teams']
  rules = [Rule(LinkExtractor(allow=['/nfl/.*/stats']), 'parse_stats')]

  def parse_stats(self, response):

    team_name = response.xpath('//div[@class="teamlabel"]/text()').extract()[0]
    app_client.get_or_create_team(team_name)

    stat_tables = response.xpath("//div[@class='divider']/following-sibling::table")
    for index, stat_table in enumerate(stat_tables):
      heading = TABLE_HEADING_MAP.get(index)
      if heading:
        self.parse_and_store_table(heading, stat_table, team_name)
    
  def parse_and_store_table(self, header, stat_table, team_name):
    """
    Pass the statistic table to the appropiate parsing function for that table
    based on the header name.

    :param str header: The statistic type of the stat_table that is being parsed
    :param `Scrapy.selector.unified` Selector stat_table: Select object containg 
            the stats to be parsed
    """
    if header == 'Passing':
      database_fields = set(['Att', 'Cmp', 'Yds', 'TD', 'Int', 'Sack']) 
    elif header == 'Rushing':
      database_fields = set(['Att', 'Yds', 'TD', 'FD'])
    elif header == 'Receiving':
      database_fields = set(['Rec', 'Yds', 'TD', 'FD', 'Tar', 'YAC'])
    elif header == 'Defense':
      database_fields = set(['Tot', 'Int', 'Sack', 'TD'])
    else:
      raise ValueError('Invalid statistics type: %s', header)

    self._parse_and_store_table(header, stat_table, database_fields, team_name)

  def _parse_and_store_table(self, header, stat_table, database_fields, team_name):
    """
    Parse the statistics table into the appropate model object and commit
    into the datastore

    :param str header: Name of the statistics table that is being parsed
    :param `Scrapy.selector.unified` Selector stat_table: Select object containg 
            the stats to be parsed
    :param set database_fields: The relevant columns that will be extracted
    """
    columns = stat_table.xpath('tr[@class="header right"]')[0].xpath('th/text()').extract()
    
    # map the appropiate column definitions to the index
    field_to_index_map = {}
    for index, column in enumerate(columns):
      if column in database_fields:
        field_to_index_map[index-1] = column
   
    stats_map = {}
    player_stats = stat_table.xpath('tr[@class="row0 right"]')
    for player in player_stats:
      player_name = player.xpath('td/a/text()').extract()
      if player_name:
        player_name = player_name[0]

        stats = player.xpath('td/text()').extract()
        for index, value in enumerate(stats):
          stat_type = field_to_index_map.get(index)
          if stat_type:
            # convert strings with commas into ints
            if ',' in value:
              stats_map[stat_type] = locale.atoi(value)
            else:
              stats_map[stat_type] = float(value)
            stats_map['team_name'] = team_name
            stats_map['player_name'] = player_name

        app_client.add_player_stats(header, stats_map)
    
    return stats_map
