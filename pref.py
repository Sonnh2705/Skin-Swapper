import bpy


def prefs():

    return bpy.context.preferences.addons[__package__].preferences


class SKIS_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_skin_index: bpy.props.BoolProperty(default=False)

    def draw(self, context):

        layout = self.layout

        row = layout.row(align=True)

        col = row.column()
        col.alignment = 'LEFT'
        col.label(text='Show skin index in list:')

        col = row.column()
        col.alignment = 'RIGHT'
        col.prop(prefs(),
                 'show_skin_index',
                 text=''
                 )
