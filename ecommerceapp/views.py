from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import Category
from ecommerceapp.models import Product,Customer,Cart
import os

# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'signin.html')

def signinurl(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = auth.authenticate(username=username, password=password)
        
        if admin is not None:
            if admin.is_staff:
                login(request,admin)
                return redirect('admin_home')
            else:
                login(request,admin)
            # request.session['uid'] = user.id
                auth.login(request, admin)
                messages.info(request, f'welcome {username}')
                return redirect('user_home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signin')
    else:
        return redirect('signin')
    
def signupurl(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        address=request.POST['address']
        contact=request.POST['contact']
        email=request.POST['email']
        image = request.FILES.get('image')
        password=request.POST['password']
        cfmpassword=request.POST['cfmpassword']


        if password==cfmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,password=password,email=email)
                user.save()
                cust=Customer(address=address,contact_number=contact,image=image,user=user)
                cust.save()
        else:
            messages.info(request, "Password doesn't match")
            return redirect('signup')   
        return redirect('signin')
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def show_user(request):
    cust=Customer.objects.all()
    return render(request,'show_user.html',{'customer':cust})
    
@login_required(login_url='signin')
def admin_home(request):
    return render(request,'admin_home.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('home')

def category(request):
    return render(request,'category.html')

def product(request):
    category=Category.objects.all()
    return render(request,'product.html',{'category':category})

def categoryurl(request):
    if request.method == 'POST':
        category_name=request.POST['category']
        category=Category(category_name=category_name)
        category.save()
        return redirect('category')
    return render(request,'category.html')

@login_required(login_url='signin')
def producturl(request):
    if request.method == 'POST':
        product_name=request.POST['name']
        product_description=request.POST['description']
        price=request.POST['price']
        select=request.POST['select']
        category=Category.objects.get(id=select)
        image = request.FILES.get('file')
        product=Product(product_name=product_name,product_description=product_description,price=price,category=category,image=image)
        product.save()
        return redirect('product')
    return render(request,'product.html')

@login_required(login_url='signin')
def show_product(request):
    product=Product.objects.all()
    return render(request,'show_product.html',{'product':product})

@login_required(login_url='signin')
def deleteproduct(request,pk):
    prod=Product.objects.get(id=pk)
    prod.delete()
    return redirect('show_product')

@login_required(login_url='signin')
def deleteuser(request,pk):
    c1=Customer.objects.get(user=pk)
    c1.delete()
    c2=User.objects.get(id=pk)
    c2.delete()
    return redirect('show_user')

@login_required(login_url='signin')
def user_home(request):
    prod=Category.objects.all()
    return render(request,'user_home.html',{'prodct':prod})

@login_required(login_url='signin') 
def categorized_products(request, pk):
    categories = Category.objects.filter(id=pk)
    
    if categories.exists():
        category = categories.first()
        products = Product.objects.filter(category=category)
        prod=Category.objects.all()
        return render(request, 'categories.html', {'categories': [category], 'products': products,'prodct':prod})
    else:
        
        return render(request, 'user_home.html')
    
@login_required(login_url='login') 
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.total_price() for item in cart_items)
    prod=Category.objects.all()
    return render(request, 'cart.html', {'cartitems':cart_items,'totalprice': total_price,'prodct':prod})

@login_required(login_url='login') 
def cart_details(request, pk):
    product = Product.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login') 
def removecart(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        cart_item.delete()
    
    return redirect('cart')



