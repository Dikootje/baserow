<template>
  <div
    class="dropdown"
    :class="{
      'dropdown--floating': !showInput,
      'dropdown--disabled': disabled,
    }"
    :tabindex="realTabindex"
    @focusin="show()"
    @focusout="focusout($event)"
  >
    <a v-if="showInput" class="dropdown__selected" @click="show()">
      <template v-if="hasValue()">
        <slot name="value">
          <i
            v-if="selectedIcon"
            class="dropdown__selected-icon fas"
            :class="'fa-' + selectedIcon"
          />
          <img
            v-if="selectedImage"
            class="dropdown__selected-image"
            :src="selectedImage"
          />
          {{ selectedName }}
        </slot>
      </template>
      <template v-else>
        <slot name="defaultValue">
          {{ placeholder ? placeholder : $t('action.makeChoice') }}
        </slot>
      </template>
      <i class="dropdown__toggle-icon fas fa-caret-down"></i>
    </a>
    <div
      ref="itemsContainer"
      class="dropdown__items"
      :class="{
        hidden: !open,
        'dropdown__items--fixed': immutableFixedItems,
      }"
    >
      <div v-if="showSearch" class="select__search">
        <i class="select__search-icon fas fa-search"></i>
        <input
          ref="search"
          v-model="query"
          type="text"
          class="select__search-input"
          :placeholder="searchText === null ? $t('action.search') : searchText"
          tabindex="0"
          @keyup="search(query)"
        />
      </div>
      <ul
        v-show="hasDropdownItem"
        ref="items"
        v-auto-overflow-scroll
        class="select__items"
        tabindex=""
      >
        <slot></slot>
      </ul>
      <div v-if="!hasDropdownItem" class="select__items--empty">
        <slot name="emptyState">
          {{ $t('dropdown.empty') }}
        </slot>
      </div>
      <div v-if="showFooter" class="select__footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import dropdown from '@baserow/modules/core/mixins/dropdown'

export default {
  name: 'Dropdown',
  mixins: [dropdown],
  props: {
    /**
     * If set, then the items element will be positioned fixed. This can be useful if
     * the parent element has an `overflow: hidden|scroll`, and you still want the
     * dropdown to break out of it. This property is immutable, so changing it
     * afterwards has no point.
     *
     * The dropdown items don't work in combination with the `moveToBody` because then
     * the `focusin` and `focusout` tab key effect doesn't work anymore. This means
     * that this option will only be compatible with the `app` layout because that one
     * has a max 100% width and height, it won't work in the API docs or publicly shared
     * form for example.
     */
    fixedItems: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  created() {
    this.immutableFixedItems = this.fixedItems
  },
  beforeDestroy() {
    if (this.immutableFixedItems) {
      window.removeEventListener('scroll', this.$el.updatePositionEvent, true)
      window.removeEventListener('resize', this.$el.updatePositionEvent)
    }
  },
  methods: {
    async show(...args) {
      if (this.disabled || this.open) {
        return
      }

      const originalReturnValue = dropdown.methods.show.call(this, ...args)

      if (this.immutableFixedItems) {
        const updatePosition = () => {
          const element = this.$refs.itemsContainer
          const targetRect = this.$el.getBoundingClientRect()
          element.style.top = targetRect.top + 'px'
          element.style.left = targetRect.left + 'px'
        }

        // Delay the position update to the next tick to let the Context content
        // be available in DOM for accurate positioning.
        await this.$nextTick()
        updatePosition()

        this.$el.updatePositionEvent = () => {
          updatePosition()
        }
        window.addEventListener('scroll', this.$el.updatePositionEvent, true)
        window.addEventListener('resize', this.$el.updatePositionEvent)
      }

      return originalReturnValue
    },
    hide(...args) {
      if (this.disabled || !this.open) {
        return
      }

      const originalReturnValue = dropdown.methods.hide.call(this, ...args)

      if (this.immutableFixedItems) {
        window.removeEventListener('scroll', this.$el.updatePositionEvent, true)
        window.removeEventListener('resize', this.$el.updatePositionEvent)
      }

      return originalReturnValue
    },
  },
}
</script>
