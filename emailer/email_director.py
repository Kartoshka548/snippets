import mandrill
import ast
import json
import random
import itertools

from lib import db
from lib.logger import Logger
import email_type
import settings


logger = Logger(__name__)


class MailTypeDescriptor(object):
    """
    Mail Type Descriptor
    """
    def __init__(self, name, iterable={}):
        self.name = name
        self.iterable = iterable

    def __set__(self, instance, value):
        assert_msg = 'Value type must be integer - not %s (provided %s)'
        assert isinstance(value, int), assert_msg % (
            type(value), value)
        if instance is None:
            return self
        if self.iterable and value not in self.iterable:
            raise NotImplementedError('Mail type # %s is not implemented' % value)
        instance.__dict__['_%s' % self.name] = value

    def __get__(self, instance, cls=None):
        if not instance:
            raise NotImplemented('Instantiate a class and call this attribute from within.')
        _v = instance.__dict__['_%s' % self.name]
        return self.iterable.get(_v)


class EmailDirector(db.DB):
    """
    Director class which decides which class to instantiate for the email type.
    It is also responsible for sending out the emails once build.
    """
    _iterator = {_c.dbkey(): _c for _c in email_type.Email.__subclasses__()}
    mail_type = MailTypeDescriptor(name='mail_type', iterable=_iterator)
    prepare_email = lambda s: s.mail_type(dict(client=s.client, **s.job)).build_email()
    __getattr__ = lambda self, item: getattr(self.mail_type, item)

    def __init__(self, mail_job_id, event_id, extra_param, mail_type, *args, **kwargs):
        self.job = locals()
        super(__class__, self).__init__()
        self.mail_type = mail_type
        self.event_id = event_id
        self.job_id = mail_job_id
        self.params, self.submid = [], []

    def __call__(self):
        """
        Main entrance.
        Executed from email scheduler.
        """
        logger.info('Mail Type: %s' % self.mail_type)
        Mail = self.prepare_email()
        self.send_email(*Mail.mailjob)
        self.update_mail_job(Mail)

    @property
    def client(self):
        """
        Get client (not end-user) details from specific event
        """
        sql = '''
            SELECT ...
        ;'''
        _r = self.select_one(sql, (self.event_id,), True)
        assert _r, 'No client found for event #%s' % self.event_id
        return dict(_r)

    def _keep_communication(self, r):
        """
        self.job_id, _r['email'], _r['status'], _r.get('reject_reason', ''), _r['_id']
        """
        # logger.debug(r)
        for _d in r:
            sql = '''
                INSERT into ...
            ;'''
            _args = self.job_id, _d['email'], _d['status'], _d.get('reject_reason', ''), _d['_id']
            self.insert(sql, _args)

    def _sent_from(self):
        """
        Find out who should be ready to listen to user replies.
        Client must define dictionary
        """
        _mta = self.client.get('...key...')
        _m = 'Reply address for %s (ID #%s) for %s (ID #%s) was not found.'
        try:
            _key= random.choice(xrange(2)) and self.dbkey() or self.mail_type.dbkey()  # same
            adb = _mta and ast.literal_eval(json.loads(_mta)) or settings.FROM_ADDR
            _d = adb.get('%s' % _key) or adb.get(_key)
            assert _d, _m % (self.mail_type, _key, self.client['name'], self.client['id'])
        except AssertionError as e:
            logger.debug(e)
            _d = dict(from_email='...@.......',
                      from_name='... ...')
        return _d

    def send_email(self, recipient, mail):
        """
        Email template prepared and ready to be sent out,
        If client has mailserver configured (boolean),
        extract values from config json.
        """
        conf, _mc = {}, 'mailserver_configuration'
        mailserver_enabled = self.client[_mc]
        _args = self.client['...'], self.client['...']
        if mailserver_enabled:
            try:
                conf = self.client['...']['...'][_mc]
            except KeyError:
                _m = '%s (ID#%d) mailserver configuration was not found'
                logger.debug(_m % _args)
                pass
            _p = conf.get('...')
            if _p != 'MANDRILL':
                # it can be any mail company
                _m = '%s (ID#%s) %s mailserver is not defined in config.'
                raise StandardError(_m % (_args + (_p,)))

        _cl = '%s (ID#%d)' % _args if mailserver_enabled else 'default'
        logger.info('Mail will be sent through %s mailserver configuration' % _cl)

        _msg_a = dict(auto_html=None, to=[{'email': recipient}])
        _msg_b = {_k: mail[_k] for _k in ('text', 'html', 'subject')}
        _msg_c = self._sent_from()
        message = itertools.chain(*map(dict.items, (_msg_a, _msg_b, _msg_c)))
        MANDRILL_API_KEY = conf.get('...', {}).get('...')
        self.mandrill(
            datablock=dict(message),
            api_key=MANDRILL_API_KEY or settings.MANDRILL_API_KEY)
        logger.info('Mail successfully sent to %s.' % recipient)
        return True

    def mandrill(self, api_key, datablock):
        try:
            mandrill_client = mandrill.Mandrill(api_key)
            _r = mandrill_client.messages.send(message=datablock, async=False, ip_pool='...')
        except mandrill.Error as e:
            logger.error('A Mandrill error occured: %s - %s' % (e.__class__, e))
            raise
        else:
            self._keep_communication(iter(_r))
            return True

    def update_mail_job(self, obj, status=settings.JOB_STATUS['...']):
        """
        Mail job is finished!
        Set status to '...' in ...
        """
        sql = """
            UPDATE ...
        ;"""
        self.update(sql, (status, self.job_id))
        self.update_status(obj)
