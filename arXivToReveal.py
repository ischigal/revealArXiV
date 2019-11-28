import numpy as np
import urllib.request
import re


def tagSub(htmlKey, text):

    return re.sub(r"\\n", " ", re.sub(r"\n ", "", re.sub("</"+htmlKey+">", "", re.sub("<"+htmlKey+">", "", re.search("<"+htmlKey+">((?s).*)</"+htmlKey+">", text).group(0))))).strip()


def authorSub(authorString):

    return re.sub("<arxiv:affiliation.*?</arxiv:affiliation>, ", "", re.sub('\s{2,}', ', ', tagSub("name", tagSub("author", authorString)))).strip()


def htmlPrinter(numberList):

    with open("arXivOut.html", "w") as outFile:
        for number in numberList:
            url = 'http://export.arxiv.org/api/query?search_query=all:'+number+'&start=0&max_results=1'
            data = urllib.request.urlopen(url).read()
            abstract = tagSub("summary", str(data, encoding="utf-8"))
            title = tagSub("title", str(data, encoding="utf-8"))
            authors = authorSub(str(data, encoding="utf-8"))

            numberOut = "<section><div class =\"arxiv-number\">"+str(number)+"</div>"
            titleOut = "<div class=\"arxiv-title\" style=\"width: 1900px; margin:2% auto\">"+title+"</div>"
            authorsOut = "<div class=\"arxiv-authors\" style=\"width: 1900px; margin: 0% auto\">"+authors+"</div>"
            abstractOut = "<div class=\"arxiv-abstract\" style=\"width: 1900;margin: 2% auto\">"+abstract+"</div></section>"
            print(numberOut+titleOut+authorsOut+abstractOut, end="\n\n", file=outFile)
    outFile.close()


inList = np.genfromtxt("arXivInList.txt", dtype=str)

htmlPrinter(inList)
