import urllib
import os
import time
import random



def make_dir(path):
    if not os.path.isdir('./%s'%(path)):
        os.mkdir('./%s'%(path))

def scrape_save_season(start_year=2014):
    num_games = 30*41
    season_string = "{0}{1}".format(start_year,start_year+1)

    make_dir('../data')
    make_dir('../data/html')
    make_dir('../data/html/%s'%season_string)

    for game in range(742,num_games+1):
        print "Downloading game: %d"%game
        make_dir('../data/html/%s/%04d'%(season_string,game))
        play_by_play_htlm = urllib.urlopen("http://www.nhl.com/scores/htmlreports/%s/PL02%04d.HTM"%(season_string,game)).read()
        time.sleep(random.expovariate(1))
        home_toi_html = urllib.urlopen('http://www.nhl.com/scores/htmlreports/%s/TH02%04d.HTM'%(season_string,game)).read()
        time.sleep(random.expovariate(1))
        away_toi_html = urllib.urlopen('http://www.nhl.com/scores/htmlreports/%s/TV02%04d.HTM'%(season_string,game)).read()
        out_file = open('./../data/html/%s/%04d/play_by_play.html'%(season_string,game), 'w')
        out_file.write(play_by_play_htlm)
        out_file.close()
        out_file = open('./../data/html/%s/%04d/home_toi.html'%(season_string,game), 'w')
        out_file.write(home_toi_html)
        out_file.close()
        out_file = open('./../data/html/%s/%04d/away_toi.html'%(season_string,game), 'w')
        out_file.write(away_toi_html)
        out_file.close()
        
        wait = 10 + random.expovariate(0.1)
        print "Wait: ",wait
        time.sleep(wait)

scrape_save_season()