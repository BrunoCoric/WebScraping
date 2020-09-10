from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import os

BASE = "https://www.imdb.com"

def series_episodes(link):
    sezona = []
    sezoneSve = {}
    episode_des = []
    ep_count = 1
    season_count = 1
    counter = 0
    while True:
        episode_page = requests.get(BASE + link + "episodes?season="+str(season_count)).text
        soup1 = bs(episode_page, "html.parser")
        html_text = soup1.get_text()
        for line in html_text.splitlines():
            if counter >0:
                    if str(line).strip():
                        episode_des.append(str(line).strip())
                        counter += 1
                    if counter == 5:
                        sezona.append(episode_des.copy())
                        episode_des = []
                        counter = 0
            elif line:
                if str(line) == "S" + str(season_count) + ", Ep" + str(ep_count):
                    ep_count += 1
                    episode_des.append(str(line))
                    counter += 1
        season_count += 1
        ep_count = 1
        if not sezona:
            break
        sezoneSve[season_count-1] = sezona.copy()
        sezona = []
    return sezoneSve


def show_stats(name,link,img):
    html_page = requests.get(BASE+link).text
    soup = bs(html_page, "html.parser")
    rating = soup.find("span",attrs={"itemprop":"ratingValue"}).contents[0]
    serija = soup.find("div",attrs={"class":"bp_content"})
    if serija:
        seasons = series_episodes(link)
        plot_episodes(name,seasons,rating)

def save_image(link,name):
    req = requests.get(link)
    with open(os.path.join("slike", name), 'wb') as file:
        for chunk in req.iter_content(512):
            file.write(chunk)

def plot_episodes(name,seasons,rating):
    x = []
    y = []
    for key,val in seasons.items():
        for something in val:
            y.append(float(something[3]))
            x.append(something[0])
    fig = plt.figure(figsize=(60,8))
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Episodes")
    plt.ylabel("Ratings")
    plt.suptitle(name + ", rating of series: " + str(rating))
    plt.show()



def plot_movies(nameList, imgList):
    fig = plt.figure()
    f, ax = plt.subplots(len(imgList),1)
    for i in range(len(imgList)):
        save_image(imgList[i], nameList[i]+str(i))
        img = mpimg.imread("slike/" + nameList[i]+str(i))
        ax[i].imshow(img)
        ax[i].set_title(nameList[i])
    plt.show()
    folder = "slike"
    for file in os.listdir(folder):
        os.remove(os.path.join(folder,file))


def get_page(url):
    html_page = requests.get(url).text
    soup = bs(html_page, "html.parser")
    nameList = []
    linkList = []
    imgList = []
    limit = 0
    for title in soup.find("table", attrs={"class":"findList"}):
        if str(title) and str(title) != '\n':
            movie = str(title).split('\"')
            linkList.append(movie[5])
            imgList.append(movie[7])
            name = movie[12].split("<")
            name = name[0]
            name = name[1:]
            nameList.append(name)
            limit += 1
            if limit>=6:
                break
    #plot_movies(nameList,imgList)
    unos = int(input("Upiši broj koji film/seriju želiš odabrat od ponuđenih:"))
    show_stats(nameList[unos-1],linkList[unos-1],imgList[unos-1])

if __name__ == "__main__":
    while True:
        unos = input("Unesi ime filma/serije: ")
        link = "https://www.imdb.com/find?q="+unos
        get_page(link)
        break
