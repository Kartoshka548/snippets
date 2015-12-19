import json
import datetime
import types
import os

from lib.db import DB
from lib.logger import Logger
from lib.template import Template
import settings


logger = Logger(__name__)

class EmailMetaClass(type):
    __str__ = lambda s: s.__name__
    _dbkeys = {
        '...':         '...',               # 1
        '...':         '...',               # 2
        # ______:      '...',     # 3_not-used
    }


class TemplateDescriptor(object):
    """
    Template Descriptor,
    used in Email (base class) to reveal client directory containing templates
    """
    def __init__(self, label=None): self.label = label

    def __set__(self, instance, value):
        if instance is None:
            return self
        assert isinstance(value, types.StringTypes), 'Value type must be string - not %s' % type(value)
        instance.__dict__['__%s_template' % self.label] = value

    def __get__(self, instance, cls=None):
        if not instance:
            raise NotImplemented('Instantiate a class and call this attribute from within.')
        _tmpl = instance.__dict__['__%s_template' % self.label]
        _folder = self._template_location(instance, _tmpl)
        return _folder + _tmpl

    def _template_location(self, instance, template):
        """
        Look for template inside client folder.
            a) check if folder exists,
            b) does the file exist?
        Return string with a folder or empty string if not found.
        In addition, log failure.
        """
        client_id, def_client_id = (_c['...'] for _c in (
            instance.client, instance.default_client))
        path = os.path.join(
            settings.TEMPLATE_PATH, '%s' % client_id, template)
        _tmpl_found = os.path.exists(path)
        if not _tmpl_found and client_id != def_client_id:
            _stf = template, instance.client['name'], client_id
            _msg = "... wasn't found. Default template will be used."
            logger.debug(_msg % _stf)
        return _tmpl_found and '%s/' % client_id or ''


class Email(DB):
    """
    Superclass for all email instances
    """
    __metaclass__ = EmailMetaClass  # MRO
    email_template = TemplateDescriptor('email')
    subject_template = TemplateDescriptor('subject')
    _undefined = '#undefined'

    @classmethod
    def dbkey(cls):
        """
        Selects from profile.mail_type name
        :return: id (integer)
        """
        sql = '''
            SELECT ...
        ;'''
        # crime against humanity
        # instantiating just for getting an access to a method
        _d = {}.fromkeys(('...', '...'), None)
        _r = cls(_d).select_one(sql, (cls._dbkeys[cls.__name__],))
        if _r: return _r
        raise ValueError('... was not found' % cls.__name__)

    @property
    def default_client(self):
        sql = '''
            SELECT ...
        ;'''
        _args = settings.DEFAULT_CLIENT_KEY,
        _r = self.select_one(sql, _args, return_row=True)
        if _r: return _r
        _msg = 'No ... %s was found in %s environment'
        raise ValueError(_msg % (_args, settings.environment))

    def __init__(self, job):
        super(Email, self).__init__()
        self.job = job
        self.client = self.job.pop('...')
        self.params, self.submid = [], []
        self.connect()

    def get_event_data(self):
        """
        Returns data for an event given an id.
        """
        sql = '''
            SELECT ...
        ;'''
        _a = self.job['...'],
        _r = self.select(sql, _a)
        assert _r, '... Aborting...' % _a
        return json.loads(dict(_r[0]).get('...'))

    def update_status(self, *args, **kwargs): pass

    def _build_response_link(self):
        """
        Links which will be included in customer communication emails
        """
        _c = self.client['...']
        if not _c:
            _cl = self.client['...'], self.client['id']
            logger.error('...' % _cl)
            return self._undefined
        _r = _c % {
            '...': '...',
        }
        # logger.debug('[ RESPONSE URL ] %s' % _r)
        return _r

    def _build_link_to_admin_page(self, _prop=None):
        """
        Links to event admin which will be included in customer communication emails.
        Currently, only VideosSent make use of this feature.
        """
        _c = self.client['...']
        if not _c:
            _cl = self.client['...'], self.client['id']
            logger.error('...' % _cl)
            return self._undefined
        _t = '...' in self.event_data['...']
        token = self.event_data['...'].get(_t and '...' or '...')
        _r = _c % {
            '...': '...',
        }
        return _r

    def _build_unsubscribe_url(self):
        url = self.client['...']
        cond = self.client['...'] == self.default_client['id']
        return cond and url % settings.HOST_URL or url

    def _get_event_name(self):
        event_name = []
        for event_tag in ['...', '...', '...']:
            _t = self.event_data['...'].get(event_tag)
            if not _t: continue
            event_name.append(_t)
        return chr(32).join(event_name)

    def _build_subject(self, args={}):
        template = Template(self.subject_template)
        return template.render(args)

    def _get_params(self):
        raise NotImplemented


class ...(Email):

    ... = '...',
    ... = {
        'default': 'something'
    }

    def __init__(self, job):
        super(Invite, self).__init__(job)
        self.email_template = '....html'
        self.subject_template = '....txt'

    def _get_params(self):
        sql = '''
            SELECT ...
        ;'''
        args = (self.job['...'], self.event_participant_name_id)
        _r = self.select(sql, args)
        assert _r, "... weren't found." % args
        return dict(_r[0])

    def update_status(self, status=11):
        sql = '''
            UPDATE ...
        ;'''
        args = (status, self.submid,)
        self.update(sql, args)
        return None

    def build_email(self):
        self.params = self._get_params()
        self.ed = super(self.__class__, self).get_event_data()
        template = Template(self.email_template)

        # holiday greeting: will affect ... and ...
        self.holiday_greeting = self.params.get('...') in self....
        subject = self._build_subject()
        self.submid = self.params['...']
        response_link = self._build_response_link()

        html_page = template.render({'...': '...'
            'static_url': settings.STATIC_URL,
            'response_link': response_link,
            'holiday': self.holiday_greeting,
            'unsubscribe_url': self._build_unsubscribe_url(),
        })
        self.mailjob = self.params['...'], {
            'subject': subject,
            'html': html_page,
            'text': "..." % dict(resp=response_link)}
        return self

    def _build_subject(self):
        """Build subject for email template"""
        subj_product = self.holiday_greeting and 5 or self.product
        _args = (
            self.ed['...']['...'] or '...',
            self.....get(subj_product) or self.....get('...'))
        return '...'.format(*_args)


class ...(Email):

    def __init__(self, job):
        super(self.__class__, self).__init__(job)
        self.email_template = '....html'
        self.subject_template = '....txt'

    def _get_params(self):
        """
        ...
        """
        sql = '''
            SELECT ...
        ;'''
        _e = self.job['...'],
        _r = self.select(sql, _e)
        assert _r, "... not found ..." % _e
        return dict(_r[0])

    def build_email(self):
        self.params = self._get_params()
        self.event_data = super(self.__class__, self).get_event_data()
        template = Template(self.email_template)
        gateway = "..." in self.params['...'] and '...' or '...'
        email_body = template.render({'...': '...'})
        self.mailjob = '...@.......', {
            'subject': self._build_subject({'...': self.params['...']}),
            'html': email_body,
            'text': "..." % dict(
                gateway=gateway,
                **{_k: self.params[_k] for _k in ('first_name', 'last_name', 'email', 'amount')}),
        }
        return self
