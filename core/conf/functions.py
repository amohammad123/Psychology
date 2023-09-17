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
