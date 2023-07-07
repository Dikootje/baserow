<template>
  <StyleForm
    :key="element.id"
    ref="panelForm"
    :style-box-properties="[
      {
        name: 'style_padding_top',
        label: $t('styleSidePanel.paddingTop'),
      },
      {
        name: 'style_padding_bottom',
        label: $t('styleSidePanel.paddingBottom'),
      },
    ]"
    :default-values="element"
    @values-changed="onChange($event)"
  />
</template>

<script>
import elementSidePanel from '@baserow/modules/builder/mixins/elementSidePanel'
import StyleForm from '@baserow/modules/builder/components/page/sidePanels/StyleForm.vue'

export default {
  name: 'StyleSidePanel',
  components: { StyleForm },
  mixins: [elementSidePanel],
}
</script>
