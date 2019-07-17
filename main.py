import requests
import re
from lxml import html
from dateutil import parser as dt_parser
import click


base_url = 'https://www.transavia.com'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
languages = 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
__session__ = None


def get_session():

    global __session__

    if __session__:
        return __session__

    session = requests.session()

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

    __session__ = session
    return session


@click.command()
@click.option('--frm', default='ORY', help='Departure: airport code')
@click.option('--to', default='AMS', help='Arrival: airport code')
def scrape(frm, to):
    session = get_session()

    response = session.post(
        base_url + "/fr-FR/reservez-un-vol/vols/multidayavailability/",
        headers={
            'Accept': '*/*',
            'Accept-Language': languages,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Referer': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/',
            'TE': 'Trailers',
            'User-Agent': user_agent,
            # 'X-Distil-Ajax': ajax_header,
            'X-Requested-With': 'XMLHttpRequest',
            'cache-control': 'no-cache',
        },
        data={
            'selectPassengersCount.AdultCount': '1',
            'selectPassengersCount.ChildCount': '0',
            'selectPassengersCount.InfantCount': '0',
            'routeSelection.DepartureStation': frm,
            'routeSelection.ArrivalStation': to,
            'dateSelection.OutboundDate.Day': '18',
            'dateSelection.OutboundDate.Month': '8',
            'dateSelection.OutboundDate.Year': '2019',
            'dateSelection.InboundDate.Day': '25',
            'dateSelection.InboundDate.Month': '8',
            'dateSelection.InboundDate.Year': '2019',
            'dateSelection.IsReturnFlight': 'true',
            'flyingBlueSearch.FlyingBlueSearch': 'false'
        }
    )

    json_content = response.json()
    inbound = json_content.get('multiDayAvailabilityInbound')
    outbound = json_content.get('multiDayAvailabilityOutbound')

    if not inbound or not outbound:
        raise Exception('Whopsey !')

    inbound = html.fromstring(inbound)
    in_availabilities = [
        (
            dt_parser.parse(div.attrib['data-date']),
            div.find('.//span[@class="price"]').text_content().strip().split("\n")[1].strip()
        ) for div in inbound.findall(
            ".//ol/li/div[@class='day day-with-availability']"
        )
    ]
    outbound = html.fromstring(outbound)
    out_availabilities = [
        (
            dt_parser.parse(div.attrib['data-date']),
            div.find('.//span[@class="price"]').text_content().strip().split("\n")[1].strip()
        ) for div in inbound.findall(
            ".//ol/li/div[@class='day day-with-availability']"
        )
    ]

    print(
        "From %s:" % frm,
        ",".join([
            "%s (%s)" % (
                d.date(),
                p
            ) for (d, p) in in_availabilities
        ]),
        "\nTo %s" % to,
        ",".join([
            "%s (%s)" % (
                d.date(),
                p
            ) for (d, p) in out_availabilities
        ]),
    )


if __name__ == '__main__':
    scrape()
