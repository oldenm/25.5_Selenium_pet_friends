import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def all_unique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Chromedriver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_all_pets():
    pytest.driver.implicitly_wait(10)
    # Вводим email
    email = pytest.driver.find_element(By.ID, 'email')
    email.send_keys('email159753@ya.ru')
    # Вводим пароль
    password = pytest.driver.find_element(By.ID, 'pass')
    password.send_keys('pswrd')
    # Нажимаем на кнопку входа в аккаунт
    submit = pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
    # Проверяем, что мы оказались на главной странице пользователя
    h1 = pytest.driver.find_element(By.TAG_NAME, 'h1')
    assert h1.text == "PetFriends"

    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    pytest.driver.implicitly_wait(10)
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets():
    pytest.driver.implicitly_wait(10)
    # Вводим email
    email = pytest.driver.find_element(By.ID, 'email')
    email.send_keys('email159753@ya.ru')
    # Вводим пароль
    password = pytest.driver.find_element(By.ID, 'pass')
    password.send_keys('pswrd')
    # Нажимаем на кнопку входа в аккаунт
    submit = pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit.click()
    # Проверяем, что мы оказались на главной странице пользователя
    h1 = pytest.driver.find_element(By.TAG_NAME, 'h1')
    assert h1.text == "PetFriends"
    my_pets = pytest.driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']")
    my_pets.click()
    h2 = pytest.driver.find_element(By.CSS_SELECTOR, 'div.\\.col-sm-4.left > h2')
    assert h2.text == 'кеша'
    pets = pytest.driver.find_element(By.CSS_SELECTOR, 'div.\\.col-sm-4.left')
    pet = pets.text.split('\n')
    pet.remove(h2.text)
    p = pet[0].split(': ')
    num_pet = int(p[1])
    table_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'table.table-hover tbody tr')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table'
                                                                                     '/tbody/tr/th/img')))
    table_imgs = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    table_names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    table_species = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    table_age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    # Проверяем что количество питомцев совпвдает с количеством питомцев в таблице
    assert num_pet == len(table_pets)

    x = 0
    images_src = list()

    for i in range(num_pet):
        images_src.append(table_imgs[i].get_attribute('src'))

    for i in range(num_pet):
        for p in range(num_pet):
            if table_imgs[p].get_attribute('src') != '':
                x += 1
        # Проверяем что у более половины питомцев есть фото
        assert x > (num_pet / 2)
        # Проверяем что у всех питомцев есть имя
        assert table_names[i].text != ''
        # Проверяем что у всех питомцев разные имена
        assert all_unique(table_names)
        # Проверяем что у всех питомцев есть заполненное поле вид
        assert table_species[i].text != ''
        # Проверяем что у всех питомцев есть возраст
        assert table_age[i].text != ''
        # Проверяем что у всех питомцев разные фото
        assert all_unique(images_src)
