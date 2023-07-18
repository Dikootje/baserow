import _ from 'lodash'

export class MissingDataProviderError extends Error {
  constructor(dataProviderName) {
    super()
    this.message = `The following data provider is missing: ${dataProviderName}`
    this.dataProviderName = dataProviderName
  }
}

export class UnresolvablePathError extends Error {
  constructor(dataProviderName, path) {
    super()
    this.message = `The path '${path}' can't be resolved in the data provider: ${dataProviderName}`
    this.dataProviderName = dataProviderName
    this.path = path
  }
}

class DataLedgerClass {
  constructor(dataProviders, ...args) {
    this.dataProviders = dataProviders
    this.context = {}

    // Populate context with all dataProvider custom contexts
    Object.values(this.dataProviders).forEach((dataProvider) => {
      const dataProviderContext = dataProvider.getContext(...args)
      this.context[dataProvider.type] = dataProviderContext
    })
  }

  /**
   * Returns the value for the given path. The first part of the path is
   * the data provider type, then the remaining parts are given to the data provider.
   *
   * @param {str} path the dotted path of the data we want to get.
   * @returns the data related to the path.
   */
  get(path) {
    const [providerName, ...rest] = _.toPath(path)

    const dataProviderType = this.dataProviders[providerName]
    console.log('fount', dataProviderType, providerName)

    if (!dataProviderType) {
      throw new MissingDataProviderError(providerName)
    }

    try {
      return dataProviderType.getDataChunk(this, rest)
    } catch (e) {
      throw new UnresolvablePathError(dataProviderType.type, rest.join('.'))
    }
  }
}

/**
 * This proxy allow the DataLedgerClass to act like a regular object.
 */
const DataLedger = (...args) =>
  new Proxy(new DataLedgerClass(...args), {
    get(target, prop) {
      const result = target.get(prop)
      return result
    },
  })

export default DataLedger
