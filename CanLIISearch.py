import requests
import json
import pprint

supported_languages = ['en', 'fr']


def get_databases_list(lang='en', database_id=None, jurisdiction=None, name=None, see_list=False):
    if lang not in supported_languages:
        return
    case_browse_url = 'http://api.canlii.org/v1/caseBrowse/{}/?api_key='.format(lang)
    canlii_database_data = requests.get(case_browse_url)
    json_data = canlii_database_data.json()
    if see_list:
        pprint.pprint(json_data)
    for data in json_data['caseDatabases']:
        if data['databaseId'] == database_id or data['jurisdiction'] == jurisdiction or data['name'] == name:
            print('Found: {}'.format(data))


def get_cases_list(lang='en', database_id=None, offset=0, result_count=10):
    if lang not in supported_languages or database_id is None:
        print('Please input the proper database_id')
        return
    case_browse_url = 'http://api.canlii.org/v1/caseBrowse/{}/{}/?offset={}&resultCount={' \
                      '}&api_key='.format(lang, database_id, offset, result_count)
    canlii_case_data = requests.get(case_browse_url)
    if canlii_case_data.status_code == 404:
        print('Could not find any results, make sure database id is correct')
        return
    json_data = canlii_case_data.json()
    pprint.pprint(json_data)


def get_case_metadata(lang='en', database_id=None, case_id=None):
    if database_id is None or case_id is None:
        print('missing_inputs')
        return
    case_browse_url = 'http://api.canlii.org/v1/caseBrowse/{}/{}/{}/?api_key='.format(lang, database_id, case_id)
    canlii_case_metadata = requests.get(case_browse_url)
    json_data = canlii_case_metadata.json()
    pprint.pprint(json_data)

if __name__ == '__main__':
    func_dict = {'getdb': get_databases_list, 'getcase': get_cases_list, 'getcasemeta': get_case_metadata}
    func_dict['getdb'](see_list=True)
    func_dict['getcase'](database_id='ntls')
    func_dict['getcasemeta'](database_id='abwcac', case_id='2013canlii10946')