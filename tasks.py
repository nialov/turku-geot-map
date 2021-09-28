"""
Tasks to create turku geot map.
"""
from invoke import task

from pathlib import Path


@task
def make(c):
    """
    Create map.
    """
    c.run(
        " ".join(
            (
                "kapalo-py",
                "remote-update",
                "--remote-sql-dir=kapalo/kapalo_sql_turku_geot_2021",
                "--remote-images-dir=kapalo/kapalo_imgs_turku_geot_2021",
            )
        )
    )
    print("Resizing images")
    c.run(
        " ".join(
            (
                "kapalo-py",
                "resize-images",
            )
        )
    )

    extra_dataset_paths = [
        Path("data/turku_lidar_infinity_geothermal_sites_traces.geojson"),
        Path("data/turku_lidar_lineaments_200k_traces.geojson"),
    ]
    print("Creating map")
    c.run(
        " ".join(
            (
                "kapalo-py",
                "compile-webmap",
                "--projects=GTK_Geotermiset",
                *[f"--extra-datasets={path}" for path in extra_dataset_paths],
                *["--extra-style-functions=Lineament" for _ in extra_dataset_paths],
                *[f"--extra-colors={col}" for col in ("red", "black")],
            )
        )
    )
