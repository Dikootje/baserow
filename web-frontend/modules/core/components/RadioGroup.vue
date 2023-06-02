<template>
  <div class="radio-group">
    <Radio
      v-for="option in options"
      :id="option.id"
      :key="option.value"
      :name="name"
      :value="option.value"
      :model-value="modelValue"
      :disabled="option.disabled"
      :loading="option.loading"
      :error="option.error"
      @input="updateModelValue"
    >
      {{ option.label }}
    </Radio>
  </div>
</template>

<script>
import Radio from '@baserow/modules/core/components/Radio.vue'

export default {
  name: 'RadioGroup',
  components: {
    Radio,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: [String, Number, Boolean, Object],
      required: true,
    },
  },
  methods: {
    updateModelValue(value) {
      this.$emit('update:modelValue', value)
    },
  },
}
</script>
