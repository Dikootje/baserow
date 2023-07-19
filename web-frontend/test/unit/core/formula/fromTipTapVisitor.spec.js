import { RuntimeFunctionCollection } from '@baserow/modules/core/functionCollection'
import { TestApp } from '@baserow/test/helpers/testApp'
import { FromTipTapVisitor } from '@baserow/modules/core/formula/fromTipTapVisitor'

describe('fromTipTapVisitor', () => {
  let testApp = null
  beforeAll(() => {
    testApp = new TestApp()
  })

  const testCases = [
    {
      content: [],
      expected: '',
    },
    {
      content: [{ type: 'text', text: 'hello' }],
      expected: "'hello'",
    },
    {
      content: [
        { type: 'text', text: 'hello' },
        { type: 'text', text: 'there' },
      ],
      expected: "concat('hello', 'there')",
    },
    {
      content: [
        { type: 'text', text: 'hello' },
        { type: 'text', text: 'there' },
        { type: 'text', text: 'friend :)' },
      ],
      expected: "concat(concat('hello', 'there'), 'friend :)')",
    },
    {
      content: [
        {
          type: 'get-formula-component',
          attrs: { path: 'data_source.hello.there' },
        },
      ],
      expected: "get('data_source.hello.there')",
    },
    {
      content: [
        {
          type: 'get-formula-component',
          attrs: { path: 'data_source.hello.there' },
        },
        { type: 'text', text: 'friend :)' },
      ],
      expected: "concat(get('data_source.hello.there'), 'friend :)')",
    },
  ]

  testCases.forEach((testCase) => {
    it('should return the expected formula', () => {
      const functionCollection = new RuntimeFunctionCollection(
        testApp.store.$registry
      )
      const result = new FromTipTapVisitor(functionCollection).visit(
        testCase.content
      )
      expect(result).toEqual(testCase.expected)
    })
  })
})
