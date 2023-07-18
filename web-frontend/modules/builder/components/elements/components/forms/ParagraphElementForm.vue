<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormElement class="control">
      <label class="control__label">
        {{ $t('paragraphElementForm.textTitle') }}
      </label>
      <div class="control__elements">
        <FormulaInputField
          v-model="values.value"
          :placeholder="$t('elementForms.textInputPlaceholder')"
          class="input paragraph-element-form__value"
        ></FormulaInputField>
      </div>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import FormulaInputField from '@baserow/modules/core/components/formula/FormulaInputField'

export default {
  name: 'ParagraphElementForm',
  components: { FormulaInputField },
  mixins: [form],
  props: {},
  data() {
    return {
      values: {
        value: '',
      },
    }
  },
}
</script>
