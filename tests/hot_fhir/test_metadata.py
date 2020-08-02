def test_metadata(client, fhir):
    res = client.get('/metadata')
    assert res.status_code == 200
    assert res.json['resourceType'] == 'CapabilityStatement'
