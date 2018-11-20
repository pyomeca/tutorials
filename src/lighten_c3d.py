import ezc3d
from pathlib import Path


def lighten_file(old_file_path, new_file_path, muscle_list, new_muscle_list=None):
    print(old_file_path)
    old = ezc3d.c3d(old_file_path)

    for imuscle_list in muscle_list:
        try:
            idx = [
                old["parameters"]["ANALOG"]["LABELS"]["value"].index(i)
                for i in imuscle_list
            ]
            break
        except:
            pass
    data = old["data"]["analogs"][0, idx, :].reshape(1, len(imuscle_list), -1)

    new = ezc3d.c3d()

    new["parameters"]["POINT"]["RATE"]["value"] = list(
        old["parameters"]["ANALOG"]["RATE"]["value"]
    )

    # fill analogs
    new["parameters"]["ANALOG"]["RATE"]["value"] = list(
        old["parameters"]["ANALOG"]["RATE"]["value"]
    )

    labels = new_muscle_list if new_muscle_list else imuscle_list
    new["parameters"]["ANALOG"]["LABELS"]["value"] = labels
    new["data"]["analogs"] = data

    # Write the data
    new.write(new_file_path)
    print(f"\twritten in {new_file_path}")


if __name__ == "__main__":
    repo = Path("/home/romain/Downloads/kin6839_data/")

    muscles = [
        ["Delt_ant.EMG1"],
        ["1_Delt_ant.EMG1"],
        ["Delt_Ant.EMG1"],
        ["Voltage.1_Delt_Ant"],
        ["Voltage.1_Delt_ant"],
        ["1_Delt_Ant"],
        ["Voltage.1-Deltoid Ant"],
        ["1-Deltoid Ant"],
        ["Voltage.1_Delt_A"],
    ]

    muscles = [['delt_ant']]

    new_muscle_list = ["delt_ant"]

    for ifile in repo.glob("*.c3d"):
        output_filename = f"{ifile}".replace(
            ifile.stem,
            ifile.stem.replace("YoaP", "")
            .replace("H6", "6kg_")
            .replace("H12", "12kg_"),
        )

        lighten_file(
            old_file_path=f"{ifile}",
            new_file_path=output_filename,
            muscle_list=muscles,
            new_muscle_list=new_muscle_list,
        )
