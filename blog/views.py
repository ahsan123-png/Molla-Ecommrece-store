from django.http import JsonResponse
from django.shortcuts import render

from users.models import UserEx
from .models import BlogPost
# Create your views here.

def blog(request):
    return render(request , "blog.html")

def review(request):
    return render(request,"single.html")

def post_blog(request):
    return render(request,"post-blog.html")

def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        user = UserEx.objects.get(id=request.user.id)
        blog_post = BlogPost(user=user, title=title, subject=subject, description=description, picture=picture)
        try:
            blog_post.save()
            return JsonResponse({'success': 'Blog post created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)