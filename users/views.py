from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import Utilisateur
from .serializers import UtilisateurSerializer
from rest_framework.decorators import api_view


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # .decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response        
        

@api_view(['GET', 'POST', 'DELETE'])
def utilisateur_list(request):
      
# *********get user*******************
    if request.method == 'GET':
       
        firstname = request.GET.get('firstname', None)
        if firstname is not None:
            utilisateurs = Utilisateur.objects.all()
            utilisateurs = utilisateurs.filter(firstname__icontains=firstname)
            utilisateurs_serializer = UtilisateurSerializer(utilisateurs, many=True)
        return JsonResponse(utilisateurs_serializer.data, safe=False)
 

# *********add user***************
    elif request.method == 'POST':
        utilisateur_data = JSONParser().parse(request)
        utilisateur_serializer = UtilisateurSerializer(data=utilisateur_data)
        if utilisateur_serializer.is_valid():
            utilisateur_serializer.save()
            return JsonResponse(utilisateur_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(utilisateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Utilisateur.objects.all().delete()
    return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def utilisateur_detail(request, pk):
    # find utilisateur by pk (id)
    try: 
        utilisateur = Utilisateur.objects.get(pk=pk) 
    except Utilisateur.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE utilisateur
    if request.method == 'GET': 
        utilisateur_serializer = UtilisateurSerializer(utilisateur) 
        return JsonResponse(utilisateur_serializer.data) 
    
    elif request.method == 'PUT': 
        utilisateur_data = JSONParser().parse(request) 
        utilisateur_serializer = UtilisateurSerializer(utilisateur, data=utilisateur_data) 
        if utilisateur_serializer.is_valid(): 
            utilisateur_serializer.save() 
            return JsonResponse(utilisateur_serializer.data) 
        return JsonResponse(utilisateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        utilisateur.delete() 
        return JsonResponse({'message': 'user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    
        
@api_view(['GET'])
def utilisateur_list_published(request):
    # GET all published utilisateurs
    utilisateurs = Utilisateur.objects.filter(published=True)
        
    if request.method == 'GET': 
        utilisateurs_serializer = UtilisateurSerializer(utilisateurs, many=True)
        return JsonResponse(utilisateurs_serializer.data, safe=False)
