from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
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
    author = Post.objects.filter(User, username=username)
    posts = User.objects.get(Post, author=author).count()
    paginator = Paginator(posts, POST_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post,id=post_id) # на страницу выводит один пост выбранный по pk
    posts_author = Post.objects.filter(author=post.author).count() # выведение общее количество постов пользователя
    context = {
        'post': post,
        'posts_author':posts_author,
    }
    return render(request, 'posts/post_detail.html', context)

send_mail(
    'Тема письма',
    'Текст письма.',
    'from@example.com',  # Это поле "От кого"
    ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
    fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
)

# @login_required
# def new_post(request):
#     form = PostForm(request.POST or None)
#     if not form.is_valid():
#         return render(request, 'new.html', {'form': form})
#     post = form.save(commit=False)
#     post.author = request.user
#     post.save()
#     return redirect("index")