<template>
  <div class="alert" :class="classes">
    <i v-if="type !== 'loading'" class="alert__icon" :class="iconClass"></i>
    <i v-else class="alert__loading"></i>

    <div class="alert__content">
      <div v-if="hasTitleSlot" class="alert__title">
        <slot name="title" />
      </div>
      <p class="alert__message"><slot /></p>

      <div v-if="hasActionsSlot" class="alert__actions">
        <slot name="actions" />
      </div>
    </div>

    <button class="alert__close" @click="$emit('close')">
      <i class="iconoir-cancel"></i>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      required: true,
      type: String,
      default: null,
      validator: function (value) {
        return [
          'info-neutral',
          'info-primary',
          'warning',
          'error',
          'success',
          'loading',
        ].includes(value)
      },
    },
    position: {
      required: false,
      type: String,
      default: null,
      validator: function (value) {
        return ['top', 'bottom'].includes(value)
      },
    },
  },
  computed: {
    hasTitleSlot() {
      return !!this.$slots.title
    },
    hasActionsSlot() {
      return !!this.$slots.actions
    },
    classes() {
      const classObj = {
        [`alert--${this.type}`]: this.type,
        [`alert--${this.position}`]: this.position,
      }
      return classObj
    },
    isWarningAlert() {
      return this.type === 'warning'
    },
    isErrorAlert() {
      return this.type === 'error'
    },
    isInfoAlert() {
      return this.type === 'info-neutral' || this.type === 'info-primary'
    },
    isSuccessAlert() {
      return this.type === 'success'
    },
    iconClass() {
      const classObj = {
        'iconoir-warning-triangle': this.isWarningAlert,
        'iconoir-info-empty': this.isInfoAlert,
        'iconoir-check-circle': this.isSuccessAlert,
        'iconoir-warning-circle': this.isErrorAlert,
      }
      return classObj
    },
  },
  methods: {
    customBind(ctaOptions) {
      const attr = {}
      if (ctaOptions.external) {
        attr.href = ctaOptions.link
        attr.target = '_blank'
        attr.rel = 'nofollow noopener noreferrer'
      } else attr.to = ctaOptions.link
      return attr
    },
  },
}
</script>
