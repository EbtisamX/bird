from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Bird,Accessory
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



def home(request):
    return render(request, 'home.html')


#Add accessory to a bird
@login_required
def assoc_accessory(request, bird_id, accessory_id):
    Bird.objects.get(id=bird_id).accessories.add(accessory_id)
    return redirect('bird_detail', bird_id=bird_id)

#Remove accessory from a bird
@login_required
def dessoc_accessory(request, bird_id, accessory_id):
    Bird.objects.get(id=bird_id).accessories.remove(accessory_id)
    return redirect('bird_detail', bird_id=bird_id)   

#Show details for one bird + the form to add appointment + unadded accessories
@login_required
def bird_detail_view(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    appointment_form = AppointmentForm()
    accessories_bird_does_not_have = Accessory.objects.exclude(id__in=bird.accessories.all().values_list('id'))
    return render(request, 'bird_detail.html', {
        'bird': bird,
        'appointment_form': appointment_form,
        'accessories_bird_does_not_have': accessories_bird_does_not_have
    })

#Save new appointment for a bird
def add_appointment(request, bird_id):
    form = AppointmentForm(request.POST)
    if form.is_valid():
        new_appointment = form.save(commit=False)
        new_appointment.bird_id = bird_id
        new_appointment.save()
    return redirect('bird_detail', bird_id=bird_id)

#All CRUD functions for the Bird
class BirdListView(LoginRequiredMixin, ListView):
    model = Bird
    template_name = 'bird_list.html'  
    context_object_name = 'birds' 
    def get_queryset(self):
        return Bird.objects.filter(user=self.request.user)

class CreateBirdView(LoginRequiredMixin, CreateView):
    model = Bird
    fields = ['name', 'species', 'color']
    template_name = 'bird_form.html'
    success_url = reverse_lazy('bird_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateBirdView(LoginRequiredMixin, UpdateView):
    model = Bird
    fields = ['name', 'species', 'color']
    template_name = 'bird_form.html'
    success_url = reverse_lazy('bird_list')

class DeleteBirdView(LoginRequiredMixin, DeleteView):
    model = Bird
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('bird_list')


# All CRUD functions for the Accessory model
class CreateAccessoryView(CreateView):
    model = Accessory
    fields = ['name', 'type']
    template_name = 'accessory_form.html'
    success_url = reverse_lazy('accessory_list')

class AccessoryListView(ListView):
    model = Accessory
    template_name = 'accessory_list.html'
    context_object_name = 'accessories'

class UpdateAccessoryView(UpdateView):
    model = Accessory
    fields = ['name', 'type']
    template_name = 'accessory_form.html'
    success_url = reverse_lazy('accessory_list')

class DeleteAccessoryView(DeleteView):
    model = Accessory
    template_name = 'confirm_delet.html'
    success_url = reverse_lazy('accessory_list')