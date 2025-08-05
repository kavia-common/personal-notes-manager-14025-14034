from rest_framework import generics, permissions, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, logout
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    NoteSerializer,
)
from .models import Note

# Health endpoint remains for liveness probe.
@api_view(['GET'])
def health(request):
    """Health check endpoint for deployment probes."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """User registration endpoint

    POST /api/register/
    Request: { username, email, password }
    Response: User info
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

# PUBLIC_INTERFACE
class LoginView(views.APIView):
    """User login endpoint

    POST /api/login/
    Request: { username, password }
    Response: {user, message}
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'message': 'Successfully logged in',
            'username': user.username,
        })

# PUBLIC_INTERFACE
class LogoutView(views.APIView):
    """User logout endpoint

    POST /api/logout/
    Response: {message}
    """
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out.'})

# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    Get list of authenticated user's notes, or create a note.
    GET /api/notes/ - list notes for the logged-in user
    POST /api/notes/ - create new note for the logged-in user
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# PUBLIC_INTERFACE
class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/notes/<pk>/ - get single note for user
    PUT/PATCH /api/notes/<pk>/ - update note
    DELETE /api/notes/<pk>/ - delete note
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
