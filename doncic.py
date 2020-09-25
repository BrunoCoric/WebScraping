from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import numpy as np

def statistics(game_list):
    turnover_list = []
    for game in game_list:
        html_page = requests.get(game).text
        soup = bs(html_page,"html.parser")
        turnover = "Turnover by <a href="+ "\""+ "/players/d/doncilu01.html" + "\""
        for turn in soup.find_all("td"):
            if turnover in str(turn):
                turnover_list.append(str(turn))


    dir_lost = {}
    dir_pass = {}
    dir_other = {}
    for turnover in turnover_list:
        if "lost ball; steal by" in turnover:
            string = turnover.split(">")[4]
            string = string.split("<")[0]
            stringer = turnover.split('\"')[5]
            string = string + "-" + stringer
            if string in dir_lost:
                dir_lost[string] += 1
            else:
                dir_lost[string] = 1
        elif "bad pass; steal by" in turnover:
            string = turnover.split(">")[4]
            string = string.split("<")[0]
            stringer = turnover.split('\"')[5]
            string = string + "-" + stringer
            if string in dir_pass:
                dir_pass[string] += 1
            else:
                dir_pass[string] = 1
        else:
            string = turnover.split("(")[1]
            string = string.split(")")[0]
            if string in dir_other:
                dir_other[string] += 1
            else:
                dir_other[string] = 1

    dict_both = {}
    for key, val in dir_lost.items():
        dict_both[key] = val
    for key, val in dir_pass.items():
        if key in dict_both:
            dict_both[key] += val
        else:
            dict_both[key] = val


    # reads statistics from the file
    
    # with open("doncic2.txt", "w") as f:
    #     print("Lost ball", file=f)
    #     for key,val in dir_lost.items():
    #         stringer = str(key) + ": " + str(val)
    #         print(stringer,file=f)
    #     print("\n", file=f)
    #
    #     print("Bad pass", file=f)
    #     for key, val in dir_pass.items():
    #         stringer = str(key) + ": " + str(val)
    #         print(stringer, file=f)
    #     print("\n", file=f)
    #
    #     print("Both", file=f)
    #     for key, val in dict_both.items():
    #         stringer = str(key) + ": " + str(val)
    #         print(stringer, file=f)
    #     print("\n", file=f)
    #
    #     print("Other turnover", file=f)
    #     for key, val in dir_other.items():
    #         stringer = str(key) + ": " + str(val)
    #         print(stringer, file=f)
    #     print("\n", file=f)


# shows the graph with players who had most steals on Luka DOnčić   
def load_statistics():
    file1 = open("doncic2.txt","r")
    lines = file1.readlines()
    good = 0
    dict = {}
    for line in lines:
        if line.strip() == "Other turnover":
            break
        if good == 1:
            if(line.strip()):
                data = line.strip().split(":")
                dict[data[0]] = data[1][1]
        if line.strip() == "Both":
            good = 1

    name = []
    value = []
    name1 = []
    value1 = []
    for i in range(6):
        ma = max(dict,key=dict.get)
        name.append(ma.split("-")[0])
        value.append(dict[ma])
        dict.pop(ma)

    for v in range(len(value)):
        value1.append(int(value.pop()))
    for v in range(len(name)):
        name1.append(str(name.pop()))

    print(name1)
    print(value1)

    plt.bar(name1,value1)
    plt.yticks(np.arange(3,8,1))
    

    plt.xlabel("Players")
    plt.ylabel("Number of steals")
    plt.title("Players with most steals on Luka Dončić")
    plt.show()



# function that gets the html file from the link and finds all the games that Luka Dončić has played
def download_page(url1,url2):
    html_page = requests.get(url1).text
    soup = bs(html_page,"html.parser")
    
    # list of links to the games that Luka Dončić has played
    game_list = []
    base = "https://www.basketball-reference.com/boxscores/pbp/"

    # finds links to the games that Luka Dončić has played in 2019
    for link in soup.find_all("td", attrs={"data-stat" : "date_game"}):
        file = str(link).split("/")[2]
        file = file.split('\"')[0]
        if(file):
            game_list.append(base+file)

    html_page = requests.get(url2).text
    soup = bs(html_page, "html.parser")
    
    #finds links to the games that Luka Dončić has played in 2020
    for link in soup.find_all("td", attrs={"data-stat": "date_game"}):
        file = str(link).split("/")[2]
        file = file.split('\"')[0]
        if (file):
            game_list.append(base + file)
            
    # plots the graph that shows players with the most steals of Luka Dončić
    #load_statistics()
    
    # gets the statistics on Luka Dončić's turnovers
    statistics(game_list)


# url that contains all the game that player Luka Dončić has played in 2019 and 2020
if __name__ == "__main__":
    download_page("https://www.basketball-reference.com/players/d/doncilu01/gamelog/2019","https://www.basketball-reference.com/players/d/doncilu01/gamelog/2020")
