import json
from ckanapi import RemoteCKAN, NotAuthorized
import ckanapi
UA = 'ckanapiclient/1.0 (+http://example.com/my/website)'

PREFIX = 'armsis'

APIKEY = open('api.key','r').read()

def register_package(record, dryrun=False):    
    work = RemoteCKAN('https://data.opendata.am', apikey=APIKEY, user_agent=UA)
    try:
        tags = []
        if not dryrun:
            pkg = work.action.package_create(name=PREFIX + '-' + str(record['id']), 
                title=record['title'], owner_org='cas',
                url='https://armsis.cas.am' + record['detail_url'],
                notes=record['abstract'], groups=[{'id' : '888f983a-c7c5-45f7-af74-979c4d03b3a2'}],
                tags=tags)
            print(pkg)
            print('Uploaded ' + pkg['name'])
            for resource in record['links']:
                rurl = resource['url']
                work.action.resource_create(package_id=pkg['id'], url=rurl, name=resource['name'], format=resource['extension'])
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