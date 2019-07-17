
import requests
import re


base_url = 'https://www.transavia.com'
session = requests.session()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
languages = 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'


def main():
    dnt_portal = session.get(
        base_url + '/fr-FR/reservez-un-vol/vols/rechercher/',
        headers={
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': languages,
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        }
    )

    script = session.get(
        base_url + re.search(
            '<script type="text/javascript" src="(.+)" defer>',
            dnt_portal.content.decode()
        ).group(1),
        headers={
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': languages,
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        }
    )

    # retrieve valid cookies
    post_url = re.search('path:"(.+)",ajax', script.content.decode()).group(1)
    ajax_header = re.search('ajax_header:"(\w+)"', script.content.decode()).group(1)
    session.post(
        base_url + post_url,
        headers={
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': languages,
            'X-Distil-Ajax': ajax_header,
            'Content-Type': 'text/plain;charset=UTF-8',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        },
        # with browser's finger print
        data={
        'p': '{'
             '"cookies":1,'
             '"setTimeout":0,'
             '"setInterval":0,'
             '"appName":"Netscape",'
             '"platform":"MacIntel",'
             '"syslang":"fr",'
             '"userlang":"fr",'
             '"cpu":"IntelMacOSX10.14",'
             '"productSub":"20100101",'
             '"plugins":{},'
             '"mimeTypes":{},'
             '"screen":{'
                '"width":1920,'
                '"height":1080,'
                '"colorDepth":24'
             '},'
             '"fonts":{'
                '"0":"HoeflerText",'
                '"1":"Monaco",'
                '"2":"Georgia",'
                '"3":"TrebuchetMS",'
                '"4":"Verdana",'
                '"5":"AndaleMono",'
                '"6":"Monaco",'
                '"7":"CourierNew",'
                '"8":"Courier"'
             '}}'
    })


if __name__ == '__main__':
    main()
