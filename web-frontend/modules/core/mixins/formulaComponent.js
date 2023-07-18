import { nodeViewProps } from '@tiptap/vue-2'

export default {
  props: nodeViewProps,
  methods: {
    emit(...args) {
      this.$parent.$emit(...args)
    },
  },
}
