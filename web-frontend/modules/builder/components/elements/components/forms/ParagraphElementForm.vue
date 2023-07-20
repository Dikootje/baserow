<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormulaFormInput
      v-model="values.value"
      :label="$t('paragraphElementForm.textTitle')"
      :placeholder="$t('elementForms.textInputPlaceholder')"
      :error="
        !$v.values.value.validFormula ? $t('elementForms.invalidFormula') : ''
      "
    />
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

import FormulaFormInput from '@baserow/modules/core/components/formula/FormulaFormInput'
import { isValidFormula } from '@baserow/formula'

export default {
  name: 'ParagraphElementForm',
  components: { FormulaFormInput },
  mixins: [form],
  props: {},
  data() {
    return {
      values: {
        value: '',
      },
    }
  },
  validations() {
    return {
      values: {
        value: { validFormula: isValidFormula },
      },
    }
  },
}
</script>
