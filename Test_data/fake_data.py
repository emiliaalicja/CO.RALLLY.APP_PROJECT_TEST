from faker import Faker

fake = Faker()

def random_meeting_name():
    return f"{fake.word().capitalize()} meeting"

def random_location():
    return fake.city()

def random_description():
    return fake.sentence(nb_words=15)

def random_author():
    return fake.name()  # np. "Jan Kowalski"

def random_comment_author():
    return fake.first_name()  # jeśli inny od autora

def random_comment_description():
    return fake.sentence(nb_words=10)  # krótki komentarz




