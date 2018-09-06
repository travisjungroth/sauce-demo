import pytest
from os import environ

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection


@pytest.fixture(scope='function')
def driver(request):
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = {}

    browser = {
        "platform": "Windows 10",
        "browserName": "internet explorer",
        "version": "11.103"
    }

    desired_caps.update(browser)
    test_name = request.node.name
    build_tag = environ.get('CIRCLE_BUILD_NUM', None)
    tunnel_id = environ.get('TRAVIS_JOB_NUMBER', None)
    username = environ.get('SAUCE_USERNAME', None)
    access_key = environ.get('SAUCE_ACCESS_KEY', None)

    selenium_endpoint = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key)
    desired_caps['build'] = build_tag
    # we can move this to the config load or not, also messing with this on a test to test basis is possible :)
    desired_caps['tunnelIdentifier'] = tunnel_id
    desired_caps['name'] = test_name

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps
    )
    yield browser

    def fin():
        browser.execute_script("sauce:job-result={}".format(str(not request.node.rep_call.failed).lower()))
        browser.quit()
    request.addfinalizer(fin)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
