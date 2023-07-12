import { dataProviderType } from '@baserow/modules/core/dataProviderTypes'

import { clone } from '@baserow/modules/core/utils/object'
import _ from 'lodash'

export class DataSourceDataProviderType extends dataProviderType {
  constructor(...args) {
    super(...args)
    this.debouncedFetches = {}
  }

  static getType() {
    return 'data_source'
  }

  get name() {
    return this.app.i18n.t('dataProviderType.dataSource')
  }

  getContext({ page }) {
    return {
      page_id: page.id,
    }
  }

  getDataChunk(dataLedger, [dataSourceName, ...rest]) {
    // Load data sources for this page.
    const dataSources = this.app.store.getters['dataSource/getDataSources']

    const dataSource = dataSources.find(({ name }) => name === dataSourceName)

    if (!dataSource) {
      return null
    }

    this.app.store.dispatch('dataSourceContent/smartFetchDataSourceContent', {
      dataSource,
      data: dataLedger.context,
    })

    const dataSourceContents =
      this.app.store.getters['dataSourceContent/getDataSourceContents']

    if (!dataSourceContents[dataSource.id]) {
      return null
    }

    // Returns the content from the store for reactivity
    return _.get(dataSourceContents[dataSource.id], rest.join('.'))
  }
}

export class PageParameterDataProviderType extends dataProviderType {
  static getType() {
    return 'page_parameter'
  }

  get name() {
    return this.app.i18n.t('dataProviderType.pageParameter')
  }

  getDataChunk(dataLedger, path) {
    if (path.length !== 1) {
      return null
    }

    const [prop] = path
    const parameters = this.app.store.getters['pageParameter/getParameters']

    if (parameters[prop] === undefined) {
      return null
    }

    return parameters[prop]
  }

  getContext() {
    return clone(this.app.store.getters['pageParameter/getParameters'])
  }
}
