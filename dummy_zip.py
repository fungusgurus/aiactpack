import tempfile, pathlib, datetime, zipfile, json

def dummy_zip(payload: dict):
    tmp = pathlib.Path(tempfile.mkdtemp())
    zip_path = tmp / f"AIACTPACK_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr("Executive_Summary.md", f"# EU AI Act Pack\n\nGenerated for {payload.get('model_name','model')}")
        z.writestr("payload.json", json.dumps(payload, indent=2))
    return zip_path
