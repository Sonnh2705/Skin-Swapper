import bpy


def prefs():

    return bpy.context.preferences.addons[__package__].preferences


class SKIS_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    is_skin_index_show: bpy.props.BoolProperty(default=False)
    is_advance: bpy.props.BoolProperty(default=False)

    def draw(self, context):

        layout = self.layout

        row = layout.row(align=True)

        col = row.column()
        col.alignment = 'LEFT'
        col.label(text='Show skin index in list:')
        col.label(text='Advance mode:')

        col = row.column()
        col.alignment = 'RIGHT'
        col.prop(prefs(),
                 'is_skin_index_show',
                 text=''
                 )
        col.prop(prefs(),
                 'is_advance',
                 text=''
                 )
