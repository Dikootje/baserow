<template>
  <PageContent
    v-if="!$fetchState.pending"
    :page="page"
    :path="path"
    :params="params"
    :elements="elements"
  />
</template>

<script>
import PageContent from '@baserow/modules/builder/components/page/PageContent'
import PublicBuilderService from '@baserow/modules/builder/services/publishedBuilder'

export default {
  components: { PageContent },
  props: {
    page: {
      type: Object,
      required: true,
    },
    path: {
      type: String,
      required: true,
    },
    params: {
      type: Object,
      required: true,
    },
  },
  data() {
    return { elements: [] }
  },
  async fetch() {
    const { data } = await PublicBuilderService(this.$client).fetchElements(
      this.page
    )

    this.elements = data
  },
}
</script>
