#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import warnings
from typing import Optional, BinaryIO
from urllib.parse import urlparse

import grpc
from zepben.auth.client import ZepbenTokenFetcher, create_token_fetcher

from zepben.evolve import GrpcChannelBuilder

__all__ = ["connect", "connect_async", "connect_tls", "connect_insecure", "connect_with_password", "connect_with_secret"]

from zepben.evolve.streaming.grpc.channel_builder import AuthTokenPlugin

GRPC_READY_TIMEOUT = 20  # seconds


def connect_insecure(
    host: str = "localhost",
    rpc_port: int = 50051
) -> grpc.aio.Channel:
    return GrpcChannelBuilder().for_address(host, rpc_port).build()


def connect_tls(
    host: str = "localhost",
    rpc_port: int = 50051,
    ca_filename: Optional[str] = None
) -> grpc.aio.Channel:
    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).build()


def connect_with_secret(
    client_id: str,
    client_secret: str,
    host: str = "localhost",
    rpc_port: int = 50051,
    conf_address: Optional[str] = None,
    conf_ca_filename: Optional[str] = None,
    auth_ca_filename: Optional[str] = None,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    if {"audience", "issuer_domain"} <= kwargs.keys():
        # noinspection PyArgumentList
        token_fetcher = ZepbenTokenFetcher(**kwargs)
    else:
        token_fetcher = create_token_fetcher(
            conf_address=conf_address or f"https://{host}/ewb/auth",
            conf_ca_filename=conf_ca_filename,
            auth_ca_filename=auth_ca_filename
        )

    if token_fetcher:
        return _connect_with_secret_using_token_fetcher(token_fetcher, client_id, client_secret, host, rpc_port, ca_filename)
    else:
        return connect_tls(host, rpc_port, ca_filename)


def connect_with_password(
    client_id: str,
    username: str,
    password: str,
    host: str = "localhost",
    rpc_port: int = 50051,
    conf_address: Optional[str] = None,
    conf_ca_filename: Optional[str] = None,
    auth_ca_filename: Optional[str] = None,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    if {"audience", "issuer_domain"} <= kwargs.keys():
        # noinspection PyArgumentList
        token_fetcher = ZepbenTokenFetcher(**kwargs)
    else:
        token_fetcher = create_token_fetcher(
            conf_address=conf_address or f"https://{host}/ewb/auth",
            conf_ca_filename=conf_ca_filename,
            auth_ca_filename=auth_ca_filename
        )

    if token_fetcher:
        return _connect_with_password_using_token_fetcher(token_fetcher, client_id, username, password, host, rpc_port, ca_filename)
    else:
        return connect_tls(host, rpc_port, ca_filename)


def _connect_with_secret_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    client_secret: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str]
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["client_secret"] = client_secret
    token_fetcher.token_request_data["grant_type"] = "client_credentials"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build()


def _connect_with_password_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    username: str,
    password: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str]
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["username"] = username
    token_fetcher.token_request_data["password"] = password
    token_fetcher.token_request_data["grant_type"] = "password"
    token_fetcher.token_request_data["scope"] = "offline_access"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build()


def _conn(host: str = "localhost", rpc_port: int = 50051, conf_address: str = None, client_id: Optional[str] = None,
          username: Optional[str] = None, password: Optional[str] = None, client_secret: Optional[str] = None, pkey=None, cert=None, ca=None,
          token_fetcher: Optional[ZepbenTokenFetcher] = None, secure: bool = False, verify_auth_certificates=False, conf_ca=None, auth_ca=None):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `token_fetcher` is not provided.
        Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `token_fetcher` A token fetcher that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    `verify_auth_certificate` Whether to authenticate the certificate from the authentication provider.
    `auth_ca` Filename of CA bundle for the authentication provider, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    if secure:
        if conf_address is None:
            conf_address = f"http://{host}/auth"
        # Channel credential will be valid for the entire channel
        channel_credentials = grpc.ssl_channel_credentials(ca, pkey, cert)

        # parsing the conf_address to host port and path
        parsed_url = urlparse(
            conf_address
        )
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path

        if token_fetcher:
            call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(token_fetcher=token_fetcher))

            # Combining channel credentials and call credentials together
            composite_credentials = grpc.composite_channel_credentials(
                channel_credentials,
                call_credentials,
            ) if channel_credentials else call_credentials
            channel = grpc.aio.secure_channel(f"{host}:{rpc_port}", composite_credentials)
        elif client_id and username and password:

            # Create a basic ClientCredentials authenticator
            token_fetcher = create_token_fetcher(host, port, path, verify_auth_certificates, conf_ca_filename=conf_ca, auth_ca_filename=auth_ca)
            token_fetcher.token_request_data.update({
                'client_id': client_id,
                'username': username,
                'password': password,
                'grant_type': 'password',
                'scope': 'offline_access'
            })

            call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(token_fetcher))

            # Combining channel credentials and call credentials together
            composite_credentials = grpc.composite_channel_credentials(
                channel_credentials,
                call_credentials,
            ) if channel_credentials else call_credentials
            channel = grpc.aio.secure_channel(f"{host}:{rpc_port}", composite_credentials)

        elif client_id and client_secret:
            # Create a basic ClientCredentials authenticator
            token_fetcher = create_token_fetcher(host, port, path, verify_auth_certificates, conf_ca_filename=conf_ca, auth_ca_filename=auth_ca)
            token_fetcher.token_request_data.update({'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'})

            call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(token_fetcher))

            # Combining channel credentials and call credentials together
            composite_credentials = grpc.composite_channel_credentials(
                channel_credentials,
                call_credentials,
            ) if channel_credentials else call_credentials
            channel = grpc.aio.secure_channel(f"{host}:{rpc_port}", composite_credentials)
        else:
            channel = grpc.aio.secure_channel(f"{host}:{rpc_port}", channel_credentials)
    else:
        if client_id or client_secret or username or password or pkey or cert:
            warnings.warn("An insecure connection is being used but some credentials were specified for connecting, did you forget to set secure=True?")
        channel = grpc.aio.insecure_channel(f"{host}:{rpc_port}")

    return channel


@contextlib.contextmanager
def connect(host: str = "localhost",
            rpc_port: int = 50051,
            conf_address: str = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            pkey=None,
            cert=None,
            ca=None,
            token_fetcher: Optional[ZepbenTokenFetcher] = None,
            secure=False,
            verify_auth_certificates=False,
            conf_ca=None,
            auth_ca=None):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `token_fetcher` is not provided.
        Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `token_fetcher` A token fetcher that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    `verify_auth_certificate` Whether to authenticate the certificate from the authentication provider.
    `auth_ca` Filename of CA bundle for the authentication provider, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    warnings.warn('The connect function is deprecated. It will be replaced with other functions like connect_secure.', DeprecationWarning, stacklevel=2)
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, token_fetcher, secure, verify_auth_certificates,
                conf_ca, auth_ca)


@contextlib.asynccontextmanager
async def connect_async(host: str = "localhost",
                        rpc_port: int = 50051,
                        conf_address: str = None,
                        client_id: Optional[str] = None,
                        client_secret: Optional[str] = None,
                        username: Optional[str] = None,
                        password: Optional[str] = None,
                        pkey=None,
                        cert=None,
                        ca=None,
                        token_fetcher: Optional[ZepbenTokenFetcher] = None,
                        secure=False,
                        verify_auth_certificates=False,
                        conf_ca=None,
                        auth_ca=None):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `token_fetcher` is not provided.
        Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `token_fetcher` A token fetcher that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    `verify_auth_certificate` Whether to authenticate the certificate from the authentication provider.
    `auth_ca` Filename of CA bundle for the authentication provider, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    warnings.warn('The connect_async function is deprecated. It will be replaced with other functions like connect_secure_async.',
                  DeprecationWarning, stacklevel=2)
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, token_fetcher, secure, verify_auth_certificates,
                conf_ca, auth_ca)
