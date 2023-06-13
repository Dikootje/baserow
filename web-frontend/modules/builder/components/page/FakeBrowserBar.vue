<template>
  <div class="fake-browser-bar">
    <div />
    <div class="fake-browser-bar__address-bar">
      <template v-for="pathPart in splittedPath">
        <input
          v-if="pathPart.type === 'variable'"
          :key="pathPart.key"
          class="fake-browser-bar__address-bar-parameter"
          :class="`fake-browser-bar__address-bar-parameter--${
            paramTypeMap[pathPart.value]
          }`"
          :value="pageParameters[pathPart.value]"
          @input="
            actionSetParameter({
              name: pathPart.value,
              value: $event.target.value,
            })
          "
        />
        <div
          v-else
          :key="pathPart.key"
          class="fake-browser-bar__address-bar-path"
        >
          {{ pathPart.value }}
        </div>
      </template>
    </div>
    <div />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { splitPath } from '@baserow/modules/builder/utils/path'

export default {
  props: {
    page: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      pageParameters: 'pageParameter/getParameters',
    }),
    splittedPath() {
      return splitPath(this.page.path).map((pathPart, index) => ({
        ...pathPart,
        key: `${pathPart.value}-${index}`,
      }))
    },
    paramTypeMap() {
      return Object.fromEntries(
        this.page.path_params.map(({ name, type }) => [name, type])
      )
    },
  },
  methods: {
    ...mapActions({ actionSetParameter: 'pageParameter/setParameter' }),
  },
}
</script>
