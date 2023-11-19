import bpy

from .pref import prefs

# FUNCTION


def use_skin_collection_or_active(index=0):

    if bpy.context.scene.skis_skin_collection_list[index].skin_coll is None:
        return bpy.context.collection
    else:
        return bpy.context.scene.skis_skin_collection_list[index].skin_coll


def hide_objs_in_coll(collection):

    for obj in collection.all_objects.keys():
        if collection.all_objects[obj].visible_get():
            collection.all_objects[obj].hide_set(state=True)


def unhide_objs(obj):

    if obj is not None:
        obj.hide_set(state=False)


# OPERATOR


class SKIS_OP_add_skin_collection_to_list(bpy.types.Operator):
    bl_idname = 'skis.add_skin_collection_to_list'
    bl_label = 'Add skin collection to list'
    bl_description = 'Add a new skin collection to list'
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.context.scene.skis_skin_collection_list.add()

        return {'FINISHED'}


class SKIS_OP_remove_skin_collection_in_list(bpy.types.Operator):
    bl_idname = 'skis.remove_skin_collection_in_list'
    bl_label = 'Remove skin collection in list'
    bl_description = 'Remove a skin collection in list'
    bl_options = {'REGISTER'}

    def execute(self, context):

        bpy.context.scene.skis_skin_collection_list.remove(
            bpy.context.scene.skis_skin_collection_list_index
            if bpy.context.scene.skis_skin_collection_list_index
            else 0
        )

        return {'FINISHED'}


class SKIS_OP_set_skin_collection(bpy.types.Operator):
    bl_idname = 'skis.set_skin_collection'
    bl_label = 'Set skin collection'
    bl_description = 'Set active collection as skin collection at index'
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):

        bpy.context.scene.skis_skin_collection_list[self.index].skin_coll = bpy.context.collection

        return {'FINISHED'}


class SKIS_OP_to_active_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_active_skin_in_collection'
    bl_label = 'To active skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    skin_name: bpy.props.StringProperty()
    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        hide_objs_in_coll(use_skin_collection_or_active(self.coll_index))
        use_skin_collection_or_active(
            self.coll_index).skis_active_skin = bpy.data.objects[self.skin_name]
        unhide_objs(bpy.data.objects[self.skin_name])

        return {'FINISHED'}


class SKIS_OP_hide_non_active_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.hide_non_active_skin_in_collection'
    bl_label = 'Hide non active skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        hide_objs_in_coll(use_skin_collection_or_active(self.coll_index))
        unhide_objs(use_skin_collection_or_active(
            self.coll_index).skis_active_skin)

        return {'FINISHED'}


class SKIS_OP_hide_all_non_active_skin(bpy.types.Operator):
    bl_idname = 'skis.hide_all_non_active_skin'
    bl_label = 'Hide all non active skin'

    def execute(self, context):

        hide_objs_in_coll(bpy.context.scene.collection)

        for index in range(0, len(bpy.context.scene.skis_skin_collection_list)):
            if bpy.context.scene.skis_skin_collection_list[index].show:
                unhide_objs(use_skin_collection_or_active(
                    index).skis_active_skin)

        return {'FINISHED'}


def sort_item_in_collection(collection):

    if use_skin_collection_or_active(collection) is bpy.context.view_layer.layer_collection.collection:
        sort_coll = bpy.context.view_layer.objects.keys().copy()
    else:
        sort_coll = use_skin_collection_or_active(
            collection).all_objects.keys().copy()
    sort_coll.sort(key=str.casefold)

    return sort_coll


class SKIS_OP_to_next_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_next_skin_in_collection'
    bl_label = 'To next skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        # get next index

        coll = use_skin_collection_or_active(self.coll_index)
        sort_coll = sort_item_in_collection(self.coll_index)
        collection_list = bpy.context.scene.skis_skin_collection_list

        index = sort_coll.index(coll.skis_active_skin.name)
        next_index = index + 1
        if next_index == len(sort_coll):
            next_index = 0

        coll.skis_active_skin = coll.all_objects[sort_coll[next_index]]

        hide_objs_in_coll(coll)

        # skip hide viewport and filtered items

        is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type
        is_hide_viewport = coll.skis_active_skin.hide_viewport

        if not collection_list[self.coll_index].use_flt:
            is_flt = False

        while is_hide_viewport or is_flt:

            index = sort_coll.index(coll.skis_active_skin.name)
            next_index = index + 1
            if next_index == len(sort_coll):
                next_index = 0

            coll.skis_active_skin = coll.all_objects[sort_coll[next_index]]

            is_hide_viewport = coll.skis_active_skin.hide_viewport

            if collection_list[self.coll_index].use_flt:
                is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type

        unhide_objs(coll.all_objects[coll.skis_active_skin.name])

        return {'FINISHED'}


class SKIS_OP_to_prev_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_prev_skin_in_collection'
    bl_label = 'To prev skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        # get prev index

        coll = use_skin_collection_or_active(self.coll_index)
        sort_coll = sort_item_in_collection(self.coll_index)
        collection_list = bpy.context.scene.skis_skin_collection_list

        index = sort_coll.index(coll.skis_active_skin.name)
        prev_index = index - 1

        coll.skis_active_skin = coll.all_objects[sort_coll[prev_index]]

        hide_objs_in_coll(coll)

        # skip hide viewport and filtered items

        is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type
        is_hide_viewport = coll.skis_active_skin.hide_viewport

        if not collection_list[self.coll_index].use_flt:
            is_flt = False

        while is_hide_viewport or is_flt:

            index = sort_coll.index(coll.skis_active_skin.name)
            prev_index = index - 1

            coll.skis_active_skin = coll.all_objects[sort_coll[prev_index]]

            is_hide_viewport = coll.skis_active_skin.hide_viewport

            if collection_list[self.coll_index].use_flt:
                is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type

        unhide_objs(coll.all_objects[coll.skis_active_skin.name])

        return {'FINISHED'}


class SKIS_OP_to_first_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_first_skin_in_collection'
    bl_label = 'To first skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        # get first index

        coll = use_skin_collection_or_active(self.coll_index)
        sort_coll = sort_item_in_collection(self.coll_index)
        collection_list = bpy.context.scene.skis_skin_collection_list

        first_index = 0

        coll.skis_active_skin = coll.all_objects[sort_coll[first_index]]

        hide_objs_in_coll(coll)

        # skip hide viewport and filtered items

        is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type
        is_hide_viewport = coll.skis_active_skin.hide_viewport

        if not collection_list[self.coll_index].use_flt:
            is_flt = False

        while is_hide_viewport or is_flt:

            index = sort_coll.index(coll.skis_active_skin.name)
            first_index = index + 1

            coll.skis_active_skin = coll.all_objects[sort_coll[first_index]]

            is_hide_viewport = coll.skis_active_skin.hide_viewport

            if collection_list[self.coll_index].use_flt:
                is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type

        unhide_objs(coll.all_objects[coll.skis_active_skin.name])

        return {'FINISHED'}


class SKIS_OP_to_last_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_last_skin_in_collection'
    bl_label = 'To last skin in collection'
    bl_options = {'REGISTER', 'UNDO'}

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        # get last index

        coll = use_skin_collection_or_active(self.coll_index)
        sort_coll = sort_item_in_collection(self.coll_index)
        collection_list = bpy.context.scene.skis_skin_collection_list

        last_index = len(sort_coll) - 1

        coll.skis_active_skin = coll.all_objects[sort_coll[last_index]]

        hide_objs_in_coll(coll)

        # skip hide viewport and filtered items

        is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type
        is_hide_viewport = coll.skis_active_skin.hide_viewport

        if not collection_list[self.coll_index].use_flt:
            is_flt = False

        while is_hide_viewport or is_flt:

            index = sort_coll.index(coll.skis_active_skin.name)
            last_index = index - 1

            coll.skis_active_skin = coll.all_objects[sort_coll[last_index]]

            is_hide_viewport = coll.skis_active_skin.hide_viewport

            if collection_list[self.coll_index].use_flt:
                is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type

        unhide_objs(coll.all_objects[coll.skis_active_skin.name])

        return {'FINISHED'}
