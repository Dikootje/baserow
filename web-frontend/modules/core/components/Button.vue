<template>
  <component
    :is="tag === 'a' || href ? 'a' : 'button'"
    class="button"
    :class="classes"
    :disabled="disabled"
    :active="active"
    :rel="rel"
    v-bind.prop="customBind"
    v-on="$listeners"
  >
    <i v-if="icon !== ''" class="button__icon" :class="`iconoir-${icon}`" />
    <span><slot /></span>
  </component>
</template>

<script>
export default {
  props: {
    tag: {
      required: false,
      type: String,
      default: 'button',
      validator: function (value) {
        return ['a', 'button'].includes(value)
      },
    },
    size: {
      required: false,
      type: String,
      default: 'regular',
      validator: function (value) {
        return ['regular', 'large'].includes(value)
      },
    },
    type: {
      required: false,
      type: String,
      default: 'primary',
      validator: function (value) {
        return ['primary', 'secondary', 'danger'].includes(value)
      },
    },
    icon: {
      required: false,
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
    href: {
      required: false,
      type: String,
      default: '',
    },
    rel: {
      required: false,
      type: String,
      default: '',
    },
    target: {
      required: false,
      type: String,
      validator: function (value) {
        return ['_blank', '_self'].includes(value)
      },
      default: '_self',
    },
  },
  computed: {
    classes() {
      const hasIcon = this.icon !== ''
      const classObj = {
        [`button--${this.size}`]: this.size,
        [`button--${this.type}`]: this.type,
        'button--icon': hasIcon,
        'button--loading': this.loading,
        disabled: this.disabled,
        active: this.active,
      }
      return classObj
    },
    customBind() {
      const attr = {}
      if (this.href) attr.href = this.href
      if (this.target) attr.target = `${this.target}`
      return attr
    },
  },
}
</script>
