import bpy


# FUNCTION


def use_skin_collection_or_active(index=0):

    if bpy.context.scene.skis_skin_collection_list[index].skin_coll:
        return bpy.context.scene.skis_skin_collection_list[index].skin_coll
    else:
        return bpy.context.collection


def hide_objs_in_coll(collection, force_hide=False):

    for obj in collection.all_objects:
        if force_hide:
            if obj.visible_get():
                obj.hide_set(state=True)
        elif obj.visible_get() and not obj.skis_hide_exclude:
            obj.hide_set(state=True)


def unhide_objs(obj):

    if obj:
        obj.hide_set(state=False)


def sort_item_in_collection(index):

    if use_skin_collection_or_active(index) is bpy.context.view_layer.layer_collection.collection:
        coll = bpy.context.view_layer.objects
    else:
        coll = use_skin_collection_or_active(index).all_objects
        if use_skin_collection_or_active(index).skis_is_local:
            coll = use_skin_collection_or_active(index).objects

    sort_coll = coll.keys().copy()
    sort_coll.sort(key=str.casefold)

    return sort_coll


# OPERATOR


class SKIS_OP_to_outliner(bpy.types.Operator):
    bl_idname = 'skis.to_outliner'
    bl_label = 'Jump to object in outliner'
    bl_description = 'Jump to the object in outliner'

    skin_name: bpy.props.StringProperty()
    coll_index: bpy.props.IntProperty()
    type: bpy.props.EnumProperty(
        name='Type',
        items=[
            ('OBJECT', 'Object', 'To object'),
            ('COLLECTION', 'Collection', 'To collection'),
        ]
    )

    def execute(self, context):

        areas = [i for i in bpy.context.screen.areas if i.type == 'OUTLINER']
        area = [a for a in areas if a.spaces[0].display_mode == 'VIEW_LAYER'][0]
        region = [j for j in area.regions if j.type == 'WINDOW'][0]

        with bpy.context.temp_override(area=area, region=region):

            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            if self.type == 'OBJECT':
                obj = bpy.data.objects[self.skin_name]
                # bpy.context.view_layer.objects.active = obj
                bpy.data.objects[self.skin_name].select_set(True)

            elif self.type == 'COLLECTION':
                obj = bpy.data.objects[sort_item_in_collection(self.coll_index)[0]]

            bpy.context.view_layer.objects.active = obj
            bpy.ops.outliner.show_hierarchy()
            bpy.ops.outliner.show_active()

        return {'FINISHED'}


class SKIS_OP_add_skin_collection_to_list(bpy.types.Operator):
    bl_idname = 'skis.add_skin_collection_to_list'
    bl_label = 'Add skin collection to list'
    bl_description = 'Add a new skin collection to list'

    def execute(self, context):

        scene = bpy.context.scene

        scene.skis_skin_collection_list_index = len(scene.skis_skin_collection_list)
        scene.skis_skin_collection_list.add()

        return {'FINISHED'}


class SKIS_OP_remove_skin_collection_in_list(bpy.types.Operator):
    bl_idname = 'skis.remove_skin_collection_in_list'
    bl_label = 'Remove skin collection in list'
    bl_description = 'Remove a skin collection in list'

    def execute(self, context):

        scene = bpy.context.scene

        scene.skis_skin_collection_list.remove(scene.skis_skin_collection_list_index or 0)
        scene.skis_skin_collection_list_index = min(
            scene.skis_skin_collection_list_index,
            len(scene.skis_skin_collection_list) - 1,
        )
        return {'FINISHED'}


class SKIS_OP_move_skin_collection_in_list(bpy.types.Operator):
    bl_idname = 'skis.move_skin_collection_in_list'
    bl_label = 'Move collection'
    bl_description = 'Move skin collection up/down in the list'

    direction: bpy.props.EnumProperty(
        name='Move direction',
        items=[
            ('UP', 'Move up', 'Move collection up'),
            ('DOWN', 'Move down', 'Move collection down'),
            ('FIRST', 'Move to first', 'Move collection to first place'),
            ('LAST', 'Move last', 'Move collection last place'),
        ]
    )

    def execute(self, context):

        scene = context.scene
        index: int

        match self.direction:
            case 'UP':
                index = scene.skis_skin_collection_list_index - 1
            case 'DOWN':
                index = scene.skis_skin_collection_list_index + 1
            case 'FIRST':
                index = 0
            case 'LAST':
                index = len(scene.skis_skin_collection_list) - 1

        scene.skis_skin_collection_list.move(scene.skis_skin_collection_list_index, index)
        scene.skis_skin_collection_list_index = index

        return {'FINISHED'}


class SKIS_OP_skin_collection_batch_setting(bpy.types.Operator):
    bl_idname = 'skis.batch_setting_skin_collection'
    bl_label = 'Setting for skin collection in batch'
    bl_description = 'Change setting for skin collection in batch'

    collapse: bpy.props.BoolProperty()

    def execute(self, context):

        for i in context.scene.skis_skin_collection_list:

            i.collapse = self.collapse

        return {'FINISHED'}


class SKIS_OP_set_skin_collection(bpy.types.Operator):
    bl_idname = 'skis.set_skin_collection'
    bl_label = 'Set skin collection'
    bl_description = 'Set active collection as skin collection at index'

    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return context.collection

    def execute(self, context):

        bpy.context.scene.skis_skin_collection_list[self.index].skin_coll = bpy.context.collection

        return {'FINISHED'}


class SKIS_OP_to_active_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.to_active_skin_in_collection'
    bl_label = 'To active skin in collection'

    skin_name: bpy.props.StringProperty()
    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        coll = use_skin_collection_or_active(self.coll_index)

        hide_objs_in_coll(coll)
        coll.skis_active_skin = bpy.data.objects[self.skin_name]
        unhide_objs(bpy.data.objects[self.skin_name])

        coll.skis_list_index = coll.all_objects.keys().index(self.skin_name)

        return {'FINISHED'}


class SKIS_OP_hide_non_active_skin_in_collection(bpy.types.Operator):
    bl_idname = 'skis.hide_non_active_skin_in_collection'
    bl_label = 'Hide non active skin in collection'

    coll_index: bpy.props.IntProperty()

    def execute(self, context):

        coll = use_skin_collection_or_active(self.coll_index)

        hide_objs_in_coll(coll)
        unhide_objs(coll.skis_active_skin)

        for obj in coll.all_objects:
            if obj.skis_hide_exclude:
                unhide_objs(obj)

        coll.skis_list_index = coll.all_objects.keys().index(coll.skis_active_skin.name)

        return {'FINISHED'}


class SKIS_OP_hide_all_non_active_skin(bpy.types.Operator):
    bl_idname = 'skis.hide_all_non_active_skin'
    bl_label = 'Hide all non active skin'

    def execute(self, context):

        hide_objs_in_coll(context.scene.collection, force_hide=True)

        for index in range(len(context.scene.skis_skin_collection_list)):
            if context.scene.skis_skin_collection_list[index].show:
                for obj in use_skin_collection_or_active(index).all_objects:
                    if obj.skis_hide_exclude or obj is use_skin_collection_or_active(index).skis_active_skin:
                        unhide_objs(obj)

        return {'FINISHED'}


class SKIS_OP_skin_jump_in_collection(bpy.types.Operator):
    bl_idname = 'skis.skin_jump_in_collection'
    bl_label = 'Jump to skin'
    bl_description = 'Jump to skin in collection'

    coll_index: bpy.props.IntProperty()
    options: bpy.props.EnumProperty(
        name='Jump options',
        items=[
            ('NEXT', 'Jump next', 'Jump to next skin'),
            ('PREV', 'Jump previous', 'Jump to previous skin'),
            ('FIRST', 'Jump first', 'Jump to first skin'),
            ('LAST', 'Jump last', 'Jump to last skin'),
        ]
    )

    def execute(self, context):

        coll = use_skin_collection_or_active(self.coll_index)
        sort_coll = sort_item_in_collection(self.coll_index)
        collection_list = bpy.context.scene.skis_skin_collection_list

        hide_objs_in_coll(coll)

        # get index

        match self.options:
            case 'NEXT':
                skin_index = sort_coll.index(coll.skis_active_skin.name)
                index = skin_index + 1
                if index == len(sort_coll):
                    index = 0
            case 'PREV':
                skin_index = sort_coll.index(coll.skis_active_skin.name)
                index = skin_index - 1
            case 'FIRST':
                index = 0
            case 'LAST':
                index = -1

        objs = coll.all_objects
        if use_skin_collection_or_active(self.coll_index).skis_is_local:
            objs = coll.objects

        coll.skis_active_skin = objs[sort_coll[index]]

        # skip hide viewport, hide exclude and filtered items

        is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type
        is_hide_viewport = coll.skis_active_skin.hide_viewport

        if not collection_list[self.coll_index].use_flt:
            is_flt = False

        step = 0

        while is_hide_viewport or is_flt:

            step += 1

            if step == len(sort_coll):
                break

            skin_index = sort_coll.index(coll.skis_active_skin.name)

            match self.options:
                case 'NEXT':
                    index = skin_index + 1
                    if index == len(sort_coll):
                        index = 0
                case 'PREV':
                    index = skin_index - 1
                case 'FIRST':
                    index = skin_index + 1
                case 'LAST':
                    index = skin_index - 1

            coll.skis_active_skin = objs[sort_coll[index]]

            is_hide_viewport = coll.skis_active_skin.hide_viewport

            if collection_list[self.coll_index].use_flt:
                is_flt = coll.skis_active_skin.type != collection_list[self.coll_index].flt_type

        unhide_objs(coll.skis_active_skin)

        coll.skis_list_index = objs.keys().index(coll.skis_active_skin.name)

        return {'FINISHED'}


class SKIS_OP_highlight_skin(bpy.types.Operator):
    bl_idname = 'skis.highlight_skin'
    bl_label = '[Skis] Highlight skin'
    bl_description = 'Highlight skin in collection'

    def execute(self, context):

        coll = context.scene.skis_skin_collection_list
        collections = []

        for index in range(len(coll)):
            collections.append(use_skin_collection_or_active(index))

        if context.object:
            obj_coll = context.object.users_collection[0]

        coll_index = []
        for index, co in enumerate(collections):
            if obj_coll == co:
                coll_index.append(index)

        for index, co in enumerate(coll):

            co.collapse = True

            objs = use_skin_collection_or_active(index).all_objects
            if co.is_local:
                objs = use_skin_collection_or_active(index).objects

            if index in coll_index:
                co.collapse = False
                use_skin_collection_or_active(index).skis_list_index = objs.keys().index(context.object.name)

        for region in context.area.regions:
            if region.type == 'UI':
                region.active_panel_category = bpy.types.SKIS_PT_side_panel_collection_list.bl_category
                region.tag_redraw()

        return {'FINISHED'}
