import bpy


def prefs():

    return bpy.context.preferences.addons[__package__].preferences


class SKIS_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    skis_skin_collection_count: bpy.props.IntProperty(
        name='Skin Collection Count',
        default=1,
        min=1,
        max=6
    )

    def draw(self, context):

        layout = self.layout

        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'LEFT'
        col.label(text='Skin collection count:')

        col = row.column()
        col.alignment = 'RIGHT'
        col.prop(prefs(),
                 'skis_skin_collection_count',
                 slider=True
                 )
