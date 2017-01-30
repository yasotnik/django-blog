from django.views import generic
from .models import Post, Category, BlogSettings, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView
from .forms import UserForm, ProfileForm


class PostsView(generic.ListView):
    template_name = 'blogpost/index.html'

    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context

    # def get_queryset(self):
    #     return Post.objects.all()


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogpost/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context


class UserFormView(View):
    form_class = UserForm
    template_name = 'blogpost/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog})

    # reg user
    def post(self, request):
        form = self.form_class(request.POST)
        blog = BlogSettings.objects.all()[0]
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blogpost:index')

        return render(request, self.template_name, {'form': form, 'blog': blog})


class LoginView(RedirectView):
    def post(self, request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blogpost:index')
                else:
                    print('Not active')
            else:
                print('No user')
                return redirect('blogpost:index')
        print('Shit')
        return redirect('blogpost:index')


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('blogpost:index')


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'blogpost/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context


class ProfileUpdate(View):

    form_class = ProfileForm
    template_name = 'blogpost/profile_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog})

    # update profile
    def post(self, request):
        # p = request.POST.get('pk', None)
        # model = Profile.objects.get_or_create(pk=p)
        form = self.form_class(request.POST, instance=request.user.profile)
        blog = BlogSettings.objects.all()[0]
        if form.is_valid():
            # user = request.POST.user
            avatar = form.cleaned_data['avatar']
            facebook = form.cleaned_data['facebook']
            twitter = form.cleaned_data['twitter']
            form.save()
            return redirect('blogpost:index')
