from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password

# View for rendering the dashboard
def dashboard(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Your dashboard logic here
    total_customer = CustomUser.objects.filter(role='User').count()
    total_policy = Policy.objects.all().count()
    total_category = Category.objects.all().count()
    total_question = CustomerQuestion.objects.all().count()
    total_applied = PolicyHolder.objects.distinct().count()
    approved_policy = PolicyHolderPolicy.objects.filter(approval_status='Approved').count()
    reject_policy = PolicyHolderPolicy.objects.filter(approval_status='Rejected').count()
    pending_policy = PolicyHolderPolicy.objects.filter(approval_status='Pending').count()
    contex = {
        'total_customer':total_customer,
        'total_policy':total_policy,
        'total_category':total_category,
        'total_question':total_question,
        'total_applied':total_applied,
        'approved_policy':approved_policy,
        'reject_policy':reject_policy,
        'pending_policy':pending_policy
    }
    return render(request, 'dashboard.html',contex)

# View for handling user registration
def register(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if email, username, or mobile already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if CustomUser.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number is already taken.")
            return redirect('register')

        # Save user if all validations pass
        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=make_password(password),  # Hash the password
            role=role
        )
        user.save()

        messages.success(request, "Registration successful. Please log in.")
        if role =='Admin':      
            return redirect('login')
        else:
            return redirect('create_policy_holder')

    return render(request, 'register.html')

# View for handling user login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                # Login user by setting the session
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, 'login.html')

# View for handling user logout
def logout(request):
    # Remove user session data
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')


def create_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if question_text:
            CustomerQuestion.objects.create(
            	user = CustomUser.objects.get(id=request.session['user_id']),
                question_text=question_text,
                status='pending'  # Set default status
            )
            return redirect('manage_questions')
        else:
            messages.error(request, "Question text cannot be empty.")
    
    return render(request, 'create_question.html')

def update_question_status(request, question_id, status):
    question = get_object_or_404(CustomerQuestion, id=question_id)
    if status in ['pending', 'answered']:
        question.status = status
        question.save()
        messages.success(request, "Question status updated successfully.")
    else:
        messages.error(request, "Invalid status value.")
    return redirect('manage_questions')

def delete_question(request, question_id):
    question = get_object_or_404(CustomerQuestion, id=question_id)
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect('manage_questions')
    
def manage_questions(request):
    if 'user_id' not in request.session:
        return redirect('login')
    questions = CustomerQuestion.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'manage_questions.html', context)

def category(request):
    if 'user_id' not in request.session:
        return redirect('login')
    cat = Category.objects.all()
    return render(request,'category.html',{'categories':cat}) 

def create_category(request):
    if request.method == 'POST':
        category = request.POST['category']

        Category.objects.create(name=category)
        cat = Category.objects.all()
        return render(request,'category.html',{'categories':cat})   
    else:
        return render(request,'create_category.html')   

def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category')

def policy(request):
    if 'user_id' not in request.session:
        return redirect('login')
    policy = Policy.objects.all()
    return render(request,'policy.html',{'policy':policy})

def create_policy(request):
    categories = Category.objects.all()
    if request.method == 'POST': 
        category = Category.objects.get(id=request.POST['category'])  # Get the Category instance
        Policy.objects.create(
            policy_name=request.POST['policy_name'],
            category=category,  # Pass the Category instance here
            description=request.POST['description'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            premium_amount=request.POST['premium_amount']
        )           
        return redirect('policy')  # Redirect after successful creation
    else:
        return render(request, 'create_policy.html', {'categories': categories})  

def delete_policy(request,id):
    policy = Policy.objects.get(id=id)
    policy.delete()
    return redirect('policy')        


def policy_holder_policy_list(request):
    if 'user_id' not in request.session:
        return redirect('login')
    policies = PolicyHolderPolicy.objects.filter(approval_status='Pending')
    return render(request, 'policy_holder_policy_list.html', {'policies': policies})


def approve_policy(request, policy_id):
    policy_holder_policy = get_object_or_404(PolicyHolderPolicy, id=policy_id)
    policy_holder_policy.approval_status = 'Approved'
    policy_holder_policy.save()
    return redirect('policy_holder_policy_list')  # Redirect to a list page after approving

def reject_policy(request, policy_id):
    policy_holder_policy = get_object_or_404(PolicyHolderPolicy, id=policy_id)
    policy_holder_policy.approval_status = 'Rejected'
    policy_holder_policy.save()
    return redirect('policy_holder_policy_list')  # Redirect to a list page after rejecting

def create_policy_holder(request):
    users = CustomUser.objects.filter(role='User')  # Fetch all users
    policies = Policy.objects.all()   # Fetch all policies

    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.POST['user'])  # Get the selected user
        policy_holder, created = PolicyHolder.objects.get_or_create(user=user)  # Create or get PolicyHolder
        
        selected_policies = request.POST.getlist('policies')  # Get selected policies as a list of ids
        
        for policy_id in selected_policies:
            policy = Policy.objects.get(id=policy_id)
            PolicyHolderPolicy.objects.create(policy_holder=policy_holder, policy=policy, payment_status='Due')  # Create through model
        
        return redirect('policy_holder_policy_list')  # Redirect after successful creation
    else:
        return render(request, 'create_policy_holder.html', {'users': users, 'policies': policies})