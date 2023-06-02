<template>
  <button class="chips" v-on="$listeners">
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Chips',
  props: {},
  computed: {},
}
</script>
