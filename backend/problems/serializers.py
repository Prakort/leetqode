from rest_framework import serializers
from .models import Problem, UserProblem


class ProblemSerializer(serializers.ModelSerializer):
    """Serializer for Problem model."""
    
    class Meta:
        model = Problem
        fields = ['id', 'title', 'url', 'difficulty', 'tags']


class UserProblemSerializer(serializers.ModelSerializer):
    """Serializer for UserProblem model with problem details."""
    problem = ProblemSerializer(read_only=True)
    problem_id = serializers.IntegerField(write_only=True)
    is_due_today = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = UserProblem
        fields = [
            'id', 'problem', 'problem_id', 'confidence', 'frequency_days',
            'last_attempted', 'next_due', 'attempts_count', 'solved_count',
            'is_due_today', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'frequency_days', 'last_attempted', 'next_due',
            'attempts_count', 'solved_count', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        """Create or get existing UserProblem."""
        problem_id = validated_data.pop('problem_id')
        user = validated_data.get('user')
        
        # Check if UserProblem already exists
        user_problem, created = UserProblem.objects.get_or_create(
            user=user,
            problem_id=problem_id,
            defaults=validated_data
        )
        
        if not created:
            # If it already exists, return the existing one
            return user_problem
        
        return user_problem


class UserProblemUpdateSerializer(serializers.Serializer):
    """Serializer for updating user problem confidence."""
    confidence_change = serializers.IntegerField(
        min_value=-100, 
        max_value=100,
        help_text="Change in confidence level (-100 to 100)"
    )
    solved = serializers.BooleanField(
        default=False,
        help_text="Whether the problem was solved"
    )
    
    def update(self, instance, validated_data):
        confidence_change = validated_data.get('confidence_change', 0)
        solved = validated_data.get('solved', False)
        
        # Adjust confidence change based on solved status
        if solved and confidence_change <= 0:
            confidence_change = 20  # Positive change for solving
        elif not solved and confidence_change >= 0:
            confidence_change = -10  # Negative change for not solving
        
        instance.update_confidence(confidence_change)
        return instance


class DashboardSerializer(serializers.ModelSerializer):
    """Serializer for dashboard problems due today."""
    problem = ProblemSerializer(read_only=True)
    is_due_today = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = UserProblem
        fields = [
            'id', 'problem', 'confidence', 'frequency_days',
            'last_attempted', 'next_due', 'attempts_count', 'solved_count',
            'is_due_today'
        ]


