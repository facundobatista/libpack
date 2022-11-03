# Copyright 2022 Facundo Batista
# https://github.com/facundobatista/pylibpack

"""A simple way to pack a multiple-files library into a single .py."""

import base64
import io
import sys
import tempfile
import zipfile

if len(sys.argv) != 2:
    print("USAGE: pylibpack.py <library package directory>")
    exit(1)

package_path = sys.argv[1]
package_name = package_path.strip("/").split("/")[-1]

mem_zip = io.BytesIO()

with tempfile.NamedTemporaryFile() as tf:
    with zipfile.PyZipFile(tf.name, mode="w") as zp:
        zp.writepy(package_name)

    with zipfile.ZipFile(tf.name, mode="r") as src:
        with zipfile.ZipFile(mem_zip, mode="w") as dst:
            members = src.namelist()
            for member in members:
                zipinfo = src.getinfo(member)
                zipinfo.filename = "packed_" + zipinfo.filename
                dst.writestr(zipinfo, src.read(member))

encoded_zipped_package = base64.b64encode(mem_zip.getvalue())


unpacker = f"""
import base64
import sys
import tempfile

magic = {encoded_zipped_package}

with tempfile.NamedTemporaryFile(suffix=".zip") as __pypack_tf:
    with open(__pypack_tf.name, "wb") as fh:
        fh.write(base64.b64decode(magic))
    del magic, fh

    sys.path.append(__pypack_tf.name)
    from packed_{package_name} import *
    sys.path.remove(__pypack_tf.name)
"""
with open(f"{package_name}.py", "wt", encoding="utf8") as fh:
    fh.write(unpacker)
