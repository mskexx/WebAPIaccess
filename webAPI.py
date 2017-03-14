#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim : set fileencoding=utf8 :

"""
Ejercicio para obtener datos mediante la API de Weather Underground
Autor: Marcos Susin

Uso: python webApi.py <api_key>
     ./webAPI.py <api_key>
"""

import sys
import bs4
import urllib2
import json

api_key = None


class WeatherClient(object):
    """Client for weather undergroUnd"""
    url_base = "http://api.wunderground.com/api/"
    url_service = {"almanac": "/almanac/q/CA/",
                   "hourly": "/hourly/q/CA/"}

    def __init__(self, apikey):
        self.api_key = apikey

    def get_servicexml(self, service, location):
        #return open("Lleida.xml", 'r')  #Offline Mode
        url = WeatherClient.url_base + self.api_key + \
            WeatherClient.url_service[service] + \
            location + "." + "xml"
        print url
        web = urllib2.urlopen(url)
        page = web.read()
        web.close()

        return page

    def almanac(self, location):
        """Almanac page"""
        # obtener URL
        almanac_page = self.get_servicexml("almanac", location)
        print almanac_page

    def hourly(self, location):
        "Hourly page"
        hourly_page = self.get_servicexml("hourly", location)
        self.hourly_forecast(hourly_page)

    def hourly_forecast(self, hourly_data):
        data = bs4.BeautifulSoup(hourly_data, 'lxml')
        temps_list = []
        for temps in data.find_all("forecast"):
            hour = temps.find("hour_padded").text + ":" \
                    + temps.find("min").text
            cond = temps.find("condition").text
            temps = temps.find("temp").find("metric").text

            temps_list.append((str(hour), int(temps), str(cond)))

        self.print_menu(temps_list)

    def print_menu(self,temps):
        print"═════════════════════════════"
        print"   Hora   ºC      Cielo      "
        print"═════════════════════════════"

        for x in range(0,7):
            print "  " + temps[x][0] + "    " + str(temps[x][1]) + "\t" + temps[x][2]
        print"═════════════════════════════"
if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "La API a la linea de comandos"

    wc = WeatherClient(api_key)
    #wc.almanac("Lleida")
    wc.hourly("Lleida")
