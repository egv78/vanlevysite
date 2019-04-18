from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import datetime
import json


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


# Class to permit the authentication using email or username
# https://stackoverflow.com/questions/37332190/django-login-with-email
class CustomBackend(ModelBackend):  # requires to define two functions authenticate and get_user

    def authenticate(self, request, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        now = datetime.datetime.now()
        now_json = json.dumps(now, sort_keys=True, indent=1, default=default)

        try:
            # below line gives query set,you can change the queryset as per your requirement
            user = usermodel.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).distinct()

        except usermodel.DoesNotExist:
            return None

        if user.exists():
            ''' get the user object from the underlying query set,
            there will only be one object since username and email
            should be unique fields in your models.'''
            user_obj = user.first()
            if user_obj.check_password(password):
                if 'bad_logins' in request.session:
                    del request.session['bad_logins']
                if 'delay' in request.session:
                    del request.session['delay']
                if 'bad_login_time' in request.session:
                    del request.session['bad_login_time']
                return user_obj
            else:
                if 'bad_login_time' in request.session:
                    past_bad_logins = request.session['bad_logins']
                    time_to_clear = datetime.timedelta(minutes=past_bad_logins)
                    first_bad_login_time = datetime.datetime.strptime(str(request.session['bad_login_time']).replace('"', ''),
                                                                      '%Y-%m-%dT%H:%M:%S.%f')
                    clear_time = first_bad_login_time + time_to_clear
                    if now > clear_time:
                        request.session['bad_logins'] = 1
                        request.session['bad_login_time'] = now_json
                        if 'delay' in request.session:
                            del request.session['delay']

                if 'bad_logins' in request.session:
                    request.session['bad_logins'] += 1
                    bad_logins = request.session['bad_logins']
                    request.session['delay'] = ((bad_logins - 1) // 3) * 5
                    if 'bad_login_time' not in request.session:
                        request.session['bad_login_time'] = now_json  # here
                else:
                    request.session['bad_logins'] = 1
                    request.session['bad_login_time'] = now_json
                    if 'delay' in request.session:
                        del request.session['delay']
                print(str(request.session['bad_logins']))
                return None
        else:
            if 'bad_logins' in request.session:
                request.session['bad_logins'] += 1
                request.session['delay'] = ((request.session['bad_logins'] - 1) // 3) * 5
            else:
                request.session['bad_logins'] = 1
            if 'bad_login_time' not in request.session:
                request.session['bad_login_time'] = now_json
            return None

    def get_user(self, user_id):
        usermodel = get_user_model()
        try:
            return usermodel.objects.get(pk=user_id)
        except usermodel.DoesNotExist:
            return None
