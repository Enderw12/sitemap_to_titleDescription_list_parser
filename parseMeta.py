import requests
from bs4 import BeautifulSoup as bs
import argparse
import lxml
import pandas as pd
import concurrent
import concurrent.futures as futures
from time import sleep
import sys
from datetime import datetime as datetime


def toExcel(dataList, fileName):
    res = pd.DataFrame()
    for values in dataList:
        res = res.append(pd.DataFrame([[values['pageLink'], values['url'],  values['title'], values['description'], ]], columns=[
                         'pageLink', 'url', 'title', 'description', ]), ignore_index=True)

    date = datetime.now()
    resultName = f'{fileName}_{date.year}—{date.month}—{date.day}_{date.hour}:{date.minute}.xlsx'
    print(resultName)
    return res.to_excel(resultName)


def concurentParsing(function, listOfUrls, max_workers):
    results = []

    executor = futures.ThreadPoolExecutor(max_workers)
    future_results = executor.map(function, listOfUrls[::])
    for future in future_results:
        results.append(future)

    return results


def parseMetaTags(pageUrl):
    page = requests.get(pageUrl, verify=False).text
    pageSoup = bs(page, features="lxml")
    values = {}
    title = pageSoup.find('meta', property='og:title')
    description = pageSoup.find('meta', property='og:title')
    url = pageSoup.find('meta', property='og:url')
    values['title'] = title['content'] if title else '-'
    values['description'] = description['content'] if description else '-'
    values['url'] = url['content'] if url else '-'
    values['pageLink'] = pageUrl
    sleep(timeout/1000)
    return values


def parsePagesUrls(sourceUrl):
    sourcePage = requests.get(sourceUrl, verify=False).text
    links = bs(sourcePage, features="lxml-xml").find_all('loc',)
    pagesUrls = []
    for loc in links:
        url = loc.text
        pagesUrls.append(url)
    return pagesUrls


def getArguments():
    parser = argparse.ArgumentParser(
        description='Parse webpages from given sitemap.xml, with given number of workers(threads)')
    parser.add_argument(
        "--sitemap", default="", help="enter an url of sitemap where you want to parse all websiteURLs")
    parser.add_argument("--threads", default=5,
                        help="number of threads(workers) for parsing")
    parser.add_argument("--timeout", default=1000,
                        help="timeout between request for individual worker default = 1000 ms")
    args = parser.parse_args()

    print('Chosen sitemap.xml is: ' + args.sitemap)
    print('Threads: ' + str(args.threads))
    print('Timeout: ' + str(args.timeout) + 'ms')
    args.threads = int(args.threads)
    args.timeout = int(args.timeout)
    if len(args.sitemap) < 1:
        print('You have to enter sitemap url!')
        sys.exit()

    return args


requests.packages.urllib3.disable_warnings()
arguments = getArguments()
sourceUrl = arguments.sitemap
threads = arguments.threads
timeout = arguments.timeout
listOfUrls = parsePagesUrls(sourceUrl)
print('Links found in sitemap.xml: ' + str(len(listOfUrls)))
resultsList = []

resultsList = concurentParsing(
    parseMetaTags, listOfUrls, max_workers=threads)

fileName = sourceUrl.replace(
    "http://", "").replace("https://", "").replace("www.", "").split('/')[0]

toExcel(resultsList, fileName)
