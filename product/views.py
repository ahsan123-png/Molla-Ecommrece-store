import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from product.models import Product
from users.views import bad_response,good_response,get_request_body
from .serializers import ProductSerializer
# Create your views here.


def products(request):
    return render(request,"list-products.html")

def product_details(request):
    return render(request,"product-detail.html")
@csrf_exempt
def add(request):
    return render(request,"add_product.html")

# ========== CURD Blog ================
@csrf_exempt
def addProduct(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        color = request.POST.get('color')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_type = request.POST.get('product_type')
        productPicture = request.FILES.get('picture')
        product = Product(
            product_name=product_name,
            description=description,
            brand=brand,
            price=price,
            color=color,
            size=size,
            stock=stock,
            category=category,
            subcategory=subcategory,
            productType=product_type,  # Add product type here
            productPicture=productPicture,
        )
        try:
            product.save()
            return redirect('blog')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



# =========== get all blogs ==============
def allProduct(request):
    try:
        blog_data = []
        blogs = Product.objects.all()
        if not blogs:
            return bad_response(
                request.method, {
                    "error": "No Blogs Data available"
                }, status=404
            )
        for blog in blogs:
            blog_serializer = ProductSerializer(blog, context={"request": request}).data
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
# # =========== Get blog by Id =============
def getProduct(request,id):
    if request.method == "GET":
        try:
            product=Product.objects.get(id = id)
            if product is None:
                return bad_response(
                    request.method,{
                        "error" : f"User with id {id} Doesn't Exits"
                    },status=404
                )
            user_serializer=ProductSerializer(product,context={"request" : request}).data
            return good_response(
                request.method,{
                    "success" : user_serializer
                },status=200
            )
        except Exception as e:
            return bad_response(
                request.method,{
                    "error" : f"Internal server error : {e}"
                },status=500
            )
    else:
        return bad_response(
            request.method,
            f"Method {request.method} Not Allowed"
        )
# # =========== update Blog ================
@csrf_exempt
def updateProduct(request, id):
    if request.method == "PUT":
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': f'Product with id {id} updated successfully'}, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': f'Method {request.method} Not Allowed'}, status=405)
# =========== delete Blog ================
def deleteProduct(request,id):
    pass