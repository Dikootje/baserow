<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormElement class="control">
      <label class="control__label">
        {{ $t('paragraphElementForm.textTitle') }}
      </label>
      <div class="control__elements">
        <textarea
          v-model="values.value"
          :placeholder="$t('elementForms.textInputPlaceholder')"
          class="input paragraph-element-form__value"
          type="text"
          rows="12"
        ></textarea>
      </div>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'ParagraphElementForm',
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
