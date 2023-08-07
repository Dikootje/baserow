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
      case 'wrapper':
        return this.visitWrapper(node)
      case 'text':
        return this.visitText(node)
      default:
        return this.visitFunction(node)
    }
  }

  visitWrapper(node) {
    if (!node.content) {
      return "'\\n'"
    }

    return this.visit(node.content)
  }

  visitArray(content) {
    const contentVisited = content
      .map((node) => this.visit(node))
      .filter((node) => node !== null)

    if (contentVisited.length === 0) {
      return ''
    }

    if (contentVisited.length === 1) {
      return contentVisited[0]
    }

    let result = `concat(${contentVisited[0]}, ${contentVisited[1]})`

    for (let i = 2; i < contentVisited.length; i++) {
      result = `concat(${result}, ${contentVisited[i]})`
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
