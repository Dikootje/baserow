<template>
  <Toast type="error" icon="warning-triangle">
    <template #title>{{ $t('authorizationErrorToast.title') }}</template>
    <span> {{ $t('authorizationErrorToast.content') }}</span>
    <template #actions>
      <ButtonText :loading="loading" size="small" @click="reload()">
        {{ $t('authorizationErrorToast.action') }}</ButtonText
      >
    </template>
  </Toast>
</template>

<script>
import Toast from '@baserow/modules/core/components/toasts/Toast'
import ButtonText from '@baserow/modules/core/components/ButtonText'
export default {
  name: 'AuthorizationErrorToast',
  components: {
    Toast,
    ButtonText,
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    reload() {
      this.loading = true
      location.reload()
    },
  },
}
</script>
