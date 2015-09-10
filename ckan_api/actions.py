'''
Exceptions

NotAuthorized - user unauthorized or accessing a deleted item
NotFound - name/id not found
ValidationError - field errors listed in .error_dict
SearchQueryError - error reported from SOLR index
SearchError
CKANAPIError - incorrect use of ckanapi or unable to parse response
ServerIncompatibleError - the remote API is not a CKAN API
'''


import time
import sys


def site_read(ckan_obj):
    if ckan_obj.action.site_read():
        print "\nCKAN instance is up and running."
    else:
        print "\nCKAN instance is down. Please retry.\n"
        sys.exit()


def status_show(ckan_obj):
    res = ckan_obj.action.status_show()
    print "\nCalling status_show: %s" % str(res)
    if 'datastore' not in res['extensions'] or 'datapusher' not in res['extensions']:
        print 'datastore and datapusher extensions are required for ckan_test_run'
        sys.exit()


def get_package_list(ckan_obj):
    print "\nCalling for package_list: \n%s" % str(ckan_obj.action.package_list())


def package_search(ckan_obj):
    print "\nChecking package_search specifically to test SOLR:"
    print ckan_obj.action.package_search()


def do_package_create(ckan_obj, ownr_org):
    try:
        res = ckan_obj.action.package_create(name='automated_ckan_feature_testing', owner_org=ownr_org)
        print '\nPackage created: %s' % str(res)
    except Exception, ex:
        print '\nError creating a package.'
        if ex.__dict__.has_key('error_dict'):
            print ex.__dict__['error_dict']['name'][0]
            if ex.__dict__['error_dict']['name'][0] == 'That URL is already in use.':
                print 'Making the package active again'
                ckan_obj.action.package_update(name='automated_ckan_feature_testing', state='active')
        else:
            print ex.__dict__


def do_resource_create(ckan_obj):
    res = ckan_obj.action.resource_create(package_id='automated_ckan_feature_testing', url='samplecsv', upload=open('files/samplecsv.csv'))
    print '\nCreating new csv resource: '
    print res
    print 'Resource with %s is created inside %s package' % (res['id'], res['package_id'])
    return res['id'], res['package_id']


def do_datastore_search(ckan_obj, res_id):
    print '\nChecking if datastore is updated with the new resource:'
    print 'The program will halt for 7 sec to let the datastore_create process to complete.'
    time.sleep(7)
    try:
        res = ckan_obj.action.datastore_search(resource_id=res_id, limit=10)
        print res
        if len(res['records']) == 0:
            print 'No records found. Datastore was not updated properly.'
            return False
        else:
            print 'Datastore/ Datapusher are working fine.'
            return True
    except Exception, ex:
        print 'Datastore failed to update. Please check datapusher logs: '+str(ex)
        return False


def do_datastore_delete(ckan_obj, res_id):
    print "\nDatastore table deleted: " + str(ckan_obj.action.datastore_delete(resource_id=res_id, force=True))


def do_resource_delete(ckan_obj, res_id):
    ckan_obj.action.resource_delete(id=res_id)
    print "\nResource deleted: %s" % res_id


def do_package_delete(ckan_obj, pack_id):
    ckan_obj.action.package_delete(id=pack_id)
    print "\nPackage deleted: %s" % pack_id


#########################
# WIP - Trying to upload json and create datastore table

'''
def do_resource_create_json(ckan_obj):
    res = ckan_obj.action.resource_create(package_id='automated_ckan_feature_testing', url='samplejson', upload=open('samplejson1.json'))
    print '\nCreating new json resource: '
    print res
    try:
        do_datastore_create(ckan_obj, res['id'])
        print 'Entering records into datastore_table. Waiting for 5 sec....'
        time.sleep(5)
        do_datastore_upsert_json(ckan_obj, res['id'], res['url'])
    except Exception, ex:
        print 'Error while calling datastore_create/ datastore_upsert: '+str(ex)
    return res['id'], res['package_id']


def do_resource_upsert_json(ckan_obj):
    print '\nAdding : '
    try:
        import json
        # read json file and create a list of dict for records
        with open('samplejson1.json') as json_file:
            recs = json.load(json_file)
        recs = [].append(recs)
        # call datastore_create with resource and records
        res_dict={}
        res_dict['package_id'] = 'automated_ckan_feature_testing'
        res_dict['url'] = 'upload'
        res = ckan_obj.action.datastore_create(resource=res_dict, records=recs, force=True)
        print res
    except Exception, ex:
        print 'Error while calling datastore_create: '+str(ex)
    #return res['id'], res['package_id']


def do_resource_create_json_manual(ckan_obj):
    print '\nCreating new json resource: '
    try:
        import json

        #res = ckan_obj.action.datastore_create(resource_id='jsonusingapi', force=True)
        #print res
        #res_id = res['id']

        # read json file and create a list of dict for records
        with open('samplejson1.json') as json_file:
            recs = json.load(json_file)
        print type(recs)
        recs_list = []
        recs_list.append(recs)
        # call datastore_create with resource and records
        res_dict={}
        res_dict['package_id'] = 'automated_ckan_feature_testing'
        #res_dict['url'] = 'automated_ckan_feature_testing'
        print res_dict
        print recs_list
        #res = ckan_obj.action.datastore_create(resource=res_dict, records=recs_list, force=True)
        res_id='2ec30eb6-ab1c-4da0-875b-6d6fe5d4baa9'
        res = ckan_obj.action.datastore_upsert(resource_id=res_id, records=recs_list, force=True, method='insert')
        print res
    except Exception, ex:
        print 'Error while calling datastore_create: '+str(ex)
    #return res['id'], res['package_id']


def do_datastore_create(ckan_obj, res_id):
    print '\nAdding the newly created resource to datastore:'
    ckan_obj.action.datastore_create(resource_id=res_id, force=True)


def do_datastore_upsert_json(ckan_obj, res_id, url):
    import requests
    import json
    try:
        resp = requests.get(url, verify=False)
    except Exception:
        print 'InsecureRequestWarning: Unverified HTTPS request is being made.'
    data = json.loads(str(resp.content))
    in_list = []
    in_list.append(data)
    print '\nAdding the newly created resource to datastore:'
    print ckan_obj.action.datastore_upsert(resource_id=res_id, records=in_list, force=True, method='insert')

'''


