import pytest
from click.testing import CliRunner
from mock import Mock

from bonfire import bonfire


@pytest.mark.parametrize(
    "name, expected",
    [
        ("namespacereservation", "ephemeral-namespace-test-1"),
        ("namespacereservation", "ephemeral-namespace-test-2"),
    ],
)
def test_ns_reserve_options_name(mocker, name, expected):
    ns = Mock()
    ns.name = expected

    mocker.patch("bonfire.bonfire.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.get_api_resources", return_value={"name": name})
    mocker.patch("bonfire.openshift.check_for_existing_reservation", return_value=True)
    mocker.patch("bonfire.openshift.parse_restype", return_value="")
    mocker.patch("bonfire.openshift.get_json", return_value="")
    mocker.patch("bonfire.openshift.get_all_reservations", return_value="")
    mocker.patch("bonfire.bonfire.reserve_namespace", return_value=ns)

    runner = CliRunner()
    result = runner.invoke(bonfire.namespace, ["reserve", "--name", name])

    assert result.output.rstrip() == expected


@pytest.mark.parametrize(
    "user, expected",
    [
        ("user1", "user1"),
        ("user2", "user2"),
    ],
)
def test_ns_reserve_options_requester(mocker, user, expected):
    ns = Mock()
    ns.name = expected

    mocker.patch("bonfire.bonfire.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.get_api_resources", return_value={"name": user})
    mocker.patch("bonfire.openshift.check_for_existing_reservation", return_value=True)
    mocker.patch("bonfire.openshift.parse_restype", return_value="")
    mocker.patch("bonfire.openshift.get_json", return_value="")
    mocker.patch("bonfire.openshift.get_all_reservations", return_value="")
    mocker.patch("bonfire.bonfire.reserve_namespace", return_value=ns)

    runner = CliRunner()
    result = runner.invoke(bonfire.namespace, ["reserve", "--requester", user])

    assert result.output.rstrip() == expected


@pytest.mark.parametrize(
    "duration, expected",
    [
        ("1h", "1h"),
        (None, "1h"),
        ("30m", "30m"),
    ],
)
def test_ns_reserve_options_duration(mocker, duration, expected):
    ns = Mock()
    ns.name = expected

    mocker.patch("bonfire.bonfire.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.has_ns_operator", return_value=True)
    mocker.patch("bonfire.openshift.get_api_resources", return_value={"name": duration})
    mocker.patch("bonfire.openshift.check_for_existing_reservation", return_value=True)
    mocker.patch("bonfire.openshift.parse_restype", return_value="")
    mocker.patch("bonfire.openshift.get_json", return_value="")
    mocker.patch("bonfire.openshift.get_all_reservations", return_value="")
    mocker.patch("bonfire.bonfire.reserve_namespace", return_value=ns)

    runner = CliRunner()
    result = runner.invoke(bonfire.namespace, ["reserve", "--duration", duration])

    assert result.output.rstrip() == expected


def test_ns_list_options(mocker):
    all_namespaces = []

    ephemeral_namespace_1 = Mock(reserved=False, status="ready", clowdapps="none", requester="user-2", expires_in="2h")
    ephemeral_namespace_1.name = "namespace-1"

    ephemeral_namespace_2 = Mock(reserved=True, status="ready", clowdapps="none", requester="user-1", expires_in="31m")
    ephemeral_namespace_2.name = "namespace-2"

    ephemeral_namespace_3 = Mock(reserved=False, status="ready", clowdapps="none", requester="user-3", expires_in="6h")
    ephemeral_namespace_3.name = "namespace-3"

    all_namespaces.append(ephemeral_namespace_1)
    all_namespaces.append(ephemeral_namespace_2)
    all_namespaces.append(ephemeral_namespace_3)

    mocker.patch("bonfire.namespaces.get_all_namespaces", return_value=all_namespaces)
    mocker.patch("bonfire.openshift.get_all_reservations", return_value="")
    mocker.patch("bonfire.bonfire.get_namespaces", return_value=all_namespaces)

    runner = CliRunner()
    result = runner.invoke(bonfire.namespace, ["list"])

    print(result.output)

    assert "namespace-1" in result.output
    assert "namespace-2" in result.output
    assert "namespace-3" in result.output
    assert "user-1" in result.output
    assert "user-2" in result.output
    assert "user-3" in result.output
    assert "31m" in result.output
    assert "2h" in result.output
    assert "6h" in result.output
