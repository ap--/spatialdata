import pytest
import zarr

from spatialdata import SpatialData


class TestRemote:
    # Test actual remote datasets from https://spatialdata.scverse.org/en/latest/tutorials/notebooks/datasets/README.html

    @pytest.fixture(params=["merfish", "mibitof", "mibitof_alt"])
    def remote_location(self, request):
        urlpath_sopts = {
            "merfish": (
                "s3://spatialdata/spatialdata-sandbox/merfish.zarr",
                {"endpoint_url": "https://s3.embl.de", "anon": True},
            ),
            "mibitof": (
                "s3://spatialdata/spatialdata-sandbox/mibitof.zarr",
                {"endpoint_url": "https://s3.embl.de", "anon": True},
            ),
            "mibitof_alt": (
                "https://dl01.irc.ugent.be/spatial/mibitof/data.zarr/",
                {},
            ),
        }
        return urlpath_sopts[request.param]

    def test_remote(self, remote_location):
        urlpath, storage_options = remote_location
        sdata = SpatialData.read(urlpath, storage_options=storage_options)
        assert len(list(sdata.gen_elements())) > 0

    def test_remote_consolidated(self, remote_location):
        urlpath, storage_options = remote_location
        root = zarr.open_consolidated(urlpath, mode="r", metadata_key="zmetadata", storage_options=storage_options)
        sdata = SpatialData.read(root)
        assert len(list(sdata.gen_elements())) > 0
