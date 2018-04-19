from django.core import validators


def IntRangeValidator(min_v=1, max_v=100):
    validatorsList = []
    if isinstance(min_v, int):
        validatorsList.append(validators.MinValueValidator(min_v, message=('不能小于%(limit_value)s.')))
    if isinstance(max_v, int):
        validatorsList.append(validators.MaxValueValidator(max_v, message=('不能大于%(limit_value)s.')))

    return validatorsList
