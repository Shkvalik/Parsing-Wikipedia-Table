import requests
from bs4 import BeautifulSoup


def getData(soup, result):
    table = soup.find("tbody")
    for row in table.find_all("tr"):
        if row.find('td') is not None:  # For skip first rows with name column
            data = {
                'country': row.find('img')['alt'],
                'full_country_name': row.find_all('td')[-1].text.replace('\n', ''),
                'count_letter': len(row.find_all('td')[-1].text.replace('\n', '').replace(' ', '')),
                'flag_img': row.find('img')['src']
            }
            result.append(data)
        else:
            continue
    return result


def getCountSameCountry(result):
    for d in result:
        count = -1  # Start from -1 because we will find current already use country name in dict
        lastLetter = d['country'][0]
        for element in result:
            if element['country'].startswith(lastLetter):
                count = count + 1
        d['countries_with_similar_letters'] = count
    return result


def findCountry(result):
    userInput = input('Enter the name of the country which you want to see ---> ').lower()
    for d in result:
        countryName = d['country'].lower()
        if userInput in countryName[0:len(userInput)]:
            return d
    else:
        return 'Incorrect input'


def start():
    result = []
    soup = BeautifulSoup(
        requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83'
                     '%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2').text, 'lxml')
    getData(soup, result)  # Return completed list of dicts
    print(getCountSameCountry(result))  # Init column countries_with_similar_letters in completed list
    print(findCountry(result))  # Return dict with found info


if __name__ == '__main__':
    start()
