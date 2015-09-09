# Automated CKAN-feature Testing

This is a project to do a test run of all the parts of the CKAN instance with just a single command.
It also includes automated tasks like

 - Calling common CKAN APIs
 - Package creation
 - Resource creation inside the package
 - CSV file upload (fileStore extension test)
 - Datastore table verification (datapusher extension test)
 - Deleting all the uploaded junk data

This project does not require to be run from the CKAN server and can be run from any machine having python with required python packages.

## Pre-requisites
- Running CKAN instance
- Correctly set filestore, datastore and datapusher extensions
- `ckan_url`: URL of ckan instance including http or https (ex: http://demo.ckan.org )
- `my_api_key`: API key for the user who can create packages, resources and upload files in 'my_test_org' (say 'my_api_key')
- `my_test_org`: Create a test-organization (say 'my_test_org')


## Installation and Instructions for Running

1. Get the code and files
    ```
    $ git clone https://github.com/tanmaythakur/automated_ckan_feature_testing.git
    ```

2. Execute the run.py script
    ```
    $ python automated_ckan_feature_testing/run.py  {ckan_url}  {my_api_key} {my_test_org}
    ```


## Common Error Messages and Solutions
 - Package not found:
    - Make sure to install the package using `pip` or `easy_install`
- Follow the steps mentioned in pre-requisites

## Not So Important Notes

- This project creates 'automated_ckan_feature_testing' package.
- After testing is done, the package will be deleted and hence if you already have a package with this name (very rare) then rename the package to anything else in `actions.py`

## Contribution Guide
We all grow together. Please feel free to make changes and make the code more robust. Please use `dev` branch for all your pull requests. This branch will be always updated with the lastest code. `master` branch should have the most recent stable release code.
