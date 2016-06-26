from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.choices import ACTIONS


class BaseTransaction(BaseUuidModel):

    tx = models.BinaryField()

    tx_name = models.CharField(
        max_length=64)

    tx_pk = models.UUIDField(
        db_index=True)

    producer = models.CharField(
        max_length=200,
        db_index=True,
        help_text='Producer name')

    action = models.CharField(
        max_length=1,
        choices=ACTIONS)

    timestamp = models.CharField(
        max_length=50,
        db_index=True)

    consumed_datetime = models.DateTimeField(
        null=True,
        blank=True)

    consumer = models.CharField(
        max_length=200,
        null=True,
        blank=True)

    is_ignored = models.BooleanField(
        default=False,
    )

    is_error = models.BooleanField(
        default=False)

    error = models.TextField(
        max_length=1000,
        null=True,
        blank=True)

    batch_seq = models.IntegerField(null=True, blank=True)

    batch_id = models.IntegerField(null=True, blank=True)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.tx_name)

    def __str__(self):
        return '</{}.{}/{}/{}/{}/>'.format(
            self._meta.app_label, self._meta.model_name, self.id, self.tx_name, self.action)

    def view(self):
        url = reverse('render_url',
                      kwargs={
                          'model_name': self._meta.object_name.lower(),
                          'pk': self.pk})
        ret = ('<a href="{url}" class="add-another" id="add_id_report" '
               'onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" '
               'width="10" height="10" alt="View"/></a>'.format(url=url))
        return ret
    view.allow_tags = True

    class Meta:
        abstract = True
