
import api
from settings import valid_email, valid_password, empty_email, empty_password, empty_auth_key, incorrect_auth_key
import os


pf = api.PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key """


    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_valid_data(name="Маня", animal_type="свинка", age="1", pet_photo="images/pig.jpg"):
    """ Проверяем что можно добавить питомца с корректными данными """


    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name


def test_delete_pet():
    """ Проверяем возможность удаления своего питомца """


    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Мурзик", "полосатый", "4", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name="Змей", animal_type="уж лесной", age="2"):
    """ Проверяем возможность обновления информации о своем питомце """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("No pets")


def test_add_new_pet_without_photo_valid_data(name="Умка", animal_type="щенок", age="0,5"):
    """ Проверяем возможность добавления питомца (без фото) с корректными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name


def test_add_new_pet_empty_data(name="", animal_type="", age="", pet_photo="images/pig.jpg"):
    """ Проверяем возможность добавить питомца с фото и незаполненными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name


def test_add_new_pet_incorrect_age(name="Маня", animal_type="свинка", age="-1", pet_photo="images/pig.jpg"):
    """ Проверяем возможность добавить питомца с отрицательным возрастом """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["age"] == age


def test_delete_not_your_pet():
    """ Проверяем возможность удаления не своего питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    if len(all_pets["pets"]) > 0:
        pet_id = all_pets["pets"][0]["id"]
        status = pf.delete_pet(auth_key, pet_id)

        assert status == 200
        assert pet_id not in all_pets.values()
    else:
        raise Exception("No pets")


def test_add_new_pet_without_photo_empty_data(name="", animal_type="", age=""):
    """ Проверяем возможность добавления питомца (без фото) с незаполненными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name


def test_set_photo_pet(pet_photo="images/cat.jpg"):
    """ Проверяем возможность добавления фото к информации о своем питомце """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.set_photo_pet(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
        assert result["pet_photo"]
    else:
        raise Exception("No pets")
