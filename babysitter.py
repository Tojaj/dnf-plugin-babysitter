import logging
import dnf.plugin
from dnf.cli.output import Output
from dnf.yum.i18n import _

class BabysitterPlugin(dnf.plugin.Plugin):

    name = 'babysitter'

    def __init__(self, base=None, *args):
        self.logger = logging.getLogger("dnf")
        self.base = base
        self.logger.info(_("The Babysitter plugin is active"))

    def config(self):
        if not self.base or not self.base.output:
            return
        self.original_remove = self.base.remove
        self.base.remove = self.babysitting_remove

    def _seriously(self, msg):
        self.base.output.logger.info(msg)
        return self.base.output.userconfirm()

    def babysitting_remove(self, pkgs):
        if "kernel" == pkgs:
            if not self._seriously(_("Do you really want to remove all your "
                                     "kernels (including the running one)?")):
                pkgs=""
        return self.original_remove(pkgs)
