__author__ = 'adarsh'

import requests
import bs4
import json
import string

run_csv = True


def main():
    my_url = 'http://www.ultimatestrictly.com/series-{0}-week-{1}/'
    my_html = open('Week_1_ULTIMATE STRICTLY.html')
    my_json = 'scd_result_set_series{0}_week{1}.json'
    my_csv = 'scd_result_series{0}_week{1}.csv'
    seriesnum = "12"

    for weeknum in range(1, 2):
        #response = requests.get(my_url.format(seriesnum, weeknum))
        #soup = bs4.BeautifulSoup(response.text, "lxml")
        soup = bs4.BeautifulSoup(my_html, "lxml")
        res = soup.find_all('td')
        totalset = {}
        scoreset = {}
        resultString = ''
        scoreset[weeknum] = {}
        i = 0

        while i < len(res) - 7:
            if len(res[i].string) > 5:
                if run_csv:
                    resultString += cleanString(str(seriesnum))
                    resultString += cleanString(str(weeknum))
                    resultString += cleanString(res[i].string)
                    resultString += cleanString(res[i + 1].string)
                    resultString += cleanString(res[i + 2].string)
                    resultString += cleanString(res[i + 3].string)
                    resultString += cleanString(res[i + 4].string)
                    resultString += cleanString(res[i + 5].string)
                    resultString += cleanString(res[i + 6].string)
                    resultString += cleanString(res[i + 7].string)
                    resultString += '\n'
                else:
                    scoreset[weeknum][res[i].string] = {}
                    scoreset[weeknum][res[i].string]['Names'] = res[i].string
                    scoreset[weeknum][res[i].string]['DanceType'] = res[i + 1].string
                    scoreset[weeknum][res[i].string]['SongName'] = res[i + 2].string
                    scoreset[weeknum][res[i].string]['Craig'] = res[i + 3].string
                    scoreset[weeknum][res[i].string]['Darcy'] = res[i + 4].string
                    scoreset[weeknum][res[i].string]['Len'] = res[i + 5].string
                    scoreset[weeknum][res[i].string]['Bruno'] = res[i + 6].string
                    scoreset[weeknum][res[i].string]['total'] = res[i + 7].string
                    totalset.update(scoreset)
            i += 8
            if run_csv:
                with open(my_csv.format(seriesnum, weeknum), 'w') as fp:
                    fp.write(resultString)
            else:
                with open(my_json.format(seriesnum, weeknum), 'w') as fp:
                    json.dump(totalset, fp)

    if run_csv:
        print resultString
    else:
        print json.dumps(totalset, sort_keys=True, indent=4)


def cleanString(s):
    s = filter(lambda x: x in string.printable, s)
    s = s.replace(',', '')
    return s + ','


if __name__ == '__main__':
    main()
