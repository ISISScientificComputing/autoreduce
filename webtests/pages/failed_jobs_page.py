# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Module for the failed jobs page model
"""
from webtests.pages.component_mixins.footer_mixin import FooterMixin
from webtests.pages.component_mixins.navbar_mixin import NavbarMixin
from webtests.pages.page import Page


class FailedJobsPage(Page, NavbarMixin, FooterMixin):
    """
    Page model class for failed jobs page
    """

    @staticmethod
    def url_path():
        """
        Return the path section of the failed jobs url
        :return: (str) Path section of the page url
        """
        return "/runs/failed/"