from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView , DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article ,Comment

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(DetailView):
    model=Article
    template_name ='article_detail.html'

class ArticleUpdateView(UserPassesTestMixin ,LoginRequiredMixin,UpdateView):
    model= Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name ='article_edit.html'

    def test_func(self):
        obj =self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView( UserPassesTestMixin, LoginRequiredMixin,DeleteView):
    model =Article
    template_name ='article_delete.html'
    success_url =reverse_lazy('article_list')

    def test_func(self):
        obj =self.get_object()
        return obj.author == self.request.user

class ArticleCreateView( UserPassesTestMixin,  LoginRequiredMixin, CreateView):
    model = Article
    template_name ='article_new.html'
    fields =('title', 'summary', 'body', 'photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(article=article, author=request.user, comment=comment)
    return redirect('articles:article_detail', pk=pk)