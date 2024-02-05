from django.http import JsonResponse
from django.shortcuts import render , redirect
from users.views import good_response,bad_response,get_request_body
from users.models import UserEx
from .models import BlogPost
from.serializers import BlogSerializer
# Create your views here.

def blog(request):
    return render(request , "blog.html")

def review(request):
    return render(request,"single.html")

def post_blog(request):
    return render(request,"post-blog.html")
# ========== CURD Blog ================
def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        user = UserEx.objects.get(id=request.user.id)
        blog_post = BlogPost(user=user,title=title, subject=subject, description=description, picture=picture)
        try:
            blog_post.save()
            return redirect('blog')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
# =========== get all blogs ==============
def all_blogs(request):
    try:
        blog_data = []
        blogs = BlogPost.objects.all()
        if not blogs:
            return bad_response(
                request.method, {
                    "error": "No Blogs Data available"
                }, status=404
            )
        for blog in blogs:
            blog_serializer = BlogSerializer(blog, context={"request": request}).data
            blog_data.append(blog_serializer)
        return good_response(
            request.method, {
                "blog_data": blog_data
            }, status=200
        )
    except Exception as e:
        return bad_response(
            request.method, {
                "error": f"Internal Server Error: {e}"
            }, status=500
        )
# =========== Get blog by Id =============
def get_blog(request,id):
    pass
# =========== update Blog ================
def update_blog(request,id):
    pass
def delete_blog(request,id):
    pass
# =========== delete Blog ================