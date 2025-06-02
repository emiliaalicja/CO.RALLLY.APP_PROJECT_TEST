from faker import Faker

fake = Faker()


def random_meeting_name():
    return f"{fake.word().capitalize()} meeting"


def random_location():
    return fake.city()


def random_description():
    return fake.sentence(nb_words=15)


def random_participant():
    return fake.name()  # np. "Jan Kowalski"


def random_email(domain="example.com"):
    name = fake.user_name()
    return f"{name}@{domain}"


def random_comment_author():
    return fake.first_name()  # jeśli inny od autora


def random_comment_description():
    return fake.sentence(nb_words=10)  # krótki komentarz
