from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Category, BlogSettings, Profile, Comment
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView, CreateView, DeleteView, UpdateView
from .forms import UserForm, ProfileForm, PostForm, CommentForm, ProfileAdminForm
from django.template.defaultfilters import slugify


class PostsView(generic.ListView):
    template_name = 'blogpost/index.html'

    queryset = Post.objects.all().order_by('-posted')

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context


class PostDetailView(View):
    template_name = 'blogpost/post.html'
    form_class = CommentForm

    def get(self, request, slug):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)
        return render(request, self.template_name, {'blog': blog, 'post': post, 'form': form, 'comments': comments})

    def post(self, request, slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            blog_post = Post.objects.filter(slug=slug)[0]
            comment.post = blog_post
            comment.user = request.user
            comment.save()
            return redirect('blogpost:post', slug)


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
        return redirect('blogpost:index')


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('blogpost:index')


class ProfileView(View):
    model = Profile
    template_name = 'blogpost/profile.html'

    def get(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        blog = BlogSettings.objects.all()[0]
        posts = Post.objects.filter(author=profile.user.pk)
        return render(request, self.template_name, {'blog': blog, 'profile': profile, 'posts': posts})


class ProfileUpdate(View):

    form_class = ProfileForm
    template_name = 'blogpost/profile_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        profile = Profile.objects.get(user=request.user)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog, 'initial': profile})

    # update profile
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        slug = slugify(request.user.username)
        if form.is_valid():
            form.save()
            return redirect('blogpost:profile', slug)


class AddPostView(View):
    form_class = PostForm
    template_name = 'blogpost/post_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog})

    # update post
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            print('Debug: ' + request.POST['title'])
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            slug = post.slug
            return redirect('blogpost:post', slug)
        else:
            print(form.errors.as_data())
            print('Debug: ' + request.POST['category'])
            form = PostForm()
            print('DEBUG ' + str(form.is_valid()))
            return render(request, self.template_name, {'form': form})


class UpdatePost(UpdateView):
    model = Post
    template_name = 'blogpost/post_update.html'
    fields = ['title', 'category', 'image', 'body_preview', 'body']

    def get_context_data(self, **kwargs):
        context = super(UpdatePost, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        pst_data = Post.objects.get(title=context['post'])
        context['initial'] = pst_data
        context['categories'] = Category.objects.all()
        return context


class CommentDelete(View):

    def post(self, request, slug, pk):
        cmnt = Comment.objects.get(pk=pk)
        cmnt.delete()
        print('debug' + request.path)
        return redirect('blogpost:post', slug)


class PostDelete(View):

    def post(self, request, slug):
        pst = Post.objects.get(slug=slug)
        pst.delete()
        return redirect('blogpost:admin_view')


class AdminView(View):
    template_name = 'blogpost/admin.html'

    def get(self, request):
        blog = BlogSettings.objects.all()[0]
        posts = Post.objects.all()
        profiles = Profile.objects.all()
        comments = Comment.objects.all()
        return render(request, self.template_name, {'blog': blog, 'posts': posts, 'comments': comments,
                                                    'profiles': profiles})


class AdminEditGroup(View):
    form_class = ProfileAdminForm
    template_name = 'blogpost/admin_profile_form.html'

    # display blank form
    def get(self, request, user):
        form = self.form_class(None)
        blog = BlogSettings.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'blog': blog})

    # update profile
    def post(self, request, user):
        usr = Profile.objects.get(username=user)
        form = self.form_class(request.POST, instance=usr)
        if form.is_valid():
            form.save()
            return redirect('blogpost:admin_view')
