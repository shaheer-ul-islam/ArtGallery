from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Customer,Seller,SellerAdditional,CustomUser,Order,Cart,CartItem,Review,order_update,Contact
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required
from .forms import SellerApplicationForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Art
from django.shortcuts import render, get_object_or_404
from .models import Art,Review
from django.shortcuts import render, get_object_or_404

from collections import defaultdict

from django.utils import timezone

Product = Art.objects.all()
parms = {"Product":Product}

# Create your views here.

def index(request):

    return render(request,'index.html',parms)


def art_detail(request, art_id):
    
    art = get_object_or_404(Art, pk=art_id)

    comments = Review.objects.filter(post=art, parent=None)
    replies = Review.objects.filter(post=art).exclude(parent=None)
    print(comments)
    replies_dict = defaultdict(list)
    for reply in replies:
        replies_dict[reply.parent.sno].append(reply)

    more_products = Art.objects.filter(upload_by=art.upload_by).exclude(pk=art_id)[:5]
    context = {
        'art': art,
        'comments': comments,
        'replies': replies_dict,
        'art': art,
        'more_products': more_products,
    }
    
   
    return render(request, 'View.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        passw1 = request.POST['pass1']
        passw2 = request.POST['pass2']

        if passw1 != passw2:
           
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        
        myuser = Customer(
            name=username,
            email=email,
            phone=phone,
        )
        myuser.set_password(passw1) 
        myuser.save()
    return redirect("/")

def handle_login(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        login_email = request.POST['email']
        loginPassword = request.POST['loginPassword']

        user = authenticate(email=login_email,password=loginPassword)

        if user is not None:
            login(request,user)
            print(user.type)
            messages.success(request,f"Welcome Back {user.name}")
            return redirect("/")

        else:
            print("Invalid Credintials")
            messages.error(request,"Invalid Credintials")

    return redirect("/")

def handle_logout(request):
    logout(request)
    messages.success(request,"You are Successfully Logout....")
    return redirect("/")

@login_required
def apply_seller(request):
    user = request.user
    store_name = request.POST.get('name')
    store_logo = request.FILES.get('store_logo')
    verification_image = request.FILES.get('verification_image')

    if user:
        # Change the user type to Seller
        user.type.append(CustomUser.Types.SELLER)
        user.save()

        
        seller_additional = SellerAdditional(
            user=user,
            store_Name=store_name,
            store_Logo=store_logo,
            Verification_Image=verification_image
        )
        seller_additional.save()

    return redirect('/')

def Direct_Order(request,art_id):
    art = get_object_or_404(Art, pk=art_id)
    return render(request,'Direct_Order.html',{'art': art,})



@login_required
def add_to_cart(request, art_id):


    product = get_object_or_404(Art, pk=art_id)
    user = request.user


    if hasattr(user, 'cart'):
        cart = user.cart
    else:
  
        cart = Cart.objects.create(user=user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request,"Successfully added in Cart")    

    return redirect('/')  

@login_required
def clear_cart(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
        CartItem.objects.filter(cart=cart).delete()
        cart.delete()
        messages.success(request, "Your cart has been cleared.")
    except Cart.DoesNotExist:
        messages.info(request, "Your cart is already empty.")

    return redirect('/')

@login_required
def order(request):
    User = request.user
    Address = request.POST.get('Address')
    Zip = request.POST.get('zip-code')
    item_json = request.POST.get('itemJson')
    method = request.POST.get('method') 
    print(item_json)
    if method =='on':
        order_Method = False
    else:
        order_Method = True
    
    order = Order(
        item_json=item_json,
        User=User,
        Address = Address,
        Zip_Code = Zip,
        order_Method=order_Method
    )
    order.save()
    update = order_update(
        order_id = order.Order_id,
        order_Status = 'Your Order as been Placed ...'
    )
    update.save()
    clear_cart(request)
    messages.success(request,f"Your Order as Been Placed ... Your Order ID is  {order.Order_id}")
    return redirect("/")

    

# def post_review(request):

#     if request.method == "POST":
#         comment = request.POST.get('comment')
#         stars = int(request.POST.get('stars', 1))
#         user = request.user
#         art_id = request.POST.get('Art_id')
#         art = get_object_or_404(Art, Art_id=art_id)
#         parentSno = request.POST.get('ParentSno')

#         if parentSno == "":
#             review = Review(comment=comment, user=user, post=art, stars=stars)
#         else:
#             parent = get_object_or_404(Review, sno=parentSno)
#             review = Review(comment=comment, user=user, post=art, stars=stars, parent=parent)
        
#         review.save()
#         messages.success(request, "Your Comment has been Successfully Posted")
#         return HttpResponse(f"/{art_id}")
#     else:
        # return HttpResponse("Error 404")


def post_review(request):
    if request.method == 'POST':
        post_sno = request.POST.get('PostSno')
        comment = request.POST.get('comment')
        parent_sno = request.POST.get('ParentSno')
        stars = request.POST.get('stars')
        art = get_object_or_404(Art, pk=post_sno)
        user = request.user

        if parent_sno:
            parent = get_object_or_404(Review, pk=parent_sno)
            review = Review(comment=comment, stars=stars, post=art, user=user, parent=parent, timez=timezone.now())
        else:
            review = Review(comment=comment, stars=stars, post=art, user=user, timez=timezone.now())
        review.save()
        return redirect('art_detail', art_id=art.pk)

    return redirect('art_detail', art_id=request.POST.get('PostSno'))

# def search(request):
#     query = request.GET['query']
#     if len(query)>78:
#         posts = []
#         messages.warning(request,"Kindly Try a Small/general Keywords... ")
#     else:
#         Art_Name = Art.objects.filter(Art_Name__icontains=query)
#         Art_Price = Art.objects.filter(price__icontains=query)
#         Art_Type = Art.objects.filter(Type__icontains=query)
#         Store = SellerAdditional.objects.filter(store_Name_icontains=query)
#         posts = Art_Name.union(Art_Price,Art_Type)
#         print(posts)
#         if posts.count() == 0:
#             messages.warning(request,"No Search Result find...Try general Keyword ")
#     parms = {"Posts":posts,"Search":query}
#     return render(request,"search.html",parms)

def search(request):
    query = request.GET.get('query', '')

    if len(query) > 78:
        posts = []
        stores = []
        messages.warning(request, "Kindly try smaller or more general keywords.")
    else:
        # Perform the search on Art model
        Art_Name = Art.objects.filter(Art_Name__icontains=query)
        Art_Price = Art.objects.filter(price__icontains=query)  # Adjust if price should be a number
        Art_Type = Art.objects.filter(Type__icontains=query)

        # Combine Art results
        art_posts = Art_Name.union(Art_Price, Art_Type)

        # Perform the search on SellerAdditional model
        store_results = SellerAdditional.objects.filter(store_Name__icontains=query)

        # Check if any results found
        if not art_posts.exists() and not store_results.exists():
            messages.warning(request, "No results found. Try general keywords.")
        
        # Prepare results for template
        posts = art_posts
        stores = store_results
    
    parms = {"Posts": posts, "Stores": stores, "Search": query}
    return render(request, "search.html", parms)

# def cart(request):
#     user = request.user
#     cart_user = Cart.objects.filter(user=user)
#     if not cart_user.exists():

#         print("Empty --------")

#     else:    
        
#         cart_ites = CartItem.objects.filter(cart=cart_user)
#         print(cart_ites)

#     return render(request,"cart.html")

    # def cart(request):
    # user = request.user
    # try:
    #     cart = Cart.objects.get(user=user)
    #     cart_items = CartItem.objects.filter(cart=cart)
    # except Cart.DoesNotExist:
    #     cart_items = []

    # return render(request, "cart.html", {'cart_items': cart_items})

# def cart(request):
#     user = request.user
#     try:
#         cart = Cart.objects.get(user=user)
#         cart_items = CartItem.objects.filter(cart=cart)
#     except Cart.DoesNotExist:
#         cart_items = []

#     return render(request, "cart.html", {'cart_items': cart_items})

def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        if cart_items.exists():
            return render(request, "cart.html", {'cart_items': cart_items, 'total_price': total_price})
        else:
            return render(request, "cart_empty.html")
    except Cart.DoesNotExist:
        return render(request, "cart.html")



@login_required
def profile_page(request):
    user = request.user
    seller = get_object_or_404(SellerAdditional, user=user)
    arts = Art.objects.filter(upload_by=seller).order_by('-date_added')[:5]
    return render(request, 'Profile.html', {'seller': seller, 'arts': arts})

@login_required
def delete_art(request, art_id):
    art = get_object_or_404(Art, Art_id=art_id)
    if art.upload_by.user == request.user:
        
        art.delete()
        
        messages.success(request, 'Art deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this art.')
    return redirect('profile_page')



def add_art(request):
    if request.method == 'POST':
        art_name = request.POST.get('Art_Name')
        price = request.POST.get('price')
        art_type = request.POST.get('Type')
        image = request.FILES.get('image')

        if art_name and price and art_type and image:
         
            try:
                upload_by_instance = SellerAdditional.objects.get(user=request.user)
                art = Art(
                    Art_Name=art_name,
                    price=price,
                    Type=art_type,
                    image=image,
                    upload_by=upload_by_instance
                )
                print(upload_by_instance)
                art.save()
                return redirect('profile_page')
            except SellerAdditional.DoesNotExist:
                # Handle case where SellerAdditional instance does not exist
                return HttpResponse("Error: SellerAdditional instance not found.")
        else:
            return HttpResponse("Error: Missing required fields.")

    return render(request, 'add_art.html')


    return render(request, 'profile.html')
    
    return render(request, 'add_art.html', {'form': form})


# @login_required
# def tracker(request):
#     if request.method == 'POST':
#         orderId = request.POST.get('order','')
#         email = request.user.email

#         try:
#             order = Order.objects.filter(Order_id=orderId,Email=email)
#             if len(order) > 0:
#                 update = order_update.objects.filter(order_id = orderId)
#                 updates = []
#                 for item in update:
#                     updates.append({"text":item.order_desc,"time":item.order_time})
#                     response = json.dumps([updates,order[0].item_json],default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('')
#         except Exception as e:
#             return HttpResponse('')
#     return render(request,'tracker.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email', '')
        phone = request.POST.get('contact', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        contact = Contact(c_name=name,c_email=email,c_phone=phone,c_subject=subject,c_message=message)
        contact.save()
        messages.success(request, "We'll Solve ")
    return render(request,'contact.html')

def tracker(request):
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(User=request.user).prefetch_related('order_updates')
        context = {
            'user_orders': user_orders,
        }
        return render(request, 'tracker.html', context)
    else:
        return redirect('login')