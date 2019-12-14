def log_addition(username, obj, object_type, message):
    from log.models import CuneiformLogEntry, ADDITION
    return CuneiformLogEntry.objects.log_action(
        username=username,
        object_id=obj.pk,
        object_type=object_type,
        action_flag=ADDITION,
        change_message=message,
    )


def log_change(username, obj, object_type, message):
    from log.models import CuneiformLogEntry, CHANGE
    return CuneiformLogEntry.objects.log_action(
        username=username,
        object_id=obj.pk,
        object_type=object_type,
        action_flag=CHANGE,
        change_message=message,
    )


def log_deletion(username, obj, object_type, message):
    from log.models import CuneiformLogEntry, DELETION
    return CuneiformLogEntry.objects.log_action(
        username=username,
        object_type=object_type,
        object_id=obj.pk,
        action_flag=DELETION,
        change_message=message,
    )


def log_doublecheck(username, obj, object_type, message):
    from log.models import CuneiformLogEntry, DOUBLECHECK
    return CuneiformLogEntry.objects.log_action(
        username=username,
        object_type=object_type,
        object_id=obj.pk,
        action_flag=DOUBLECHECK,
        change_message=message,
    )


def log_signoff(username, obj, object_type, message):
    from log.models import CuneiformLogEntry, SIGNOFF
    return CuneiformLogEntry.objects.log_action(
        username=username,
        object_type=object_type,
        object_id=obj.pk,
        action_flag=SIGNOFF,
        change_message=message,
    )


def get_matrix_hr_summary(pk):
    from .models import Prescription
    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("prescription does not exist")

    ret = '''
    <td>
    '''

    return ret
