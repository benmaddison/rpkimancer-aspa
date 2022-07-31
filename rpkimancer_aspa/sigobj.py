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
"""RPKI ASPA implementation - draft-ietf-sidrops-rpki-aspa."""

from __future__ import annotations

import logging
import typing

from rpkimancer.asn1.mod import RPKI_ASPA_2022
from rpkimancer.resources import AFI, AsResourcesInfo
from rpkimancer.sigobj.base import EncapsulatedContentType, SignedObject

log = logging.getLogger(__name__)

ProviderASSetInfo = typing.Iterable[typing.Tuple[int, typing.Optional[int]]]


def provider(as_id: int,
             afi: typing.Optional[int]) -> typing.Dict[str, typing.Any]:
    """Construct ProviderAS dict object."""
    provider_as: typing.Dict[str, typing.Any] = {"providerASID": as_id}
    if afi is not None:
        provider_as["afiLimit"] = AFI[afi]
    return provider_as


class AspaContentType(EncapsulatedContentType):
    """encapContentInfo for RPKI ASPA Objects."""

    asn1_definition = RPKI_ASPA_2022.ct_ASPA
    file_ext = "asa"
    ip_resources = None

    def __init__(self, *,
                 version: int = 0,
                 customer_as: int,
                 provider_as_set: ProviderASSetInfo) -> None:
        """Initialise the encapContentInfo."""
        providers = [provider(as_id, afi) for as_id, afi in provider_as_set]
        data: typing.Dict[str, typing.Any] = {"version": version,
                                              "customerASID": customer_as,
                                              "providers": providers}
        super().__init__(data)
        self._as_resources = [customer_as]

    @property
    def as_resources(self) -> typing.Optional[AsResourcesInfo]:
        """Get the AS Number Resources covered by this ASPA."""
        return self._as_resources


class Aspa(SignedObject[AspaContentType]):
    """CMS ASN.1 ContentInfo for RPKI ASPA Objects."""
