<template>
  <div
    class="avatar"
    :class="{
      'avatar--rounded': rounded,
      [`avatar--${size}`]: true,
      [`avatar--${color}`]: color,
    }"
  >
    <!-- <i v-if="icon" class="fas" :class="`fa-${icon}`" /> -->
    <img v-if="image" :src="image" class="avatar__image" />
    <span v-if="initials && !image" class="avatar__initials">{{
      initials
    }}</span>
  </div>
</template>

<script>
export default {
  name: 'Avatar',
  props: {
    image: {
      type: String,
      required: false,
      default: null,
    },
    rounded: {
      type: Boolean,
      required: false,
      default: false,
    },
    initials: {
      type: String,
      required: false,
      default: null,
    },
    color: {
      required: false,
      type: String,
      default: 'blue',
      validator: function (value) {
        return [
          'blue',
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
    size: {
      type: String,
      required: false,
      default: 'medium',
      validator: function (value) {
        return ['small', 'medium', 'large', 'x-large'].includes(value)
      },
    },
  },
}
</script>
