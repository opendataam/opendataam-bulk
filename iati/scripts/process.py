import json
def run():
    out = open('../data/data.jsonl', 'w', encoding='utf8')
    f = open('../data/iati.jsonl', 'r', encoding='utf8')
    for l in f:
        record = json.loads(l)
        record['owner_org']  = 'iati'
        # Finances group
        record['groups'] = [{'id' : '289c2ac0-2b46-4aad-b6f2-c8c9633b79c7'}]
        del record['organization']
        out.write(json.dumps(record) + '\n')
    f.close()
    out.close()

if __name__ == '__main__':
    run()