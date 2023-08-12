from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username__iexact=username)  # case-insensitive comparison
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # If multiple objects are returned, get the first one. This is a rare case and can be handled differently if needed.
            user = UserModel.objects.filter(username__iexact=username).first()
        if user.check_password(password):
            return user
        return None
