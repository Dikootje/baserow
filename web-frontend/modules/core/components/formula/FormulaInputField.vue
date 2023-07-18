<template>
  <EditorContent :editor="editor" @remove="remove" />
</template>

<script>
import { Editor, EditorContent, generateHTML } from '@tiptap/vue-2'
import { Placeholder } from '@tiptap/extension-placeholder'
import { Text } from '@tiptap/extension-text'
import { Document } from '@tiptap/extension-document'
import { StarterKit } from '@tiptap/starter-kit'
import _ from 'lodash'
import { Paragraph } from '@tiptap/extension-paragraph'
import { NoNewLineExt } from '@baserow/modules/core/components/tiptap/extensions/noNewLine'
import { GetFormulaComponentExt } from '@baserow/modules/core/components/tiptap/extensions/getFormulaComponent'
import { uuid } from '@baserow/modules/core/utils/string'

export default {
  name: 'FormulaInputField',
  components: {
    EditorContent,
  },
  props: {
    value: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      editor: null,
      content: null,
    }
  },
  computed: {
    placeHolderExt() {
      return Placeholder.configure({
        placeholder: this.placeholder,
      })
    },
    extensions() {
      return [
        StarterKit,
        Document,
        GetFormulaComponentExt,
        Text,
        Paragraph.configure({
          HTMLAttributes: { class: 'formula-input-field__paragraph' },
        }),
        NoNewLineExt,
        this.placeHolderExt,
      ]
    },
    htmlContent() {
      return generateHTML(this.content, this.extensions)
    },
  },
  watch: {
    value(value) {
      if (!_.isEqual(value, this.toFormula(this.editor.getJSON()))) {
        // this.editor.commands.setContent(value, this.toContent(value))
      }
    },
    content: {
      handler() {
        this.editor?.commands.setContent(this.htmlContent, true)
      },
      deep: true,
    },
  },
  mounted() {
    this.content = this.toContent(this.value)
    this.editor = new Editor({
      content: this.htmlContent,
      editable: true,
      onUpdate: this.onUpdate,
      extensions: this.extensions,
      editorProps: {
        attributes: {
          class: 'formula_input_field__editor',
        },
      },
    })
  },
  beforeDestroy() {
    this.editor?.destroy()
  },
  methods: {
    remove(id) {
      const deleteObjectById = (obj, id) => {
        if (obj?.attrs?.id === id) {
          return true
        }

        if (_.isObject(obj)) {
          Object.keys(obj).forEach((key) => {
            if (deleteObjectById(obj[key], id)) {
              if (_.isArray(obj)) {
                obj.splice(key, 1)
              } else {
                delete obj[key]
              }
              return true
            }
          })
        }
      }

      deleteObjectById(this.content, id)
    },
    onUpdate() {
      this.$emit('input', this.toFormula(this.content))
    },
    toContent(formula) {
      return {
        type: 'doc',
        content: [
          {
            type: 'text',
            text: 'hello',
          },
          {
            type: 'get-formula-component',
            attrs: {
              id: uuid(),
              path: 'data_source.test.name',
            },
          },
        ],
      }
    },
    toFormula(content) {
      return this.editor.getText()
    },
  },
}
</script>
