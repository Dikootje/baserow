from collections import defaultdict
from typing import Dict, List, Optional, Union

from rest_framework.request import Request

from baserow.contrib.builder.data_sources.handler import DataSourceHandler
from baserow.contrib.builder.data_sources.models import DataSource
from baserow.contrib.builder.pages.exceptions import PageDoesNotExist
from baserow.contrib.builder.pages.handler import PageHandler
from baserow.contrib.builder.pages.models import Page
from baserow.core.formula.data_ledger import DataLedger
from baserow.core.formula.exceptions import DispatchContextError
from baserow.core.formula.registries import DataProviderType
from baserow.core.services.handler import ServiceHandler
from baserow.core.services.models import Service
from baserow.core.utils import get_nested_value_from_dict


class PageParameterDataProviderType(DataProviderType):
    """
    This data provider reads page parameter information from the data sent by the
    frontend during the dispatch. The data are then available for the formulas.
    """

    type = "page_parameter"

    def get_context(self, request: Optional[Request] = None, **kwargs) -> Dict:
        """Extracts the page parameter from the query."""

        # We need a request to get this context
        if request is None:
            return {}

        return request.data.get("page_parameter", {})

    def get_data_chunk(
        self, data_ledger: DataLedger, path: List[str]
    ) -> Union[int, str]:
        """
        When a page parameter is read, returns the value previously saved from the
        request object.
        """

        if len(path) != 1:
            return None

        first_part = path[0]

        return data_ledger.context["page_parameter"].get(first_part, None)


class DataSourceDataProviderType(DataProviderType):
    """
    The data source provider can read data from registered page data sources.
    """

    type = "data_source"

    def get_context(
        self,
        service: Optional[Service] = None,
        request: Optional[Request] = None,
        **kwargs
    ):
        """
        Loads the page from the page_id given during the dispatch request.
        """

        # An lazy dict to prevent unnecessary queries if the keys are not used in
        # any formula
        class LazyContext(defaultdict):
            def __missing__(self, key: str):
                # We need a service to call this get context
                if not service or not service.integration:
                    return None

                if key == "page":
                    if request is None:
                        return None
                    page_id = request.data.get("data_source", {}).get("page_id", None)

                    if page_id:
                        base_queryset = Page.objects.filter(datasource__service=service)
                        try:
                            self["page"] = PageHandler().get_page(
                                page_id, base_queryset=base_queryset
                            )
                        except PageDoesNotExist:
                            raise DispatchContextError(
                                "The given page_id doesn't exist or is not readable."
                            )
                    else:
                        raise DispatchContextError("Missing page_id parameter.")
                    return self["page"]

        return LazyContext()

    def get_data_chunk(self, data_ledger: DataLedger, path: List[str]):
        """Load a data chunk from a datasource of the page in context."""

        data_source_name, *rest = path

        page = data_ledger.context["data_source"]["page"]
        if not page:
            return None

        data_source = DataSourceHandler().get_data_source_by_name(
            data_source_name, base_queryset=DataSource.objects.filter(page=page)
        )

        service_dispatch = ServiceHandler().dispatch_service(
            data_source.service.specific, data_ledger
        )

        return get_nested_value_from_dict(service_dispatch, rest)
