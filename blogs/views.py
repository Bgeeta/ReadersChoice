from django.views import generic
from .models import Post, Images
from django.forms import modelformset_factory
from django.contrib import messages
from .forms import CommentForm, PostForm, ImageForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


class PostList(generic.ListView):
    """
    Return all posts that are with status 1 (published) and order from the latest one.
    """
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'index.html'


def post_detail(request, slug):
    template_name = 'post_details.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    images = Images.objects.filter(post=post)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            # if request.user.is_authenticated:
            new_comment.created_by = request.user

            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'images': images,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

@login_required
def post_create(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    if request.method == 'POST':
        creation_from = PostForm(data=request.POST)
        files = request.FILES.getlist('images')
        #formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if creation_from.is_valid():
            new_form = creation_from.save(commit=False)
            new_form.author = request.user
            if 'Publish' in request.POST:
                new_form.status = 1
            elif 'Draft' in request.POST:
                new_form.status = 0
            new_form.save()
            print("--",files,"--")
            for f in files:
                Images.objects.create(post = new_form, image=f)
            '''for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(post=new_form, image=image)
                    photo.save()
                else:
                    print("Upload faild\n\n\n\n")
                    '''
            messages.success(request, f"Post created successfully")
            return redirect('home')
    else:
        creation_from = PostForm()
        #formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'post_create.html', {'postForm' : creation_from})


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_details.html'