<template>
  <div class="switch" :class="classNames" @click="toggle(checked)">
    <div class="switch__label">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SwitchInput',
  props: {
    checked: {
      type: Boolean,
      required: false,
      default: false,
    },
    small: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classNames() {
      return {
        'switch--small': this.small,
        'switch--disabled': this.disabled,
        active: this.checked === true,
      }
    },
  },
  methods: {
    toggle(value) {
      if (this.disabled) {
        return
      }
      this.$emit('input', !value)
    },
  },
}
</script>
