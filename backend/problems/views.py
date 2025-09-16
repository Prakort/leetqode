from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Problem, UserProblem
from .serializers import (
    ProblemSerializer, UserProblemSerializer, UserProblemUpdateSerializer,
    DashboardSerializer
)


class ProblemListView(generics.ListAPIView):
    """List all problems with optional filtering."""
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Problem.objects.all()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by tags
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__overlap=tags)
        
        return queryset


class UserProblemListView(generics.ListCreateAPIView):
    """List user's problems or create new user problem."""
    serializer_class = UserProblemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserProblem.objects.filter(user=self.request.user)
        
        # Filter by confidence level
        confidence = self.request.query_params.get('confidence')
        if confidence:
            queryset = queryset.filter(confidence__gte=confidence)
        
        # Filter by next due date
        due_today = self.request.query_params.get('due_today')
        if due_today == 'true':
            queryset = queryset.filter(next_due__date__lte=timezone.now().date())
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(problem__difficulty=difficulty)
        
        # Filter by tags
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(problem__tags__overlap=tags)
        
        return queryset.select_related('problem')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProblemUpdateView(generics.UpdateAPIView):
    """Update user problem confidence and progress."""
    serializer_class = UserProblemUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProblem.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated user problem data
        response_serializer = UserProblemSerializer(instance)
        return Response(response_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """Get problems due today for dashboard."""
    due_problems = UserProblem.objects.filter(
        user=request.user,
        next_due__date__lte=timezone.now().date()
    ).select_related('problem').order_by('next_due')
    
    serializer = DashboardSerializer(due_problems, many=True)
    return Response({
        'due_today': serializer.data,
        'total_due': due_problems.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def problem_stats(request):
    """Get user's problem statistics."""
    user_problems = UserProblem.objects.filter(user=request.user)
    
    stats = {
        'total_problems': user_problems.count(),
        'solved_problems': user_problems.filter(solved_count__gt=0).count(),
        'due_today': user_problems.filter(next_due__date__lte=timezone.now().date()).count(),
        'average_confidence': user_problems.aggregate(
            avg_confidence=Avg('confidence')
        )['avg_confidence'] or 0,
        'difficulty_breakdown': {
            'Easy': user_problems.filter(problem__difficulty='Easy').count(),
            'Medium': user_problems.filter(problem__difficulty='Medium').count(),
            'Hard': user_problems.filter(problem__difficulty='Hard').count(),
        }
    }
    
    return Response(stats)
