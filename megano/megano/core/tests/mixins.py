from django.contrib.auth import get_user_model

User = get_user_model()

ROOT_USERNAME = "root"
NOT_ROOT_USERNAME = "danil"


class TestInitialUserDataMixin:
    model = User

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username=ROOT_USERNAME,
            password="1234",
            is_superuser=True,
        )

        User.objects.create(
            username=NOT_ROOT_USERNAME,
            password="1234",

        )

    @classmethod
    def get_root_user(cls):
        root = User.objects.get(username=ROOT_USERNAME)
        new_password = User.objects.make_random_password()
        root.set_password(new_password)
        root.save()

        return root.username, new_password

    @classmethod
    def get_basic_user(cls):
        user = User.objects.get(username=NOT_ROOT_USERNAME)
        new_password = User.objects.make_random_password()

        user.set_password(new_password)
        user.save()
        return user.username, new_password
