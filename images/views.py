from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            print(new_image)
            new_image.user = request.user
            new_image.save()
            messages.success(request,
                             'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'images/image/create.html',
                  {'section': 'imgaes',
                   'form': form})


def image_detail(request, image_id: int, slug: str):
    image = get_object_or_404(Image, id=image_id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
        return JsonResponse({'status': 'error'})
