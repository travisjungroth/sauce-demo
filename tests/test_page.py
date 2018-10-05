import pytest


@pytest.mark.usefixtures('driver')
@pytest.mark.parametrize('name',
                         [
                             'Ryan Basch',
                             'Paul Barber',
                             'Ruairi Wiepking',
                             'Dylan Scandalios',
                         ]
                         )
def test_name_form(driver, name):
    min_length = 12
    driver.get('http://localhost:5000/')
    driver.find_element_by_id('name').send_keys(name)
    driver.find_element_by_id('submit').click()
    if len(name) >= min_length:
        assert driver.title == 'Success!'
    else:
        assert driver.title == 'Test Page'

