from pathlib import Path

import numpy as np
from pyomeca import Analogs3d

home = Path().home()
in_data_path = home / "Downloads/irsst"
out_data_path = home / "Documents/codes/tutorials/data/emg"


muscles = ["deltant", "deltmed", "deltpost", "ssp"]
time_normalization_vector = np.linspace(0, 100, 100)


def get_filename(filename: str) -> str:
    participant = filename[:4].lower()
    men = 1 if filename[4] == "H" else 0
    height = int(filename[-3])
    mass = int(filename[5:].split("H")[0])
    trial = int(filename[-1])
    return f"{participant}_{mass}kg_{height}H_{men}sex_{trial}"


def create_csv():
    for file in in_data_path.glob("*/0_emg/*.sto"):
        emg = (
            Analogs3d.from_sto(file)
            .time_normalization(time_normalization_vector)
            .to_dataframe()[muscles]
        )
        if emg.notna().all().all():
            emg.to_csv(out_data_path / f"{get_filename(file.stem)}.csv", index=False)


if __name__ == "__main__":
    create_csv()
