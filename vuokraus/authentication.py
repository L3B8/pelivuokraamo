from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            #etsi käyttäjä, jonka käyttäjätunnus vastaa annettua arvoa, mutta ei välitä kirjainkoosta.
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
