# -*- coding: utf-8 -*-

import abc

from ..utils import Snowflake


def maybe_impossible(func):
    """A decorator that wraps methods whose executions may be impossible.

    This decorator basically wraps around some methods in the general Abstract Base Class
    for all models of this library. As not all models provide an ID value, this defaults to 0.
    And for such cases, there are special methods that should raise an error because of that
    incorrect value.

    Parameters
    ----------
    func : typing.Callable
        The method that was decorated by this function.

    Raises
    ------
    NotImplementedError
        If the execution of a function is impossible due to a missing or invalid ID,
        this error will be raised.
    """

    def decorator(*args, **kwargs):
        if not hasattr(args[0], 'id'):
            raise NotImplementedError
        return func(*args, **kwargs)

    return decorator


class Model(abc.ABC):
    """Represents an Abstract Base Class for all models in this library.

    Most of this library's implementations of the Discord API models implement
    this ABC which mainly provides some core functionality.

    Attributes
    ----------
    id : int, optional
        The ID of the model. This should always be retrieved from the Discord API.
        For the case a model doesn't have an ID, defaults to 0.
    """

    def __init__(self, model_id=0, *, http):
        self._json = None
        self.id = model_id
        self._http = http

    @maybe_impossible
    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __repr__(self):
        return '<shitcord.Model id={}>'.format(self.id)

    @maybe_impossible
    def __hash__(self):
        return self.id

    @property
    @maybe_impossible
    def created_at(self):
        return Snowflake(self.id).timestamp

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        return object.__setattr__(self, key, value)

    @abc.abstractmethod
    def to_json(self, **kwargs):
        pass
