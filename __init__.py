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

from .ops import (SKIS_OP_set_skin_collection, SKIS_OP_to_active_skin_in_collection,
                  SKIS_OP_hide_non_active_skin_in_collection, SKIS_OP_hide_all_non_active_skin,
                  SKIS_OP_to_next_skin_in_collection, SKIS_OP_to_prev_skin_in_collection,
                  SKIS_OP_to_first_skin_in_collection, SKIS_OP_to_last_skin_in_collection,
                  )
from .gui import SKIS_PT_side_panel, SKIS_UL_skin_list
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


class SKIS_PG_skin_collection(bpy.types.PropertyGroup):

    skin_coll: bpy.props.PointerProperty(name='Skin collection', type=bpy.types.Collection)
    collapse: bpy.props.BoolProperty(name='Skin collection collapse', default=True)
    show: bpy.props.BoolProperty(name='Skin collection visible', default=True)
    use_flt: bpy.props.BoolProperty(name='Filter item in collection', default=False)
    flt_type: bpy.props.EnumProperty(
        name='Filter object by type',
        items=[('MESH', 'Skin (Mesh)', 'Filter items by mesh'),
               ('ARMATURE', 'Skeleton (Armature)', 'Filter items by armature'),
               ('CURVE', 'Curve', 'Filter items by curve')
               ]
    )


classes = (SKIS_PG_skin_collection,
           SKIS_OP_set_skin_collection,
           SKIS_OP_to_active_skin_in_collection,
           SKIS_OP_hide_non_active_skin_in_collection,
           SKIS_OP_hide_all_non_active_skin,
           SKIS_OP_to_next_skin_in_collection,
           SKIS_OP_to_prev_skin_in_collection,
           SKIS_OP_to_first_skin_in_collection,
           SKIS_OP_to_last_skin_in_collection,
           SKIS_PT_side_panel,
           SKIS_UL_skin_list,
           SKIS_preferences,
           )


def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Collection.skis_list_index = bpy.props.IntProperty(
        default=0
    )
    bpy.types.Collection.skis_active_skin = bpy.props.PointerProperty(
        type=bpy.types.Object
    )
    bpy.types.Scene.skis_skin_coll_1 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_2 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_3 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_4 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_5 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_6 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_7 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_8 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_9 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_10 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_11 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )
    bpy.types.Scene.skis_skin_coll_12 = bpy.props.PointerProperty(
        type=SKIS_PG_skin_collection
    )

def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Collection.skis_list_index
    del bpy.types.Collection.skis_active_skin
    del bpy.types.Scene.skis_skin_coll_1
    del bpy.types.Scene.skis_skin_coll_2
    del bpy.types.Scene.skis_skin_coll_3
    del bpy.types.Scene.skis_skin_coll_4
    del bpy.types.Scene.skis_skin_coll_5
    del bpy.types.Scene.skis_skin_coll_6
