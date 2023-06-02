import { shallowMount } from '@vue/test-utils'
import FormTextarea from '@baserow/modules/core/components/FormTextarea.vue'

describe('FormTextarea.vue', () => {
  it('renders the textarea with the correct classes when props are provided', () => {
    const wrapper = shallowMount(FormTextarea, {
      propsData: {
        id: 'description',
        label: 'Description',
        disabled: true,
        smallLabel: true,
        required: true,
        helperText: 'Enter a description',
      },
    })
    expect(wrapper.find('.form-textarea').classes()).toContain('form-textarea')
    expect(wrapper.find('.form-textarea').classes()).toContain(
      'form-textarea--disabled'
    )
    expect(wrapper.find('.control__required').exists()).toBe(false)
  })

  it('renders the textarea with the correct attributes when props are provided', () => {
    const wrapper = shallowMount(FormTextarea, {
      propsData: {
        id: 'description',
        label: 'Description',
        disabled: true,
        smallLabel: true,
        required: true,
        helperText: 'Enter a description',
      },
    })
    expect(wrapper.find('.control__label-label').text()).toBe('Description')
    expect(wrapper.find('.form-textarea__textarea').attributes('id')).toBe(
      'description'
    )
    expect(
      wrapper.find('.form-textarea__textarea').attributes('disabled')
    ).toBe('disabled')
    expect(
      wrapper.find('.form-textarea__textarea').attributes('placeholder')
    ).toBeFalsy()
  })

  it('emits the "input" event when the textarea value changes', () => {
    const wrapper = shallowMount(FormTextarea, {
      propsData: { id: 'description', label: 'Description' },
    })
    const textareaElement = wrapper.find('.form-textarea__textarea')
    textareaElement.setValue('Lorem ipsum dolor sit amet')
    expect(wrapper.emitted('input')[0]).toEqual(['Lorem ipsum dolor sit amet'])
  })
})
