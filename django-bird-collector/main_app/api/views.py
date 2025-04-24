from rest_framework.views import APIView
from rest_framework.response import Response
from main_app.models import Bird,Accessory
from .serializers import BirdSerializer,VetSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class SignUpView(APIView):
    permission_classes = [AllowAny]
    # When we recieve a POST request with username, email, and password. Create a new user.
    def post(self, request):
        # Using .get will not error if there's no username
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            validate_password(password)
        except ValidationError as err:
            return Response({'error': err.messages}, status=400)

        # Actually create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # create an access and refresh token for the user and send this in a response
        tokens = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            },
            status=201
        )

class BirdListAPI(APIView):
    # protect this from unauthenticated users
    permission_classes = [IsAuthenticated]
    def get(self, request):
        birds = Bird.objects.filter(user=request.user) 
        serializer = BirdSerializer(birds, many=True) 
        return Response(serializer.data) 
    def post(self, request):
        serializer = BirdSerializer(data=request.data)  
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

class CreateVetAPI(APIView):
    def post(self, request, bird_id):
        bird = get_object_or_404(Bird, pk=bird_id)
        data = request.data.copy()
        data['bird'] = bird.id
        serializer = VetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
'''The old @api_view ones are still here but commented out.'''

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_accessory_to_bird(request, bird_id, accessory_id):
    try:
        bird = Bird.objects.get(pk=bird_id)
        accessory = Accessory.objects.get(pk=accessory_id)
        bird.accessories.add(accessory)
        return Response({'message': 'Accessory was added!'}, status=status.HTTP_200_OK)
    except Bird.DoesNotExist:
        return Response({'error': 'Bird does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Accessory.DoesNotExist:
        return Response({'error': 'Accessory does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
 
    

@api_view(['POST'])
def remove_accessory_from_bird(request, bird_id, accessory_id):
    try:
        bird = Bird.objects.get(pk=bird_id)
        accessory = Accessory.objects.get(pk=accessory_id)
        if bird.accessories.filter(id=accessory.id).exists():
            bird.accessories.remove(accessory)
            return Response({'message': 'Accessory was Removed!'}, status=200)
        else:
            return Response({'message': 'The accessory is in the DB but it is not on the bird!'})
    
    except Bird.DoesNotExist:
        return Response({'error': 'The Bird Does Not Exist'}, status=404)
    
    except Accessory.DoesNotExist:
        return Response({'error': 'The Accessory Does Not Exist'}, status=404)
    
    except:
        return Response({'error': 'Something went wrong'}, status=500)

    

'''I tested another way using class-based views to add/remove accessories.'''
# class AddAccessoryToBirdAPI(APIView):
#     def post(self, request, bird_id, accessory_id):
#         try:
#             bird = Bird.objects.get(pk=bird_id)
#             accessory = Accessory.objects.get(pk=accessory_id)
#             bird.accessories.add(accessory)
#             return Response({'message': 'Accessory was added!'}, status=200)
        
#         except Bird.DoesNotExist:
#             return Response({'error': 'Bird does not exist'}, status=404)
        
#         except Accessory.DoesNotExist:
#             return Response({'error': 'Accessory does not exist'}, status=404)
        
#         except:
#             return Response({'error': 'Something went wrong'}, status=500)
        

# class RemoveAccessoryFromBirdAPI(APIView):
#     def post(self, request, bird_id, accessory_id):
#         try:
#             bird = Bird.objects.get(pk=bird_id)
#             accessory = Accessory.objects.get(pk=accessory_id)
            
#             if bird.accessories.filter(id=accessory.id).exists():
#                 bird.accessories.remove(accessory)
#                 return Response({'message': 'Accessory removed successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'Accessory is not linked to the bird'}, status=status.HTTP_400_BAD_REQUEST)
        
#         except Bird.DoesNotExist:
#             return Response({'error': 'Bird not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Accessory.DoesNotExist:
#             return Response({'error': 'Accessory not found'}, status=status.HTTP_404_NOT_FOUND)
#         except:
#             return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

