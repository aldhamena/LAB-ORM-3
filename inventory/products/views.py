from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Product, Review, Category
from .forms import ProductForm
from suppliers.models import Supplier

from django.core.paginator import Paginator
from django.contrib import messages

from django.db.models import Q, F, Count, Avg, Sum, Max, Min


# add your views here.

def add_product_view(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add products", "alert-warning")
        return redirect("main:home")

    product_form = ProductForm()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    # if request.method == "POST":
    #     supplier = supplier.objects.get(id=request.POST["supplier"])
    #     new_product = Product(title=request.POST["title"], description=request.POST["description"], supplier=supplier, production_date=request.POST["production_date"], poster=request.FILES["poster"])
    #     new_product.save()
    #     return redirect("main:home")
    # else:
    #     print("not valid form", product_form.errors)

    # return render(request, "products/add.html", {"product_form":product_form, "categories":categories, "suppliers": suppliers})

    if request.method == "POST":
        
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Added Product Successfuly", "alert-success")
            return redirect('main:home_view')
        else:
            print("not valid form", product_form.errors)

    return render(request, "products/create.html", {"product_form":product_form,"RatingChoices": reversed(Product.RatingChoices.choices), "categories":categories, "suppliers": suppliers})



def product_detail_view(request:HttpRequest, product_id:int):

    product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product=product)

    avg = reviews.aggregate(Avg("rating"))
    print(avg)

    return render(request, 'products/product_detail.html', {"product" : product, "reviews":reviews, "average_rating":avg["rating__avg"]})


def product_update_view(request:HttpRequest, product_id:int):

    if not request.user.is_staff:
        messages.warning(request, "only staff can update products", "alert-warning")
        return redirect("main:home")
    

    product = Product.objects.get(pk=product_id)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        #using ProductForm for updating
        product_form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if product_form.is_valid():
            product_form.save()
        else:
            print(product_form.errors)
        ##basic update
        # product.title = request.POST["title"]
        # product.description = request.POST["description"]
        # product.production_date = request.POST["production_date"]
        # product.supplier = request.POST["supplier"]
        # product.rating = request.POST["rating"]
        # if "poster" in request.FILES: product.poster = request.FILES["poster"]
        # product.save()

        return redirect("products:product_detail_view", product_id=product.id)

    return render(request, "products/product_update.html", {"product":product, "categories" : categories, "suppliers": suppliers})


def product_delete_view(request:HttpRequest, product_id:int):

    if not request.user.is_staff:
        messages.warning(request, "only staff can delete products", "alert-warning")
        return redirect("main:home")

    # product = Product.objects.get(pk=product_id)
    # product.delete()

    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Deleted product successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete product", "alert-danger")


    return redirect("main:home")


def all_products_view(request:HttpRequest, category_name):
    #products = Product.objects.filter(rating__gte=3).order_by("-production_date")
    #products = Product.objects.filter(rating__gte=3).exclude(title__contains="Legends").order_by("-production_date")
    
    # if  Category.objects.filter(name=category_name).exists():
    #     products = Product.objects.filter(categories__name__in=[category_name]).order_by("-production_date")
    # elif category_name == "all":
    #     products = Product.objects.all().order_by("-production_date")
    # else:
    #     products = []

    
    if category_name == "all":
        products = Product.objects.all().order_by("-production_date")
    else:
        products = Product.objects.filter(categories__name__in=[category_name]).order_by("-production_date")

    # products = products.filter( Q(title_startswith="C") | Q(title_endswith="T"))

    products = products.annotate(reviews_count=Count("review"))

    # if "esrb" in request.GET:
    #     products = products.filter(esrb=request.GET["esrb"])



    page_number = request.GET.get("page", 1)
    paginator = Paginator(products, 6)
    products_page = paginator.get_page(page_number)


    return render(request, "products/all_products.html", {"products":products_page, "category_name":category_name})
    # return render(request, "products/all_products.html", {"products":products_page, "category_name":category_name, "esrb_ratings": Product.ESRBRating.choices})



def search_products_view(request:HttpRequest):

    if "search" in request.GET and len(request.GET["search"]) >= 3:
        products = Product.objects.filter(title__contains=request.GET["search"])

        if "order_by" in request.GET and request.GET["order_by"] == "rating":
            products = products.order_by("-rating")
        elif "order_by" in request.GET and request.GET["order_by"] == "production_date":
            products = products.order_by("-production_date")
    else:
        products = []


    return render(request, "products/search_products.html", {"products" : products})


def add_review_view(request:HttpRequest, product_id):

    # if request.method == "POST":
    #     product_object = Product.objects.get(pk=product_id)
    #     new_review = Review(product=product_object,name=request.POST["name"],comment=request.POST["comment"],rating=request.POST["rating"])
    #     new_review.save()

    # return redirect("products:product_detail_view", product_id=product_id)

    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add review","alert-danger")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        product_object = Product.objects.get(pk=product_id)
        new_review = Review(product=product_object,user=request.user,comment=request.POST["comment"],rating=request.POST["rating"])
        new_review.save()

        messages.success(request, "Added Review Successfully", "alert-success")

    return redirect("products:product_detail_view", product_id=product_id)