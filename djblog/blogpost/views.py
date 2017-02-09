from django.views import generic
from .models import Post, Category, BlogSettings, Profile
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView, CreateView
from .forms import UserForm, ProfileForm, PostForm


class PostsView(generic.ListView):
    template_name = 'blogpost/index.html'

    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogpost/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context


class CategoryDetailView(View):
    template_name = 'blogpost/category.html'

    def get(self, request, slug):
        blog = BlogSettings.objects.all()[0]
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(category=category)
        return render(request, self.template_name, {'blog': blog, 'posts': posts})


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
        form = self.form_class(request.POST, instance=request.user.profile)
        blog = BlogSettings.objects.all()[0]
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            facebook = form.cleaned_data['facebook']
            twitter = form.cleaned_data['twitter']
            form.save()
            return redirect('blogpost:index')


class AddPostView(View):
    form_class = PostForm
    template_name = 'blogpost/post_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog})

    # update profile
    def post(self, request):
        form = PostForm(request.POST)
        blog = BlogSettings.objects.all()[0]
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blogpost:index')
