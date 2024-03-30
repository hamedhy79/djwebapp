import django.views.generic
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote, PersonSer, Question, Answer, Car
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, PostSearchInput, CreateCarForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PersonSerialiser, QuestionSer, AnswerSer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView


class HomeList(ListView):
    template_name = 'home/shop.html'
    model = Car
    ordering = 'year'
    context_object_name = 'cars'
    allow_empty = True


class CarDetail(DetailView):
    template_name = 'home/detail_car.html'
    model = Car
    context_object_name = 'car'


# class CreateCarView(FormView):
#     template_name = 'home/create_car.html'
#     form_class = CreateCarForm
#     success_url = reverse_lazy('home:home')
#
#     def form_valid(self, form):
#         self._create_car(form.cleaned_data)
#         messages.success(self.request, 'created car', 'success')
#         return super().form_valid(form)
#
#     def _create_car(self, data):
#         Car.objects.create(name=data['name'], owner=data['owner'], year=data['year'])
class CreateCarView(CreateView):
    model = Car
    fields = ['name', 'year']
    template_name = 'home/create_car.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user.username
        car.save()
        messages.success(self.request,'success', 'success')
        return super().form_valid(form)


class DeleteCarView(DeleteView):
    model = Car
    success_url = reverse_lazy('home:home')
    template_name = 'home/delete_car.html'


class UpdateCarView(UpdateView):
    model = Car
    fields = ['name']
    success_url = reverse_lazy('home:home')
    template_name = 'home/update.html'


class Home(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        # name = request.query_params['name']
        persons = PersonSer.objects.all()
        ser_data = PersonSerialiser(instance=persons, many=True)  # many for several arguments
        return Response(data=ser_data.data)

    # def post(self, request):
    #     name = request.data['name']
    #     return Response({'name': name})


class QuestionListView(APIView):
    def get(self, request):
        question = Question.objects.all()
        ser_data = QuestionSer(instance=question, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    def post(self, request):
        ser_data = QuestionSer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        ser_data = QuestionSer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'question deleted'}, status=status.HTTP_200_OK)


class HomeView(ListView):
    form_class = PostSearchInput

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': self.form_class})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.post_comments.filter(is_reply=False)
        return render(request, 'home/detail.html',
                      {'post': self.post_instance, 'comments': comments, 'form': self.form_class,
                       'reply_form': self.form_class_reply})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment is ok', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Delete Success', 'success')
        else:
            messages.error(request, "You can't delete post", 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you can't edit this post", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:10])
            new_post.save()
            messages.success(request, 'post updated')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:10])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post created')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply is sent', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostLikeView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you liked this post before')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'like ok')
        return redirect('home:post_detail', post.id, post.slug)
