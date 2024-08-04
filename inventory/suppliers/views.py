from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from products.models import Product

from .models import Supplier
from .forms import SupplierForm


# Create your views here.
# def add_supplier(request:HttpRequest):

#     if request.method == "POST":
#         #addin a new product in database
#         supplier_form = SupplierForm(request.POST, request.FILES)
#         if supplier_form.is_valid():
#             supplier_form.save()
#         else:
#             print(supplier_form.errors)

#         return redirect("suppliers:suppliers_page")

#     return render(request, "suppliers/add_supplier.html")
def add_supplier(request: HttpRequest):
    if request.method == "POST":
        new_product = Supplier(name=request.POST['name'],  #send to data base
                                description=request.POST['description'],
                                logo= request.FILES['logo'])
        new_product.save()#save to database
        return redirect("suppliers:suppliers_page1")
    
    return render(request,"suppliers/add_supplier.html")


def suppliers_page1(request:HttpRequest):
# Abdullah The beat teacher

    suppliers = Supplier.objects.all()[:8]

    return render(request, "suppliers/suppliers.html", {"suppliers" : suppliers})


def supplier_page(request:HttpRequest, supplier_id):

    supplier = supplier.objects.get(id=supplier_id)
    #product_by_supplier = Product.objects.filter(supplier=supplier)

    #product = supplier.product_set.all()
    #print(product_by_supplier)
    #print(product)



    return render(request, "suppliers/supplier_page.html", {"supplier" : supplier})
