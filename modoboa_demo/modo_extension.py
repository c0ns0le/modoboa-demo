"""Demo extension."""

from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.lib.parameters import save_admin

from modoboa_admin.factories import DomainFactory, MailboxFactory


class Demo(ModoExtension):

    """The demo extension."""

    name = "modoboa_demo"
    label = ugettext_lazy("Demo")
    version = "1.0.0"
    description = ugettext_lazy("Demonstration features for Modoboa")

    def load_initial_data(self):
        """Load demo data."""
        domain = DomainFactory.create(name="demo.local")
        dadmin = MailboxFactory.create(
            address="admin", domain=domain, user__username="admin@demo.local",
            user__groups=["DomainAdmins"]
        )
        dadmin.user.set_password("admin")
        dadmin.user.save()
        domain.add_admin(dadmin.user)
        user = MailboxFactory.create(
            address="user", domain=domain, user__username="user@demo.local",
            user__groups=["SimpleUsers"]
        )
        user.user.set_password("user")
        user.user.save()

        # Configure parameters
        save_admin("HANDLE_MAILBOXES", "yes", app="modoboa_admin")
        save_admin("AM_PDP_MODE", "inet", app="modoboa_amavis")
        save_admin("RRD_ROOTDIR", "/srv/modoboa/rrdfiles", app="modoboa_stats")
        save_admin(
            "STORAGE_DIR", "/srv/modoboa/pdfcredentials",
            app="modoboa_pdfcredentials")

exts_pool.register_extension(Demo)
