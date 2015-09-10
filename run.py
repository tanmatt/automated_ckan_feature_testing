"""
# common, error, remoteckan scripts are taken from ckanapi: https://github.com/ckan/ckanapi
#    and remoteckan script is modified to deal with self-signed certifified CKAN instance
# documentation for API: http://docs.ckan.org/en/latest/api/index.html#get-able-api-functions


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
"""

from ckan_api.remoteckan import RemoteCKAN
from ckan_api.actions import *


def main(CKAN_URL, API_KEY, OWNER_ORG):
    print "Starting Automated CKAN feature testing...."

    # create ckan_object
    ckan_obj = RemoteCKAN(CKAN_URL, apikey=API_KEY, user_agent='ckan_test_run/1.0 (+https://github.com/tanmaythakur/ckan_test_run)')

    # check if instance is up and running
    site_read(ckan_obj)
    status_show(ckan_obj)

    # make few API calls
    get_package_list(ckan_obj)
    package_search(ckan_obj)

    # try to create a new package inside org
    do_package_create(ckan_obj, OWNER_ORG)

    # try upload a resource
    # CSV
    res_id, pack_id = do_resource_create(ckan_obj)
    site_read(ckan_obj)

    # checking entry in datastore
    ready_to_delete = do_datastore_search(ckan_obj, res_id)

    # try deleting all these uploaded test data
    if ready_to_delete:
        do_datastore_delete(ckan_obj, res_id)
    do_resource_delete(ckan_obj, res_id)
    do_package_delete(ckan_obj, pack_id)

    site_read(ckan_obj)
    print '\nTesting completed and all the test-junk is removed for your ckan instance.'


if __name__ == "__main__":
    CKAN_URL = sys.argv[1]
    API_KEY = sys.argv[2]
    OWNER_ORG = sys.argv[3]
    main(CKAN_URL, API_KEY, OWNER_ORG)