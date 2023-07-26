import { IntegrationType } from '@baserow/modules/core/integrationTypes'
import LocalBaserowForm from '@baserow/modules/integrations/components/integrations/LocalBaserowForm'
import localBaserowIntegration from '@baserow/modules/integrations/assets/images/localBaserowIntegration.svg'

export class LocalBaserowIntegrationType extends IntegrationType {
  static getType() {
    return 'local_baserow'
  }

  get name() {
    return this.app.i18n.t('integrationType.localBaserow')
  }

  get image() {
    return localBaserowIntegration
  }

  getSummary(integration, workspace) {
    const authorizedUser = this.getAuthorizedUser(integration, workspace)
    return this.app.i18n.t('integrationType.localBaserowSummary', {
      name: authorizedUser.name,
      username: authorizedUser.email,
    })
  }

  get formComponent() {
    return LocalBaserowForm
  }

  /**
   * Displays a warning if the logged-in user is the integration authorized user.
   * We'll recommend that they add a separate user just for the integration.
   @param {object} integration: The integration we may warn the user about.
   @param {object} workspace The workspace record, in case it's needed.
   @returns An optional warning.
   */
  getWarning(integration, workspace) {
    const user = this.app.store.getters['auth/getUserObject']
    return integration && integration.authorized_user === user.id
      ? this.app.i18n.t('integrationType.localBaserowWarning')
      : ''
  }

  getDefaultValues() {
    const user = this.app.store.getters['auth/getUserObject']
    return {
      authorized_user: { username: user.username, first_name: user.first_name },
    }
  }

  getOrder() {
    return 10
  }
}
