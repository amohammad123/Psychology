from django.db.models import Case, When, IntegerField


def get_sub_ids(obj_id, obj, parent_field):
    my_list = set()

    def collect_parent_ids(model):
        parents_obj = getattr(model, parent_field).all()

        for parent in parents_obj:
            my_list.add(parent.id)
            collect_parent_ids(model=parent)

    collect_parent_ids(model=obj)
    my_list.add(obj_id)
    return list(my_list)


class Ordering:
    def __init__(self, request, queryset, category_id=None):
        self.request = request
        self.category_id = category_id
        self.model_name = queryset.model.__name__
        if category_id is not None:
            self.queryset = queryset.annotate(
                custom_order=Case(
                    When(category=category_id, then=1),
                    default=2,
                    output_field=IntegerField()
                )
            )
        else:
            self.queryset = queryset
        self.ordering_param_map = self.ordering_items()

    def get_order(self):
        list(self.ordering_param_map.keys())
        ordering_param = self.request.GET.get('ordering')
        if self.category_id is not None:
            actual_ordering = self.ordering_param_map.get(ordering_param, 'custom_order')
            queryset = self.queryset.order_by(actual_ordering, 'custom_order', '-create_date', '-update_date')
        else:
            actual_ordering = self.ordering_param_map.get(ordering_param, '-create_date')
            queryset = self.queryset.order_by(actual_ordering, '-create_date', '-update_date')

        return queryset

    def ordering_items(self):
        if self.model_name == 'Package':
            items = {
                'price': 'payment__offer_price',
                '-price': '-payment__offer_price',
                'like': 'rates__like',
                '-like': '-rates__like',
                'sell': 'sell_count',
                '-sell': '-sell_count',
                'view': 'views',
                '-view': '-views',
                'time': 'time',
                '-time': '-time',
            }
        if self.model_name == 'Test':
            items = {
                'price': 'payment__offer_price',
                '-price': '-payment__offer_price',
                'time': 'time',
                '-time': '-time',
                'like': 'rates__like',
                '-like': '-rates__like',
                'min_age': 'min_age',
                '-min_age': '-min_age',
                'max_age': 'max_age',
                '-max_age': '-max_age',
                'question': 'question_count',
                '-question': '-question_count',
            }
        if self.model_name == 'Post':
            items = {
                'view': 'views',
                '-view': '-views',
                'time_to_read': 'time_to_read',
                '-time_to_read': '-time_to_read',
                'like': 'rates__like',
                '-like': '-rates__like',
            }
        return items
