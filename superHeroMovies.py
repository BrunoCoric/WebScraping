from bs4 import BeautifulSoup as bs
import requests
import os
import csv

genres = {}

def get_page(url):
    html_page = requests.get(url).text
    soup = bs(html_page, "html.parser")
    for genre in soup.find_all("span", attrs={"class":"genre"}):
        gen = str(genre.contents[0]).strip()
        list_gen = gen.split(", ")
        for g in list_gen:
            if g in genres:
                genres[g] += 1
            else:
                genres[g] = 1



if __name__ == "__main__":
    for number in range(1,5):
        url = "https://www.imdb.com/search/keyword/?keywords=based-on-comic-book&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=C66DEPE5FGKPB63TNEW1&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_nxt&mode=detail&sort=num_votes,desc&title_type=movie&page="+str(number)
        get_page(url)
    with open('comicMovies.csv','w') as f:
        for key in genres.keys():
            f.write("%s,%s\n"%(key,genres[key]))