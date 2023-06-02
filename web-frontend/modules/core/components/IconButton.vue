<template>
  <button
    class="icon-button"
    :class="classes"
    :disabled="disabled"
    v-on="$listeners"
  >
    <i v-if="!loading" class="icon-button__icon" :class="`iconoir-${icon}`" />
  </button>
</template>

<script>
export default {
  props: {
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
  },
  computed: {
    classes() {
      const classObj = {
        'icon-button--loading': this.loading,
        disabled: this.disabled,
        active: this.active,
      }
      return classObj
    },
  },
}
</script>
