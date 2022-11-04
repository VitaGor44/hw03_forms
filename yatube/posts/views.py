from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User
from django.core.mail import send_mail


POST_PAGES = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POST_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page_obj': page_obj,})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related()
    paginator = Paginator(post_list, POST_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count = post_list.count()
    paginator = Paginator(post_list, POST_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count': count,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post,id=post_id) # на страницу выводит один пост выбранный по pk
    count = Post.objects.filter(author=post.author).count() # выведение общее количество постов пользователя
    context = {
        'post': post,
        'count':count,
    }
    return render(request, 'posts/post_detail.html', context)

send_mail(
    'Тема письма',
    'Текст письма.',
    'from@example.com',  # Это поле "От кого"
    ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
    fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(form)
        if form.is_valid:
            author = User.objects.get(pk=request.user.id)
            post = Post(text=form.cleaned_data['text'],
                        author=author)
            post.save()
            return redirect('posts:post_detail', post_id=post.id)
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form,})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        if request.user is not post.author:
            return redirect('posts:post_detail', post.id)
    form = PostForm(request.POST or None, instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post.id)

    return render(request, 'posts/create_post.html', {'form': form, 'is_edit': True, 'post': post})
