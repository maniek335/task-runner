import subprocess

from charset_normalizer import from_bytes


def format(item: str, template: str) -> tuple[str, str | None]:
    return template.format(item), None


def command(item: str, command: str) -> tuple[str, str | None]:
    proccess = subprocess.run(
        command.format(item),
        shell=True,
        capture_output=True,
    )

    stdout = str(from_bytes(proccess.stdout).best())
    stderr = str(from_bytes(proccess.stderr).best())

    return stdout, None if proccess.returncode == 0 else stderr


def ping(item: str) -> tuple[str, str | None]:
    output, error = command(item, "ping -n 1 {}")

    return "True" if error is None else "False", error
