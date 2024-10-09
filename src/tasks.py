import subprocess


def format(item: str, template: str) -> tuple[str, bool]:
    return template.format(item), None


def command(item: str, command: str) -> tuple[str, bool]:
    proccess = subprocess.run(
        command.format(item),
        shell=True,
        capture_output=True,
        text=True,
    )

    return proccess.stdout.strip(), None if proccess.returncode == 0 else proccess.stderr.strip()


def ping(item: str) -> tuple[str, bool]:
    output, error = command(item, "ping -n 1 {}")

    return not error, error
