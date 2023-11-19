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

        layout.label(text='Skin collection list:')

        row = layout.row(align=True)
        col = row.column(align=True)
        col.template_list('SKIS_UL_collection_list',
                          '1',
                          bpy.context.scene,
                          'skis_skin_collection_list',
                          bpy.context.scene,
                          'skis_skin_collection_list_index',
                          )

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


class SKIS_PT_side_panel_skin_list(bpy.types.Panel):
    bl_label = 'Skin management'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SkiS'

    def draw(self, context):

        layout = self.layout

        # hide all non active button

        col = layout.column(align=True)
        col.operator('skis.hide_all_non_active_skin', icon='GROUP_VERTEX')
        col.scale_y = 1.5

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
             icon=('DOWNARROW_HLT'
                   if collection_list[index].collapse
                   else 'RIGHTARROW'
                   ),
             emboss=False,
             )

    # skin collection show hide

    row.prop(collection_list[index],
             'show',
             text='',
             emboss=True
             )

    # skin collection index

    box = row.box()
    box.scale_x = 0.4
    box.scale_y = 0.6
    box.label(text=f'{index + 1}',)
    box.alignment = 'CENTER'

    # set collection button

    col = row.column()
    col.scale_x = 0.7
    op = col.operator('skis.set_skin_collection',
                      text='Set',
                      icon='PINNED'
                      )
    op.index = index

    # skin collection prop

    row.prop(collection_list[index], 'skin_coll', text='',)

    # skin collection hide viewport

    if collection_list[index].skin_coll is not None:
        row.prop(collection_list[index].skin_coll, 'hide_viewport', text='', emboss=False)
    else:
        row.label(icon='RESTRICT_VIEW_ON')

    # skin collection collapse

    if collection_list[index].collapse:

        # skin collection item filter type

        row = layout.row(align=True)

        # box = row.box()
        # box.label(text=f'{len(collection_list[index].skin_coll.all_objects)} skins')
        # box.scale_y = 0.6

        row.prop(collection_list[index],
                 'use_flt',
                 text='Filter',
                 toggle=True,
                 icon='FILTER',
                 )

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
        row.enabled = use_skin_collection_or_active(index).skis_active_skin != None
        op = row.operator('skis.hide_non_active_skin_in_collection',
                          text='',
                          icon='COMMUNITY',
                          emboss=True
                          )
        op.coll_index = index

        # first skin button

        col.separator()

        op = col.operator('skis.to_first_skin_in_collection',
                          text='',
                          icon='ANCHOR_TOP',
                          emboss=True
                          )
        op.coll_index = index

        # prev skin button

        row = col.row()
        row.enabled = use_skin_collection_or_active(index).skis_active_skin != None
        op = row.operator('skis.to_prev_skin_in_collection',
                          text='',
                          icon='TRIA_UP_BAR',
                          emboss=True
                          )
        op.coll_index = index

        # next skin button

        row = col.row()
        row.enabled = use_skin_collection_or_active(index).skis_active_skin != None
        op = row.operator('skis.to_next_skin_in_collection',
                          text='',
                          icon='TRIA_DOWN_BAR',
                          emboss=True,
                          )
        op.coll_index = index

        # last skin button button

        op = col.operator('skis.to_last_skin_in_collection',
                          text='',
                          icon='ANCHOR_BOTTOM',
                          emboss=True
                          )
        op.coll_index = index


class SKIS_UL_collection_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):

        layout.scale_y = 1.2

        row = layout.row(align=True)
        row.prop(item,
                 'show',
                 text='',
                 emboss=True,
                 )

        row = layout.row()
        row.label(text=f'{index + 1}')
        row.scale_x = .08

        row = row.row()
        row.scale_x = 1.2
        op = row.operator('skis.set_skin_collection',
                          text='',
                          icon='PINNED',
                          emboss=True,
                          )
        op.index = index

        row = layout.row()
        row.prop(item,
                 'skin_coll',
                 text='',
                 emboss=True,
                 )
        row.scale_x = 0.7
        row.alignment = 'LEFT'

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
        row.scale_x = .9
        row.prop(item,
                 'hide_viewport',
                 text='',
                 emboss=False
                 )

        row = layout.row()
        row.scale_x = .8
        row.alert = True
        row.enabled = not item.hide_viewport
        row.label(icon=f'OUTLINER_OB_{item.type}')

        row = layout.row()
        row.enabled = not item.hide_viewport
        row.label(text=f'{item.name}')

        box = layout.box()
        box.enabled = not item.hide_viewport
        box.label(text=f'{index + 1}')
        box.scale_x = 0.08
        box.scale_y = 0.5

        # operator

        row = layout.row()
        row.scale_x = .8
        row.enabled = not item.hide_viewport
        op = row.operator('skis.to_active_skin_in_collection', text='', emboss=False,
                          icon=('OUTLINER_OB_ARMATURE'
                                if item == use_skin_collection_or_active(int(self.list_id)).skis_active_skin else
                                'DOT'
                                )
                          )
        op.skin_name = item.name
        op.coll_index = int(self.list_id)

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
