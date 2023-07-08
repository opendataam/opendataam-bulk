import json
from ckanapi import RemoteCKAN, NotAuthorized
import ckanapi
UA = 'ckanapiclient/1.0 (+http://example.com/my/website)'

PREFIX = 'wdwp'

APIKEY = open('api.key','r').read()

def register_package(record, dryrun=False):    
    work = RemoteCKAN('https://data.opendata.am', apikey=APIKEY, user_agent=UA)
    try:
        tags = []
        if not dryrun:
            print(PREFIX + "-" + record['id'])
            pkg = work.action.package_create(name=PREFIX + "-" + record['id'], 
                title=record['title'], owner_org='worldpop',
                url=record['url_summary'],
                notes=record['desc'], groups=[{'id' : '888f983a-c7c5-45f7-af74-979c4d03b3a2'}],
                tags=tags)
            print('Uploaded ' + pkg['name'])
            for resource_url in record['files']:
                work.action.resource_create(package_id=pkg['id'], url=resource_url, name=resource_url.rsplit('/', 1)[-1], format=record['data_format'])
        else:
            print('Dry run')
    except NotAuthorized:
        print('denied')
    except ckanapi.errors.ValidationError:
        print('Already uploaded. Continue')


def run():
    f = open('../data/armenia.jsonl', 'r', encoding='utf8')
    for l in f:
        record = json.loads(l)
        register_package(record['data'])
    f.close()

if __name__ == '__main__':
    run()