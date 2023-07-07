import json
from ckanapi import RemoteCKAN, NotAuthorized
import ckanapi
UA = 'ckanapiclient/1.0 (+http://example.com/my/website)'

PREFIX = 'dcwb'

APIKEY = open('api.key','r').read()

def register_package(record, dryrun=False):    
    work = RemoteCKAN('https://data.opendata.am', apikey=APIKEY, user_agent=UA)
    try:
        tags = []
        for word in record['keywords_list']:
            tags.append({'name': word})
        if not dryrun:
            pkg = work.action.package_create(name=PREFIX + record['dataset_unique_id'], 
                title=record['name'], owner_org='opendataam',
                url='https://datacatalog.worldbank.org/search/dataset/' + record['dataset_unique_id'],
                notes=record['identification']['description'] if record['identification']['description'] is not None else "" + '\n\n' + 'Data collected from World Bank data catalog https://datacatalog.worldbank.org', groups=[{'id' : '1cd0d2a6-7e8c-4c7d-be0f-ce4f4bdac08b'}],
                tags=tags)
            print('Uploaded ' + pkg['name'])
            for resource in record['Resources']:
                rurl = resource['url'] if resource['url'] is not None and len(resource['url']) > 0 else resource['website_url']
                work.action.resource_create(package_id=pkg['id'], url=rurl, name=resource['name'], description=resource['description'], format=resource['format'])
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
        register_package(record)
    f.close()

if __name__ == '__main__':
    run()