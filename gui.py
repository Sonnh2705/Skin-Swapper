import bpy

from .ops import skin_collection_from_index, use_skin_collection_or_active
from .pref import prefs


# side panel class


class SKIS_PT_side_panel(bpy.types.Panel):
    bl_label = 'Skin Switcher'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SkiS'

    def draw(self, context):

        layout = self.layout

        layout.prop(prefs(), 'skis_skin_collection_count')

        # collection visible prop

        row = layout.row(align=True)
        for index in range(1, prefs().skis_skin_collection_count + 1):
            row.prop(skin_collection_from_index(index),
                     'show',
                     text=f'{index}',
                     toggle=True,
                     icon=('HIDE_OFF'
                           if skin_collection_from_index(index).show
                           else
                           'HIDE_ON'
                           )
                     )

        # hide all non active button

        col = layout.column(align=True)
        col.separator()
        col.operator('skis.hide_all_non_active_skin', icon='GROUP_VERTEX')
        col.scale_y = 1.5
        col.separator()

        # skin collections

        for index in range(1, prefs().skis_skin_collection_count + 1):
            if skin_collection_from_index(index).show:
                skin_list_side_panel(layout, index)


# skin collection panel func


def skin_list_side_panel(layout, index):

    row = layout.row(align=True)

    op = row.operator('skis.set_skin_collection',
                      text='Set skin collection',
                      icon='PINNED'
                      )
    op.index = index
    box = row.box()
    box.scale_x = 0.25
    box.scale_y = 0.6
    box.label(text=f'{index}')

    # skin collection prop

    row.prop(skin_collection_from_index(index), 'skin_coll', text='')

    # skin collection item filter type

    row = layout.row(align=True)
    row.prop(skin_collection_from_index(index),
             'use_flt',
             text='Filter object',
             toggle=True,
             icon='FILTER',
             )

    col = row.column()
    col.prop(skin_collection_from_index(index),
             'flt_type',
             text='',
             )
    col.enabled = skin_collection_from_index(index).use_flt

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
        row.prop(item, 'hide_viewport', text='', emboss=False)

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

        flt_item = []
        use_filter = skin_collection_from_index(int(self.list_id)).use_flt
        obj_type = skin_collection_from_index(int(self.list_id)).flt_type

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
