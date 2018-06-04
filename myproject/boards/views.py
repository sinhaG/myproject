from django.http import HttpResponse
from django.shortcuts import redirect,render,get_object_or_404
from .models import Board,Topics,Post
from django.http import Http404
from .forms import NewTopicForm

from django.contrib.auth.models import User

def home(request):
    boards = Board.objects.all()
    

    return render(request,'index.html',{'boards':boards})

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})