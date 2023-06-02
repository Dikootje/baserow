<template>
  <div class="badge" :class="classes">
    <i v-if="indicator" class="badge__indicator"></i>
    <slot />
  </div>
</template>

<script>
export default {
  name: 'Badge',
  props: {
    color: {
      type: String,
      required: false,
      default: 'cyan',
      validator: function (value) {
        return [
          'cyan',
          'green',
          'yellow',
          'red',
          'magenta',
          'purple',
          'neutral',
        ].includes(value)
      },
    },
    indicator: {
      type: Boolean,
      required: false,
      default: false,
    },
    rounded: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String,
      required: false,
      default: 'regular',
      validator: function (value) {
        return ['regular', 'small', 'large'].includes(value)
      },
    },
  },
  computed: {
    classes() {
      const classObj = {
        [`badge--${this.color}`]: this.color,
        [`badge--${this.size}`]: this.size,
        [`badge--rounded`]: this.rounded,
      }
      return classObj
    },
  },
}
</script>
