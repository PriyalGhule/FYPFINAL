from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Person
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate, login, logout


def signup(request):
    if request.method=="POST":
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        role=request.POST.get("role")
        print(email, phone, password, role)
        obj=Person()  #This code creates an instance of the Person model (assuming it exists) and assigns values to its attributes.
        obj.email=email
        obj.role=role
        obj.password=password
        obj.phone=phone
        if Person.objects.filter(email=email).exists():
            messages.info(request, 'Account already exists')
            return redirect('signup')
        else:
            has_upper = any(char.isupper() for char in password)
            has_lower = any(char.islower() for char in password)
            has_digit = any(char.isdigit() for char in password)
            has_special_char = any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/? " for char in password)
            if(len(password)<8):
                messages.info(request,"Password must be atleast 8 characters")
                return redirect("signup")
            if(has_upper==False):
                messages.info(request,"Password must contain atleast one uppercase letter")
                return redirect("signup")
            if(has_lower==False):
                messages.info(request,"Password must contain atleast one lowercase letter")
                return redirect("signup")
            if(has_digit==False):
                messages.info(request,"Password must contain atleast one digit")
                return redirect("signup")
            if(has_special_char==False):
                messages.info(request,"Password must contain atleast one special character")
                return redirect("signup") 
            if(len(phone)!=10):
                messages.info(request,"Phone number should be of 10 digits")
                return redirect("signup")               
            obj.save()
            detail=Person.objects.all()   #partoapp_Person table entry
            #return redirect(request,"registration/login.html")
            user=User.objects.create_user(email=email, password=password,username=email)#auth_user table  entry
            #user_id = request.session.get('user_id')
            return redirect("signup")
            for i in detail:
                print(email)
    return render(request,"signup.html")


def loginView(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=authenticate(request,username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("signup") 
        else:
            messages.info(request, "Incorrect credentials")
            return redirect("login")
    return render(request,"login.html")

# def home(request):
#     return render(request,"home.html")

def landing(request):
    return render(request,"landing.html")

def about(request):
    return render(request,"about.html")

def editor(request):
    return render(request,"editor.html")

def explore(request):
    return render(request,"explore.html")



# views.py
import os
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from stable_diffusion.demo import main

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model = request.POST.get('model', "bes-dev/stable-diffusion-v1-4-openvino")
        device = request.POST.get('device', "CPU")
        seed = request.POST.get('seed')
        beta_start = float(request.POST.get('beta_start', 0.00085))
        beta_end = float(request.POST.get('beta_end', 0.012))
        beta_schedule = request.POST.get('beta_schedule', "scaled_linear")
        num_inference_steps = int(request.POST.get('num_inference_steps', 32))
        guidance_scale = float(request.POST.get('guidance_scale', 7.5))
        eta = float(request.POST.get('eta', 0.0))
        tokenizer = request.POST.get('tokenizer', "openai/clip-vit-large-patch14")
        init_image = request.POST.get('init_image')
        strength = float(request.POST.get('strength', 0.5))
        mask = request.POST.get('mask')
        output = request.POST.get('output', "output.png")
        
        try:
            main(prompt=prompt, model=model, device=device, seed=seed, beta_start=beta_start, beta_end=beta_end, beta_schedule=beta_schedule, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale, eta=eta, tokenizer=tokenizer, init_image=init_image, strength=strength, mask=mask, output=output)
            
            # Check if the output image file exists
            if os.path.exists(output):
                # Return the generated image file as a response
                return FileResponse(open(output, 'rb'), content_type='image/png')
            else:
                return JsonResponse({'error': 'Failed to generate image'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'generate_image.html')
