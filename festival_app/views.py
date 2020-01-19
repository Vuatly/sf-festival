from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView, RedirectView
from festival_app.forms import CreateApplicationForm
from festival_app.models import Application, Scene, count_rating, count_votes
from user_profiles.models import UserProfile


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['scenes'] = Scene.objects.all()
        if self.request.user.is_anonymous:
            return context
        if self.request.user.is_authenticated:
            user = UserProfile.objects.get(user=self.request.user)
            if user.type == 'MU' and Application.objects.filter(user=user):
                context['app'] = Application.objects.get(user=user)
                return context
            if user.type == 'CE':
                context['censor'] = user
                return context
        return context


class ErrorView(TemplateView):
    template_name = 'error.html'


class WayView(TemplateView):
    template_name = 'way.html'


class CreateApplication(FormView):
    form_class = CreateApplicationForm
    template_name = 'application-create.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'MU':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        if Application.objects.filter(user=user):
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(CreateApplication, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = UserProfile.objects.get(user=self.request.user)
        instance.save()
        return super(CreateApplication, self).form_valid(form)


class ViewApplications(ListView):
    model = Application
    context_object_name = 'applications'
    template_name = 'view-applications.html'
    queryset = Application.objects.filter(denied=False)
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(ViewApplications, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewApplications, self).get_context_data(**kwargs)
        context['accepted_apps'] = Application.objects.filter(accepted=True)
        context['unreviewed_apps'] = Application.objects.filter(accepted=False, denied=False)
        context['sum_unrw_apps'] = Application.objects.filter(accepted=False, denied=False).count()
        return context


class ViewApplicationDetailCensor(DetailView):
    model = Application
    template_name = 'view-app-detail-censor.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(ViewApplicationDetailCensor, self).dispatch(request, *args, **kwargs)


class ViewApplicationDetailMusican(DetailView):
    model = Application
    template_name = 'view-app-detail-musican.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        slug = self.kwargs.get('slug')
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'MU':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        if user != Application.objects.get(slug=slug).user:
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(ViewApplicationDetailMusican, self).dispatch(request, *args, **kwargs)

 
    


class AppLikeToggle(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(AppLikeToggle, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Application, slug=slug)
        url_ = obj.get_absolute_url()
        user = UserProfile.objects.get(user=self.request.user)
        if user in obj.dislikes.all():
            obj.dislikes.remove(user)
        if user in obj.abstain.all():
            obj.abstain.remove(user)
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)
        count_votes(slug)
        count_rating(slug)
        return url_


class AppDislikeToggle(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(AppDislikeToggle, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Application, slug=slug)
        url_ = obj.get_absolute_url()
        user = UserProfile.objects.get(user=self.request.user)
        if user in obj.likes.all():
            obj.likes.remove(user)
        if user in obj.abstain.all():
            obj.abstain.remove(user)
        if user in obj.dislikes.all():
            obj.dislikes.remove(user)
        else:
            obj.dislikes.add(user)
        count_votes(slug)
        count_rating(slug)
        return url_


class AppAbstainToggle(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(AppAbstainToggle, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Application, slug=slug)
        url_ = obj.get_absolute_url()
        user = UserProfile.objects.get(user=self.request.user)
        if user in obj.likes.all():
            obj.likes.remove(user)
        if user in obj.dislikes.all():
            obj.dislikes.remove(user)
        if user in obj.abstain.all():
            obj.abstain.remove(user)
        else:
            obj.abstain.add(user)
        count_votes(slug)
        count_rating(slug)
        return url_


class AppAcceptToggle(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(AppAcceptToggle, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Application, slug=slug)
        url_ = obj.get_absolute_url()
        if not obj.accepted:
            obj.accepted = True
            obj.save()
        return url_


class AppDeniedToggle(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('user_profiles:login'))
        user = UserProfile.objects.get(user=self.request.user)
        if user.type != 'CE':
            return HttpResponseRedirect(reverse_lazy('festival_app:error'))
        else:
            return super(AppDeniedToggle, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Application, slug=slug)
        url_ = obj.get_absolute_url()
        if not obj.denied:
            obj.denied = True
            obj.save()
        return url_



