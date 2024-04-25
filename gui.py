import bpy

from .ops import use_skin_collection_or_active
from .pref import prefs


# side panel class


class SKIS_PT_side_panel_collection_list(bpy.types.Panel):
    bl_label = 'Skin swapper'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SkiS'
    bl_order = 0

    def draw(self, context):

        layout = self.layout

        # layout.label(text='Skin collection list:')

        row = layout.row(align=True)

        # left panel operator, add, remove

        col = row.column(align=True)
        # add
        col.operator('skis.add_skin_collection_to_list',
                     text='',
                     icon='ADD',
                     emboss=True
                     )
        # remove
        col.operator('skis.remove_skin_collection_in_list',
                     text='',
                     icon='REMOVE',
                     emboss=True
                     )

        # skin collection list

        col = row.column(align=True)
        col.template_list('SKIS_UL_collection_list',
                          '1',
                          bpy.context.scene,
                          'skis_skin_collection_list',
                          bpy.context.scene,
                          'skis_skin_collection_list_index',
                          )

        # right panel navigation operator

        col = row.column(align=True)
        # move to first
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_UP_BAR',
                          emboss=True
                          )
        op.direction = 'FIRST'
        # move up
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_UP',
                          emboss=True
                          )
        op.direction = 'UP'
        # move down
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_DOWN',
                          emboss=True
                          )
        op.direction = 'DOWN'
        # move to last
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_DOWN_BAR',
                          emboss=True
                          )
        op.direction = 'LAST'


class SKIS_PT_side_panel_skin_list(bpy.types.Panel):
    bl_label = 'Skin management'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SkiS'

    def draw(self, context):

        layout = self.layout

        # hide all non active button

        row = layout.row()
        col = row.column(align=True)
        col.scale_y = .8
        op = col.operator('skis.batch_setting_skin_collection', text='', icon='REMOVE')
        op.collapse = True
        op = col.operator('skis.batch_setting_skin_collection', text='', icon='DOWNARROW_HLT')
        op.collapse = False

        col = row.column(align=True)
        col.operator('skis.hide_all_non_active_skin', icon='GROUP_VERTEX')
        col.scale_y = 1.6

        # skin collections

        for index in range(len(bpy.context.scene.skis_skin_collection_list)):
            if bpy.context.scene.skis_skin_collection_list[index].show:
                skin_list_side_panel(context, layout, index)


# skin collection panel func


def skin_list_side_panel(context, layout, index):

    collection_list = bpy.context.scene.skis_skin_collection_list

    # get obj in collection

    if collection_list[index].skin_coll:
        obj = [
            i for i in collection_list[index].skin_coll.all_objects
        ]
    elif collection_list[index].skin_coll is None:
        obj = [
            i for i in bpy.context.collection.all_objects
        ]

    # get filtered skins

    if collection_list[index].use_flt:
        filtered_obj = [
            j for j in obj if j.type == collection_list[index].flt_type
        ]
    else:
        filtered_obj = [
            j for j in obj
        ]

    # get active skin existance

    is_active_exist = False
    if collection_list[index].skin_coll:
        is_active_exist = collection_list[index].skin_coll.skis_active_skin in filtered_obj
    else:
        is_active_exist = context.collection.skis_active_skin in filtered_obj

    # layout

    row = layout.row(align=True)

    # skin collection collapse

    row.prop(collection_list[index],
             'collapse',
             text='',
             icon=('RIGHTARROW'
                   if collection_list[index].collapse
                   else 'DOWNARROW_HLT'
                   ),
             emboss=False,
             )

    # skin collection show hide

    row.prop(collection_list[index],
             'show',
             text='',
             emboss=True,
             )

    # skin collection index

    box = row.box()
    box.scale_x = 0.4
    box.scale_y = 0.5
    box.label(text=f'{index + 1}',)
    box.alignment = 'CENTER'

    # set collection button

    col = row.column()
    col.scale_x = 1.2
    op = col.operator('skis.set_skin_collection',
                      text='',
                      icon='PINNED'
                      )
    op.index = index

    # to outliner button

    col = row.column()
    col.scale_x = 1.2
    op2 = col.operator('skis.to_outliner',
                       text='',
                       icon='ZOOM_SELECTED'
                       )
    op2.type = 'COLLECTION'
    op2.coll_index = index

    # skin collection prop

    row.prop(collection_list[index],
             'skin_coll',
             text='',
             icon=('NONE'
                   if collection_list[index].skin_coll is None or collection_list[index].skin_coll.color_tag == 'NONE'
                   else f'COLLECTION_{collection_list[index].skin_coll.color_tag}'
                   )
             )

    # skin collection hide viewport

    if collection_list[index].skin_coll:
        row.prop(collection_list[index].skin_coll,
                 'hide_viewport', text='', emboss=False)

    # under collapse line

    if not collection_list[index].collapse:

        row = layout.row(align=True)

        # skin count

        count_box = row.box()
        count_box.label(text=f'{len(filtered_obj)} skins')
        count_box.scale_y = 0.6
        count_box.scale_x = 0.7

        # skin collection item filter type

        # use filter prop
        filter = row.column()
        filter.prop(collection_list[index],
                    'use_flt',
                    text='Filter',
                    toggle=True,
                    icon='FILTER',
                    )
        filter.scale_x = 0.6

        # filter type prop
        flt_type = row.column()
        flt_type.prop(collection_list[index],
                      'flt_type',
                      text='',
                      )

        # skin collection list

        ui_list_row = layout.row(align=True)
        ui_list_row.template_list('SKIS_UL_skin_list',
                                  f'{index}',
                                  use_skin_collection_or_active(index),
                                  'all_objects',
                                  use_skin_collection_or_active(index),
                                  'skis_list_index',
                                  )
        ui_list_row.separator(factor=0.5)

        # hide non active button

        ops_col = ui_list_row.column(align=True)
        hide_non_acti_row = ops_col.row()
        hide_non_acti_row.enabled = is_active_exist
        hide_non_acti_op = hide_non_acti_row.operator('skis.hide_non_active_skin_in_collection',
                                                      text='',
                                                      icon='COMMUNITY',
                                                      emboss=True
                                                      )
        hide_non_acti_op.coll_index = index

        # first skin button

        ops_col.separator()

        first_op = ops_col.operator('skis.skin_jump_in_collection',
                                    text='',
                                    icon='TRIA_UP_BAR',
                                    emboss=True
                                    )
        first_op.coll_index = index
        first_op.options = 'FIRST'

        # prev skin button

        prev_row = ops_col.row()
        prev_row.enabled = is_active_exist
        prev_op = prev_row.operator('skis.skin_jump_in_collection',
                                    text='',
                                    icon='TRIA_UP',
                                    emboss=True
                                    )
        prev_op.coll_index = index
        prev_op.options = 'PREV'

        # next skin button

        next_row = ops_col.row()
        next_row.enabled = is_active_exist
        next_op = next_row.operator('skis.skin_jump_in_collection',
                                    text='',
                                    icon='TRIA_DOWN',
                                    emboss=True,
                                    )
        next_op.coll_index = index
        next_op.options = 'NEXT'

        # last skin button

        last_op = ops_col.operator('skis.skin_jump_in_collection',
                                   text='',
                                   icon='TRIA_DOWN_BAR',
                                   emboss=True
                                   )
        last_op.coll_index = index
        last_op.options = 'LAST'


class SKIS_UL_collection_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):

        # show property

        show_row = layout.row(align=True)
        show_row.prop(item,
                      'show',
                      text='',
                      emboss=True,
                      )
        show_row.scale_x = 0.6

        # index property

        index_row = layout.row()
        index_row.label(text=f'{index + 1}')
        index_row.scale_x = .09

        # to outliner op

        to_outliner_row = layout.row()
        to_outliner_op = to_outliner_row.operator('skis.to_outliner',
                                                  text='',
                                                  icon='ZOOM_SELECTED',
                                                  emboss=True
                                                  )
        to_outliner_op.type = 'COLLECTION'
        to_outliner_op.coll_index = index

        # skin collection property

        skin_coll_row = layout.row()
        skin_coll_row.prop(item,
                           'skin_coll',
                           text='',
                           emboss=True,
                           icon=('NONE'
                                 if item.skin_coll is None or item.skin_coll.color_tag == 'NONE'
                                 else f'COLLECTION_{item.skin_coll.color_tag}'
                                 )
                           )
        skin_coll_row.scale_x = 0.65

        # hide viewport property

        hide_viewport_row = layout.row()
        if item.skin_coll:
            hide_viewport_row.prop(item.skin_coll,
                                   'hide_viewport',
                                   text='',
                                   emboss=False,
                                   )

# skin collection UILIST class


class SKIS_UL_skin_list(bpy.types.UIList):

    index: bpy.props.IntProperty()

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, _index):

        # sort skin in collection

        # if data is context.view_layer.layer_collection.collection:
        #     data = context.view_layer.objects
        #     sort_coll = data.keys().copy()
        # else:
        #     sort_coll = data.all_objects.keys().copy()
        sort_coll = data.all_objects.keys().copy()
        sort_coll.sort(key=str.casefold)

        # skin index in sorted collection

        index = sort_coll.index(item.name)

        # get all parent collections

        parent_collections = [i for i in bpy.data.collections[:] if item.users_collection[0] in i.children_recursive]
        # get all parent collections hide viewport
        parent_colls_hide_viewport = [j.hide_viewport for j in parent_collections]
        # get highest in hierachy collection hide viewport
        is_parent_colls_hide_viewport = False
        for i in parent_colls_hide_viewport:
            if i == True:
                is_parent_colls_hide_viewport = True
                break

        # get collection in use hide viewport
        is_coll_hide_viewport = item.users_collection[0].hide_viewport or is_parent_colls_hide_viewport

        # get skin hide viewport
        is_item_enable = not item.hide_viewport and not is_coll_hide_viewport

        # item prop

        # to active skin op

        to_active_skin_row = layout.row()
        to_active_skin_row.scale_x = .8
        to_active_skin_row.enabled = is_item_enable
        to_active_skin_op = to_active_skin_row.operator('skis.to_active_skin_in_collection',
                                                        text='',
                                                        emboss=False,
                                                        icon=('GHOST_ENABLED'
                                                              if item == use_skin_collection_or_active(int(self.list_id)).skis_active_skin else
                                                              'GHOST_DISABLED'
                                                              )
                                                        )
        to_active_skin_op.skin_name = item.name
        to_active_skin_op.coll_index = int(self.list_id)

        # to outliner op

        to_outliner_row = layout.row()
        to_outliner_row.alert = not is_item_enable
        to_outliner_op = to_outliner_row.operator('skis.to_outliner',
                                                  text='',
                                                  emboss=True,
                                                  icon=f'OUTLINER_OB_{item.type}',
                                                  )
        to_outliner_op.skin_name = item.name
        to_outliner_op.coll_index = int(self.list_id)
        to_outliner_op.type = 'OBJECT'

        # name prop

        name_row = layout.row()
        name_row.prop(item, 'name', text='', emboss=False,)

        # index prop

        index_box = layout.box()
        index_box.enabled = is_item_enable
        index_box.alert = not is_item_enable
        index_box.label(text=f'{index + 1}')
        index_box.scale_x = 0.12
        index_box.scale_y = 0.5

        # hide exclude prop

        hide_exclude_row = layout.row()
        hide_exclude_row.scale_x = .9
        hide_exclude_row.prop(item,
                              'skis_hide_exclude',
                              text='',
                              icon=('FAKE_USER_ON'
                                    if item.skis_hide_exclude == True
                                    else 'FAKE_USER_OFF'
                                    ),
                              emboss=False,
                              )
        hide_exclude_row.prop(item,
                              'hide_viewport',
                              text='',
                              emboss=False
                              )

    def filter_items(self, context, data, property):

        item = getattr(data, property)
        collection_list = bpy.context.scene.skis_skin_collection_list

        flt_item = []

        # if self.filter_name:
        #     flt_item = bpy.types.UI_UL_list.filter_items_by_name(
        #         self.filter_name,
        #         self.bitflag_filter_item,
        #         item,
        #         'name',
        #         reverse=self.use_filter_sort_reverse
        #     )

        use_filter = collection_list[int(self.list_id)].use_flt
        obj_type = collection_list[int(self.list_id)].flt_type

        for i in item:
            if i in bpy.context.view_layer.objects.values():
                if use_filter and i.type == obj_type:
                    flt_item.append(self.bitflag_filter_item)
                elif not use_filter:
                    flt_item.append(self.bitflag_filter_item)
                else:
                    flt_item.append(0)
            else:
                flt_item.append(0)

        order = []
        order = bpy.types.UI_UL_list.sort_items_by_name(item, 'name')

        return flt_item, order
