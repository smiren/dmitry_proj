from django.contrib import admin, messages
from .models import (ExtUser, BaseOrder, SimpleOrder, UserOrder, StaffComment,
                     OrderPosition,
                     )
from main.utils import (CONFIRM_ORDER_MSG, READY_ORDER_MSG, PROBLEM_ORDER_MSG,
                        FINISH_ORDER_MSG,
                        )

admin.site.register(ExtUser)


class OrderPositionInline(admin.TabularInline):
    model = OrderPosition
    extra = 0


class StaffCommentInline(admin.TabularInline):
    model = StaffComment
    extra = 0
    can_delete = False
    readonly_fields = ['comment']


@admin.register(BaseOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'status', 'total_cost', 'phone']
    search_fields = ['phone']
    list_filter = ['finished', 'status']
    actions = ['set_confirm_status', 'set_ready_status', 'set_problem_status',
               'set_finished',
               ]
    inlines = [OrderPositionInline, StaffCommentInline]

    def update_orders_and_send_comments(self, request, queryset=None,
                                        message="Processed", field='status', value=None):
        """Utility method for Actions"""
        if queryset is None or value is None:
            return
        comments = []
        for order in queryset:
            comments.append(StaffComment(order=order, comment=message))
        StaffComment.objects.bulk_create(comments)
        count = queryset.update(**{field: value})
        self.message_user(request, "Изменено заказов(а): %s." % count)

    def get_targets_queryset(self, request, queryset=None,
                             field='status', values=None):
        """Utility method for Actions"""
        if queryset is not None and values is not None:
            filter_kw = {field+'__in': values}
            targets = queryset.filter(**filter_kw)
        elif queryset is not None:
            targets = queryset
        else:
            targets = None
        if not targets:
            self.message_user(
                request, 'Нет подходящих заказов для данного действия')
        return targets

    def set_confirm_status(self, request, queryset):
        """Action"""
        targets = self.get_targets_queryset(request, queryset,
                                            values=('OP', 'PR'))
        if targets:
            self.update_orders_and_send_comments(request, targets,
                                                 CONFIRM_ORDER_MSG, value='CF')
    set_confirm_status.short_description = "ПОДТВЕРДИТЬ -изменить статус"

    def set_ready_status(self, request, queryset):
        """Action"""
        targets = self.get_targets_queryset(request, queryset,
                                            values=('CF', 'PR'))
        if targets:
            self.update_orders_and_send_comments(request, targets,
                                                 READY_ORDER_MSG, value='RD')
    set_ready_status.short_description = "ВЫПОЛНИТЬ -изменить статус"

    def set_problem_status(self, request, queryset):
        """Action"""
        targets = self.get_targets_queryset(request, queryset)
        if targets:
            self.update_orders_and_send_comments(request, targets,
                                                 PROBLEM_ORDER_MSG, value='PR')
    set_problem_status.short_description = "ПРОБЛЕМА -изменить статус"

    def set_finished(self, request, queryset):
        """Action"""
        targets = self.get_targets_queryset(request, queryset,
                                            field='finished', values=[False])
        if targets:
            self.update_orders_and_send_comments(request, targets,
                                                 FINISH_ORDER_MSG, field='finished',  value=True)
    set_finished.short_description = "ЗАКРЫТЬ заказ"


@admin.register(SimpleOrder)
class SimpleOrderAdmin(OrderAdmin):
    list_display = ['__str__', 'created',
                    'status', 'total_cost', 'email', 'phone']
    search_fields = ['phone', 'email']


@admin.register(UserOrder)
class UserOrderAdmin(OrderAdmin):
    list_display = ['__str__', 'created', 'status',
                    'total_cost', 'user_email', 'phone']
    search_fields = ['phone', 'user__email']

    def user_email(self, obj):
        return obj.user.email
