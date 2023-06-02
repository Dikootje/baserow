<template>
  <div class="badge-counter">{{ value }}</div>
</template>

<script>
export default {
  name: 'BadgeCounter',
  props: {
    count: {
      type: Number,
      required: true,
      default: 0,
    },
    limit: {
      type: Number,
      required: false,
      default: 10,
    },
  },
  computed: {
    value() {
      if (this.count > this.limit) return `${this.limit - 1}+`
      return this.count
    },
  },
}
</script>
