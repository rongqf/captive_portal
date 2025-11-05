import asyncio
import os
import shutil
import subprocess
import sys
import tempfile
import click

from datetime import datetime, timedelta
from multiprocessing import cpu_count
from configs import settings



@click.group()
def main():
    pass


@main.command()
def run_server():
    PROMETHEUS_MULTIPROC_DIR = tempfile.mkdtemp(
        prefix=f"metrics_{settings.PROJECT_NAME}",
        suffix=f"_{datetime.now().strftime('%Y-%m-%d.%H.%M.%S')}",
    )
    run_args = [
        sys.executable,
        "-OO",
        "-m",
        "uvicorn",
        "--host",
        "0.0.0.0",
        "--port",
        str(settings.PORT),
    ]
    if settings.DEBUG is False:
        run_args.extend(["--workers", str(cpu_count())])
    if settings.RELOAD:
        run_args.append("--reload")
    env = {
        "PYTHONPATH": ":".join(sys.path),
        "PROMETHEUS_MULTIPROC_DIR": PROMETHEUS_MULTIPROC_DIR,
    }
    env |= dict(os.environ)
    if PROJECT_CONFIG_PATH := os.environ.get("PROJECT_CONFIG_PATH"):
        env["PYTHONPATH"] = ":".join([PROJECT_CONFIG_PATH] + list(sys.path))
    try:
        subprocess.run(
            run_args + ["app:app"],
            env=env,
        )
    except Exception as ex:
        print("RUN SERVER ERROR", ex)
    finally:
        print("server shutting down, perform clean task")
        shutil.rmtree(PROMETHEUS_MULTIPROC_DIR, ignore_errors=True)

    
    
if __name__ in ("main", "__main__"):
    main()