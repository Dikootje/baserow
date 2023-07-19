from typing import List, Union

from baserow.contrib.builder.data_sources.handler import DataSourceHandler
from baserow.contrib.builder.data_sources.models import DataSource
from baserow.contrib.builder.pages.exceptions import PageDoesNotExist
from baserow.contrib.builder.pages.handler import PageHandler
from baserow.contrib.builder.pages.models import Page
from baserow.core.formula.data_ledger import DataLedger
from baserow.core.formula.exceptions import DispatchContextError
from baserow.core.formula.registries import DataProviderType
from baserow.core.services.handler import ServiceHandler
from baserow.core.utils import get_nested_value_from_dict


class PageParameterDataProviderType(DataProviderType):
    """
    This data provider reads page parameter information from the data sent by the
    frontend during the dispatch. The data are then available for the formulas.
    """

    type = "page_parameter"

    def get_data_chunk(
        self, data_ledger: DataLedger, path: List[str]
    ) -> Union[int, str]:
        """
        When a page parameter is read, returns the value previously saved from the
        request object.
        """

        if "request" not in data_ledger.application_context:
            return None

        if len(path) != 1:
            return None

        first_part = path[0]

        return (
            data_ledger.application_context["request"]
            .data.get("page_parameter", {})
            .get(first_part, None)
        )


class DataSourceDataProviderType(DataProviderType):
    """
    The data source provider can read data from registered page data sources.
    """

    type = "data_source"

    def get_data_chunk(self, data_ledger: DataLedger, path: List[str]):
        """Load a data chunk from a datasource of the page in context."""

        data_source_name, *rest = path

        if "request" not in data_ledger.application_context:
            return None
        if "service" not in data_ledger.application_context:
            return None

        page_id = (
            data_ledger.application_context["request"]
            .data.get("data_source", {})
            .get("page_id", None)
        )
        print(page_id)
        base_queryset = Page.objects.filter(
            datasource__service=data_ledger.application_context["service"]
        )

        try:
            page = PageHandler().get_page(page_id, base_queryset=base_queryset)
        except PageDoesNotExist:
            raise DispatchContextError(
                "The given page_id doesn't exist or is not readable."
            )

        data_source = DataSourceHandler().get_data_source_by_name(
            data_source_name, base_queryset=DataSource.objects.filter(page=page)
        )

        service_dispatch = ServiceHandler().dispatch_service(
            data_source.service.specific, data_ledger
        )

        return get_nested_value_from_dict(service_dispatch, rest)
