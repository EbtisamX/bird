from rest_framework import serializers
from main_app.models import Bird,Accessory,Vet

class BirdSerializer(serializers.ModelSerializer):
    accessories = serializers.PrimaryKeyRelatedField(
        many=True,  
        queryset=Accessory.objects.all(),  
        allow_empty=True,  
        required=False,)
    class Meta:
        model = Bird  
        fields = '__all__'  
        
class VetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vet
        fields = '__all__'