<script>
export default {
  name: 'PermissionsUpdatedToast',
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
    close() {
      this.$store.dispatch('toast/setPermissionsUpdated', false)
    },
  },
}
</script>

<template>
  <Toast @close="close" type="warning" icon="warning-triangle">
    <template #title>{{ $t('permissionsUpdatedToast.title') }}</template>
    <span>{{ $t('permissionsUpdatedToast.content') }}</span>
    <template #actions>
      <button :loading="loading" @click="reload()">
        {{ $t('permissionsUpdatedToast.action') }}
      </button>
    </template>
  </Toast>
</template>

<script>
import Toast from './Toast.vue'
export default {
  name: 'PermissionsUpdatedToast',
  components: {
    Toast,
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
    close() {
      this.$store.dispatch('toast/setPermissionsUpdated', false)
    },
  },
}
</script>
