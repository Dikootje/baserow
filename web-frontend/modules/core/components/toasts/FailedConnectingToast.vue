<template>
  <Toast type="error" icon="warning-triangle">
    <template #title>{{ $t('failedConnectingToast.title') }}</template>
    <span>{{ $t('failedConnectingToast.content') }}</span>
    <template #actions>
      <ButtonText :loading="loading" @click="reload()">
        {{ $t('failedConnectingToast.action') }}
      </ButtonText>
    </template>
  </Toast>
</template>

<script>
import Toast from '@baserow/modules/core/components/toasts/Toast'
import ButtonText from '@baserow/modules/core/components/ButtonText'
export default {
  name: 'FailedConnectingToast',
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
