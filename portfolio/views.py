from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Project, Category, ProjectImage


def home(request):

    profile = Profile.objects.first()
    categories = Category.objects.all()

    search_query = request.GET.get('search')

    if search_query:
        projects = Project.objects.filter(
            title__icontains=search_query
        ).order_by('-created_at')
    else:
        projects = Project.objects.all().order_by('-created_at')

    context = {
        'profile': profile,
        'projects': projects,
        'categories': categories
    }

    return render(request, 'home.html', context)


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):

    logout(request)
    return redirect('home')


@login_required
def dashboard(request):

    projects = Project.objects.all().order_by('-created_at')

    context = {
        'projects': projects
    }

    return render(request, 'dashboard.html', context)


@login_required
def add_project(request):

    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        year = request.POST.get('year')
        category_id = request.POST.get('category')

        category = get_object_or_404(Category, id=category_id)

        cover = request.FILES.get('cover_image')

        project = Project.objects.create(
            title=title,
            description=description,
            location=location,
            year=year,
            category=category,
            cover_image=cover
        )

        images = request.FILES.getlist('gallery')

        for img in images:
            ProjectImage.objects.create(
                project=project,
                image=img
            )

        messages.success(request, "Project added successfully")

        return redirect('dashboard')

    return render(request, 'add_project.html', {
        'categories': categories
    })


@login_required
def edit_project(request, id):

    project = get_object_or_404(Project, id=id)
    categories = Category.objects.all()

    if request.method == "POST":

        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.location = request.POST.get('location')
        project.year = request.POST.get('year')

        category_id = request.POST.get('category')
        project.category = get_object_or_404(Category, id=category_id)

        if request.FILES.get('cover_image'):
            project.cover_image = request.FILES.get('cover_image')

        project.save()

        images = request.FILES.getlist('gallery')

        for img in images:
            ProjectImage.objects.create(
                project=project,
                image=img
            )

        messages.success(request, "Project updated successfully")

        return redirect('dashboard')

    return render(request, 'edit_project.html', {
        'project': project,
        'categories': categories
    })


@login_required
def delete_project(request, id):

    project = get_object_or_404(Project, id=id)
    project.delete()

    messages.success(request, "Project deleted")

    return redirect('dashboard')


@login_required
def edit_profile(request):

    profile = Profile.objects.first()

    if not profile:
        profile = Profile.objects.create(
            name="Architect",
            bio="Write your bio here"
        )

    if request.method == "POST":

        profile.name = request.POST.get('name')
        profile.bio = request.POST.get('bio')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')

        profile.save()

        messages.success(request, "Profile updated successfully")

        return redirect('dashboard')

    return render(request, 'edit_profile.html', {
        'profile': profile
    })