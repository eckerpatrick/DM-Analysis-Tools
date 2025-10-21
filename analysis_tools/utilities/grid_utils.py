from b2luigi.batch.processes.gbasf2 import run_with_gbasf2
from ping3 import ping
from typing import List


def get_grid_paths(lpn: str) -> List[str]:
    details = run_with_gbasf2(cmd=["gb2_ds_list", "-ll", lpn], capture_output=True)

    file_locations = []

    for d in details.stdout.split(" "):
        for x in d.split("\n"):
            if "davs://" in x or "root://" in x:
                file_locations.append(x)

    return file_locations

def get_closest_grid_path(lpn: str) -> str:
    closest_file = None
    current_time = 99999.0
    for file in get_grid_paths(lpn=lpn):
        server = file.split(":")[1].replace("//", "")

        time = ping(server)
        if time < current_time:
            closest_file = file
            current_time = time

    return closest_file
