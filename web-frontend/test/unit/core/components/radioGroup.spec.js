import { shallowMount } from '@vue/test-utils'
import RadioGroup from '@baserow/modules/core/components/RadioGroup.vue'
import Radio from '@baserow/modules/core/components/Radio.vue'

describe('RadioGroup', () => {
  const options = [
    { id: 'option-1', value: 'option-1', label: 'Option 1' },
    { id: 'option-2', value: 'option-2', label: 'Option 2' },
    { id: 'option-3', value: 'option-3', label: 'Option 3', disabled: true },
    { id: 'option-4', value: 'option-4', label: 'Option 4', loading: true },
  ]

  it('renders the correct number of radio buttons', () => {
    const wrapper = shallowMount(RadioGroup, {
      propsData: {
        name: 'my-radio-group',
        options,
        modelValue: 'option-1',
      },
    })
    expect(wrapper.findAllComponents(Radio).length).toEqual(options.length)
  })

  it('emits an input event when a radio button is selected', () => {
    const wrapper = shallowMount(RadioGroup, {
      propsData: {
        name: 'my-radio-group',
        options,
        modelValue: 'option-1',
      },
    })

    wrapper.findAllComponents(Radio).at(1).vm.$emit('input', options[1].value)

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual([options[1].value])
  })
})
