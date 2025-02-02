from studio.app.common.dataclass import HeatMapData
from studio.app.optinist.core.nwb.nwb import NWBDATASET
from studio.app.optinist.dataclass import FluoData, IscellData


def correlation(
    neural_data: FluoData,
    output_dir: str,
    iscell: IscellData = None,
    params: dict = None,
    **kwargs,
) -> dict():
    import numpy as np

    function_id = output_dir.split("/")[-1]
    print("start correlation:", function_id)

    neural_data = neural_data.data

    # data shold be time x component matrix
    if params["transpose"]:
        X = neural_data.transpose()
    else:
        X = neural_data

    if iscell is not None:
        iscell = iscell.data
        ind = np.where(iscell > 0)[0]
        X = X[ind, :]

    num_cell = X.shape[0]

    # calculate correlation
    corr = np.corrcoef(X)
    for i in range(num_cell):
        corr[i, i] = np.nan

    # NWB追加
    nwbfile = {}
    nwbfile[NWBDATASET.POSTPROCESS] = {
        function_id: {
            "corr": corr,
        }
    }

    info = {
        "corr": HeatMapData(corr, file_name="corr"),
        "nwbfile": nwbfile,
    }

    return info
