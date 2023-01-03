from megano.core.loading import get_model

Role = get_model('user', 'Role')


class RoleManager:
    def __init__(self, user):
        self.user = user

    def create_roles(self):
        if not Role.objects.all():
            Role.objects.bulk_create(
                [Role(name='admin'), Role(name='customer'), Role(name='anon')]
            )

    def get_user_role(self) -> str:
        self.create_roles()
        if not self.user.is_staff:
            role = "customer"
        else:
            role = "admin"

        return role

