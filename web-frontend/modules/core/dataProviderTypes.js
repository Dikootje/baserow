import { Registerable } from '@baserow/modules/core/registry'

/**
 * A data provider gets data from the application context and populate the context for
 * the formula resolver.
 */
export class dataProviderType extends Registerable {
  get name() {
    throw new Error('`name` must be set on the dataProviderType.')
  }

  /**
   * Returns the actual data.
   * @param {object} dataLedger the data ledger instance.
   * @param {Array<str>} path the path of the data we want to get
   */
  getDataChunk(dataLedger, path) {
    throw new Error('.getDataChunk() must be set on the dataProviderType.')
  }

  /**
   * Should return the context needed to be send to the backend for each dataProvider
   * to be able to solve the formulas on the backend.
   * @returns An object if the dataProvider wants to send something to the backend.
   */
  getContext() {
    return null
  }

  getOrder() {
    return 0
  }
}
