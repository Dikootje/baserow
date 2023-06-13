from unittest.mock import MagicMock

import pytest

from baserow.contrib.builder.data_providers.data_provider_types import (
    DataSourceDataProviderType,
    PageParameterDataProviderType,
)
from baserow.contrib.builder.data_providers.registries import (
    builder_data_provider_type_registry,
)
from baserow.core.formula.data_ledger import DataLedger
from baserow.core.formula.exceptions import DispatchContextError


def test_page_parameter_data_provider_get_context():
    page_parameter = PageParameterDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {"page_parameter": {"id": 1}}

    result = page_parameter.get_context(request=fake_request)

    assert result == {"id": 1}

    fake_request.data = {}

    result = page_parameter.get_context(request=fake_request)

    assert result == {}


def test_page_parameter_data_provider_get_data_chunk():
    page_parameter_provider = PageParameterDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {"page_parameter": {"id": 1}}

    data_ledger = MagicMock()
    data_ledger.context = {"page_parameter": {"id": 42}}

    assert page_parameter_provider.get_data_chunk(data_ledger, ["id"]) == 42
    assert page_parameter_provider.get_data_chunk(data_ledger, []) is None
    assert page_parameter_provider.get_data_chunk(data_ledger, ["id", "test"]) is None
    assert page_parameter_provider.get_data_chunk(data_ledger, ["test"]) is None


@pytest.mark.django_db
def test_data_source_data_provider_get_context(data_fixture, django_assert_num_queries):
    page = data_fixture.create_builder_page()
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {"data_source": {"page_id": page.id}}

    with django_assert_num_queries(0):
        result = data_source_provider.get_context(
            service=data_source.service, request=fake_request
        )

    with django_assert_num_queries(1):
        assert result["page"] == page

    fake_request.data = {}

    result = data_source_provider.get_context(request=fake_request)

    assert dict(result) == {}


@pytest.mark.django_db
def test_data_source_data_provider_get_context_bad_page(data_fixture):
    page = data_fixture.create_builder_page()
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source()

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {"data_source": {"page_id": page.id}}

    result = data_source_provider.get_context(
        service=data_source.service, request=fake_request
    )

    with pytest.raises(DispatchContextError):
        result["page"]


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk(data_fixture):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table,
        row_id="2",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    data_ledger = MagicMock()
    data_ledger.context = {"data_source": {"page": page}}

    assert (
        data_source_provider.get_data_chunk(data_ledger, ["Item", "My Color"])
        == "Orange"
    )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula(data_fixture):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table,
        row_id="get('page_parameter.id')",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {"id": 2},
    }

    data_ledger = DataLedger(
        builder_data_provider_type_registry,
        service=data_source.service,
        request=fake_request,
    )

    assert (
        data_source_provider.get_data_chunk(data_ledger, ["Item", "My Color"])
        == "Orange"
    )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula_using_datasource(
    data_fixture,
):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    table2, fields2, rows2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Id", "text"),
        ],
        rows=[
            ["1"],
            ["2"],
            ["3"],
            ["3"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table,
        row_id="get('data_source.Id source.Id')",
        name="Item",
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table2,
        row_id="get('page_parameter.id')",
        name="Id source",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {"id": 2},
    }

    data_ledger = DataLedger(
        builder_data_provider_type_registry,
        service=data_source.service,
        request=fake_request,
    )

    assert (
        data_source_provider.get_data_chunk(data_ledger, ["Item", "My Color"])
        == "Orange"
    )
