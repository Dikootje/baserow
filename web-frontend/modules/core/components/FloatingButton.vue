<template>
  <button
    class="floating-button"
    :class="classes"
    :disabled="disabled"
    v-on="$listeners"
  >
    <i
      v-if="!loading"
      class="floating-button__icon"
      :class="`iconoir-${icon}`"
    />
  </button>
</template>

<script>
export default {
  props: {
    type: {
      required: false,
      type: String,
      default: 'primary',
      validator: function (value) {
        return ['primary', 'secondary'].includes(value)
      },
    },
    icon: {
      required: true,
      type: String,
      default: '',
    },
    loading: {
      required: false,
      type: Boolean,
      default: false,
    },
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
    active: {
      required: false,
      type: Boolean,
      default: false,
    },
    position: {
      required: false,
      type: String,
      default: 'relative',
      validator: function (value) {
        return ['relative', 'fixed'].includes(value)
      },
    },
  },
  computed: {
    classes() {
      const classObj = {
        'floating-button--loading': this.loading,
        'floating-button--fixed': this.position === 'fixed',
        [`floating-button--${this.type}`]: this.type,
        disabled: this.disabled,
        active: this.active,
      }
      return classObj
    },
  },
}
</script>
