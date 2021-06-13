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

from rpkimancer.asn1.mod import RPKI_ASPA_2020
from rpkimancer.resources import AFI, AsResourcesInfo
from rpkimancer.sigobj.base import EncapsulatedContent, SignedObject

log = logging.getLogger(__name__)

ProviderASSetInfo = typing.Optional[typing.Iterable[int]]


class AspaEContent(EncapsulatedContent):
    """encapContentInfo for RPKI ASPA Objects."""

    content_type = RPKI_ASPA_2020.id_ct_ASPA
    content_syntax = RPKI_ASPA_2020.ASProviderAttestation
    file_ext = "aspa"
    ip_resources = None

    def __init__(self, *,
                 version: int = 0,
                 afi: int,
                 customer_as: int,
                 provider_as_set: ProviderASSetInfo = None) -> None:
        """Initialise the encapContentInfo."""
        if provider_as_set is None:
            provider_as_set = list()
        else:
            provider_as_set = list(provider_as_set)
        data: typing.Dict[str, typing.Any] = {"version": version,
                                              "aFI": AFI[afi],
                                              "customerASID": customer_as}
        if provider_as_set is not None:
            data["providerASSET"] = list(provider_as_set)
        super().__init__(data)
        self._as_resources = [customer_as]

    @property
    def as_resources(self) -> typing.Optional[AsResourcesInfo]:
        """Get the AS Number Resources covered by this ASPA."""
        return self._as_resources


class Aspa(SignedObject, econtent_type=RPKI_ASPA_2020.ct_ASPA):
    """CMS ASN.1 ContentInfo for RPKI ASPA Objects."""

    econtent_cls = AspaEContent
