<template>
  <form @submit.prevent>
    <StyleBoxForm v-model="topStyle" :label="$t('styleForm.boxTop')" />
    <StyleBoxForm v-model="bottomStyle" :label="$t('styleForm.boxBottom')" />
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import StyleBoxForm from '@baserow/modules/builder/components/page/sidePanels/StyleBoxForm'

export default {
  components: { StyleBoxForm },
  mixins: [form],
  props: {},
  data() {
    return {
      allowedValues: ['style_padding_top', 'style_padding_bottom'],
      values: {
        style_padding_top: 0,
        style_padding_bottom: 0,
      },
    }
  },
  computed: {
    topStyle: {
      get() {
        return { padding: this.getDefaultValues().style_padding_top }
      },
      set(newValue) {
        if (newValue.padding !== undefined) {
          this.values.style_padding_top = newValue.padding
        }
      },
    },
    bottomStyle: {
      get() {
        return { padding: this.getDefaultValues().style_padding_bottom }
      },
      set(newValue) {
        if (newValue.padding !== undefined) {
          this.values.style_padding_bottom = newValue.padding
        }
      },
    },
  },
}
</script>
