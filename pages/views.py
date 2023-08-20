from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View 
from django.urls import reverse
from django import forms 
from django.core.exceptions import ValidationError
from .models import Product

# Create your views here.
# def homePageView(request): 
#     return HttpResponse("Hello World!") 

class ProductForm(forms.ModelForm): 
    # name = forms.CharField(required=True) 
    # price = forms.FloatField(required=True) 
    class Meta:
        model = Product
        fields = ['name', 'price']

def clean_price(self): 
    price = self.cleaned_data.get('price') 
    if price is not None and price <= 0: 
        raise ValidationError('Price must be greater than zero.') 
    return price 
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save()
            # return redirect("form")  
            return render(request,"./products/p_created.html")
            #return redirect('p_created')
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)


# class Product: 
#     products = [ 
#         {"id":"1", "name":"TV", "description":"Best TV", "price":600}, 
#         {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":1000}, 
#         {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":95}, 
#         {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":700} 
#     ] 


 
class ProductIndexView(View): 
    template_name = './products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all() 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = './products/show.html' 
 
 
    def get(self, request, id): 
        viewData = {} 
        # product = Product.products[int(id)-1]
        try:
            #product = Product.products[int(id)-1]             
            product = get_object_or_404(Product, pk=int(id))
        except:
            return HttpResponseRedirect(reverse('home'))
        
        product = get_object_or_404(Product, pk=int(id))
        viewData["title"] = product.name + " - Online Store" 
        viewData["subtitle"] =  product.name + " - Product information" 
        viewData["product"] = product 
 
        return render(request, self.template_name, viewData)
    
class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context 

class HomePageView(TemplateView): 
    template_name = "./pages/home.html"

class AboutPageView(TemplateView): 
    template_name = './pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
 
        return context 

class ContactPageView(TemplateView):
    template_name = './pages/contact.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "Contact us - Online Store", 
            "subtitle": "Contact us", 
            "email": "Email: email@company.com", 
            "address": "Address: calle 1 # 2 - 3",
            "number": "Telephone number: +57 3213213213", 
        }) 
 
        return context
    
