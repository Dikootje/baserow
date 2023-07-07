<template>
  <form @submit.prevent>
    <FormInput
      v-for="prop in styleBoxProperties"
      :key="prop.name"
      v-model="values[prop.name]"
      :label="prop.label"
      type="number"
      :error="$v.values[prop.name].$error ? $t('styleForm.paddingError') : ''"
      @blur="$v.values[prop.name].$touch()"
    />
  </form>
</template>

<script>
import { required, integer, between } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'StyleBoxForm',
  mixins: [form],
  props: {
    styleBoxProperties: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: this.styleBoxProperties.map(({ name }) => name),
      values: Object.fromEntries(
        this.styleBoxProperties.map(({ name }) => {
          return [name, 0]
        })
      ),
    }
  },
  validations() {
    return {
      values: Object.fromEntries(
        this.styleBoxProperties.map(({ name }) => {
          return [
            name,
            {
              required,
              integer,
              between: between(0, 200),
            },
          ]
        })
      ),
    }
  },
}
</script>
