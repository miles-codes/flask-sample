from flask import current_app

from fixtures import plaintext_password, user


class DescribeUser:
    def it_hashes_password_when_reseting_it(self, user, plaintext_password):
        user.password = plaintext_password
        assert user.plaintext_password == plaintext_password
        assert user.password != plaintext_password

    def it_foo_anther_test(self, user):
        assert user.email is not None
