from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from user_profiles.forms import RegistrationForm


class RegisterView(FormView):
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)


