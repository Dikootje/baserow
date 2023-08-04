<template>
  <PageContent
    :page="page"
    :path="path"
    :params="params"
    :elements="elements"
  />
</template>

<script>
import PageContent from '@baserow/modules/builder/components/page/PageContent'
import { resolveApplicationRoute } from '@baserow/modules/builder/utils/routing'
import RuntimeFormulaContext from '@baserow/modules/core/runtimeFormulaContext'

export default {
  components: { PageContent },
  provide() {
    return { builder: this.builder, page: this.page, mode: this.mode }
  },
  async asyncData(context) {
    let builder = context.store.getters['application/getSelected']
    let mode = 'public'
    const builderId = parseInt(context.route.params.builderId, 10)

    if (!builder) {
      try {
        if (builderId) {
          // We have the builderId in the params so this is a preview
          // Must fetch the builder instance by this Id.
          await context.store.dispatch('publicBuilder/fetchById', {
            builderId,
          })
          builder = await context.store.dispatch(
            'application/selectById',
            builderId
          )
        } else {
          // We don't have the builderId so it's a public page.
          // Must fetch the builder instance by domain name.
          const host = process.server
            ? context.req.headers.host
            : window.location.host
          const domain = new URL(`http://${host}`).hostname

          const { id: receivedBuilderId } = await context.store.dispatch(
            'publicBuilder/fetchByDomain',
            {
              domain,
            }
          )
          builder = await context.store.dispatch(
            'application/selectById',
            receivedBuilderId
          )
        }
      } catch (e) {
        return context.error({
          statusCode: 404,
          message: context.app.i18n.t('publicPage.siteNotFound'),
        })
      }
    }

    if (builderId) {
      mode = 'preview'
    }

    const found = resolveApplicationRoute(
      builder.pages,
      context.route.params.pathMatch
    )

    // Handle 404
    if (!found) {
      return context.error({
        statusCode: 404,
        message: context.app.i18n.t('publicPage.pageNotFound'),
      })
    }

    const [pageFound, path, params] = found

    const page = await context.store.getters['page/getById'](
      builder,
      pageFound.id
    )

    await Promise.all([
      context.store.dispatch('dataSource/fetchPublished', {
        page,
      }),
      context.store.dispatch('element/fetchPublished', { page }),
    ])

    const runtimeFormulaContext = new RuntimeFormulaContext(
      context.$registry.getAll('builderDataProvider'),
      {
        builder,
        page,
        pageParamsValue: params,
        mode,
      }
    )

    // Initialize all data provider contents
    await runtimeFormulaContext.initAll()

    // And finally select the page to display it
    await context.store.dispatch('page/selectById', {
      builder,
      pageId: pageFound.id,
    })

    return {
      builder,
      page,
      path,
      params,
      mode,
    }
  },
  head() {
    return {
      titleTemplate: '',
      title: this.page.name,
      bodyAttrs: {
        class: 'public-page',
      },
    }
  },
  computed: {
    elements() {
      return this.$store.getters['element/getRootElements'](this.page)
    },
  },
}
</script>
