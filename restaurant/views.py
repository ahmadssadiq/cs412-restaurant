from django.shortcuts import render
import random
from datetime import datetime, timedelta

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_specials = ['Pasta Primavera', 'Grilled Salmon', 'Vegetarian Stir-Fry', 'Chef\'s Special Pizza']
    context = {
        'daily_special': random.choice(daily_specials)
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        order_items = []
        total_price = 0
        menu_items = {
            'pizza': 10,
            'burger': 8,
            'salad': 6,
            'daily_special': 12
        }
        
        for item, price in menu_items.items():
            if request.POST.get(item):
                order_items.append(item.capitalize())
                total_price += price
        
        special_instructions = request.POST.get('special_instructions', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        
        context = {
            'order_items': order_items,
            'total_price': total_price,
            'special_instructions': special_instructions,
            'name': name,
            'phone': phone,
            'email': email,
            'ready_time': ready_time.strftime("%I:%M %p")
        }
        return render(request, 'restaurant/confirmation.html', context)
    return render(request, 'restaurant/order.html')