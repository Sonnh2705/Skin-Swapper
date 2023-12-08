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
        col.operator('skis.add_skin_collection_to_list',
                     text='',
                     icon='ADD',
                     emboss=True
                     )
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
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='ANCHOR_TOP',
                          emboss=True
                          )
        op.direction = 'FIRST'
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_UP',
                          emboss=True
                          )
        op.direction = 'UP'
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='TRIA_DOWN',
                          emboss=True
                          )
        op.direction = 'DOWN'
        op = col.operator('skis.move_skin_collection_in_list',
                          text='',
                          icon='ANCHOR_BOTTOM',
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

        for index in range(0, len(bpy.context.scene.skis_skin_collection_list)):
            if bpy.context.scene.skis_skin_collection_list[index].show:
                skin_list_side_panel(layout, index)


# skin collection panel func


def skin_list_side_panel(layout, index):

    collection_list = bpy.context.scene.skis_skin_collection_list

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
    op = col.operator('skis.set_skin_collection',
                      text='Set',
                      icon='PINNED'
                      )
    col.scale_x = 0.5
    op.index = index

    op2 = row.operator('skis.to_outliner',
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

    if collection_list[index].skin_coll is not None:
        row.prop(collection_list[index].skin_coll,
                 'hide_viewport', text='', emboss=False)
    else:
        row.label(icon='RESTRICT_VIEW_ON')

    # under collapse line

    if not collection_list[index].collapse and not collection_list[index].skin_coll.hide_viewport:

        # get filtered skins

        if collection_list[index].use_flt:
            filtered_obj = [
                x for x in collection_list[index].skin_coll.all_objects if x.type == collection_list[index].flt_type
            ]
        else:
            filtered_obj = [
                x for x in collection_list[index].skin_coll.all_objects
            ]

        row = layout.row(align=True)

        # skin count

        box = row.box()
        box.label(text=f'{len(filtered_obj)} skins')
        box.scale_y = 0.6
        box.scale_x = 0.7

        # skin collection item filter type
        row2 = row.row()
        row2.prop(collection_list[index],
                  'use_flt',
                  text='Filter',
                  toggle=True,
                  icon='FILTER',
                  )
        row2.scale_x = 0.6

        col = row.column()
        col.prop(collection_list[index],
                 'flt_type',
                 text='',
                 )
        col.enabled = collection_list[index].use_flt

        # skin collection list

        row = layout.row(align=True)
        row.template_list('SKIS_UL_skin_list',
                          f'{index}',
                          use_skin_collection_or_active(index),
                          'all_objects',
                          use_skin_collection_or_active(index),
                          'skis_list_index',
                          )
        row.separator(factor=0.5)

        # hide non active button

        col = row.column(align=True)
        row = col.row()
        row.enabled = use_skin_collection_or_active(
            index).skis_active_skin != None
        op = row.operator('skis.hide_non_active_skin_in_collection',
                          text='',
                          icon='COMMUNITY',
                          emboss=True
                          )
        op.coll_index = index

        # first skin button

        col.separator()

        op = col.operator('skis.skin_jump_in_collection',
                          text='',
                          icon='ANCHOR_TOP',
                          emboss=True
                          )
        op.coll_index = index
        op.options = 'FIRST'

        # prev skin button

        row = col.row()
        row.enabled = use_skin_collection_or_active(index).skis_active_skin != None
        op = row.operator('skis.skin_jump_in_collection',
                          text='',
                          icon='TRIA_UP_BAR',
                          emboss=True
                          )
        op.coll_index = index
        op.options = 'PREV'

        # next skin button

        row = col.row()
        row.enabled = use_skin_collection_or_active(index).skis_active_skin != None
        op = row.operator('skis.skin_jump_in_collection',
                          text='',
                          icon='TRIA_DOWN_BAR',
                          emboss=True,
                          )
        op.coll_index = index
        op.options = 'NEXT'

        # last skin button

        op = col.operator('skis.skin_jump_in_collection',
                          text='',
                          icon='ANCHOR_BOTTOM',
                          emboss=True
                          )
        op.coll_index = index
        op.options = 'LAST'


class SKIS_UL_collection_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):

        # show property

        row = layout.row(align=True)
        row.prop(item,
                 'show',
                 text='',
                 emboss=True,
                 )
        row.scale_x = 0.6

        # index property

        row = layout.row()
        row.label(text=f'{index + 1}')
        row.scale_x = .09

        row = layout.row()
        op = row.operator('skis.to_outliner',
                          text='',
                          icon='ZOOM_SELECTED',
                          emboss=True
                          )
        op.type = 'COLLECTION'
        op.coll_index = index

        # set active collection operator

        # row = layout.row(align=True)
        # row.scale_x = 1.1
        # op = row.operator('skis.set_skin_collection',
        #                   text='',
        #                   icon='PINNED',
        #                   emboss=True,
        #                   )
        # op.index = index

        # skin collection property

        row = layout.row()
        row.prop(item,
                 'skin_coll',
                 text='',
                 emboss=True,
                 icon=('NONE'
                       if item.skin_coll is None or item.skin_coll.color_tag == 'NONE'
                       else f'COLLECTION_{item.skin_coll.color_tag}'
                       )
                 )
        row.scale_x = 0.65
        row.alignment = 'LEFT'

        # hide viewport property

        row = layout.row()
        if item.skin_coll is not None:
            row.prop(item.skin_coll,
                     'hide_viewport',
                     text='',
                     emboss=False,
                     )
        else:
            row.label(icon='RESTRICT_VIEW_ON')

# skin collection UILIST class


class SKIS_UL_skin_list(bpy.types.UIList):

    index: bpy.props.IntProperty()

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        # sort skin in collection

        if data is context.view_layer.layer_collection.collection:
            data = context.view_layer.objects
            sort_coll = data.keys().copy()
        else:
            sort_coll = data.all_objects.keys().copy()
        sort_coll.sort(key=str.casefold)

        index = sort_coll.index(item.name)

        # item prop

        row = layout.row()
        row.scale_x = .8
        row.enabled = not item.hide_viewport
        op = row.operator('skis.to_active_skin_in_collection',
                          text='',
                          emboss=False,
                          icon=('GHOST_ENABLED'
                                if item == use_skin_collection_or_active(int(self.list_id)).skis_active_skin else
                                'GHOST_DISABLED'
                                )
                          )
        op.skin_name = item.name
        op.coll_index = int(self.list_id)

        row = layout.row()
        # row.scale_x = .8
        row.alert = True
        row.enabled = not item.hide_viewport
        # row.label(icon=f'OUTLINER_OB_{item.type}')
        op = row.operator('skis.to_outliner',
                          text='',
                          emboss=True,
                          icon=f'OUTLINER_OB_{item.type}',
                          )
        op.skin_name = item.name
        op.coll_index = int(self.list_id)
        op.type = 'OBJECT'

        row = layout.row()
        row.enabled = not item.hide_viewport
        row.prop(item, 'name', text='', emboss=False,)

        box = layout.box()
        box.enabled = not item.hide_viewport
        box.label(text=f'{index + 1}')
        box.scale_x = 0.12
        box.scale_y = 0.5

        row = layout.row()
        row.scale_x = .9
        row.prop(item,
                 'skis_hide_exclude',
                 text='',
                 icon=('FAKE_USER_ON'
                       if item.skis_hide_exclude == True
                       else 'FAKE_USER_OFF'
                       ),
                 emboss=False,
                 )
        row.prop(item,
                 'hide_viewport',
                 text='',
                 emboss=False
                 )

        # operator

    def filter_items(self, context, data, property):

        item = getattr(data, property)
        collection_list = bpy.context.scene.skis_skin_collection_list

        flt_item = []
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
