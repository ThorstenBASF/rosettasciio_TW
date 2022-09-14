# -*- coding: utf-8 -*-
# Copyright 2007-2022 The HyperSpy developers
#
# This file is part of RosettaSciIO.
#
# RosettaSciIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RosettaSciIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RosettaSciIO. If not, see <https://www.gnu.org/licenses/#GPL>.

import importlib


def test_import_version():
    from rsciio import __version__


def test_rsciio_dir():
    import rsciio

    assert dir(rsciio) == ["IO_PLUGINS", "__version__"]


def test_import_all():
    from rsciio import IO_PLUGINS

    plugin_name_to_remove = []

    # Remove plugins which require not installed optional dependencies
    try:
        import skimage
    except:
        plugin_name_to_remove.append("Blockfile")

    try:
        import mrcz
    except:
        plugin_name_to_remove.append("MRCZ")

    try:
        import tifffile
    except:
        plugin_name_to_remove.append("TIFF")
        plugin_name_to_remove.append("Phenom")

    try:
        import pyUSID
    except:
        plugin_name_to_remove.append("USID")

    try:
        import zarr
    except:
        plugin_name_to_remove.append("ZSPY")

    IO_PLUGINS = list(
        filter(
            lambda plugin: plugin["format_name"] not in plugin_name_to_remove,
            IO_PLUGINS,
        )
    )

    for plugin in IO_PLUGINS:
        importlib.import_module(plugin["api"])


def test_format_name_aliases():
    from rsciio import IO_PLUGINS

    for reader in IO_PLUGINS:
        assert isinstance(reader["format_name"], str)
        if reader.get("format_name_aliases"):
            assert isinstance(reader["format_name_aliases"], list)
            for aliases in reader["format_name_aliases"]:
                assert isinstance(aliases, str)
        assert isinstance(reader["description"], str)
        assert isinstance(reader["full_support"], bool)
        assert isinstance(reader["file_extensions"], list)
        for extensions in reader["file_extensions"]:
            assert isinstance(extensions, str)
        assert isinstance(reader["default_extension"], int)
        if isinstance(reader["writes"], list):
            for i in reader["writes"]:
                assert isinstance(i, list)
        else:
            assert isinstance(reader["writes"], bool)
        assert isinstance(reader["non_uniform_axis"], bool)
