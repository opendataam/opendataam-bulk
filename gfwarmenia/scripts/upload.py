import json
from ckanapi import RemoteCKAN, NotAuthorized
import ckanapi
UA = 'ckanapiclient/1.0 (+http://example.com/my/website)'

PREFIX = 'recc'

APIKEY = open('api.key','r').read()

def register_package(record, dryrun=False):    
    work = RemoteCKAN('https://data.opendata.am', apikey=APIKEY, user_agent=UA)
    try:
        tags = []
        for word in record['keyword']:
            tags.append({'name': word})
        if not dryrun:
            identifier = record['identifier'].rsplit('?', 1)[-1].split('&')[0].split('=', 1)[-1]
            print(PREFIX + '-' + identifier)
            pkg = work.action.package_create(name=PREFIX + '-' + identifier, 
                title=record['title'], owner_org='reccaucasus',
                url=record['landingPage'],
                notes=record['description'], groups=[{'id' : '888f983a-c7c5-45f7-af74-979c4d03b3a2'}],
                tags=tags, license_url=record['license'])
            print(pkg)
            print('Uploaded ' + pkg['name'])
            for resource in record['distribution']:
                rurl = resource['accessURL']
                work.action.resource_create(package_id=pkg['id'], url=rurl, name=resource['title'], format=resource['format'])
        else:
            print('Dry run')
    except NotAuthorized:
        print('denied')
    except ckanapi.errors.ValidationError:
        print('Already uploaded. Continue')


def run():
    f = open('../data/data.jsonl', 'r', encoding='utf8')
    for l in f:
        record = json.loads(l)
        register_package(record)
    f.close()

if __name__ == '__main__':
    run()