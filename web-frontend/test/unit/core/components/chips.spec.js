import { shallowMount } from '@vue/test-utils'
import Chips from '@baserow/modules/core/components/Chips'

describe('Chips.vue', () => {
  it('renders chips text in slot', () => {
    const text = 'Click me'
    const wrapper = shallowMount(Chips, {
      slots: {
        default: text,
      },
    })
    expect(wrapper.find('button').text()).toMatch(text)
  })

  it('emits click event when clicked', () => {
    const wrapper = shallowMount(Chips)
    wrapper.vm.$emit('click')
    expect(wrapper.emitted().click).toBeTruthy()
  })
})
