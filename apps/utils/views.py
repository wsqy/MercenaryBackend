from django.http import JsonResponse
from celery.result import AsyncResult


def get_celery_task_status(request):
    try:
        job_id = request.GET.get('task_id')
        return JsonResponse({
            'job_status': AsyncResult(job_id).state,
            'job_result': AsyncResult(job_id).result,
        })
    except Exception as e:
        return JsonResponse({'msg': e})
