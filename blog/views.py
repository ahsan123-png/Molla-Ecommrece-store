from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render , redirect
from users.views import good_response,bad_response,get_request_body
from users.models import UserEx
from .models import BlogPost, Like
from.serializers import BlogSerializer
from users.serializers import UserSerializer
# Create your views here.
def review(request):
    pass

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
def blog(request):
    try:
        blog_data = []
        # Order the queryset by publish_date
        blogs = BlogPost.objects.order_by('-publish_date')
        paginator = Paginator(blogs, 3)  # Display 3 blogs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if not blogs:
            return render(
                request, 
                "blog.html",
                {
                    "error": "No Blogs Data available"
                }
            )
        for blog in page_obj:
            blog_serializer = BlogSerializer(blog, context={"request": request}).data
            blog_data.append(blog_serializer)
        return render(
            request, 
            "blog.html",
            {
                "blog_data": blog_data,
                "page_obj": page_obj
            }
        )
    except Exception as e:
        return render(
            request, 
            "blog.html",
            {
                "error": f"Internal Server Error: {e}"
            },
            status=500  # This parameter should be removed
        )
# =========== Get blog by Id =============
def get_blog(request, id):
    if request.method == "GET":
        try:
            blog = BlogPost.objects.get(id=id)
            if blog is None:
                return bad_response(
                    request.method,{
                        "error" : f"Post with id {id} Doesn't Exist"
                    },status=404
                )
            next_post = BlogPost.objects.filter(id__gt=id).order_by('id').first()
            previous_post = BlogPost.objects.filter(id__lt=id).order_by('-id').first()

            formatted_date = blog.publish_date.strftime('%Y-%m-%d %H:%M')
            user = UserEx.objects.get(id=blog.user_id)
            userSerializer = UserSerializer(user, context={"request": request}).data 
            blogSerializer = BlogSerializer(blog, context={"request": request}).data
            blogSerializer['publish_date'] = formatted_date
            blogSerializer['like_count'] = Like.objects.filter(blog_post=blog).count()

            next_post_id = next_post.id if next_post else None
            previous_post_id = previous_post.id if previous_post else None

            return render(request, "single.html", {
                "blog_data": blogSerializer,
                "user_data": userSerializer,
                "next_post_id": next_post_id,
                "previous_post_id": previous_post_id
            }) 
        except Exception as e:
            return bad_response(
                request.method,{
                    "error" : f"Internal server error {e}"
                },status=500
            )
    else:
        return bad_response(
            request.method,
            f"Method {request.method} Not Allowed"
        )

# =========== update Blog ================
def update_blog(request,id):
    if request.method == "POST":
        try:
            blog = BlogPost.objects.get(id=id)
            if 'title' in request.POST:
                blog.title = request.POST['title']
            if 'subject' in request.POST:
                blog.subject = request.POST['subject']
            if 'description' in request.POST:
                blog.description = request.POST['description']
            blog.save()
            return redirect('blog')
        except UserEx.DoesNotExist:
            return JsonResponse({'error': f'User with id {id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': f"Method {request.method} Not Allowed"}, status=405)
# =========== delete Blog ================
def delete_blog(request,id):
    pass
# ============ Likes on Post ================
def increment_count(request, id):
    if request.method == 'POST':
        blog_post = BlogPost.objects.get(id=id)
        user = request.user
        userInstance = UserEx.objects.get(user_ptr_id=user.id)
        if not Like.objects.filter(user=userInstance, blog_post=blog_post).exists():
            Like.objects.create(user=userInstance, blog_post=blog_post)
            blog_post.like_count += 1
            blog_post.save()
    return redirect('get_blog', id=id)
# =========== detail post Pagination =====
