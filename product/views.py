import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from product.models import Inventory, Product, ProductPicture
from users.views import bad_response,good_response,get_request_body
from .serializers import ProductPictureSerializer, ProductSerializer
# Create your views here.
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
        product_pictures = request.FILES.getlist('pictures')  # Get list of uploaded images
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
            productType=product_type,
        )
        product.save()
        
        # Create ProductPicture instances for each uploaded image
        for picture in product_pictures:
            product_picture = ProductPicture(product=product, picture=picture)
            product_picture.save()
        # Update or create inventory entry
        inventory, created = Inventory.objects.get_or_create(
            product=product,
            defaults={'stock_quantity': stock}
        )
        if not created:
            inventory.stock_quantity = stock
            inventory.save()

        return redirect('add')
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# =========== get all blogs ==============
def products(request):
    try:
        product_data = []
        products = Product.objects.all()
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if not products:
            return render(
                request, 
                "list-products.html",
                {
                    "error": "No products available"
                }
            )
        for product in page_obj:
            product_serializer = ProductSerializer(product, context={"request": request}).data
            product_pictures = ProductPicture.objects.filter(product=product)
            product_serializer['product_pictures'] = product_pictures
            product_data.append(product_serializer)
        return render(
            request, 
            "list-products.html",
            {
                "product_data": product_data,
                "page_obj": page_obj
            }
        )
    except Exception as e:
        return render(
            request, 
            "list-products.html",
            {
                "error": f"Internal Server Error: {e}"
            },
            status=500
        )
# # =========== Get blog by Id =============
def getProduct(request, id):
    if request.method == "GET":
        try:
            product = get_object_or_404(Product, id=id)
            product_serializer = ProductSerializer(product, context={"request": request}).data
            product_images = ProductPicture.objects.filter(product_id=id)
            product_images_serializer = ProductPictureSerializer(product_images, many=True).data
            return render(request, "product-detail.html", {
                "product_data": product_serializer,
                "product_images": product_images_serializer
            })
        except Exception as e:
            return render(request, "error.html", {
                "error": f"Internal server error: {e}"
            }, status=500)
    else:
        return render(request, "404.html", {
            "error": f"Method {request.method} not allowed"
        }, status=405)
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
                serialized_data = serializer.data
                return JsonResponse({'success': f'Product with id {id} updated successfully',
                                     "product" : serialized_data}, status=200)
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

