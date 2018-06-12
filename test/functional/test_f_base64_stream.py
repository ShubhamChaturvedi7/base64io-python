# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Test Base64IO against a wide variety of values generated by hypothesis."""
import base64
import io

import pytest

from base64io import Base64IO

hypothesis = pytest.importorskip("hypothesis")
hypothesis_strategies = pytest.importorskip("hypothesis.strategies")

pytestmark = [pytest.mark.functional]

HYPOTHESIS_SETTINGS = hypothesis.settings(
    suppress_health_check=(
        hypothesis.HealthCheck.too_slow,
        hypothesis.HealthCheck.data_too_large,
        hypothesis.HealthCheck.hung_test,
        hypothesis.HealthCheck.large_base_example,
    ),
    timeout=hypothesis.unlimited,
    deadline=None,
    max_examples=1000,
    max_iterations=1500,
)
BINARY = hypothesis_strategies.binary()


@pytest.mark.hypothesis
@HYPOTHESIS_SETTINGS
@hypothesis.given(source=BINARY)
def test_cycle(source):
    source_b64 = base64.b64encode(source)
    encoded_stream = io.BytesIO()

    with Base64IO(encoded_stream) as encoded_wrapped:
        encoded_wrapped.write(source)
    encoded_stream.seek(0)

    decoded_stream = io.BytesIO()
    with Base64IO(encoded_stream) as encoded_wrapped:
        decoded_stream.write(encoded_wrapped.read())

    assert encoded_stream.getvalue() == source_b64
    assert decoded_stream.getvalue() == source
