# Copyright (c) 2021 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rpkincant conjure plugins for RPKI ASPA objects."""

from __future__ import annotations

import logging
import typing

from rpkimancer.cli import Args
from rpkimancer.cli.conjure import (ConjurePlugin,
                                    DEFAULT_CA_AS_RESOURCES,
                                    META_AS,
                                    PluginReturn)

if typing.TYPE_CHECKING:
    from rpkimancer.cert import CertificateAuthority

log = logging.getLogger(__name__)

META_AFI = "<afi>"
META_PROVIDER_AS = "<asn[:(4|6)]>"


def provider_as(spec: str) -> typing.Tuple[int, typing.Optional[int]]:
    """Argument type checker for `ASID:AFI` pair."""
    afi: typing.Optional[int]
    try:
        as_id, afi = map(int, spec.split(":", 1))
    except ValueError:
        as_id = int(spec)
        afi = None
    return as_id, afi


class ConjureAspa(ConjurePlugin):
    """rpkincant conjure plugin for RPKI ASPA Objects."""

    def init_parser(self) -> None:
        """Set up command line argument parser."""
        self.parser.add_argument("--aspa-customer-as",
                                 type=int,
                                 default=DEFAULT_CA_AS_RESOURCES[0],
                                 metavar=META_AS,
                                 help="ASPA customer AS "
                                      "(default: %(default)s)")
        self.parser.add_argument("--aspa-provider-asns",
                                 nargs="+", type=provider_as,
                                 default=[(65001, None), (65002, 4)],
                                 metavar=META_PROVIDER_AS,
                                 help="ASPA provider ASNs "
                                      "(default: %(default)s)")

    def run(self,
            parsed_args: Args,
            ca: CertificateAuthority,
            *args: typing.Any,
            **kwargs: typing.Any) -> PluginReturn:
        """Run with the given arguments."""
        # create ASPA object
        from .sigobj import Aspa
        log.info("creating ASPA object")
        Aspa(issuer=ca,
             customer_as=parsed_args.aspa_customer_as,
             provider_as_set=parsed_args.aspa_provider_asns)
        return None
