from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# This class defines the Accessory model with name and type fields.
# It is used to represent bird accessories.
class Accessory(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  

    def __str__(self):
        return self.name
    
    
# This class defines the Bird model with name, species, color, and a many-to-many relationship with accessories.
class Bird(models.Model):
    name = models.CharField(max_length=100)         
    species = models.CharField(max_length=100)      
    color = models.CharField(max_length=50)
    accessories = models.ManyToManyField(Accessory) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.species}' 
    

# This class defines the Vet model which stores clinic info, appointment time, nurse name, and links to a specific bird.
class Vet(models.Model):

    clinic =  models.CharField(max_length=100)
    appointment = models.DateTimeField(default=timezone.now)
    nurse_name =  models.CharField(max_length=100)


    bird = models.ForeignKey(Bird, on_delete=models.CASCADE) 
    def __str__(self):                                          #(%Y-%m-%d %H:%M) Format the appointment date and time as (Year-Month-Day Hour:Minute)
        return f"{self.bird.name} - {self.clinic} on {self.appointment.strftime('%Y-%m-%d %H:%M')}"