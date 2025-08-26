from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets
from core.models import Game, Post
from core.forms import PostForm
from core.serializers import GameSerializer, PostSerializer

def game_menu_view(request):
    games = Game.objects.all()
    return render(request, 'game_menu.html', {'games': games})

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    form = PostForm(request.POST or None)

    if request.method == 'POST':
        if 'rating' in request.POST and not request.POST.get('content'):
            try:
                rating_value = int(request.POST.get('rating'))
                if 1 <= rating_value <= 10:
                    Post.objects.create(
                        game=game,
                        rating=rating_value,
                        author='Оценка',
                        content=''
                    )
                    return redirect('game_detail', game_id=game.id)
            except ValueError:
                pass

        elif 'content' in request.POST:
            if form.is_valid():
                post = form.save(commit=False)
                post.game = game
                post.save()
                return redirect('game_detail', game_id=game.id)

    average_rating = (
        Post.objects
        .filter(game=game, rating__isnull=False)
        .aggregate(Avg('rating'))['rating__avg']
    )
    metacritic_score = int(average_rating * 10) if average_rating is not None else None


    template_name = 'game_detail_fable.html' if game.title == "Fable" else 'game_detail.html'

    return render(request, template_name, {
        'game': game,
        'form': form,
        'posts': Post.objects.filter(game=game),
        'metacritic_score': metacritic_score,
    })

def fable_detail(request):
    game = get_object_or_404(Game, title="Fable")
    posts = Post.objects.filter(game=game).order_by('-created_at')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.game = game
            post.save()
    else:
        form = PostForm()

    context = {
        'game': game,
        'posts': posts,
        'form': form,
        'metacritic_score': game.metacritic_score,
    }
    return render(request, 'game_detail_fable.html', context)
