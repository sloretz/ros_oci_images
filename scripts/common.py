import subprocess
import time


def _full_name(registry, name, tag):
    return f"{registry}/{name}:{tag}"


def retry_with_backoff(func):
    def new_func(*args, **kwargs):
        for i in range(5):
            try:
                return func(*args, **kwargs)
            except subprocess.CalledProcessError:
                print("Hmm command failed, retrying in case it's network related")
                time.sleep(i * i * 15)
        raise RuntimeError("Unable to build image")

    return new_func


def _buildah_manifest(registry, name, tag, image_names, push, dry_run):
    full_name = _full_name(registry, name, tag)
    print("MANIFEST", full_name)

    create_cmd = ["buildah", "manifest", "create", full_name]
    if dry_run:
        print(create_cmd)
    else:
        subprocess.check_call(create_cmd)

    for image in image_names:
        add_cmd = ["buildah", "manifest", "add", full_name, image]
        if dry_run:
            print(add_cmd)
        else:
            subprocess.check_call(add_cmd)

    if push:
        # Pushing as we go reduces impact of rate limiting on github packages
        _buildah_push_manifest(full_name, dry_run)


@retry_with_backoff
def _buildah_push_image(image_name, dry_run):
    cmd = ["buildah", "push", image_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


@retry_with_backoff
def _buildah_push_manifest(image_name, dry_run):
    cmd = ["buildah", "manifest", "push", image_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def _image_exists(full_name):
    cmd = ["buildah", "inspect", full_name]
    ret = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0 == ret