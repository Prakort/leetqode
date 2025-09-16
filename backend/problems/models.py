from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Problem(models.Model):
    """LeetCode problem model."""
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    tags = models.JSONField(default=list, help_text="List of problem tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.id}. {self.title}"


class UserProblem(models.Model):
    """User's progress on a specific problem with spaced repetition."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_problems')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='user_problems')
    confidence = models.IntegerField(default=0, help_text="Confidence level 0-100")
    frequency_days = models.IntegerField(default=1, help_text="Days between reviews")
    last_attempted = models.DateTimeField(null=True, blank=True)
    next_due = models.DateTimeField(default=timezone.now)
    attempts_count = models.IntegerField(default=0)
    solved_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'problem']
        ordering = ['next_due']
    
    def __str__(self):
        return f"{self.user.email} - {self.problem.title}"
    
    def update_confidence(self, confidence_change):
        """Update confidence and recalculate next_due date."""
        self.confidence = max(0, min(100, self.confidence + confidence_change))
        self.last_attempted = timezone.now()
        self.attempts_count += 1
        
        # Spaced repetition algorithm
        if confidence_change > 0:
            self.solved_count += 1
            # Increase frequency for successful attempts
            self.frequency_days = min(30, self.frequency_days * 1.5)
        else:
            # Decrease frequency for failed attempts
            self.frequency_days = max(1, self.frequency_days * 0.7)
        
        # Calculate next due date
        self.next_due = timezone.now() + timedelta(days=self.frequency_days)
        self.save()
    
    def is_due_today(self):
        """Check if problem is due for review today."""
        return self.next_due.date() <= timezone.now().date()


class ProblemList(models.Model):
    """Metadata lists like Top100, Top200, Amazon, Meta."""
    LIST_TYPE_CHOICES = [
        ('top100', 'Top 100'),
        ('top200', 'Top 200'),
        ('company', 'Company Specific'),
        ('topic', 'Topic Based'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list_type = models.CharField(max_length=20, choices=LIST_TYPE_CHOICES, default='custom')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProblemListItem(models.Model):
    """Links problems to metadata lists."""
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='list_items')
    list = models.ForeignKey(ProblemList, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['problem', 'list']
        ordering = ['problem__id']
    
    def __str__(self):
        return f"{self.list.name} - {self.problem.title}"


class UserList(models.Model):
    """User-created lists for organizing problems."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class UserListItem(models.Model):
    """Links problems to user-created lists."""
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='user_list_items')
    user_list = models.ForeignKey(UserList, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['problem', 'user_list']
        ordering = ['problem__id']
    
    def __str__(self):
        return f"{self.user_list.name} - {self.problem.title}"
