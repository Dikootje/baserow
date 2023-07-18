import { Node, VueNodeViewRenderer } from '@tiptap/vue-2'
import GetFormulaComponent from '@baserow/modules/core/components/formula/GetFormulaComponent'
import { mergeAttributes } from '@tiptap/core'

export const GetFormulaComponentExt = Node.create({
  name: 'get-formula-component',
  group: 'inline',
  inline: true,
  addNodeView() {
    return VueNodeViewRenderer(GetFormulaComponent)
  },
  addAttributes() {
    return {
      id: {
        default: '',
      },
      path: {
        default: '',
      },
    }
  },
  parseHTML() {
    return [
      {
        tag: 'get-formula-component',
      },
    ]
  },
  renderHTML({ HTMLAttributes }) {
    return ['get-formula-component', mergeAttributes(HTMLAttributes)]
  },
})
