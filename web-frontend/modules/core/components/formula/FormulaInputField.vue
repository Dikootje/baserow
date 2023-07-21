<template>
  <EditorContent :class="classes" :editor="editor" @remove="remove" />
</template>

<script>
import { Editor, EditorContent, generateHTML, Node } from '@tiptap/vue-2'
import { Placeholder } from '@tiptap/extension-placeholder'
import { Document } from '@tiptap/extension-document'
import { Paragraph } from '@tiptap/extension-paragraph'
import { Text } from '@tiptap/extension-text'
import _ from 'lodash'
import { NoNewLineExt } from '@baserow/modules/core/components/tiptap/extensions/noNewLine'
import parseBaserowFormula from '@baserow/formula/parser/parser'
import { ToTipTapVisitor } from '@baserow/modules/core/formula/toTipTapVisitor'
import { RuntimeFunctionCollection } from '@baserow/modules/core/functionCollection'
import { FromTipTapVisitor } from '@baserow/modules/core/formula/fromTipTapVisitor'
import { mergeAttributes } from '@tiptap/core'

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
      isFocused: false,
    }
  },
  computed: {
    classes() {
      return {
        'formula_input_field--focused': this.isFocused,
      }
    },
    placeHolderExt() {
      return Placeholder.configure({
        placeholder: this.placeholder,
      })
    },
    formulaComponents() {
      return Object.values(this.$registry.getAll('runtime_formula_type'))
        .map((type) => type.formulaComponent)
        .filter((component) => component !== null)
    },
    extensions() {
      const TextNode = Text.extend({ inline: true })
      const ParagraphNode = Paragraph.configure({
        HTMLAttributes: { class: 'formula-input-field__paragraph' },
      })

      return [
        Document,
        ParagraphNode,
        TextNode,
        NoNewLineExt,
        this.placeHolderExt,
        ...this.formulaComponents,
      ]
    },
    htmlContent() {
      return generateHTML(this.content, this.extensions)
    },
    internalContent() {
      // The content of the editor is stored in a nested structure. The first element
      // is a wrapper paragraph that we can safely ignore.
      const paragraph = this.editor.getJSON().content[0]
      return paragraph.content
    },
  },
  watch: {
    value(value) {
      if (!_.isEqual(value, this.toFormula(this.content.content))) {
        this.content = this.toContent(value)
      }
    },
    content: {
      handler() {
        this.editor?.commands.setContent(this.htmlContent, false, {
          preserveWhitespace: 'full',
        })
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
      onFocus: this.onFocus,
      onBlur: this.onBlur,
      extensions: this.extensions,
      editorProps: {
        attributes: {
          class: 'formula_input_field__editor',
        },
      },
      parseOptions: {
        preserveWhitespace: 'full',
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
      this.$emit('input', this.toFormula(this.internalContent))
    },
    onFocus() {
      this.isFocused = true
    },
    onBlur() {
      this.isFocused = false
    },
    toContent(formula) {
      if (_.isEmpty(formula)) {
        return {
          type: 'doc',
          content: [
            {
              type: 'paragraph',
              content: [],
            },
          ],
        }
      }

      const tree = parseBaserowFormula(formula)
      const functionCollection = new RuntimeFunctionCollection(this.$registry)
      const content = new ToTipTapVisitor(functionCollection).visit(tree)

      return {
        type: 'doc',
        content: [
          {
            type: 'paragraph',
            content,
          },
        ],
      }
    },
    toFormula(content) {
      const functionCollection = new RuntimeFunctionCollection(this.$registry)
      return new FromTipTapVisitor(functionCollection).visit(content || [])
    },
  },
}
</script>
