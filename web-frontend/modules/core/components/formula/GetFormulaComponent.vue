<template>
  <NodeViewWrapper as="span" class="get-formula-component">
    {{ pathParts.dataProvider }}
    <template v-for="(part, index) in pathParts.parts">
      <i :key="index" class="get-formula-component__caret fas fa-angle-right">
      </i>
      <span :key="index + part">{{ part }}</span>
    </template>
    <a
      class="get-formula-component__remove"
      @click="emitToEditor('remove', node.attrs.id)"
    >
      <i class="fas fa-times"></i>
    </a>
  </NodeViewWrapper>
</template>

<script>
import { NodeViewWrapper } from '@tiptap/vue-2'
import formulaComponent from '@baserow/modules/core/mixins/formulaComponent'
export default {
  name: 'GetFormulaComponent',
  components: {
    NodeViewWrapper,
  },
  mixins: [formulaComponent],
  computed: {
    dataProviderTypeCaptionMapping() {
      // TODO this might become obsolete once jeremies DS MR is merged
      return {
        data_source: this.$t('dataProviderTypes.dataSource'),
        path_param: this.$t('dataProviderTypes.pathParam'),
      }
    },
    path() {
      return this.node.attrs.path
    },
    pathParts() {
      const [dataProviderType, ...parts] = this.path.split('.')

      return {
        dataProvider: this.dataProviderTypeCaptionMapping[dataProviderType],
        parts,
      }
    },
  },
}
</script>
