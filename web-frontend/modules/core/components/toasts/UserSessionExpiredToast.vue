<template>
  <Toast icon="warning-triangle">
    <Template #title>{{ $t('userSessionExpiredToast.title') }}</Template>
    <span> {{ $t('userSessionExpiredToast.content') }}</span>
  </Toast>
</template>

<script>
import Toast from '@baserow/modules/core/components/toasts/Toast'
export default {
  name: 'UserSessionExpiredToast',
  components: {
    Toast,
  },
  mounted() {
    setTimeout(() => {
      this.acknowledge()
    }, 7000)
  },
  beforeDestroy() {
    this.acknowledge()
  },
  methods: {
    acknowledge() {
      this.$store.dispatch('toast/setUserSessionExpired', false)
    },
  },
}
</script>
