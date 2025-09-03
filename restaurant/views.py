from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu, Booking
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from .serializers import BookingSerializer, MenuSerializer, UserSerializer, AuthTokenSerializer, User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics

# User Registration and Authentication Views
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class AuthTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

# ViewSets for Menu and Booking
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

# Function-based Views
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {"menu": {"menu": menu_data}})

def display_menu_item(request, pk=None):
    menu_item = Menu.objects.get(pk=pk) if pk else None
    return render(request, 'menu_item.html', {"menu_item": menu_item})

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()
        if not exist:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
            return HttpResponse(status=201)  # Created
        else:
            return HttpResponse("{'error': 1}", content_type='application/json')

    # SIMPLER FIX: Check if date parameter is empty
    date_param = request.GET.get('date', '')
    
    if date_param:
        # Use the provided date
        bookings = Booking.objects.filter(reservation_date=date_param)
    else:
        # Use today's date if no date provided
        bookings = Booking.objects.filter(reservation_date=datetime.today().date())
    
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')