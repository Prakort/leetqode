from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from problems.models import Problem


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint that doesn't require authentication."""
    return JsonResponse({
        'status': 'healthy',
        'message': 'LeetQode API is running',
        'total_problems': Problem.objects.count()
    })


@csrf_exempt
@require_http_methods(["GET"])
def public_problems(request):
    """Get a few sample problems without authentication."""
    problems = Problem.objects.all()[:5]
    data = []
    for problem in problems:
        data.append({
            'id': problem.id,
            'title': problem.title,
            'difficulty': problem.difficulty,
            'tags': problem.tags,
            'url': problem.url
        })
    
    return JsonResponse({
        'problems': data,
        'total': Problem.objects.count(),
        'message': 'Sample problems (login required for full access)'
    })
