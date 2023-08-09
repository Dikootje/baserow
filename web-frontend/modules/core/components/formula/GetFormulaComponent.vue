<template>
  <NodeViewWrapper
    as="span"
    class="get-formula-component"
    :class="{ 'get-formula-component--selected': selected }"
  >
    {{ pathParts.dataProvider }}
    <template v-for="(part, index) in pathParts.parts">
      <i :key="index" class="get-formula-component__caret fas fa-angle-right">
      </i>
      <span :key="index + part">{{ part }}</span>
    </template>
    <a class="get-formula-component__remove" @click="deleteNode">
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
    path() {
      return this.node.attrs.path
    },
    pathParts() {
      const [dataProvider, ...parts] = this.path.split('.')
      const dataProviderType = this.$registry.get(
        'builderDataProvider',
        dataProvider
      )

      return {
        dataProvider: dataProviderType.name,
        parts,
      }
    },
  },
}
</script>
