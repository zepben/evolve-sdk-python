#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["StreamingException", "UnsupportedOperationException"]


class StreamingException(Exception):
    pass


class UnsupportedOperationException(Exception):
    pass
