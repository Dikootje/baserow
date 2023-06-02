<template>
  <div class="toast" :class="classes">
    <div v-if="type">
      <div class="toast__icon" :class="`toast__icon--${type}`">
        <i v-if="icon" :class="`iconoir-${icon}`"></i>

        <i v-if="type === 'loading'" class="toast__loading"></i>
      </div>
    </div>

    <div class="toast__content">
      <div v-if="hasTitleSlot" class="toast__title">
        <slot name="title" />
      </div>
      <p class="toast__message"><slot /></p>

      <div v-if="hasActionsSlot" class="toast__actions">
        <slot name="actions" />
      </div>
    </div>

    <button class="toast__close" @click="$emit('close')">
      <i class="iconoir-cancel"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  props: {
    type: {
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
    icon: {
      type: String,
      default: null,
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
    classes() {
      if (this.position) return `toast--${this.position}`
      return null
    },
    hasTitleSlot() {
      return !!this.$slots.title
    },
    hasActionsSlot() {
      return !!this.$slots.actions
    },
  },
  mounted() {
    setTimeout(() => {
      this.close(this.toast)
    }, 5000)
  },
  methods: {
    close(toast) {
      this.$store.dispatch('toast/remove', toast)
    },
  },
}
</script>
