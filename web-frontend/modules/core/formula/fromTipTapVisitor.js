import _ from 'lodash/fp'

export class FromTipTapVisitor {
  constructor(functions) {
    this.functions = functions
  }

  visit(content) {
    if (_.isArray(content)) {
      return this.visitArray(content)
    } else {
      return this.visitNode(content)
    }
  }

  visitNode(node) {
    switch (node.type) {
      case 'text':
        return this.visitText(node)
      default:
        return this.visitFunction(node)
    }
  }

  visitArray(content) {
    if (content.length === 0) {
      return ''
    }

    if (content.length === 1) {
      return this.visit(content[0])
    }

    let result = `concat(${this.visit(content[0])}, ${this.visit(content[1])})`

    for (let i = 2; i < content.length; i++) {
      result = `concat(${result}, ${this.visit(content[i])})`
    }

    return result
  }

  visitText(node) {
    return `'${node.text}'`
  }

  visitFunction(node) {
    const formulaFunction = Object.values(this.functions.getAll()).find(
      (functionCurrent) => functionCurrent.formulaComponentType === node.type
    )

    return formulaFunction?.fromNodeToFormula(node)
  }
}
