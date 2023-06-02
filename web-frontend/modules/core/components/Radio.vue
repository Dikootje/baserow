<template>
  <div class="radio" :class="classNames" @click="select">
    <div v-if="loading" class="radio__loading"></div>
    <div v-else class="radio__input">
      <input
        :id="id"
        type="radio"
        :name="name"
        :value="value"
        :checked="isSelected"
        :disabled="disabled || loading"
      />
      <label :for="id"></label>
    </div>
    <div class="radio__label">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Radio',
  model: {
    prop: 'modelValue',
    event: 'input',
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number, Boolean, Object],
      required: true,
    },
    modelValue: {
      type: [String, Number, Boolean, Object],
      required: false,
      default: '',
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
    error: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classNames() {
      return {
        'radio--disabled': this.disabled,
        'radio--loading': this.loading,
        'radio--error': this.error,
        selected: this.isSelected,
      }
    },
    isSelected() {
      return this.modelValue === this.value
    },
  },
  methods: {
    select() {
      if (this.disabled || this.loading || this.isSelected) {
        return
      }

      this.$emit('input', this.value)
    },
  },
}
</script>
