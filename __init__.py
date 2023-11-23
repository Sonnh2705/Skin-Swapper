# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from .ops import (SKIS_OP_add_skin_collection_to_list,
                  SKIS_OP_remove_skin_collection_in_list,
                  SKIS_OP_skin_collection_batch_setting,
                  SKIS_OP_set_skin_collection,
                  SKIS_OP_move_skin_collection_in_list,
                  SKIS_OP_to_active_skin_in_collection,
                  SKIS_OP_hide_non_active_skin_in_collection,
                  SKIS_OP_hide_all_non_active_skin,
                  SKIS_OP_to_next_skin_in_collection,
                  SKIS_OP_to_prev_skin_in_collection,
                  SKIS_OP_to_first_skin_in_collection,
                  SKIS_OP_to_last_skin_in_collection,
                  )
from .gui import (SKIS_PT_side_panel_collection_list,
                  SKIS_PT_side_panel_skin_list,
                  SKIS_UL_skin_list, SKIS_UL_collection_list
                  )
from .pref import SKIS_preferences

bl_info = {
    "name": "Skin swapper",
    "author": "SonNH",
    "description": "Tools for managing multiple mesh and armature as skin for game",
    "blender": (3, 3, 0),
    "version": (1, 0, 0),
    "location": "Sidebar -> SkiS",
    "category": "3D View"
}


def filter_use_match_collection_color(self, context):

    print(self)
    if self.use_flt:
        match self.flt_type:
            case 'ARMATURE':
                self.skin_coll.color_tag = 'COLOR_01'
            case 'MESH':
                self.skin_coll.color_tag = 'COLOR_05'
            case 'CURVE':
                self.skin_coll.color_tag = 'COLOR_06'
    else:
        self.skin_coll.color_tag = 'NONE'


class SKIS_PG_skin_collection(bpy.types.PropertyGroup):

    skin_coll: bpy.props.PointerProperty(name='Skin collection',
                                         type=bpy.types.Collection,
                                         )
    collapse: bpy.props.BoolProperty(name='Skin collection collapse', default=False)
    show: bpy.props.BoolProperty(name='Skin collection visible', default=True)
    use_flt: bpy.props.BoolProperty(name='Filter item in collection',
                                    default=False,
                                    update=filter_use_match_collection_color
                                    )
    flt_type: bpy.props.EnumProperty(name='Filter object by type',
                                     items=[
                                         ('MESH', 'Skin (Mesh)', 'Filter items by mesh'),
                                         ('ARMATURE', 'Skeleton (Armature)', 'Filter items by armature'),
                                         ('CURVE', 'Curve', 'Filter items by curve')
                                     ],
                                     update=filter_use_match_collection_color,
                                     )


classes = (SKIS_PG_skin_collection,
           SKIS_OP_add_skin_collection_to_list,
           SKIS_OP_remove_skin_collection_in_list,
           SKIS_OP_set_skin_collection,
           SKIS_OP_skin_collection_batch_setting,
           SKIS_OP_move_skin_collection_in_list,
           SKIS_OP_to_active_skin_in_collection,
           SKIS_OP_hide_non_active_skin_in_collection,
           SKIS_OP_hide_all_non_active_skin,
           SKIS_OP_to_next_skin_in_collection,
           SKIS_OP_to_prev_skin_in_collection,
           SKIS_OP_to_first_skin_in_collection,
           SKIS_OP_to_last_skin_in_collection,
           SKIS_PT_side_panel_collection_list,
           SKIS_PT_side_panel_skin_list,
           SKIS_UL_skin_list,
           SKIS_UL_collection_list,
           SKIS_preferences,
           )


def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.skis_skin_collection_list = bpy.props.CollectionProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_collection_list_index = bpy.props.IntProperty(
        default=0
    )
    bpy.types.Collection.skis_list_index = bpy.props.IntProperty(
        default=0
    )
    bpy.types.Collection.skis_active_skin = bpy.props.PointerProperty(
        type=bpy.types.Object
    )


def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.skis_skin_collection_list
    del bpy.types.Scene.skis_skin_collection_list_index
    del bpy.types.Collection.skis_list_index
    del bpy.types.Collection.skis_active_skin
