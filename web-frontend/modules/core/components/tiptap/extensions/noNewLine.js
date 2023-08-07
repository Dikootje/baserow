import { Extension } from '@tiptap/core'
import { Plugin, PluginKey } from '@tiptap/pm/state'

export const NoNewLineExt = Extension.create({
  name: 'no_new_line',

  addProseMirrorPlugins() {
    return [
      new Plugin({
        key: new PluginKey('eventHandler'),
        props: {
          handleKeyDown: (view, event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              return true
            }
          },
        },
      }),
    ]
  },
})
