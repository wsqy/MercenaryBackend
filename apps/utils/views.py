from rest_framework import status
from rest_framework.response import Response
from celery.result import AsyncResult


def get_celery_status(request):
    job_id = request.GET.get('task_id')
    state = AsyncResult(job_id).state
    state_http_status = {
        'SUCCESS': status.HTTP_200_OK,
        'FAILURE': status.HTTP_400_BAD_REQUEST,
    }
    res_status = state_http_status.get(state, status.HTTP_202_ACCEPTED)

    return Response({}, status=res_status)
