from django.shortcuts import render
from django.views import View

class Cart(View):
	def get(self, request):
		# Example: render a cart page
		return render(request, 'cart.html')