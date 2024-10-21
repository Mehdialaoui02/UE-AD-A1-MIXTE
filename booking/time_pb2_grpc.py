# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import time_pb2 as time__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in time_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TimeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTimes = channel.unary_unary(
                '/Time/GetTimes',
                request_serializer=time__pb2.Empty.SerializeToString,
                response_deserializer=time__pb2.Schedule.FromString,
                _registered_method=True)
        self.ShowMovies = channel.unary_unary(
                '/Time/ShowMovies',
                request_serializer=time__pb2.Date.SerializeToString,
                response_deserializer=time__pb2.MovieList.FromString,
                _registered_method=True)


class TimeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetTimes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShowMovies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TimeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTimes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTimes,
                    request_deserializer=time__pb2.Empty.FromString,
                    response_serializer=time__pb2.Schedule.SerializeToString,
            ),
            'ShowMovies': grpc.unary_unary_rpc_method_handler(
                    servicer.ShowMovies,
                    request_deserializer=time__pb2.Date.FromString,
                    response_serializer=time__pb2.MovieList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Time', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Time', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Time(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetTimes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Time/GetTimes',
            time__pb2.Empty.SerializeToString,
            time__pb2.Schedule.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ShowMovies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Time/ShowMovies',
            time__pb2.Date.SerializeToString,
            time__pb2.MovieList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)