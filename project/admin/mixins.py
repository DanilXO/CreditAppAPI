
class ClickModelAdminMixin:
    change_list_template = "core/click_change_list.html"

    def suit_row_attributes(self, obj, request):
        attrs = {'data-href': '{}{}'.format(request.path, obj.pk)}
        return attrs
