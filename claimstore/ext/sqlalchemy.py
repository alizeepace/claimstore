# -*- coding: utf-8 -*-
#
# This file is part of ClaimStore.
# Copyright (C) 2015 CERN.
#
# ClaimStore is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ClaimStore is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClaimStore; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
# USA.

"""Sqlalchemy setup."""

import click
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cli import with_appcontext
from flask_registry import ModuleAutoDiscoveryRegistry, RegistryProxy

db = SQLAlchemy()

models = RegistryProxy(
    'models',  # Registry namespace
    ModuleAutoDiscoveryRegistry,
    'models'   # Module name (i.e. models.py)
)


def setup_app(app):
    """Setup sqlalchemy."""
    # Add extension CLI to application.
    app.cli.add_command(initdb)
    app.cli.add_command(dropalldb)
    db.init_app(app)


@click.command()
@with_appcontext
def initdb():
    """Initialise database."""
    list(models)  # load all modules
    db.create_all()


@click.command()
@with_appcontext
def dropalldb():
    """Drop database."""
    db.drop_all()
