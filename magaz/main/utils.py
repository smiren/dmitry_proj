# Other functions
import random
import string


def get_product_main_image_path(instance, filename):
    return f"products/{instance.slug}/main_image.{filename.split('.')[-1]}"


def get_extra_image_path(instance, filename):
    imagefile = "{0:0>8}.{1}".format(
        instance.product.image_quantity, filename.split('.')[-1])
    path = 'products/' + instance.product.slug + '/' + imagefile
    instance.product.increment_image()
    return path


def get_infopage_image_path(instance, filename):
    imagefile = "{0:0>8}.{1}".format(
        instance.pagename.image_quantity, filename.split('.')[1])
    path = 'infopages/' + instance.pagename.slug + '/' + imagefile
    instance.pagename.increment_image()
    return path


def get_random_string(length=20):
    return "".join([random.choice(string.ascii_letters+string.digits) for _ in range(length)])


CREATE_ORDER_MSG = (
    "Заказ принят в обработку, в ближайшее время наш менеджер свяжится с вами "
    "для подтверждения деталей заказа."
)

CONFIRM_ORDER_MSG = (
    "Заказ успешно подтвержден."
)

READY_ORDER_MSG = (
    "Заказ выполнен и ожидает завершения."
)

PROBLEM_ORDER_MSG = (
    "Проблема с заказом. Наш менеджер свяжется с вами в ближайшее время."
)

FINISH_ORDER_MSG = (
    "Заказ завершен."
)
