import subprocess


def _check_call(cmd, dry_run):
    if dry_run:
        print(cmd)
    else:
        return subprocess.check_call(cmd)


def _check_output(cmd, dry_run):
    if dry_run:
        print(cmd)
        return "fake-container"
    else:
        return subprocess.check_output(cmd).decode().strip()


def arch_specific_tag(tag, arch):
    return tag + "-" + arch.replace("/", "-")


class BuildahManifest:

    def __init__(self, *, registry, name, tag, dry_run=False):
        self.registry = registry
        self.name = name
        self.tag = tag
        self.dry_run = dry_run
        self.__create_manifest()

    @property
    def full_name(self):
        return f"{self.registry}/{self.name}:{self.tag}"

    def __create_manifest(self):
        _check_call(["buildah", "manifest", "create", self.full_name], self.dry_run)


class BuildahContainer:

    def __init__(
        self,
        *,
        registry,
        name,
        tag,
        base_image,
        arch=None,
        manifest=None,
        dry_run=False,
    ):
        self.registry = registry
        self.name = name
        self.tag = tag
        self.base_image = base_image
        self.arch = arch
        self.manifest = manifest
        self.dry_run = dry_run

        self.__container = self.__start_container()
        self.__committed = False

    @property
    def full_name(self):
        return f"{self.registry}/{self.name}:{self.tag}"

    def __start_container(self):
        cmd = ["buildah", "from"]
        if self.arch:
            cmd.append("--arch")
            cmd.append(self.arch)
        cmd.append(self.base_image)
        return _check_output(cmd, self.dry_run)

    def run(self, args):
        if self.__committed:
            raise RuntimeError("Cannot run commands after a container is committed")
        _check_call(["buildah", "run", self.__container, "--"] + args, self.dry_run)

    def config(self, *, env=None, cmd=None, entrypoint=None):
        if self.__committed:
            raise RuntimeError("Cannot alter config after a container is committed")
        config_cmd = ["buildah", "config"]
        if env:
            config_cmd.append("--env")
            config_cmd.append(env)
        if entrypoint:
            config_cmd.append("--entrypoint")
            config_cmd.append(entrypoint)
        if cmd:
            config_cmd.append("--cmd")
            config_cmd.append(cmd)
        config_cmd.append(self.__container)
        _check_call(config_cmd, self.dry_run)

    def commit(self):
        if self.__committed:
            raise RuntimeError("Container is already committed")
        cmd = ["buildah", "commit"]
        if self.manifest:
            cmd.append("--manifest")
            cmd.append(self.manifest.full_name)
        cmd.append(self.__container)
        cmd.append(self.full_name)
        _check_call(cmd, self.dry_run)
        self.__committed = True
