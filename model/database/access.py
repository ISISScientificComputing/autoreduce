# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Common functions for accessing and creating records in the database
"""
from utils.clients.django_database_client import DatabaseClient


def start_database():
    """
    Create and connect a database client
    :return: The connected database client
    """
    database = DatabaseClient()
    database.connect()
    return database


def get_instrument(instrument_name, create=False):
    """
    Find the instrument record associated with the name provided in the database
    :param instrument_name: (str) The name of the instrument to search for
    :param create: (bool) If True, then create the record if it does not exist
    :return: (Instrument) The instrument object from the database
    """
    database = start_database()
    instrument_record = database.data_model.Instrument.objects \
        .filter(name=instrument_name).first()
    if not instrument_record and create:
        instrument_record = database.data_model.Instrument(name=instrument_record, is_active=True, is_paused=False)
        instrument_record.save()
    return instrument_record


def get_status(status_value, create=False):
    """
    Find the status record associated with the value provided in the database
    :param status_value: (str) The value of the status record e.g. 'Completed'
    :param create: (bool) If True, then create the record if it does not exist
    :return: (Status) The Status object from the database
    :raises: (ValueError): If status_value is not: Error, Queued, Processing, Completed or Skipped
    """
    # verbose values = ["Error", "Queued", "Processing", "Completed", "Stopped"]
    if status_value not in ['e', 'q', 'p', 'c', 's']:
        raise ValueError("Invalid status value passed")

    database = start_database()
    status_record = database.data_model.Status.objects.filter(value=status_value).first()
    if not status_record and create:
        status_record = database.data_model.Status(value=status_value)
        save_record(status_record)
    return status_record


def get_experiment(rb_number, create=False):
    """
    Find the Experiment record associated with the rb_number provided in the database
    :param rb_number: (str) The rb_number of the Experiment record e.g. 12345
    :param create: (bool) If True, then create the record if it does not exist
    :return: (Experiment) The Experiment object from the database
    """
    database = start_database()
    experiment_record = database.data_model.Experiment.objects \
        .filter(reference_number=rb_number).first()
    if not experiment_record and create:
        experiment_record = database.data_model.Experiment(reference_number=rb_number)
        save_record(experiment_record)
    return experiment_record


def get_software(name, version, create=False):
    """
    Find the Software record associated with the name and version provided
    :param name: (str) The name of the software
    :param version: (str) The version number of the software
    :param create: (bool) If True, then create the record if it does not exist
    :return: (Software) The Software object from the database
    """
    database = start_database()
    software_record = database.data_model.Software.objects \
        .filter(name=name) \
        .filter(version=version) \
        .first()
    if not software_record and create:
        software_record = database.data_model.Software(name=name, version=version)
        save_record(software_record)
    return software_record


def get_reduction_run(instrument, run_number):
    """
    Returns a QuerySet of all ReductionRun versions that have the given instrument/run_number
    :param instrument: (str) The name of the instrument to search for
    :param run_number: (str/int) The run number to search for
    :return: (QuerySet[ReductionRun,]) ReductionRun records that match the criteria

    Note: The query set could contain multiple records or None
    """
    database = start_database()
    instrument_record = get_instrument(instrument)
    # if instrument not yet in database then return empty record
    if not instrument_record:
        return instrument_record
    return database.data_model.ReductionRun.objects \
        .filter(instrument=instrument_record.id) \
        .filter(run_number=run_number)


def find_highest_run_version(experiment, run_number) -> int:
    """
    Search for the highest run version in the database
    :param experiment: (str) The experiment number associated
    :param run_number: (int) The run number to search for
    :return: (int) The highest known version number for a given reduction job
    """
    last_run = experiment.reduction_runs.filter(run_number=run_number).order_by('-run_version').first()
    if last_run:  # previous run exists - increment version by 1 for this run
        return last_run.run_version + 1
    else:  # previous run doesn't exist - start at 0
        return 0


def save_record(record):
    """
    Save a record to the database
    :param record: (DbObject)The record to save

    Note: This is mostly a wrapper to aid unit testing
    """
    record.save()
