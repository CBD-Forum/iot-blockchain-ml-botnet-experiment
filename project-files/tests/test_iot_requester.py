from unittest import mock

from iot_requester import make_request, run_threaded


@mock.patch('iot_requester.requests.get')
def test_make_request(mock_get):
    """Tests make_request function"""

    mock_get.return_value.ok = True

    make_request('http://localhost')

    assert mock_get.call_count in range(1, 4)


@mock.patch('threading.Thread')
def test_run_threaded(mock_tread):
    """Tests run_threaded function"""

    run_threaded(lambda ip: ip, 'http://localhost')

    assert mock_tread.called
